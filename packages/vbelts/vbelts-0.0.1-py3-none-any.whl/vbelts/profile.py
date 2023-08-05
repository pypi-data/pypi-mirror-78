# internal functions
# function value computing
def _func_val(a, b, c, x, upper):
    # if the value is within the linear function range
    if x < upper:
        eq = a * x + b
        return abs(eq)
    # if the value is within the constant range
    elif x >= upper:
        eq = c
        return eq


# external functions
def hi_power_2(power, rpm):
    # compute all three boundaries for the same power
    rpm_a = _func_val(81.9, 8.57, 3300, power, 40.5)
    rpm_b = _func_val(21.23, 11.00, 2132, power, 100)
    rpm_c = _func_val(6.06, -0.02, 1328, power, 220)
    # categorizes by band where the value stands
    if rpm >= rpm_a:
        return 'A'
    elif rpm_b <= rpm < rpm_a:
        return 'B'
    elif rpm_c <= rpm < rpm_b:
        return 'C'
    elif rpm_c < rpm:
        return 'D'
