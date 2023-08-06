from vbelts import length as l
import pytest


# ########### Eval func

def eval_belt_superhc(model, length):  # OK
    return l.belt_super_hc(model, length)

def eval_belt_hipower2(model, length):  # OK
    return l.belt_hi_power_2(model, length)

def eval_corr_dist_factor(max_diam, min_diam, l_a):  # OK
    return l.corr_dist_factor(max_diam, min_diam, l_a)

def eval_center_dist_uncorr(max_diam, min_diam):  # OK
    return l.center_dist_uncorr(max_diam, min_diam)

def eval_belt_len_uncorr(center, max_diam, min_diam):  # OK
    return l.belt_len_uncorr(center, max_diam, min_diam)

def eval_belt_len_corr(l_c, max_diam, min_diam):  # OK
    return l.belt_len_corr(l_c, max_diam, min_diam)

def eval_center_dist_corr(l_a, h, max_diam, min_diam):  # OK
    return l.center_dist_corr(l_a, h, max_diam, min_diam)

# ######## Test func

def test_center_dist_corr():
    assert eval_center_dist_corr(1009.5, 0.13, 450, 200) == 488.5

def test_belt_len_corr():
    assert eval_belt_len_corr(2030, 450, 200) == 1009.5

def test_center_dist_uncorr():
    assert eval_center_dist_uncorr(450, 200) == 525

def test_eval_belt_len_uncorr():
    assert eval_belt_len_uncorr(525, 450, 200) == 2100.26

def test_belt_superhc():
    assert eval_belt_superhc('3V', 675) == (675, '3V265')
    assert eval_belt_superhc('3V', 680) == (675, '3V265')
    assert eval_belt_superhc('3V', 705) == (710, '3V280')
    assert eval_belt_superhc('5V', 1275) == (1270, '5V500')
    assert eval_belt_superhc('5V', 1895) == (1905, '5V750')
    assert eval_belt_superhc('5V', 1650) == (1700, '5V670')
    assert eval_belt_superhc('8V', 12700) == (12700, '8V5000')

def test_belt_hipower2():
    assert eval_belt_hipower2('A', 1000) == (1000, 'A-38')
    assert eval_belt_hipower2('A', 1010) == (1000, 'A-38')
    assert eval_belt_hipower2('B', 1910) == (1900, 'B-73')

def test_corr_dist_factor():
    assert eval_corr_dist_factor(400, 200, 1000) == 0.1
    assert eval_corr_dist_factor(500, 280, 1285) == 0.09

# ######### Test fail func

def test_corr_dist_factor_fail():  # OK
    with pytest.raises(Exception):
        eval_corr_dist_factor(450, 250, 392)
        eval_corr_dist_factor('a', 250, 1000)
        eval_corr_dist_factor([1,2], 250, 1000)

def test_belt_hipower2_fail():  # OK
    with pytest.raises(Exception):
        eval_belt_hipower2('A', 694.999)
        eval_belt_hipower2('A', 4605.1)
        eval_belt_hipower2('B', 300)
        eval_belt_hipower2('V', 0)

def test_belt_superhc_fail():  # OK
    with pytest.raises(Exception):
        eval_belt_superhc('3V', 634.9)
        eval_belt_superhc('3V', 3555.1)

def test_center_dist_uncorr_fail():  # OK
    with pytest.raises(Exception):
        eval_center_dist_uncorr('a', 2)
        eval_center_dist_uncorr([1,2], 2)

def test_belt_len_uncorr_fail():  # OK
    with pytest.raises(Exception):
        eval_belt_len_uncorr('a', 450, 200)

def test_belt_len_corr_fail():  # OK
    with pytest.raises(Exception):
        eval_belt_len_corr('A', 450, 200)
        eval_belt_len_corr(1009.5, 'A', 200)

def test_center_dist_corr_fail():  # OK
    with pytest.raises(Exception):
        eval_center_dist_corr('A', 0.2, 450, 200)
        eval_center_dist_corr(1009.5, 'A', 450, 200)
