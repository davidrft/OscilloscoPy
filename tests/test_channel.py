import pytest
from pytest_mock import mocker
from unittest.mock import call
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

@pytest.fixture
def mock_inst_ask_true(mocker):
    mock = mocker.patch('usbtmc.Instrument.ask')
    mock.return_value = "1"
    return mock

@pytest.fixture
def mock_inst_ask_false(mocker):
    mock = mocker.patch('usbtmc.Instrument.ask')
    mock.return_value = "0"
    return mock

def test_get_time_scale(mock_inst, mock_inst_ask):
    ch = channel.Channel(mock_inst)
    result = ch.get_time_scale()
    assert result == 100 and type(result) is float
 
def test_set_time_scale(mock_inst):
    ch = channel.Channel(mock_inst)
    ch.set_time_scale(120)
    mock_inst.write.assert_called_with(':TIM:SCAL 120')

def test_get_time_delay(mock_inst, mock_inst_ask):
    ch = channel.Channel(mock_inst)
    result = ch.get_time_delay()
    assert result == 100.0 and type(result) is float
 
def test_set_time_delay(mock_inst):
    ch = channel.Channel(mock_inst)
    ch.set_time_delay(120)
    mock_inst.write.assert_called_with(':TIM:POS 120')

def test_get_volt_scale(mock_inst, mock_inst_ask):
    ch = channel.Channel(mock_inst)
    result = ch.get_volt_scale(1)
    assert result == 100.0 and type(result) is float

def test_set_volt_scale(mock_inst):
    ch = channel.Channel(mock_inst)
    ch.set_volt_scale(1, 100)
    mock_inst.write.assert_called_with(':CHAN1:SCAL 100')
    
def test_get_volt_offset(mock_inst, mock_inst_ask):
    ch = channel.Channel(mock_inst)
    result = ch.get_volt_offset(1)
    assert result == 100.0 and type(result) is float

def test_set_volt_offset(mock_inst):
    ch = channel.Channel(mock_inst)
    ch.set_volt_offset(1, 500)
    mock_inst.write.assert_called_with(':CHAN1:OFFS 500')

def test_auto_trigger(mock_inst):
    ch = channel.Channel(mock_inst)
    ch.auto_trigger(1)
    calls = [call(':TRIG:SOUR CHAN1'), call(':TRIG:LEV:ASET')]
    mock_inst.write.assert_has_calls(calls, any_order=False)

def test_set_trigger(mock_inst, mock_inst_ask):
    ch = channel.Channel(mock_inst)
    ch.set_trigger(1, 50)
    calls = [call(':TRIG:SOUR CHAN1'), call(':TRIG:LEV 50')]
    mock_inst.write.assert_has_calls(calls, any_order=False)
    
def test_get_vpp(mock_inst, mock_inst_ask):
    ch = channel.Channel(mock_inst)
    result = ch.get_vpp(1)
    assert result == 100.0 and type(result) is float
    
def test_get_vrms(mock_inst, mock_inst_ask):
    ch = channel.Channel(mock_inst)
    result = ch.get_vrms(1)
    assert result == 100.0 and type(result) is float
    
def test_get_frequency(mock_inst, mock_inst_ask):
    ch = channel.Channel(mock_inst)
    result = ch.get_frequency(1)
    assert result == 100.0 and type(result) is float
    
def test_get_period(mock_inst, mock_inst_ask):
    ch = channel.Channel(mock_inst)
    result = ch.get_period(1)
    assert result == 100.0 and type(result) is float
    
def test_get_phase(mock_inst, mock_inst_ask):
    ch = channel.Channel(mock_inst)
    result = ch.get_phase(1, 2)
    assert result == 100.0 and type(result) is float

def test_set_coupling_ac(mock_inst):
    ch = channel.Channel(mock_inst)
    ch.set_coupling(1, "AC")
    mock_inst.write.assert_called_with(':CHAN1:COUP AC')

def test_set_coupling_dc(mock_inst):
    ch = channel.Channel(mock_inst)
    ch.set_coupling(1, "DC")
    mock_inst.write.assert_called_with(':CHAN1:COUP DC')

def test_toggle_channel_off(mock_inst, mock_inst_ask_true):
    ch = channel.Channel(mock_inst)
    ch.toggle_channel(1)
    mock_inst.write.assert_called_with('CHAN1:DISP OFF')

def test_toggle_channel_on(mock_inst, mock_inst_ask_false):
    ch = channel.Channel(mock_inst)
    ch.toggle_channel(1)
    mock_inst.write.assert_called_with('CHAN1:DISP ON')
