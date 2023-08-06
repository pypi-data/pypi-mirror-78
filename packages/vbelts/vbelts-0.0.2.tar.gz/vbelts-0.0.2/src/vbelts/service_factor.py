"""Service Factor

This module calculate the service factor for v-belts."""

import re

mach_group_data = [
    ['stirrer', '1'],
    ['small blower', '1'],
    ['exhaustor', '1'],
    ['centrifugal pump', '1'],
    ['regular compressor', '1'],
    ['light conveyor belt', '1'],
    ['heavy conveyor belt', '2'],
    ['large blower', '2'],
    ['generator', '2'],
    ['transmission axle', '2'],
    ['laundry machine', '2'],
    ['press', '2'],
    ['graphical machine', '2'],
    ['positive displacement pump', '2'],
    ['sieving machine', '2'],
    ['pottery machine', '3'],
    ['bucket elevator', '3'],
    ['reciprocating compressor', '3'],
    ['mill', '3'],
    ['carpentry machine', '3'],
    ['textile machine', '3'],
    ['crusher', '4'],
    ['crane', '4'],
    ['tire shop machine', '4'],
]

drive_group_data = [
    ['normal torque ac', '1'],
    ['ring cage ac', '1'],
    ['synchronous ac', '1'],
    ['phase division ac', '1'],
    ['derivation dc', '1'],
    ['multiple cylinder combustion', '1'],
    ['high torque ac', '2'],
    ['high slipping ac', '2'],
    ['repulsion induction ac', '2'],
    ['monophasic ac', '2'],
    ['series winding dc', '2'],
    ['collector rings ac', '2'],
    ['mixed winding dc', '2'],
    ['single cylinder combustion', '2'],
    ['transmission axle', '2'],
    ['clutch', '2'],
]


def _group(entry, comp_list):
    """Searches the comp_list for the string in the entry and returns the second item

    Args:
        entry (str): string used on the search
        comp_list (list): list of lists that contains the values used on the search
    
    Returns:
        int: second item on the sublist converted to integer"""
    data_regex = re.compile(entry)
    try:
        for item in comp_list:
            m = data_regex.search(item[0])  # search the first item
            if m is not None:
                return int(item[1])
    except:  # stop the execution if nothing is found
        raise ValueError

def _sf_partial(mach_group, service_hours):
    """Select the partial result for the service factor

    Args:
        mach_group (int): machine group for a particular entry
        service_hours (float): hours of service per day of the machine
    
    Returns:
        float: partial service factor regarding machine group and service hours"""
    if mach_group == 1:
        if 0 < service_hours <= 5:
            sf_part = 1.0
        elif 5 < service_hours <= 10:
            sf_part = 1.1
        elif 10 < service_hours <= 24:
            sf_part = 1.2
    elif mach_group == 2:
        if 0 < service_hours <= 5:
            sf_part = 1.1
        elif 5 < service_hours <= 10:
            sf_part = 1.2
        elif 10 < service_hours <= 24:
            sf_part = 1.3
    elif mach_group == 3:
        if 0 < service_hours <= 5:
            sf_part = 1.2
        elif 5 < service_hours <= 10:
            sf_part = 1.3
        elif 10 < service_hours <= 24:
            sf_part = 1.4
    elif mach_group == 4:
        if 0 < service_hours <= 5:
            sf_part = 1.3
        elif 5 < service_hours <= 10:
            sf_part = 1.4
        elif 10 < service_hours <= 24:
            sf_part = 1.5
    return sf_part

def _calc(mach_group, drive_group, _sf_p):
    """Select and calculate the main service factor

    Args:
        mach_group (int): machine group for a particular entry
        drive_group (int): drive group for a particular entry
        _sf_p (float): partial service factor previously calculated
    
    Returns:
        float: service factor
    """
    if mach_group == 1 and drive_group == 2:
        result = _sf_p + 0.1
    elif mach_group == 2 and drive_group == 2:
        result = _sf_p + 0.1
    elif mach_group == 3 and drive_group == 2:
        if _sf_p == 1.4:
            result = _sf_p + 0.1
        else:
            result = _sf_p + 0.2
    elif mach_group == 4 and drive_group == 2:
        if _sf_p == 1.4:
            result = _sf_p + 0.2
        else:
            result = _sf_p + 0.3
    else:
        result = _sf_p
    return round(result, 1)

        
def service_factor(machine:str, drive:str, hours_service:float, mach_list=mach_group_data, drive_list=drive_group_data):
    """Calculate the service factor based on the machine driven, the drive and hours of service per day

    Args:
        machine (str): The type of machine driven. Valid arguments are:
            stirrer, small blower, exhaustor, centrifugal pump, regular compressor, light conveyor,
            heavy conveyor, large blower, generator, transmission axle, laundry machine, press, graphical machine,
            positive displacement pump, sieving machine, pottery machine, bucket elevator, reciprocating compressor,
            mill, carpentry machine, textile machine, crusher, crane, tire shop machine
        drive (str): The type of drive for the machine. Valid arguments are:
            ac motors: normal torque ac, ring cage ac, synchronous ac, phase division ac, high torque ac, high slipping ac, repulsion induction ac,
                       monophasic ac
            dc motors: derivation dc, series winding dc, mixed winding dc
            combustion engine: multiple cylinder combustion, single cylinder combustion
            transmission axle
            clutch
    
    Kargs:
        mach_list: Variable for valid machine list, already configured.
        drive_list: Variable for valid drive list, already configured.

    Returns:
        float: the service factor"""
    machine_group = _group(machine, mach_list)
    drive_group = _group(drive, drive_list)
    precalc = _sf_partial(machine_group, hours_service)
    result = _calc(machine_group, drive_group, precalc)
    return result
