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

import locale
import os

from .logger import log


def get_default_paper_size():
    # Check LC_PAPER environment variable
    loc = os.environ.get('LC_PAPER')
    loc = loc and loc.split('.') or loc
    if not loc:
        # Fallback: Check locale settings
        loc = locale.getlocale()

    if loc[0] and ('US' in loc[0] or 'CA' in loc[0]):
        return 'letter'
    return 'a4'  # Most other countries use A4


def test_write_to_folder(folder_path):
    """
    Tests if we have write access to folder in `folder_path`.
    This method attempts to create a temporary file in the folder to check the permission.
    The file is not actually created, ensuring no changes are made to the filesystem.

    :param folder_path: Path to the folder to test
    :return: True if write access is available, False otherwise
    """
    try:
        # Attempt to open a temporary file in write mode without actually creating it
        test_file_path = os.path.join(folder_path, "temp_file_test")
        with open(test_file_path, 'w'):
            pass

        # Clean up: Delete the test file if it gets created in case of an unexpected behavior
        if os.path.exists(test_file_path):
            os.remove(test_file_path)

        return True

    except IOError:
        # File could not be written, hence no write access
        return False

    except Exception as e:
        # Handle any other unexpected exceptions
        log.e(f"An unexpected error occurred while testing write access: {e}")
        return False
