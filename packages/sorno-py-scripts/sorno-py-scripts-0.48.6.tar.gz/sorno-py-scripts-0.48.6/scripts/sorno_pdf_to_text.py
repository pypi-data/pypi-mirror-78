#!/usr/bin/env python
"""Convert a PDF to text file

    Copyright 2017 Heung Ming Tai

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import PyPDF2

import argparse
import logging
import subprocess
import sys

from sorno import loggingutil
from sorno import pdfutil

_log = logging.getLogger()
_plain_logger = None  # will be created in main()
_plain_error_logger = None  # will be created in main()


class App(object):
    """A console application to do work"""
    def __init__(self, args):
        """
        Args:
            args (argparse.Namespace): The flags for the script.
        """
        self.args = args

    def run(self):
        for pdf_file in self.args.pdf_file:
            print(pdfutil.pdf_to_text(pdf_file))
        return 0

    def _run_cmd(self, cmd):
        """Run a shell command

        Args:
            cmd (string or a list of strings): The shell command to run. If
                it's a string, uses the system shell to run the command. If
                it's a list of strings, the first string is the program to run
                and the rest are its arguments. The arguments are quoted
                properly by the subprocess module, so the arguments do not
                have to be quoted when passing to this method.
        """
        _log.info(cmd)
        if isinstance(cmd, list):
            use_shell = False
        else:
            use_shell = True
        return subprocess.check_call(cmd, shell=use_shell)


def parse_args(cmd_args):
    description = __doc__.split("Copyright 2017")[0].strip()

    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--debug",
        action="store_true",
    )
    parser.add_argument(
        "pdf_file",
        nargs='+',
    )

    args = parser.parse_args(cmd_args)
    return args


def main():
    global _plain_logger, _plain_error_logger

    args = parse_args(sys.argv[1:])

    loggingutil.setup_logger(_log, debug=args.debug)
    _plain_logger = loggingutil.create_plain_logger(
        "PLAIN",
        debug=args.debug,
    )
    _plain_error_logger = loggingutil.create_plain_logger(
        "PLAIN_ERROR",
        debug=args.debug,
        stdout=False,
    )

    app = App(args)
    sys.exit(app.run())


if __name__ == '__main__':
    main()
