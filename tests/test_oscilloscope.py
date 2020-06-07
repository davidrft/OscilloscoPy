import pytest
from pytest_mock import mocker
import usbtmc
from src.oscilloscopy import oscilloscope

@pytest.fixture
def mock_inst(mocker):
    mock = mocker.patch('usbtmc.Instrument')
    return mock

def test_reset(mock_inst):
    osc = oscilloscope.Oscilloscope(mock_inst)
    osc.reset()
    mock_inst.write.assert_called_with(":RST")

def test_stop(mock_inst):
    osc = oscilloscope.Oscilloscope(mock_inst)
    osc.stop()
    mock_inst.write.assert_called_with(":STOP")

def test_run(mock_inst):
    osc = oscilloscope.Oscilloscope(mock_inst)
    osc.run()
    mock_inst.write.assert_called_with(":RUN")

def test_single(mock_inst):
    osc = oscilloscope.Oscilloscope(mock_inst)
    osc.single()
    mock_inst.write.assert_called_with(":SINGLE")

def test_auto_scale(mock_inst):
    osc = oscilloscope.Oscilloscope(mock_inst)
    osc.auto_scale()
    mock_inst.write.assert_called_with(":AUT")

def test_set_acquire(mock_inst):
    osc = oscilloscope.Oscilloscope(mock_inst)
    osc.set_acquire('normal')
    mock_inst.write.assert_called_with(":ACQ:TYPE NORMAL")