#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This sample script will get deployed in the bin directory of the
users' virtualenv when the parent module is installed using pip.
"""

import argparse
import logging
import sys
import traceback

from easy_caesar import Cipher, get_module_version

###############################################################################

log = logging.getLogger()
logging.basicConfig(
    level=logging.INFO, format="[%(levelname)4s:%(lineno)4s %(asctime)s] %(message)s"
)

###############################################################################


class Args(argparse.Namespace):

    DEFAULT_STEP_SIZE = 30
    DEFAULT_INPUT_STRING = "Hello, world."

    def __init__(self):
        # Arguments that could be passed in through the command line
        self.encrypt = True
        self.step_size = self.DEFAULT_STEP_SIZE
        self.debug = False
        self.input_string = self.DEFAULT_INPUT_STRING
        self.__parse()

    def __parse(self):
        p = argparse.ArgumentParser(
            prog="easy_cipher",
            description="Encrypt or decrypt a string",
        )

        p.add_argument(
            "-v",
            "--version",
            action="version",
            version="%(prog)s " + get_module_version(),
        )
        p.add_argument(
            "-s",
            "--step",
            action="store",
            dest="step_size",
            type=int,
            default=self.step_size,
            help="Caesarian step size",
        )
        p.add_argument(
            "-e",
            "--encrypt",
            action="store_true",
            dest="encrypt",
            help="Encrypt the input string",
        )
        p.add_argument(
            "-d",
            "--decrypt",
            action="store_false",
            dest="encrypt",
            help="Decrypt the input string",
        )
        p.add_argument(
            "--debug",
            action="store_true",
            dest="debug",
            help=argparse.SUPPRESS,
        )
        p.add_argument(
            "input_string",
            action="store",
            default=self.input_string,
            help="Target string to encrypt or decrypt.",
        )
        p.parse_args(namespace=self)


###############################################################################


def main():
    try:
        args = Args()
        dbg = args.debug

        # Do your work here - preferably in a class or function,
        # passing in your args. E.g.
        cipher = Cipher(cipher_length=args.step_size, debug=dbg)
        if args.encrypt:
            print(
                "{} => {}".format(args.input_string, cipher.encrypt(args.input_string))
            )
        else:
            print(
                "{} => {}".format(args.input_string, cipher.decrypt(args.input_string))
            )

    except Exception as e:
        log.error("=============================================")
        if dbg:
            log.error("\n\n" + traceback.format_exc())
            log.error("=============================================")
        log.error("\n\n" + str(e) + "\n")
        log.error("=============================================")
        sys.exit(1)


###############################################################################
# Allow caller to directly run this module (usually in development scenarios)

if __name__ == "__main__":
    main()
