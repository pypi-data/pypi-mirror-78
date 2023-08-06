"""Pulley diameter utilities

Utilities for determining pulley mininimum diameter and related variables"""

super_hc = [
    [485, 575, {0.5:0, 0.75:0, 1:3, 1.5:3, 2:3.8, 3:4.5, 5:4.5, 7.5:5.2, 10:6, 15:6.8, 20:8.2, 25:9, 30:10, 40:10, 50:11, 60:12, 75:14, 100:18, 125:20, 150:22, 200:22, 250:22, 300:27}],
    [575, 690, {0.5:0, 0.75:0, 1:2.5, 1.5:3, 2:3, 3:3.8, 5:4.5, 7.5:4.5, 10:5.2, 15:6, 20:6.8, 25:8.2, 30:9, 40:10, 50:10, 60:11, 75:13, 100:15, 125:18, 150:20, 200:22, 250:22, 300:27}],
    [690, 870, {0.5:2.2, 0.75:2.4, 1:2.4, 1.5:2.4, 2:3, 3:3, 5:3.8, 7.5:4.4, 10:4.4, 15:5.2, 20:6, 25:6.8, 30:6.8, 40:8.2, 50:8.4, 60:10, 75:9.5, 100:12, 125:15, 150:18, 200:22}],
    [870, 1160, {0.5:0, 0.75:2.2, 1:2.4, 1.5:2.4, 2:2.4, 3:3, 5:3, 7.5:3.8, 10:4.4, 15:4.4, 20:5.2, 25:6, 30:6.8, 40:6.8, 50:8.2, 60:8, 75:10, 100:10, 125:12, 150:13}],
    [1160, 1750, {0.5:0, 0.75:0, 1:2.2, 1.5:2.4, 2:2.4, 3:2.4, 5:3, 7.5:3, 10:3.8, 15:4.4, 20:4.4, 25:4.4, 30:5.2, 40:6, 50:6.8, 60:7.4, 75:8.6, 100:8.6, 125:10.5, 150:10.5, 200:13.2}],
    [1750, 3450, {0.5:0, 0.75:0, 1:0, 1.5:2.2, 2:2.4, 3:2.4, 5:2.4, 7.5:3, 10:3, 15:3.8, 20:4.4, 25:4.4}]
]

hi_power_2 = [
    [485, 575, {0.5:2.5, 0.75:3, 1:3, 1.5:3, 2:3.8, 3:4.5, 5:4.5, 7.5:5.2, 10:6, 15:6.8, 20:8.2, 25:9, 30:10, 40:10, 50:11, 60:12, 75:14, 100:18, 125:20, 150:22, 200:22, 250:22, 300:27}],
    [575, 690, {0.5:2.5, 0.75:2.5, 1:3, 1.5:3, 2:3, 3:3.8, 5:4.5, 7.5:4.5, 10:5.2, 15:6, 20:6.8, 25:8.2, 30:9, 40:10, 50:10, 60:11, 75:13, 100:15, 125:18, 150:20, 200:22, 250:22, 300:27}],
    [690, 870, {0.5:2.2, 0.75:2.4, 1:2.4, 1.5:2.4, 2:3, 3:3, 5:3.8, 7.5:4.4, 10:4.6, 15:5.4, 20:6, 25:6.8, 30:6.8, 40:8.2, 50:9.0, 60:10, 75:10.5, 100:12.5, 125:15, 150:18, 200:22}],
    [870, 1160, {0.5:0, 0.75:2.2, 1:2.4, 1.5:2.4, 2:2.4, 3:3, 5:3, 7.5:3.8, 10:4.4, 15:4.6, 20:5.4, 25:6, 30:6.8, 40:6.8, 50:8.2, 60:9, 75:10, 100:11, 125:12.5, 150:13}],
    [1160, 1750, {0.5:0, 0.75:0, 1:2.2, 1.5:2.4, 2:2.4, 3:2.4, 5:3, 7.5:3, 10:3.8, 15:4.4, 20:4.6, 25:5, 30:5.4, 40:6, 50:6.8, 60:7.4, 75:9, 100:10, 125:11.5}],
    [1750, 3450, {0.5:0, 0.75:0, 1:0, 1.5:2.2, 2:2.4, 3:2.4, 5:2.6, 7.5:3, 10:3, 15:3.8, 20:4.4, 25:4.4}]
]


