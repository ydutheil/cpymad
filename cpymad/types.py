"""
Python type analogues for MAD-X data structures.
"""

from __future__ import division

from collections import namedtuple

from unum import Unum


__all__ = [
    'Range',
    'Constraint',
    'Expression',
]


Range = namedtuple('Range', ['first', 'last'])


class Constraint(object):

    """Represents a MAD-X constraint, which has either min/max/both/value."""

    def __init__(self, val=None, min=None, max=None):
        """Just store the values"""
        self.val = val
        self.min = min
        self.max = max


class Expression(object):

    """
    Data type for lazy-evaluated expressions in MAD-X.

    Instances of this class store the expression string as well as the current
    value (at time of instanciation) of the input expression.

    To re-evaluate the expression, call :meth:`Madx.evaluate`.
    """

    def __init__(self, expr, value, value_type=float):
        """Store string expression and value."""
        self._expr = expr
        self._value = value
        self._type = value_type

    def __repr__(self):
        """Return string representation of this object."""
        return '{}({!r}, {}, {})'.format(self.__class__.__name__,
                                         self.expr, self.value,
                                         self._type.__name__)

    def __str__(self):
        """Get the expression as string."""
        return self.expr

    @property
    def value(self):
        """The numeric value of the expression."""
        return self._type(self._value)

    @property
    def expr(self):
        """The expression string."""
        return self._expr

    # casts to primitive types:

    def __bool__(self):     # python3
        """Get the value as boolean."""
        return bool(self._value)

    __nonzero__ = __bool__  # python2

    def __int__(self):
        """Get the value as integer."""
        return int(self._value)

    def __float__(self):
        """Get the value as double."""
        return float(self._value)

    # arithmetic operators:

    def __add__(self, other): return self.value + other
    def __radd__(self, other): return other + self.value

    def __sub__(self, other): return self.value - other
    def __rsub__(self, other): return other - self.value

    def __mul__(self, other): return self.value * other
    def __rmul__(self, other): return other * self.value

    def __truediv__(self, other): return self.value / other
    def __rtruediv__(self, other): return other / self.value

    def __floordiv__(self, other): return self.value // other
    def __rfloordiv__(self, other): return other // self.value

    def __mod__(self, other): return self.value % other
    def __rmod__(self, other): return other % self.value

    def __divmod__(self, other): return divmod(self.value, other)
    def __rdivmod__(self, other): return divmod(other, self.value)

    def __pow__(self, other): return self.value ** other
    def __rpow__(self, other): return other ** self.value

    # python2 compatibility aliases

    __div__ = __truediv__
    __rdiv__ = __rtruediv__


class UnumExpression(Unum, Expression):

    """Expression with a quantity that has a unit."""

    # NOTE: Unum must be the first base class, so its operator overloads
    # override the ones defined in Expression.

    def __init__(self, expr, unit, value):
        """Initialize the Unum and store the expr as a member."""
        Unum.__init__(self, unit, value)
        self._expr = expr

    def __repr__(self):
        """Return string representation of this object."""
        return '{}({!r}, {})'.format(self.__class__.__name__,
                                     self.expr, self.value)

    @property
    def value(self):
        """Return a copy of the underlying Unum."""
        return Unum(self._unit, self._value)
