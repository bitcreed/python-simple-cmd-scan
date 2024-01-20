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

import pytest
from simple_cmd_scan.scan_controller import SimpleCmdScan
from unittest.mock import patch, MagicMock


@pytest.fixture
def mock_sane(mocker):
    mocker.patch('sane.init')
    mocker.patch('sane.get_devices', return_value=[('device1', 'manufacturer', 'model', 'type')])
    sane_open_mock = mocker.patch('sane.open')
    sane_open_mock.return_value = MagicMock()
    return sane_open_mock


@pytest.fixture
def mock_create_pdf(mocker):
    return mocker.patch('simple_cmd_scan.scan_controller.ScanJob.create_pdf')


@patch.object(SimpleCmdScan, 'MAX_SCANS', 10)
class TestSimpleCmdScan:
    @classmethod
    def setup_class(cls):
        cls.fake_temp_dir = '/tmp/fake/dir'  # Fake temporary directory path
        cls.mock_temp_dir_patch = patch('tempfile.TemporaryDirectory')
        cls.mock_temp_dir = cls.mock_temp_dir_patch.start()
        cls.mock_temp_dir.return_value.__enter__.return_value = cls.fake_temp_dir

    @classmethod
    def teardown_class(cls):
        cls.mock_temp_dir_patch.stop()

    def test_list_scanners(self, mock_sane):
        args = MagicMock(find_scanners=True)
        scanner_app = SimpleCmdScan(args)
        ret = scanner_app.run()
        assert ret == SimpleCmdScan.RET_OK, "ret is not RET_OK"
        assert mock_sane.get_devices, "List of devices is empty"

    def test_list_scanners_no_devices(self, mocker):
        # Override the mock_sane fixture for this test
        mocker.patch('sane.get_devices', return_value=[])
        args = MagicMock(find_scanners=True)
        scanner_app = SimpleCmdScan(args)
        ret = scanner_app.run()
        assert ret == SimpleCmdScan.RET_NO_SCANNER, "List of devices is not empty or wrong return value"

    def test_scan_single_sided(self, mock_sane, mock_create_pdf):
        args = MagicMock(adf=False, double_sided=False, multidoc=None)
        scanner_app = SimpleCmdScan(args)
        with patch('builtins.input', return_value=''):
            ret = scanner_app.scan_single_sided()
        assert ret == SimpleCmdScan.RET_OK, "ret is not RET_OK"
        mock_sane.return_value.scan.assert_called_once()
        mock_create_pdf.assert_called_once()

    def test_scan_adf_double_sided(self, mock_sane, mock_create_pdf):
        args = MagicMock(adf=True, double_sided=True)
        scanner_app = SimpleCmdScan(args)
        # # Two pages in the ADF, flip, two pages
        # side_effect = [MagicMock(), MagicMock(), MagicMock(), MagicMock()]
        # with patch.object(mock_sane.return_value, 'multi_scan', side_effect=side_effect):
        with patch('builtins.input', return_value=''):
            ret = scanner_app.scan_double_sided()
        assert ret == SimpleCmdScan.RET_OK, "ret is not RET_OK"
        assert mock_sane.return_value.multi_scan.call_count == 2, "multi_scan not called twice"
        mock_create_pdf.assert_called_once()

    def test_multidoc_mode_split(self, mock_sane, mock_create_pdf):
        args = MagicMock(adf=False, double_sided=False, multidoc='split')
        scanner_app = SimpleCmdScan(args)

        # Simulate pressing Enter to proceed with scanning and then stop
        with patch('builtins.input', side_effect=['', EOFError]):
            ret = scanner_app.scan_single_sided()

        assert ret == SimpleCmdScan.RET_OK, "ret is not RET_OK"
        assert mock_create_pdf.call_count == 2, "create_pdf() call count is not 2"

    def test_multidoc_mode_join(self, mock_sane, mock_create_pdf):
        args = MagicMock(adf=False, double_sided=False, multidoc='join')
        scanner_app = SimpleCmdScan(args)

        # Simulate pressing Enter to proceed with scanning and then stop
        with patch('builtins.input', side_effect=['', EOFError]):
            ret = scanner_app.scan_single_sided()

        assert ret == SimpleCmdScan.RET_OK, "ret is not RET_OK"
        mock_create_pdf.assert_called_once()
