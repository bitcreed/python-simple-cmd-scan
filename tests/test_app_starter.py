import pytest
import sys

from unittest.mock import patch
from simple_cmd_scan.__main__ import main, AppStarter
from simple_cmd_scan import __version__
from simple_cmd_scan.scan_controller import SimpleCmdScan


@pytest.fixture
def mock_sane(mocker):
    mocker.patch('sane.init')


def test_args_version(capsys):
    with patch.object(sys, 'exit') as mock_exit:
        main(['simple-cmd-scan', '-v'])

    capture = capsys.readouterr()
    output_version = capture.out.strip()
    assert output_version == __version__, "App version does not match stdout"
    mock_exit.assert_called_once_with(0)


def test_args_output_dir(monkeypatch):
    output_dir = '/tmp/test'
    args = AppStarter.parse_arguments(['simple-cmd-scan', '-o', output_dir])
    assert args.output_dir == output_dir, "Output dir doesn't match when fed through sys.argv"

    monkeypatch.setenv('SCAN_OUTPUT_DIR', output_dir)
    args = AppStarter.parse_arguments(['simple-cmd-scan'])
    assert args.output_dir == output_dir, "Output dir doesn't match when fed through env"


def test_args_adf(monkeypatch):
    args = AppStarter.parse_arguments(['simple-cmd-scan', '-a'])
    assert args.adf is True, "ADF scan not set when fed through sys.argv"

    monkeypatch.setenv('SCAN_ADF', '1')
    args = AppStarter.parse_arguments(['simple-cmd-scan'])
    assert args.adf is True, "ADF scan not set when fed through env"


def test_args_resolution(mock_sane, monkeypatch):
    res = 'picture'
    args = AppStarter.parse_arguments(['simple-cmd-scan', '-r', res])
    assert args.resolution == res, "Resolution not set when fed through sys.argv"

    monkeypatch.setenv('SCAN_RESOLUTION_DPI', res)
    args = AppStarter.parse_arguments(['simple-cmd-scan'])
    assert args.resolution == res, "Resolution not set when fed through env"

    scs = SimpleCmdScan(args)
    assert scs.resolution_dpi == SimpleCmdScan.DEFAULT_RESOLUTION_PICTURE, "Resolution argument not properly converted"
