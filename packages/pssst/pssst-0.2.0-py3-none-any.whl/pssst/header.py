# This file is part of the PSSST Python module
# Copyright 2020 Nicko van Someren
# SPDX-License-Identifier: MIT
# See the LICENSE.md file for full license terms

"""
Packet header abstraction and details
"""

from enum import Enum, IntFlag
import struct

from .errors import PSSSTUnsupportedCipher


class HeaderFlag(IntFlag):
    """Flags as used in PSSST packet headers"""
    REPLY = (1 << 15)
    CLIENT_AUTH = (1 << 14)


class CipherSuite(Enum):
    """Identifiers for known cipher suites"""
    NONE = 0
    X25519_AESGCM128 = 1


class Header:
    """PSSST packet header definition"""
    def __init__(self, cipher_suite=CipherSuite.NONE, reply=False, client_auth=False):
        self._flags = (
            (HeaderFlag.REPLY if reply else 0) |
            (HeaderFlag.CLIENT_AUTH if client_auth else 0)
        )
        self._suite = cipher_suite

    def __repr__(self):
        return "{}(cipher_suite={}, reply={}, client_auth={})".format(
            self.__class__.__name__,
            self.cipher_suite, self.reply, self.client_auth)

    @classmethod
    def from_packet(cls, packet):
        """Create a new Header object from packet bytes"""
        # pylint: disable=protected-access
        hdr = cls()
        flags, suite = struct.unpack(">HH", packet)
        hdr._flags = flags
        try:
            hdr._suite = CipherSuite(suite)
        except ValueError as err:
            raise PSSSTUnsupportedCipher() from err
        return hdr

    @property
    def reply(self):
        """True if the packet is a reply"""
        return bool(self._flags & HeaderFlag.REPLY)

    @reply.setter
    def reply(self, is_reply):
        if is_reply:
            self._flags |= HeaderFlag.REPLY
        else:
            self._flags &= ~HeaderFlag.REPLY

    @property
    def client_auth(self):
        """True if client authentication is used"""
        return bool(self._flags & HeaderFlag.CLIENT_AUTH)

    @client_auth.setter
    def client_auth(self, has_client_auth):
        if has_client_auth:
            self._flags |= HeaderFlag.CLIENT_AUTH
        else:
            self._flags &= ~HeaderFlag.CLIENT_AUTH

    @property
    def cipher_suite(self):
        """Cipher suite used by this packet"""
        return self._suite

    @cipher_suite.setter
    def cipher_suite(self, suite):
        self._suite = suite

    @property
    def packet_bytes(self):
        """The packet header as a byte block"""
        return struct.pack(">HH", self._flags, self._suite.value)
