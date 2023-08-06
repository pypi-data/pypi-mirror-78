# This file is part of the PSSST Python module
# Copyright 2020 Nicko van Someren
# SPDX-License-Identifier: MIT
# See the LICENSE.md file for full license terms

"""
Exception definitions for PSSST
"""


class PSSSTException(Exception):
    """General PSSST exception"""


class PSSSTUnsupportedCipher(PSSSTException):
    """Cipher suite not supported"""


class PSSSTClientAuthFailed(PSSSTException):
    """Client authentation failed"""


class PSSSTReplyMismatch(PSSSTException):
    """Reply packed does not match request"""


class PSSSTNotReply(PSSSTException):
    """Packet is not a reply"""


class PSSSTNotRequest(PSSSTException):
    """Packet is not a request"""


class PSSSTDecryptFailed(PSSSTException):
    """Authenticated decryption failed"""
