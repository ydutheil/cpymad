"""
Add units to quantities as used by MAD-X.
"""

import warnings

from unum import Unum
import unum.units           # imported for side effects

from .types import Expression, UnumExpression


__all__ = [
    'add',
    'remove',
    'label',
]


# Units of the quantities spit-out and accepted by MAD-X:
units = {
    'l':        {'m': 1},
    'lrad':     {'m': 1},
    'at':       {'m': 1},
    's':        {'m': 1},
    'x':        {'m': 1},
    'y':        {'m': 1},
    'betx':     {'m': 1},
    'bety':     {'m': 1},
    'angle':    {'rad': 1},
    'k1':       {'m': -2},
    'k1s':      {'m': -2},
    'k1l':      {'m': -2},
    'ex':       {'m': 1},
    'ey':       {'m': 1},
    'tilt':     {'rad': 1},
    'hgap':     {'m': 1},
    'h':        {'rad': 1, 'm': -1},
    'fint':     {},
    'fintx':    {},
    'e1':       {'rad': 1},
    'e2':       {'rad': 1},
    'ks':       {'m': -1},
}


def add(name, value):
    """Add units to a number spit out by MAD-X."""
    try:
        unit = units[name]
    except KeyError:
        return value
    if isinstance(value, Expression):
        return UnumExpression(value.expr, unit, value.value)
    return Unum(unit, value)


def remove(name, value):
    """Remove units from a quantity to feed to MAD-X."""
    try:
        unit = Unum(units[name])
    except KeyError:
        unit = None
    try:
        return value.asNumber(unit)
    except AttributeError:
        if unit is not None:
            warnings.warn("Unit should be used for {0}={1}"
                          .format(name, value))
        return value


def label(quantity):
    """Get name of the unit."""
    return quantity.strUnit().strip('[]')


def dict_add(d):
    """Add units to all known quantities in a dictionary."""
    return {k: add(k, v) for k, v in d.items()}


def dict_remove(d):
    """Remove units from all known quantities in a dictionary."""
    return {k: remove(k, v) for k, v in d.items()}
