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

import logging

from . import __app_name__

logging.basicConfig(level=logging.WARN)
log = logging.getLogger(__app_name__)


def set_log_level(level_str):
    """Set logging level based on the provided string."""
    global log
    level = getattr(logging, level_str.upper(), None)
    if not isinstance(level, int):
        raise ValueError(f"Invalid log level: {level_str}")
    log.setLevel(level=level)
