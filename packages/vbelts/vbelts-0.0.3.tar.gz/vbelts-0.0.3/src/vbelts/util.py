"""Utilities"""

def gear_ratio(input_pulley:float, output_pulley:float):
    """Calculates the gear ratio

    Args:
        input pulley (float): input (drive) pulley diameter
        output pulley (float): output (driven) pulley diameter
    
    Returns:
        float: gear ratio"""
    if isinstance(input_pulley, (float, int)) and isinstance(output_pulley, (float, int)):
        return output_pulley/input_pulley
    else:
        raise ValueError


def est_power(engine_power:float, serv_factor:float):
    """Calculates the estimated power to run the pulley system

    Args:
        engine_power (float): engine power, hp
        serv_factor (float): calculated service factor, use vbelts.service_factor()
    
    Returns:
        float: estimated power, hp"""
    if isinstance(engine_power, (float, int)) and isinstance(serv_factor, (float, int)):
        return engine_power * serv_factor
    else:
        raise ValueError