from vbelts import profile as prf
from vbelts import service_factor as sf
import pytest

def eval_service_factor(mach, dr, sh):
    return sf(mach, dr, sh)

def eval_profile(power, rpm):
    return prf.hi_power_2(power, rpm)

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

def test_profile():
    assert eval_profile(8,540) == 'B'
