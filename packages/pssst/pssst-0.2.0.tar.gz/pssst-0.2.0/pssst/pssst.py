# This file is part of the PSSST Python module
# Copyright 2020 Nicko van Someren
# SPDX-License-Identifier: MIT
# See the LICENSE.md file for full license terms

"""
PSSST client and server interfaces
"""

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
from cryptography.hazmat.primitives.serialization import (
    Encoding, PrivateFormat, PublicFormat, NoEncryption
    )
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidTag

from .header import Header, CipherSuite
from .errors import (
    PSSSTUnsupportedCipher, PSSSTClientAuthFailed,
    PSSSTReplyMismatch, PSSSTNotReply, PSSSTNotRequest,
    PSSSTDecryptFailed
    )


def _DKF_SHA256(dh_param, shared_secret):  # pylint: disable=invalid-name
    h256 = hashes.Hash(hashes.SHA256(), default_backend())
    h256.update(dh_param)
    h256.update(shared_secret)
    derived_bytes = h256.finalize()
    key = derived_bytes[:16]
    iv_c = derived_bytes[16:24] + b"RQST"
    iv_s = derived_bytes[24:32] + b"RPLY"
    return (key, iv_c, iv_s)


def generate_key_pair(cipher_suite=CipherSuite.X25519_AESGCM128):
    """A utility function to generate a suitable key pair for the given cipher suite

    :param cipher_suite: cipher suite for which to generate asymmetric key pair

    :raises PSSSTUnsupportedCipher: requested cipher suite is not supported.

    :return: (private_key, public_key) tuple
    """
    if cipher_suite != CipherSuite.X25519_AESGCM128:
        raise PSSSTUnsupportedCipher()

    new_private_key = X25519PrivateKey.generate()
    return (new_private_key, new_private_key.public_key())


def _key_check(key_value, public):
    if key_value is None:
        return None
    if isinstance(key_value, str):
        key_value = bytes.fromhex(key_value)
    if isinstance(key_value, bytes):
        if public:
            key_value = X25519PublicKey.from_public_bytes(key_value)
        else:
            key_value = X25519PrivateKey.from_private_bytes(key_value)
    return key_value


