from vbelts import profile as prf
from vbelts import service_factor as sf
import pytest

def eval_service_factor(drive, power):
    return sf.rec_comp(drive,power)

def eval_profile(power, rpm):
    return prf.hi_power_2(power, rpm)

def test_service_factor():
    assert eval_service_factor('axle',8) == 1.5

def test_profile():
    assert eval_profile(8,540) == 'B'
