import pytest
from pytest_mock import mocker
import usbtmc
from src.oscilloscopy import channel

@pytest.fixture
def mock_inst(mocker):
    mock = mocker.patch('usbtmc.Instrument')
    return mock

@pytest.fixture
def mock_inst_ask(mocker):
    mock = mocker.patch('usbtmc.Instrument.ask')
    mock.return_value = 100
    return mock

def test_get_time_scale(mock_inst, mock_inst_ask):
    ch = channel.Channel(mock_inst)
    result = ch.get_time_scale()
    assert result == 100 and type(result) is float
 
def test_set_time_scale(mock_inst, mock_inst_ask):
    ch = channel.Channel(mock_inst)
    ch.set_time_scale(120)
    mock_inst.write.assert_called_with(':TIM:SCAL 120')

def test_get_time_delay(mock_inst, mock_inst_ask):
    ch = channel.Channel(mock_inst)
    result = ch.get_time_delay()
    assert result == 100.0 and type(result) is float
 
def test_set_time_delay(mock_inst, mock_inst_ask):
    ch = channel.Channel(mock_inst)
    ch.set_time_delay(120)
    mock_inst.write.assert_called_with(':TIM:POS 120')
