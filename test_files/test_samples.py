import pytest
from lab.thermostat import caclulate_temp_change

def test_calculus():
    assert caclulate_temp_change(-1) == 0