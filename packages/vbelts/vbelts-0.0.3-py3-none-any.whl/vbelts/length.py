"""Length

Utilities for determining center distances between pulleys and belt length"""

from vbelts.diam import _interpol
from vbelts.diam import OutOfRangeError

super_hc_length = [
    ['3V', {635:'3V250', 675:'3V265', 710:'3V280', 760:'3V300', 800:'3V315', 850:'3V355', 900:'3V355', 955:'3V375', 1015:'3V400', 1080:'3V425', 1145:'3V450', 1205:'3V475', 1270:'3V500', 1345:'3V530', 1420:'3V560', 1525:'3V600', 1600:'3V630', 1700:'3V670', 1805:'3V710', 1905:'3V750', 2030:'3V800', 2160:'3V850', 2285:'3V900', 2415:'3V950', 2540:'3V1000', 2690:'3V1060', 2845:'3V1120', 2995:'3V1180', 3175:'3V1250', 3355:'3V1320', 3555:'3V1400'}],
    ['5V', {1270:'5V500', 1345:'5V530', 1420:'5V560', 1525:'5V600', 1600:'5V630', 1700:'5V670', 1805:'5V710', 1905:'5V750', 2030:'5V800', 2160:'5V850', 2285:'5V900', 2415:'5V950', 2540:'5V1000', 2690:'5V1060', 2845:'5V1120', 2995:'5V1180', 3175:'5V1250', 3355:'5V1320', 3555:'5V1400', 3810:'5V1500', 4065:'5V1600', 4320:'5V1700', 4570:'5V1800', 4825:'5V1900', 5080:'5V2000', 5385:'5V2120', 5690:'5V2240', 5995:'5V2360', 6350:'5V2500', 6730:'5V2650', 7110:'5V2800', 7620:'5V3000', 8000:'5V3150', 8510:'5V3350', 9015:'5V3350'}],
    ['8V', {2540:'8V1000', 2690:'8V1060', 2845:'8V1120', 2995:'8V1180', 3175:'8V1250', 3355:'8V1320', 3555:'8V1400', 3810:'8V1500', 4065:'8V1600', 4320:'8V1700', 4570:'8V1800', 4825:'8V1900', 5080:'8V2000', 5385:'8V2120', 5690:'8V2240', 5995:'8V2360', 6350:'8V2500', 6730:'8V2650', 7110:'8V2800', 7620:'8V3000', 8000:'8V3150', 8510:'8V3350', 9017:'8V3550', 9525:'8V3750', 10160:'8V4000', 10795:'8V4250', 11430:'8V4500', 12065:'8V4750', 12700:'8V5000', 14225:'8V5600'}]
]