class OutOfRangeError(Exception):
    """Raised when value is out of range of the list"""
    pass

class NotValidError(Exception):
    """Raised when the value passed to the function is not valid"""


def _diam(vbelt_list:list, power:float, speed:float):
    """Chosses the minimum diameter for in a list containing the engine power and rpm

    Args:
        vbelt_list (list): list of pulley diameters containing speed range and engine power
        power (float): engine power, hp
        speed (float): main rotation speed of the engine, rpm
    
    Returns:
        float: pulley diameter, in"""
    for item in vbelt_list:
        if item[0] <= speed < item[1]:
            last_power = 0
            last_diam = 0
            for key in item[2].keys():  # loops through the keys of dict
                if power == key:
                    if item[2].get(key) == 0:  # zero diameter is not valid
                        raise OutOfRangeError('Value out of range for these parameters')
                    else:
                        return item[2].get(key)
                elif key > power:
                    power_max = key
                    diam_max = item[2].get(key)
                    power_min = last_power
                    diam_min = last_diam
                    pulley_diam = _interpol(power, power_min, power_max, diam_min, diam_max)  # interpolates using the function
                    if pulley_diam == 0:  # zero diameter is not valid
                        raise OutOfRangeError('Value out of range for these parameters')
                    return pulley_diam
                last_power = key  # stores the last power
                last_diam = item[2].get(key)  # stores the last diameter
            raise OutOfRangeError('Value out of range for these parameters')


def _interpol(x_data:float, x_min:float, x_max:float, y_min:float, y_max:float):
    """Linear interpolation of the table data

    Args:
        x_data (float): desired input data point
        x_min (float): nearest minimum input value in relation to the data point
        x_max (float): nearest maximum input value in relation to the data point
        y_min (float): nearest minimum output value in the relation to the data point
        y_max (float): nearest maximum output value in the relation to the data point
    
    Results:
        float: interpolated output value"""
    return y_max-((x_max - x_data)/(x_max - x_min))*(y_max - y_min)


def min_pulley(vbelt_model:str, axle_power:float, axle_speed:float, mode='si'):
    """Select the minimum pulley diameter for a pulley, given the drive power and speed

    Args:
        vbelt_model (str): set the vbelt model from the two available: \'super hc\' or \'hi power 2\'
        axle_power (float): axle power, hp
        axle_speed (float): speed of the fastest axle, rpm
    
    Kargs:
        mode (str): sets the result diameter unit, the standard is in the SI unit, \'imp\' for imperial
    
    Returns:
        float: minimum diameter for the pulley, mm or in
    """
    # chooses the model
    if vbelt_model == 'super hc':
        li = super_hc
    elif vbelt_model == 'hi power 2':
        li = hi_power_2
    else:
        raise NotValidError("Value of the vbelt_model variable is not valid")
    diameter = _diam(li, axle_power, axle_speed)
    if mode == 'si':
        return 25.4 * diameter
    elif mode == 'imp':
        return diameter
    else:
        raise ValueError

def driven_pulley(input_pulley_diam:float, gear_ratio:float):
    """Calculates the driven pulley diameter

    Args:
        input_pulley_diam (float): Input (drive) pulley diameter
        gear_ratio (float): transmission ratio, decimal
    
    Returns:
        float: driven pulley diameter"""
    # check for the right data type
    if isinstance(input_pulley_diam, (float, int)) and isinstance(gear_ratio, (float, int)):
        return input_pulley_diam*gear_ratio
    else:
        raise ValueError

def drive_pulley(output_pulley_diam:float, gear_ratio:float):
    """Calculates the drive pulley diameter

    Args:
        output_pulley_diam (float): output (driven) pulley diameter
        gear_ratio (float): transmission ratio, decimal
    
    Returns:
        float: drive pulley diameter"""
    # check for the right data type
    if isinstance(output_pulley_diam, (float, int)) and isinstance(gear_ratio, (float, int)):
        return output_pulley_diam/gear_ratio
    else:
        raise ValueError
