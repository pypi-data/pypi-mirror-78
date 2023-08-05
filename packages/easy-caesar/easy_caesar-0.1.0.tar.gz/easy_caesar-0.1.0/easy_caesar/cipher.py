#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

log = logging.getLogger(__name__)


class Cipher:
    """
    This class encapsulates the cipher object. Providing configuration options and exposing the
    encrypt/decrypt methods that make up the data contract.
    """

    def __init__(self, cipher_length: int = 1, debug: bool = False) -> str:
        self._cipher_length = cipher_length
        self._dbg = debug

    def _modify(self, input_str: str, offset: int, encoding: str) -> str:
        ba = bytearray(input_str, encoding)
        if self._dbg:
            log.info("BA: %s", ba)
        for i, item in enumerate(ba):
            if self._dbg:
                log.info("BA[%s] = %s", i, ba[i])
            ba[i] = (ba[i] + offset - 65) % 63 + 65
            if self._dbg:
                log.info("BA[%s] = %s", i, ba[i])

        if self._dbg:
            log.info("BA: %s", ba)
        return ba.decode(encoding)

    def encrypt(self, input_str: str, encoding: str = "utf8") -> str:
        """Encrypt the string using a Caesar Cipher"""
        return self._modify(input_str, self._cipher_length, encoding)

    def decrypt(self, input_str: str, encoding: str = "utf8") -> str:
        """Decrypt the string using a Caesar Cipher"""
        return self._modify(input_str, -self._cipher_length, encoding)
