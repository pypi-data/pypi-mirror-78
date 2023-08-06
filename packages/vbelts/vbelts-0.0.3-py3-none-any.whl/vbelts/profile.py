"""Profile

Calculate and select vbelt profiles"""

# internal functions
# function value computing
def _func_val(a:float, b:float, c:float, x:float, upper:float):
    """Calculates x for a mathematical function with a linear (ax + b) and a constant part

    Args:
        a (float): a coefficient for the linear part of the function
        b (float): b coefficient for the linear part of the function
        c (float): y value for the constant part of the function
        x (float): the desired value of x
        upper (float): the upper limit of the linear function
    
    Results:
        float: the y value for math function"""
    # if the value is within the linear function range
    if x < upper:
        eq = a * x + b
        return abs(eq)
    # if the value is within the constant range
    elif x >= upper:
        eq = c
        return eq


# external functions
def hi_power_2(power:float, rpm:float):
    """Select the profile for Hi Power 2 type v-Belts with the estimated power and the rpm of the fastest axle

    Args:
        power (float): estimated power of the system, hp
        rpm (float): rotational speed of the fastest axle, rpm
    
    Returns:
        str: v-belt chosen profile"""
    # compute all three boundaries for the same power
    rpm_a = _func_val(74.1950272674027, 47.215442190042, 3322, power, 50.7)
    rpm_b = _func_val(19.3889694765281, 32.2532889843209, 2151.4, power, 122.3)
    rpm_c = _func_val(4.94622293507244, 19.7301462298106, 1335.9, power, 277.35)
    # categorizes by band where the value stands
    if rpm >= rpm_a:
        return 'A'
    elif rpm_b <= rpm < rpm_a:
        return 'B'
    elif rpm_c <= rpm < rpm_b:
        return 'C'
    elif rpm_c > rpm:
        return 'D'

def super_hc(power:float, rpm:float):
    """Select the profile for Super HC type v-Belts with the estimated power and the rpm of the fastest axle

    Args:
        power (float): estimated power of the system, hp
        rpm (float): rotational speed of the fastest axle, rpm
    
    Returns:
        str: v-belt chosen profile"""
    rpm_3v = _func_val(40.6961726224751, 11.8866879052094, 3316.25, power, 91)
    rpm_5v = _func_val(4.30114168431602, 3.84423100031302, 1332.74, power, 309)
    if rpm >= rpm_3v:
        return '3V'
    elif rpm_5v <= rpm < rpm_3v:
        return '5V'
    elif rpm_5v > rpm:
        return '8V'
