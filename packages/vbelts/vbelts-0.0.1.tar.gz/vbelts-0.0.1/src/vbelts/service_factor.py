"""Service Factor

This module provides functions for service factor v-belt calculations.

The user must know of the type of drive or engine and the running conditions for the machine. Other information, as
the group of the machine are described in the function documentation."""

import re

# internal functions
def _mrt_calc_factr(mtr_ty, mach_grp):
    mtr_ty_regex = re.compile(r'\d|high|normal|clutch|axle')
    # searches for some common types of engine
    mo = mtr_ty_regex.search(mtr_ty)
    try:
        int(mo.group())
        check = True
    except ValueError:
        check = False
    if check:
        # if possible to convert group type to int
        mo_int = int(mo.group())
    else:
        if mo.group() == 'high' or mo.group() == 'clutch' or mo.group() == 'axle':
            mo_int = 1
        elif mo.group() == 'normal':
            mo_int = 2
    if mach_grp == 1 or mach_grp == 2:
        if mo_int > 1:
            mtr_factr = 0
        elif mo_int <= 1:
            mtr_factr = 0.1
    elif mach_grp == 3:
        if mo_int > 1:
            mtr_factr = 0
        elif mo_int <= 1:
            mtr_factr = 0.2
    elif mach_grp == 4:
        if mo_int > 1:
            mtr_factr = 0
        elif mo_int <= 1:
            mtr_factr = 0.3
    else:
        mtr_factr = 0
    return mtr_factr


def _task(service_hours, mach_grp):
    if mach_grp == 1:
        if 0 < service_hours <= 5:
            sf_part = 1.0
        elif 5 < service_hours <= 10:
            sf_part = 1.1
        elif 10 < service_hours <= 24:
            sf_part = 1.2
    elif mach_grp == 2:
        if 0 < service_hours <= 5:
            sf_part = 1.1
        elif 5 < service_hours <= 10:
            sf_part = 1.2
        elif 10 < service_hours <= 24:
            sf_part = 1.3
    elif mach_grp == 3:
        if 0 < service_hours <= 5:
            sf_part = 1.2
        elif 5 < service_hours <= 10:
            sf_part = 1.3
        elif 10 < service_hours <= 24:
            sf_part = 1.4
    elif mach_grp == 4:
        if 0 < service_hours <= 5:
            sf_part = 1.3
        elif 5 < service_hours <= 10:
            sf_part = 1.4
        elif 10 < service_hours <= 24:
            sf_part = 1.5
    return sf_part


# external functions
# group 1: stirrer, air blowers e exhaust fans, centrifugal pumps e compressors
def stirrer(mtr_ty, service_hours):
    mach_grp = 1
    # mach_grp define the machine group type
    mtr_factr = _mrt_calc_factr(mtr_ty, mach_grp)
    sf_part = _task(service_hours, mach_grp)
    return round(sf_part + mtr_factr, 1)


def blower10hp_exhaust(mtr_ty, service_hours):
    mach_grp = 1
    mtr_factr = _mrt_calc_factr(mtr_ty, mach_grp)
    sf_part = _task(service_hours, mach_grp)
    return round(sf_part + mtr_factr, 1)


def cfp_comp(mtr_ty, service_hours):
    mach_grp = 1
    mtr_factr = _mrt_calc_factr(mtr_ty, mach_grp)
    sf_part = _task(service_hours, mach_grp)
    return round(sf_part + mtr_factr, 1)


# group 2: air blowers > 10hp, generators, transmission axles, positive displacement pumps
def blower_p10hp(mtr_ty, service_hours):
    mach_grp = 2
    mtr_factr = _mrt_calc_factr(mtr_ty, mach_grp)
    sf_part = _task(service_hours, mach_grp)
    return round(sf_part + mtr_factr, 1)


def generator(mtr_ty, service_hours):
    mach_grp = 2
    mtr_factr = _mrt_calc_factr(mtr_ty, mach_grp)
    sf_part = _task(service_hours, mach_grp)
    return round(sf_part + mtr_factr, 1)


def tr_axle(mtr_ty, service_hours):
    mach_grp = 2
    mtr_factr = _mrt_calc_factr(mtr_ty, mach_grp)
    sf_part = _task(service_hours, mach_grp)
    return round(sf_part + mtr_factr, 1)


def pd_pump(mtr_ty, service_hours):
    mach_grp = 2
    mtr_factr = _mrt_calc_factr(mtr_ty, mach_grp)
    sf_part = _task(service_hours, mach_grp)
    return round(sf_part + mtr_factr, 1)


# group 3: reciprocating compressors
def rec_comp(mtr_ty, service_hours):
    mach_grp = 3
    mtr_factr = _mrt_calc_factr(mtr_ty, mach_grp)
    sf_part = _task(service_hours, mach_grp)
    if mtr_factr == 0.2 and sf_part == 1.4:
        correcao = 0.1
    else:
        correcao = 0
    return round(sf_part + mtr_factr - correcao, 1)


# group 4: cranes
def crane(mtr_ty, service_hours):
    mach_grp = 4
    mtr_factr = _mrt_calc_factr(mtr_ty, mach_grp)
    sf_part = _task(service_hours, mach_grp)
    if mtr_factr == 0.3 and sf_part == 1.4:
        correcao = 0.1
    else:
        correcao = 0
    return round(sf_part + mtr_factr - correcao, 1)
