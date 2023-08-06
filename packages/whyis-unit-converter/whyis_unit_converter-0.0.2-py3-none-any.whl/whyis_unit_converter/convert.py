""" Converts a value from one unit to another.
    Uses pint to do the actual conversion, expects the user to pass in
    pint-recognized unit names.
"""
from pint import UnitRegistry, UndefinedUnitError, DimensionalityError
import re
from math import log10, floor

ureg = UnitRegistry()
Q_ = ureg.Quantity

def load_user_definitions(user_defs):
    """ Allows the user to load their own unit definitions and aliases."""
    ureg.load_definitions(user_defs)

def convert_to_other_units(from_unit, val, unit_list):
    """ Takes a list of units and converts a value to all of them.
        Returns a list of tuples containing the new unit and value."""
    converted = []
    for to_unit in unit_list:
        if to_unit != from_unit:
            new_value = convert(val, from_unit, to_unit)
            if new_value is not None:
                converted.append((to_unit, new_value))
    return converted

def convert(value, from_unit, to_unit):
    """ Converts a value from one unit to another, and returns the result.
        Expects from_unit and to_unit are pint-recognized strings, else it
        returns None. If an invalid conversion is attempted, it also returns
        None.
    """
    try:
        converted = Q_(value, from_unit).to(to_unit)
    except (UndefinedUnitError, DimensionalityError):
        return None
    else:
        converted_val = round_sig(converted.m, number_of_significant_figures(value))
        return converted_val

def round_sig(x, sig=2):
    """ Rounds to the given number of significant digits, default of 2"""
    return round(x, sig-int(floor(log10(abs(x)))))

def number_of_significant_figures(num):
    """ Returns the number of significant figures a value has. """
    if isinstance(num, int) or num.is_integer():
        num = int(num)
        sig_figs = len(str(num).strip('0'))
    else:
        num_parts = re.split(r'[\.eE]', str(num))
        sig_figs = len(num_parts[1])
    return sig_figs
