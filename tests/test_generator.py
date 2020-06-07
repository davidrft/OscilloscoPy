import pytest
from pytest_mock import mocker
import usbtmc
from src.oscilloscopy import generator

@pytest.fixture
def mock_inst(mocker):
    mock = mocker.patch('usbtmc.Instrument')
    return mock

def test_sin(mock_inst):
    gen = generator.Generator(mock_inst)
    gen.sin(amp=2.0, freq=13000, offs=0.5)
    mock_inst.write.assert_called_with(
        'WGEN:FUNC SIN;FREQ 13000;VOLT 2.0;VOLT:OFFS 0.5')

def test_square(mock_inst):
    gen = generator.Generator(mock_inst)
    gen.square(amp=2.0, freq=13000, duty_cycle=60.0, offs=0.5)
    mock_inst.write.assert_called_with(
        'WGEN:FUNC SQU;FREQ 13000;VOLT 2.0;VOLT:OFFS 0.5;:WGEN:FUNC:SQU:DCYC 60.0')

def test_ramp(mock_inst):
    gen = generator.Generator(mock_inst)
    gen.ramp(amp=2.0, freq=13000, symmetry=60.0, offs=0.5)
    mock_inst.write.assert_called_with(
        'WGEN:FUNC RAMP;FREQ 13000;VOLT 2.0;VOLT:OFFS 0.5;:WGEN:FUNC:RAMP:SYMM 60.0')

def test_pulse(mock_inst):
    gen = generator.Generator(mock_inst)
    gen.pulse(amp=2.0, freq=13000, width=20, offs=0.5)
    mock_inst.write.assert_called_with(
        'WGEN:FUNC PULS;FREQ 13000;VOLT:HIGH 2.0;VOLT:LOW 0.5;:WGEN:FUNC:PULS:WIDT 20')

def test_dc(mock_inst):
    gen = generator.Generator(mock_inst)
    gen.dc(amp=2.0)
    mock_inst.write.assert_called_with("WGEN:FUNC DC;VOLT:OFFS 2.0")

def test_noise(mock_inst):
    gen = generator.Generator(mock_inst)
    gen.noise(amp=2.0, offs=0.5)
    mock_inst.write.assert_called_with("WGEN:FUNC NOIS;VOLT 2.0;VOLT:OFFS 0.5")

def test_on(mock_inst):
    gen = generator.Generator(mock_inst)
    gen.on()
    mock_inst.write.assert_called_with("WGEN:OUTP ON")

def test_off(mock_inst):
    gen = generator.Generator(mock_inst)
    gen.off()
    mock_inst.write.assert_called_with("WGEN:OUTP OFF")