class PSSSTClient:
    """PSSST client interface

    :param server_public_key: Public key of the target server
    :param client_private_key: Private key for client authentication, defaults to None
    :param cipher_suite: cipher suite for which to generate asymmetric key pair

    :raises PSSSTUnsupportedCipher: requested cipher suite is not supported.
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, server_public_key,
                 client_private_key=None,
                 cipher_suite=CipherSuite.X25519_AESGCM128):
        """Return a new PSSSTClient"""
        if cipher_suite != CipherSuite.X25519_AESGCM128:
            raise PSSSTUnsupportedCipher()

        self._request_hdr = Header(cipher_suite=cipher_suite,
                                   reply=False,
                                   client_auth=(client_private_key is not None))

        self._server_public = _key_check(server_public_key, True)
        self._client_private = _key_check(client_private_key, False)
        if client_private_key is not None:
            self._client_public = self._client_private.public_key()
            partial_key_bytes = self._client_private.exchange(self._server_public)
            self._client_server_pub = X25519PublicKey.from_public_bytes(partial_key_bytes)

    def pack_request(self, data):
        """Pack an outbound request

        :param data: message bytes to be encrypted
        :type data: bytes

        :returns: tuple of encrypted packet and reply handler
        """
        temp_priv_key = X25519PrivateKey.generate()
        if self._client_private:
            exchange_dh = temp_priv_key.exchange(self._client_public)
            shared_secret = temp_priv_key.exchange(self._client_server_pub)
            client_pub_bytes = self._client_public.public_bytes(encoding=Encoding.Raw,
                                                                format=PublicFormat.Raw)
            temp_private_bytes = temp_priv_key.private_bytes(encoding=Encoding.Raw,
                                                             format=PrivateFormat.Raw,
                                                             encryption_algorithm=NoEncryption())
            data = client_pub_bytes + temp_private_bytes + data
        else:
            exchange_dh = temp_priv_key.public_key().public_bytes(encoding=Encoding.Raw,
                                                                  format=PublicFormat.Raw)
            shared_secret = temp_priv_key.exchange(self._server_public)

        key, nonce_client, nonce_server = _DKF_SHA256(exchange_dh, shared_secret)

        packet = self._request_hdr.packet_bytes + exchange_dh
        cipher = AESGCM(key)

        packet += cipher.encrypt(nonce_client, data, packet[:4])

        def reply_handler(packet):
            """Unpack the reply to a request packet"""
            hdr = Header.from_packet(packet[:4])
            if not hdr.reply:
                raise PSSSTNotReply()
            if (not hdr.reply or
                    hdr.cipher_suite != self._request_hdr.cipher_suite or
                    hdr.client_auth != self._request_hdr.client_auth or
                    packet[4:36] != exchange_dh):
                raise PSSSTReplyMismatch()
            try:
                plaintext = cipher.decrypt(nonce_server, packet[36:], packet[:4])
            except InvalidTag as err:
                raise PSSSTDecryptFailed() from err
            return plaintext

        return (packet, reply_handler)


class PSSSTServer:
    """PSSST server interface

    :param server_private_key: Private key for the server
    :param cipher_suite: cipher suite for which to generate asymmetric key pair

    :raises PSSSTUnsupportedCipher: requested cipher suite is not supported.
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, server_private_key, cipher_suite=CipherSuite.X25519_AESGCM128):
        """Return a new PSSST server"""
        if cipher_suite != CipherSuite.X25519_AESGCM128:
            raise PSSSTUnsupportedCipher()
        self._suite = cipher_suite
        self._server_private = _key_check(server_private_key, False)

    def unpack_request(self, packet):
        # pylint: disable=too-many-locals
        """Unpack an incoming request

        :param packet: Incoming packet to unpack
        :type packet: bytes

        :raises PSSSTUnsupportedCipher: cipher suite indicated in packet is not supported.
        :raises PSSSTNotRequest: packet is not a request packet.
        :raises PSSSTDecryptFailed: payload did not decrypt to valid and authentic data
        :raises PSSSTClientAuthFailed: client auth was present but did not match request
        :returns: tuple of unpacked data, authenticated client public key and reply handler

        """
        hdr = Header.from_packet(packet[:4])
        if hdr.reply:
            raise PSSSTNotRequest()
        if hdr.cipher_suite != self._suite:
            raise PSSSTUnsupportedCipher()
        dh_bytes = packet[4:36]
        exchange_dh = X25519PublicKey.from_public_bytes(dh_bytes)
        shared_secret = self._server_private.exchange(exchange_dh)

        key, nonce_client, nonce_server = _DKF_SHA256(dh_bytes, shared_secret)

        cipher = AESGCM(key)

        try:
            plaintext = cipher.decrypt(nonce_client, packet[36:], packet[:4])
        except InvalidTag as err:
            raise PSSSTDecryptFailed() from err

        if hdr.client_auth:
            client_public_key = X25519PublicKey.from_public_bytes(plaintext[:32])
            temp_privte_key = X25519PrivateKey.from_private_bytes(plaintext[32:64])
            auth_dh = temp_privte_key.exchange(client_public_key)
            if auth_dh != exchange_dh.public_bytes(encoding=Encoding.Raw, format=PublicFormat.Raw):
                raise PSSSTClientAuthFailed()
            plaintext = plaintext[64:]
        else:
            client_public_key = None

        def reply_handler(data):
            """Pack a reply to the request"""
            reply_hdr = Header(reply=True,
                               client_auth=hdr.client_auth,
                               cipher_suite=hdr.cipher_suite)
            header_bytes = reply_hdr.packet_bytes
            return header_bytes + packet[4:36] + cipher.encrypt(nonce_server, data, header_bytes)

        return (plaintext, client_public_key, reply_handler)