hipower_2_length = [
    ['A', {695:'A-26', 720:'A-27', 820:'A-31', 845:'A-32', 870:'A-33', 920:'A-35', 975:'A-37', 1000:'A-38', 1075:'A-41', 1100:'A-42', 1175:'A-45', 1200:'A-46', 1225:'A-47', 1280:'A-49', 1305:'A-50', 1330:'A-51', 1380:'A-53', 1405:'A-54', 1430:'A-55', 1480:'A-57', 1555:'A-60', 1610:'A-62', 1660:'A-64', 1710:'A-66', 1760:'A-68', 1785:'A-69', 1835:'A-71', 1940:'A-75', 2065:'A-80', 2190:'A-85', 2320:'A-90', 2470:'A-96', 2700:'A-105', 2880:'A-112', 3080:'A-120', 3285:'A-128', 3485:'A-136', 3690:'A-144', 4045:'A-158', 4150:'A-162', 4425:'A-173', 4605:'A-180'}],
    ['B', {935:'B-35', 985:'B37', 1010:'B-38', 1035:'B-39', 1115:'B-42', 1215:'B-46', 1265:'B-48', 1315:'B-50', 1340:'B-51', 1365:'B-52', 1390:'B-53', 1445:'B-55', 1570:'B-60', 1645:'B-63', 1670:'B-64', 1695:'B-65', 1775:'B-68', 1850:'B-71', 1900:'B-73', 1950:'B-75', 2025:'B-78', 2105:'B-81', 2205:'B-85', 2330:'B-90', 2410:'B-93', 2460:'B-95', 2510:'B-97', 2715:'B-105', 2890:'B-112', 3095:'B-120', 3195:'B-124', 3295:'B-128', 3500:'B-136', 3705:'B-144', 4060:'B-158', 4160:'B-162', 4440:'B-173', 4620:'B-180', 5000:'B-195', 5360:'B-210', 5725:'B-225', 6105:'B-240', 6865:'B-270', 7630:'B-300', 8390:'B-330', 9150:'B-360'}],
    ['C', {1370:'C-51', 1470:'C-55', 1545:'C-58', 1600:'C-60', 1675:'C-63', 1800:'C-68', 1875:'C-71', 1900:'C-72', 1930:'C-73', 1980:'C-75', 2130:'C-81', 2235:'C-85', 2360:'C-90', 2510:'C-96', 2615:'C-100', 2740:'C-105', 2920:'C-112', 3120:'C-120', 3325:'C-128', 3530:'C-136', 3730:'C-144', 4085:'C-158', 4190:'C-162', 4470:'C-173', 4645:'C-180', 5025:'C-195', 5410:'C-210', 5470:'C-225', 6120:'C-240', 6500:'C-255', 6880:'C-270', 7645:'C-300', 8405:'C-330', 9165:'C-360', 9930:'C-390', 10690:'C-420'}],
    ['D', {3130:'D-120', 3335:'D-128', 3540:'D-136', 3740:'D-144', 4095:'D-158', 4200:'D-162', 4480:'D-173', 4655:'D-180', 5035:'D-195', 5420:'D-210', 5735:'D-225', 6115:'D-240', 6370:'D-250', 6880:'D-270', 7640:'D-300', 8400:'D-330', 9165:'D-360', 9925:'D-390', 10690:'D-420', 12210:'D-480'}]
]

h_factor = {0:0, 0.02:0.01, 0.04:0.02, 0.06:0.03, 0.08:0.04, 0.1:0.05, 0.12:0.06, 0.14:0.07, 0.16:0.08, 0.18:0.09, 0.2:0.1, 0.21:0.11, 0.23:0.12, 0.25:0.13, 0.27:0.14, 0.29:0.15, 0.3:0.16, 0.32:0.17, 0.34:0.18, 0.35:0.19, 0.37:0.2, 0.39:0.21, 0.4:0.22, 0.41:0.23, 0.43:0.24, 0.44:0.25, 0.46:0.26, 0.47:0.27, 0.48:0.28, 0.5:0.29, 0.51:0.3}


def _min_dist(x:float, x_min:float, x_max:float):
    """Returns the nearest value between two items, given one item that is in the interval of the two

    Args:
        x (float): desired value for calculation
        x_min (float): nearest minimum value on the scale
        x_max (float): nearest maximum value on the scale
    
    Returns:
        float: nearest value of x"""
    dist_1 = (x - x_min)/x
    dist_2 = (x_max - x)/x
    if dist_1 < dist_2:
        return x_min
    elif dist_1 > dist_2:
        return x_max
    elif dist_1 == dist_2: # if both are equal, return the maximum
        return x_max
    else:
        raise ValueError


def _belt_std(b_type:str, length:float, vbelt_list:list):
    """Select an item (belt model) on a dictionary inside a list

    Args:
        b_type (str): type of v-belt, valid values depend on the list passed
        length (float): linear length of the v-belt, mm
        vbelt_list (list): formatted list containing the model, length and type

    Returns:
        tuple: first item is the selected length, second item is the selected model"""
    for item in vbelt_list:
        if b_type == item[0]:
            last_length = 0
            for key in item[1].keys():
                if length < next(iter(item[1])):  # if the length is smaller than the first item on the dictionary
                    raise OutOfRangeError('The value is too small, please select another')
                if key == length:
                    return (key, item[1].get(key))
                elif key > length:
                    chosed_key = _min_dist(length, last_length, key)
                    return (chosed_key, item[1].get(chosed_key))
                last_length = key
            raise OutOfRangeError('Value out of range for these parameters')


