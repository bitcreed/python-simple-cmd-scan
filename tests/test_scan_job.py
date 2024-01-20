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

from simple_cmd_scan.scan_controller import ScanJob


class TestScanJob:
    def test_merge(self):
        front = ['1', '3', '5']
        back = ['6', '4', '2']

        front_job = ScanJob()
        for i in front:
            front_job.add_image(i)

        back_job = ScanJob()
        for i in back:
            back_job.add_image(i)

        combined = front_job.merge_back_images(back_job)
        imgs = combined.images
        assert combined.num_pages == front_job.num_pages + back_job.num_pages
        assert imgs[0] == front[0]
        assert imgs[1] == back[2]
        assert imgs[2] == front[1]
        assert imgs[3] == back[1]
        assert imgs[4] == front[2]
        assert imgs[5] == back[0]
