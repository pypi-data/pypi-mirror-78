from vbelts import profile as prf
from vbelts import service_factor as sf
from vbelts import diam as d
import pytest

def eval_service_factor(mach, dr, sh):  # OK
    return sf(mach, dr, sh)

def eval_profile_hipower(power, rpm):  # OK
    return prf.hi_power_2(power, rpm)

def eval_profile_superhc(power, rpm):
    return prf.super_hc(power, rpm)

def eval_diam_min_pulley(vbelt_mod, power, speed):  # OK
    return d.min_pulley(vbelt_mod, power, speed, mode='imp')

def eval_driven_pulley(d1, i): # OK
    return d.driven_pulley(d1, i)

def test_driven_pulley():
    assert eval_driven_pulley(2,2) == 4

def test_driven_pulley_fail():
    with pytest.raises(ValueError):
        eval_driven_pulley('a',4)
        eval_driven_pulley(1, [1,2])

def test_diam_min_pulley():
    assert eval_diam_min_pulley('super hc', 1, 575) == 2.5
    assert eval_diam_min_pulley('super hc', 22.5, 485) == 8.6
    assert eval_diam_min_pulley('super hc', 200, 700) == 22
    assert eval_diam_min_pulley('super hc', 6, 1500) == 3

def test_min_pulley_fail():
    with pytest.raises(Exception):
        eval_diam_min_pulley('fff', 1, 575)
        eval_diam_min_pulley('super hc', 'm', 500)
        eval_diam_min_pulley('super hc', 1, '4746')
        eval_diam_min_pulley('super hc', 0.9, 500)
        eval_diam_min_pulley('super hc', 300.1, 574)
        eval_diam_min_pulley('super hc', 0.9, 600)
        eval_diam_min_pulley('super hc', 300.1, 600)
        eval_diam_min_pulley('super hc', 0.49, 690)
        eval_diam_min_pulley('super hc', 201, 690)
        eval_diam_min_pulley('super hc', 0.74, 1000)
        eval_diam_min_pulley('super hc', 150.5, 1159)
        eval_diam_min_pulley('super hc', 0.99, 1160)
        eval_diam_min_pulley('super hc', 200.1, 1749)
        eval_diam_min_pulley('super hc', 1.49, 1750)
        eval_diam_min_pulley('super hc', 25.1, 3449)
        eval_diam_min_pulley('super hc', 0, 500)
        eval_diam_min_pulley('super hc', 400, 1750)
        eval_diam_min_pulley('super hc', 3, 4000)
        eval_diam_min_pulley('hi power 2', 0.49, 485)
        eval_diam_min_pulley('hi power 2', 300.01, 574.99)

def test_profile_hipower():
    assert eval_profile_hipower(8,540) == 'B'

def test_profile_superhc():
    assert eval_profile_superhc(8, 540) == '3V'

def test_service_factor():
    assert eval_service_factor('stirrer','normal',3) == 1.0
    assert eval_service_factor('stirrer','normal',6) == 1.1
    assert eval_service_factor('stirrer','normal',11) == 1.2
    assert eval_service_factor('stirrer','high',3) == 1.1
    assert eval_service_factor('stirrer','high',6) == 1.2
    assert eval_service_factor('stirrer','high',11) == 1.3
    assert eval_service_factor('transmission','synchronous ac',4) == 1.1
    assert eval_service_factor('transmission','synchronous ac',7) == 1.2
    assert eval_service_factor('transmission','synchronous ac',16) == 1.3
    assert eval_service_factor('transmission','monophasic ac',5) == 1.2
    assert eval_service_factor('transmission','monophasic ac',8) == 1.3
    assert eval_service_factor('transmission','monophasic ac',24) == 1.4
    assert eval_service_factor('reciprocating compressor','multiple cylinder',5) == 1.2
    assert eval_service_factor('reciprocating compressor','multiple cylinder',10) == 1.3
    assert eval_service_factor('reciprocating compressor','multiple cylinder',20) == 1.4
    assert eval_service_factor('reciprocating compressor','single cylinder',5) == 1.4
    assert eval_service_factor('reciprocating compressor','single cylinder',10) == 1.5
    assert eval_service_factor('reciprocating compressor','single cylinder',20) == 1.5
    assert eval_service_factor('crane','multiple cylinder',5) == 1.3
    assert eval_service_factor('crane','multiple cylinder',10) == 1.4
    assert eval_service_factor('crane','multiple cylinder',20) == 1.5
    assert eval_service_factor('crane','clutch',5) == 1.6
    assert eval_service_factor('crane','clutch',10) == 1.6
    assert eval_service_factor('crane','clutch',20) == 1.8