def corr_dist_factor(max_diam:float, min_diam:float, l_a:float, corr_list=h_factor):
    """Calculate and select the appropriate correction factor for the center distance

    Args:
        max_diam (float): major diameter of the pulley, mm
        min_diam (float): minor diameter of the pulley, mm
        l_a (float): corrected belt length, mm
    
    Returns:
        float: correction factor for the center distance"""
    adim_factor = (max_diam - min_diam)/l_a
    for key in corr_list:
        last_factor = 0
        if key == adim_factor:
            return corr_list.get(key)
        elif key > adim_factor:
            return round(_interpol(adim_factor, last_factor, key, corr_list.get(last_factor), corr_list.get(key)), 2)  # 2 digits
        last_factor = key
    raise OutOfRangeError('Value out of range for these parameters')

def belt_super_hc(superhc_model:str, length:float):
    """Select the model for a Super-HC like v-belt based on the linear length of the belt
    
    Args:
        superhc_model (str): selected type of Super-HC, valid values are \'3V\', \'5V\' and \'8V\'
        length (float): linear length needed for the belt, mm
    
    Returns:
        tuple: first item is the selected length, second item is the selected model"""
    return _belt_std(superhc_model, length, super_hc_length)

def belt_hi_power_2(hipower2_model:str, length:float):
    """Select the model for a Hi-Power 2 like v-belt based on the linear length of the belt
    
    Args:
        hipower2_model (str): selected type of Hi-Power 2, valid values are \'A\', \'B\', \'C\' and \'D\'
        length (float): linear length needed for the belt, mm
    
    Returns:
        tuple: first item is the selected length, second item is the selected model"""
    return _belt_std(hipower2_model, length, hipower_2_length)


def center_dist_uncorr(max_diam:float, min_diam:float):
    """Calculate the predetermined center distance between two pulleys

    Args:
        max_diam (float): major diameter of the pulleys, mm
        min_diam (float): minor diameter of the pulleys, mm
    
    Returns:
        float: center distance for the pulleys used, mm"""
    return (3 * min_diam + max_diam)/2


def belt_len_corr(l_c:float, max_diam:float, min_diam:float):
    """Calculates the corrected belt length for commercial belts

    Args:
        l_c (float): commercial belt length, mm
        max_diam (float): major diameter of the pulleys, mm
        min_diam (float): minor diameter of the pulleys, mm
    
    Returns:
        float: belt length corrected, mm"""
    return round(l_c - 1.57*(max_diam + min_diam), 2)


def center_dist_corr(l_a:float, h:float, max_diam:float, min_diam:float):
    """Calculates the corrected center distance for commercial belts

    Args:
        l_a (float): corrected belt length, mm
        h (float): correction factor for the center distance
        max_diam (float): major diameter of the pulleys, mm
        min_diam (float): minor diameter of the pulleys, mm
    
    Returns:
        float: corrected center distance between the pulleys, mm"""
    return round((l_a - h*(max_diam - min_diam))/2, 2)


def belt_len_uncorr(center:float, max_diam:float, min_diam:float):
    """Calculate the uncorrected belt length

    Args:
        center (float): distance between pulleys, mm
        min_diam (float): minor diameter between the pulleys, mm
        max_diam (float): major diameter between the pulleys, mm
    
    Returns:
        float: uncorrected belt length, mm"""
    return round((2*center) + 1.57*(max_diam + min_diam) + ((max_diam - min_diam)**2)/(4 * center), 2)
