#!/usr/bin/env python3
# SimpleCmdScan - A simple command line scanning tool
# Copyright (C) 2024, bitcreed LLC
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import sys

from decouple import config
from . import __version__
from .logger import set_log_level
from .scan_controller import SimpleCmdScan


class AppStarter:
    def __init__(self):
        self.controller = None

    @staticmethod
    def parse_arguments(argv):
        options = argparse.ArgumentParser()
        options.add_argument(
            "-a",
            "--adf",
            action="store_true",
            help="Scan all documents from the Automated Document Feeder (ADF). "
            "Also via env SCAN_ADF=1 or .env",
        )
        options.add_argument(
            "-d",
            "--double-sided",
            action="store_true",
            help="Double-sided scan. Prompts the user to flip the stack, then merges pages. "
            "Also via env SCAN_DOUBLE_SIDED=1 or .env",
        )
        options.add_argument(
            "-m",
            "--multidoc",
            choices=["join", "split"],
            default="join",
            help="Keep scanning documents until the user aborts."
            "If used with --adf, separate documents are created regardless of the option chosen, "
            "without --adf the following options are available: join [default] or split. "
            "With `join' a single document is produced from all scanned pages, "
            "With `split' separate documents are produced from each scanned page "
            "Also via env SCAN_MULTIPLE_DOCUMENTS=join or .env",
        )
        options.add_argument(
            "-o",
            "--output-dir",
            help="Output directory to store scanned documents in. "
            "Default is the current work directory. "
            "Also via env SCAN_OUTPUT_DIR or .env",
        )
        options.add_argument(
            "-n",
            "--output-filename",
            help="Filename or filename format of files in output folder. "
            "Do not include the .pdf ending. "
            "A suffix _front or _incomplete is added if the scan aborts. "
            "Default is %%Y-%%m-%%d_%%H%%M_scan. "
            "Also via env SCAN_OUTPUT_FILENAME or .env",
        )
        options.add_argument(
            "-p",
            "--paper-format",
            choices=["A4", "Letter", "Legal"],
            help="Paper format to use. "
            "Default is depending on your locale. "
            "Also via env SCAN_PAPER_FORMAT or .env",
        )
        options.add_argument(
            "-r",
            "--resolution",
            help=f"Scan resolution in DPI Text is recommended at {SimpleCmdScan.DEFAULT_RESOLUTION_TEXT}, "
            f"pictures at {SimpleCmdScan.DEFAULT_RESOLUTION_PICTURE}. "
            f"Default {SimpleCmdScan.DEFAULT_RESOLUTION_TEXT} (Text). "
            "Also via env SCAN_RESOLUTION_DPI or .env",
        )
        options.add_argument(
            "-f",
            "--find-scanners",
            action="store_true",
            help="Find and list scanners - no actual scanning (useful to set a default with .env)",
        )
        options.add_argument(
            "-s",
            "--scanner",
            help="Set the scanner to use. "
            "Default is the first listing with --find-scanners. "
            "Also via env SCAN_DEVICE or .env.",
        )
        options.add_argument(
            "-l",
            "--loglevel",
            help="Log level. Also via env LOGLEVEL or .env. "
            "Default is WARN. "
            "Valid values are DEBUG, INFO, WARN, ERROR, FATAL.",
        )
        options.add_argument(
            "-v",
            "--version",
            action="store_true",
            help="Print version and exit"
        )

        args = options.parse_args(argv[1:])

        args.adf = args.adf or config("SCAN_ADF", default="0") == "1"
        args.double_sided = (
            args.double_sided or config("SCAN_DOUBLE_SIDED", default="0") == "1"
        )
        args.multidoc = args.double_sided or config(
            "SCAN_MULTIPLE_DOCUMENTS", default=None
        )
        if args.multidoc not in [None, "join", "split"]:
            args.multidoc = "join"  # default value off an unknown value set through env
        args.output_dir = args.output_dir or config("SCAN_OUTPUT_DIR", default=None)
        args.output_filename = args.output_filename or config("SCAN_OUTPUT_FILENAME", default=None)
        args.scanner = args.scanner or config("SCAN_DEVICE", default=None)
        args.paper_format = args.paper_format or config("SCAN_PAPER_FORMAT", default=None)
        args.resolution_dpi = args.resolution or config("SCAN_RESOLUTION_DPI", default=None)
        args.loglevel = args.loglevel or config("LOGLEVEL", default="WARN")

        return args

    def run(self, argv):
        args = AppStarter.parse_arguments(argv)
        if (args.version):
            print(__version__)
            sys.exit(0)

        if args.loglevel:
            set_log_level(args.loglevel)

        self.controller = SimpleCmdScan(args)
        try:
            ret = self.controller.run()
            sys.exit(ret)
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(1)


def main():
    app = AppStarter()
    app.run(sys.argv)


if __name__ == "__main__":
    main()
