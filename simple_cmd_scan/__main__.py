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
    def add_env_argument(options, env_var, *args, **kwargs):
        env_val = config(env_var, default=None)
        env_text = env_val is not None and f"{env_var}={env_val}" or "unset"
        help_suffix = f"Also via env {env_var} or .env file, currently {env_text}"
        if env_val and 'action' in kwargs and kwargs["action"] == "store_true":
            env_val = bool(env_val)

        if 'help' in kwargs:
            kwargs['help'] += f" {help_suffix}"
        else:
            kwargs['help'] = help_suffix

        if env_val is not None:
            kwargs['default'] = env_val

        options.add_argument(*args, **kwargs)

    @staticmethod
    def parse_arguments(argv):
        options = argparse.ArgumentParser()

        AppStarter.add_env_argument(
            options, 'SCAN_ADF',
            "-a", "--adf",
            action="store_true",
            help="Scan all documents from the Automated Document Feeder (ADF) instead of the flatbed scanner."
        )
        AppStarter.add_env_argument(
            options, 'SCAN_COLOR_MODE',
            "-c", "--color-mode",
            nargs='?',
            choices=['color', 'grayscale', 'bw'],
            const='color',
            help="Color mode. Default is color."
        )
        AppStarter.add_env_argument(
            options, 'SCAN_DOUBLE_SIDED',
            "-d", "--double-sided",
            action="store_true",
            help="Double-sided scan. Prompts the user to flip the stack, then merges pages."
        )
        AppStarter.add_env_argument(
            options, 'SCAN_MULTIPLE_DOCUMENTS',
            "-m", "--multidoc",
            nargs='?',
            choices=["join", "split"],
            const="join",
            help="Keep scanning documents until the user aborts."
            "If used together with --adf, --multidoc split is used "
            "and separate documents are created regardless of the option chosen, "
            "without --adf the following options are available: join [default] or split. "
            "With `join' a single document is produced from all scanned pages, "
            "With `split' separate documents are produced from each scanned page."
        )
        AppStarter.add_env_argument(
            options, 'SCAN_OUTPUT_DIR',
            "-o", "--output-dir",
            help="Output directory to store scanned documents in. "
            "Default is the current work directory."
        )
        AppStarter.add_env_argument(
            options, 'SCAN_OUTPUT_FILENAME',
            "-n", "--output-filename",
            help="Filename or filename format of files in output folder. "
            "Do not include the .pdf ending. "
            "A suffix _front or _incomplete is added if the scan aborts. "
            "Default is %%Y-%%m-%%d_%%H%%M_scan."
        )
        AppStarter.add_env_argument(
            options, 'SCAN_PAPER_FORMAT',
            "-p", "--paper-format",
            choices=["A4", "Letter", "Legal"],
            help="Paper format to use. "
            "Default is depending on your locale."
        )
        AppStarter.add_env_argument(
            options, 'SCAN_RESOLUTION_DPI',
            "-r", "--resolution",
            help=f"Scan resolution in DPI Text is recommended at {SimpleCmdScan.DEFAULT_RESOLUTION_TEXT}, "
            f"pictures at {SimpleCmdScan.DEFAULT_RESOLUTION_PICTURE}. "
            f"Default {SimpleCmdScan.DEFAULT_RESOLUTION_TEXT} (Text). "
            "Choices [int], text, image."
        )
        options.add_argument(
            "-f",
            "--find-scanners",
            action="store_true",
            help="Find and list scanners - no actual scanning (useful to set a default with .env)",
        )
        AppStarter.add_env_argument(
            options, 'SCAN_DEVICE',
            "-s", "--scanner",
            help="Set the scanner to use. "
            "Default is the first listing with --find-scanners."
        )
        AppStarter.add_env_argument(
            options, 'LOG_LEVEL',
            "-l", "--loglevel",
            choices=['DEBUG', 'INFO', 'WARN', 'ERROR', 'FATAL'],
            help="Set the log level. Default is WARN."
        )
        options.add_argument(
            "-v",
            "--version",
            action="store_true",
            help="Print version and exit"
        )

        return options.parse_args(argv[1:])

    def run(self, argv):
        args = AppStarter.parse_arguments(argv)
        if (args.version):
            print(__version__)
            return 0

        if args.loglevel:
            set_log_level(args.loglevel)

        self.controller = SimpleCmdScan(args)
        try:
            return self.controller.run()
        except KeyboardInterrupt:
            print("\nExiting...")
            return 1


def main(argv=sys.argv):
    app = AppStarter()
    sys.exit(app.run(argv))


if __name__ == "__main__":
    main()
