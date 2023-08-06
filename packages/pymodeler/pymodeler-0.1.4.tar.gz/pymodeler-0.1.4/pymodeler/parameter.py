#!/usr/bin/env python
"""
Classes used to describe aspect of Models.

The base class is `Property` which describes any one property of a model,
such as the name, or some other fixed property.

The `Parameter` class describes variable model parameters.

The `Derived` class describes model properies that are derived
from other model properties.

"""
from __future__ import absolute_import, division, print_function

from copy import deepcopy
from numbers import Number
from collections import OrderedDict as odict

import numpy as np
import yaml

# Python 3 compatibility
try:
    basestring
except NameError:
    basestring = str


def asscalar(a):
    """Convert single-item lists and numpy arrays to scalars. Does
    not care about the type of the elements (i.e., will work fine on
    strings, etc.)

    https://github.com/numpy/numpy/issues/4701
    https://github.com/numpy/numpy/pull/5126
    """
    try:
        return a.item()
    except AttributeError:
        return np.asarray(a).item()


def defaults_docstring(defaults, header=None, indent=None, footer=None):
    """Return a docstring from a list of defaults.
    """
    if indent is None:
        indent = ''
    if header is None:
        header = ''
    if footer is None:
        footer = ''

    width = 60
    #hbar = indent + width * '=' + '\n'  # horizontal bar
    hbar = '\n'

    s = hbar + (header) + hbar
    for key, value, desc in defaults:
        if isinstance(value, basestring):
            value = "'" + value + "'"
        if hasattr(value, '__call__'):
            value = "<" + value.__name__ + ">"

        s += indent +'%-12s\n' % ("%s :" % key)
        s += indent + indent + (indent + 23 * ' ').join(desc.split('\n'))
        s += ' [%s]\n\n' % str(value)
    s += hbar
    s += footer
    return s


def defaults_decorator(defaults):
    """Decorator to append default kwargs to a function.
    """
    def decorator(func):
        """Function that appends default kwargs to a function.
        """
        kwargs = dict(header='Keyword arguments\n-----------------\n', 
                      indent='  ',
                      footer='\n')
        doc = defaults_docstring(defaults, **kwargs)
        if func.__doc__ is None:
            func.__doc__ = ''
        func.__doc__ += doc
        return func

    return decorator


class Meta(type):
    """Meta class for appending docstring with defaults
    """
    def __new__(mcs, name, bases, attrs):
        attrs['_doc'] = attrs.get('__doc__', '')
        return super(Meta, mcs).__new__(mcs, name, bases, attrs)

    @property
    def __doc__(cls):
        kwargs = dict(header='Parameters\n----------\n', 
                      indent='  ',
                      footer='\n')
        return cls._doc + cls.defaults_docstring(**kwargs)


class Property(object):
    """Base class for model properties.

    This class and its sub-classes implement variations on the concept
    of a 'mutable' value or 'l-value', i.e., an object that can be
    assigned a value.

    This class defines some interfaces that help read/write
    heirachical sets of properties between various formats
    (python dictionaries, yaml files, astropy tables, etc..)

    The pymodeler.model.Model class maps from property names to
    Property instances.

    """
    __metaclass__ = Meta

    __value__ = None

    defaults = [
        ('value', __value__, 'Property value'),
        ('help', "", 'Help description'),
        ('format', '%s', 'Format string for printing'),
        ('dtype', None, 'Data type'),
        ('default', None, 'Default value'),
        ('required', False, 'Is this propery required?'),
        ('unit', None, 'Units associated to value'),
    ]

    @defaults_decorator(defaults)
    def __init__(self, **kwargs):
        self._load(**kwargs)
        if self.__value__ is None and self.__dict__['default'] is not None:
            self.set_value(self.__dict__['default'])

    def __str__(self):
        return self.__value__.__str__()

    def __repr__(self):
        return self.__value__.__str__()

    def _load(self, **kwargs):
        """Load kwargs key,value pairs into __dict__
        """
        defaults = dict([(d[0], d[1]) for d in self.defaults])
        # Require kwargs are in defaults
        for k in kwargs:
            if k not in defaults:
                msg = "Unrecognized attribute of %s: %s" % (
                    self.__class__.__name__, k)
                raise AttributeError(msg)
        defaults.update(kwargs)

        # This doesn't overwrite the properties
        self.__dict__.update(defaults)

        # This should now be set
        self.check_type(self.__dict__['default'])

        # This sets the underlying property values (i.e., __value__)
        self.set(**defaults)

    @classmethod
    def defaults_docstring(cls, header=None, indent=None, footer=None):
        """Add the default values to the class docstring"""
        return defaults_docstring(cls.defaults, header=header,
                                  indent=indent, footer=footer)

    @property
    def value(self):
        """Return the current value

        This may be modified by sub-classes to do additional
        operations (such as caching the results of
        complicated operations needed to compute the value)
        """
        return self.__value__

    def innertype(self):
        """Return the type of the current value
        """
        return type(self.__value__)

    def __call__(self):
        """ __call__ will return the current value

        By default this invokes `self.value`
        so, any additional functionality that sub-classes implement,
        (such as caching the results of
        complicated operations needed to compute the value)
        will also be invoked
        """
        return self.value

    def set(self, **kwargs):
        """Set the value to kwargs['value']

        The invokes hooks for type-checking and bounds-checking that
        may be implemented by sub-classes.
        """
        if 'value' in kwargs:
            self.set_value(kwargs.pop('value', None))

    def set_value(self, value):
        """Set the value

        This invokes hooks for type-checking and bounds-checking that
        may be implemented by sub-classes.
        """
        self.check_bounds(value)
        self.check_type(value)
        self.__value__ = value

    def clear_value(self):
        """Set the value to None

        This can be useful for sub-classes that use None
        to indicate an un-initialized value.

        Note that this invokes hooks for type-checking and
        bounds-checking that may be implemented by sub-classes, so it
        should will need to be re-implemented if those checks do note
        accept None as a valid value.

        """
        self.set_value(None)

    def todict(self):
        """Convert to a '~collections.OrderedDict' object.

        By default this only assigns {'value':self.value}
        """
        return odict(value=self.value)

    def dump(self):
        """Dump this object as a yaml string
        """
        return yaml.dump(self)

    def check_bounds(self, value):
        """Hook for bounds-checking, invoked during assignment.

        Sub-classes can raise an exception for out-of-bounds input values.
        """
        pass

    def check_type(self, value):
        """Hook for type-checking, invoked during assignment.

        raises TypeError if neither value nor self.dtype are None and they
        do not match.

        will not raise an exception if either value or self.dtype is None
        """
        if self.__dict__['dtype'] is None:
            return
        elif value is None:
            return
        elif isinstance(value, self.__dict__['dtype']):
            return
        msg = "Value of type %s, when %s was expected." % (
            type(value), self.__dict__['dtype'])
        raise TypeError(msg)


class Derived(Property):
    """Property sub-class for derived model properties (i.e., properties
    that depend on other properties)

    This allows specifying the expected data type and formatting
    string for printing, and specifying a 'loader' function by name
    that is used to compute the value of the property.

    """

    defaults = deepcopy(Property.defaults) + [
        ('loader', None, 'Function to load datum')
    ]

    @defaults_decorator(defaults)
    def __init__(self, **kwargs):
        super(Derived, self).__init__(**kwargs)

    @property
    def value(self):
        """Return the current value.

        This first checks if the value is cached (i.e., if
        `self.__value__` is not None)

        If it is not cached then it invokes the `loader` function to
        compute the value, and caches the computed value

        """

        if self.__value__ is None:
            try: 
                loader = self.__dict__['loader']
            except KeyError:
                raise AttributeError("Loader is not defined")

            # Try to run the loader.
            # Don't catch expections here, let the Model class figure it out
            val = loader()

            # Try to set the value
            try:
                self.set_value(val)
            except TypeError:
                msg = "Loader must return variable of type %s or None, got %s" % (self.__dict__['dtype'], type(val))
                raise TypeError(msg)
        return self.__value__


class Parameter(Property):
    """Property sub-class for defining a numerical Parameter.

    This includes value, bounds, error estimates and fixed/free status
    (i.e., for fitting)

    Adapted from MutableNum: https://gist.github.com/jheiv/6656349

    """

    __value__ = None
    __bounds__ = None
    __free__ = False
    __errors__ = None

    # Better to keep the structure consistent with Property
    defaults = deepcopy(Property.defaults) + [
        ('bounds', __bounds__, 'Allowed bounds for value'),
        ('errors', __errors__, 'Errors on this parameter'),
        ('free', __free__, 'Is this propery allowed to vary?'),
    ]
    # Overwrite the default dtype
    idx = [d[0] for d in defaults].index('dtype')
    defaults[idx] = ('dtype', Number, 'Data type')

    @defaults_decorator(defaults)
    def __init__(self, **kwargs):
        super(Parameter, self).__init__(**kwargs)

    def check_type(self, value):
        """Hook for type-checking, invoked during assignment. Allows size 1
        numpy arrays and lists, but raises TypeError if value can not
        be cast to a scalar.

        """
        try:
            scalar = asscalar(value)
        except ValueError as e:
            raise TypeError(e)

        super(Parameter, self).check_type(scalar)

    # Comparison Methods
    def __eq__(self, x):
        return self.__value__ == x

    def __ne__(self, x):
        return self.__value__ != x

    def __lt__(self, x):
        return self.__value__ < x

    def __gt__(self, x):
        return self.__value__ > x

    def __le__(self, x):
        return self.__value__ <= x

    def __ge__(self, x):
        return self.__value__ >= x

    def __cmp__(self, x):
        return 0 if self.__value__ == x else 1 if self.__value__ > 0 else -1

    # Unary Ops

    def __pos__(self):
        return +self.__value__

    def __neg__(self):
        return -self.__value__

    def __abs__(self):
        return abs(self.__value__)

    # Bitwise Unary Ops

    def __invert__(self):
        return ~self.__value__

    # Arithmetic Binary Ops

    def __add__(self, x):
        return self.__value__ + x

    def __sub__(self, x):
        return self.__value__ - x

    def __mul__(self, x):
        return self.__value__ * x

    def __div__(self, x):
        return self.__value__ / x

    def __mod__(self, x):
        return self.__value__ % x

    def __pow__(self, x):
        return self.__value__ ** x

    def __floordiv__(self, x):
        return self.__value__ // x

    def __divmod__(self, x):
        return divmod(self.__value__, x)

    def __truediv__(self, x):
        return self.__value__.__truediv__(x)

    # Reflected Arithmetic Binary Ops

    def __radd__(self, x):
        return x + self.__value__

    def __rsub__(self, x):
        return x - self.__value__

    def __rmul__(self, x):
        return x * self.__value__

    def __rdiv__(self, x):
        return x / self.__value__

    def __rmod__(self, x):
        return x % self.__value__

    def __rpow__(self, x):
        return x ** self.__value__

    def __rfloordiv__(self, x):
        return x // self.__value__

    def __rdivmod__(self, x):
        return divmod(x, self.__value__)

    def __rtruediv__(self, x):
        return x.__truediv__(self.__value__)

    # Bitwise Binary Ops

    def __and__(self, x):
        return self.__value__ & x

    def __or__(self, x):
        return self.__value__ | x

    def __xor__(self, x):
        return self.__value__ ^ x

    def __lshift__(self, x):
        return self.__value__ << x

    def __rshift__(self, x):
        return self.__value__ >> x

    # Reflected Bitwise Binary Ops

    def __rand__(self, x):
        return x & self.__value__

    def __ror__(self, x):
        return x | self.__value__

    def __rxor__(self, x):
        return x ^ self.__value__

    def __rlshift__(self, x):
        return x << self.__value__

    def __rrshift__(self, x):
        return x >> self.__value__

    # ADW: Don't allow compound assignments
    # Compound Assignment
    #def __iadd__(self, x):      self.set(self + x); return self
    #def __isub__(self, x):      self.set(self - x); return self
    #def __imul__(self, x):      self.set(self * x); return self
    #def __idiv__(self, x):      self.set(self / x); return self
    #def __imod__(self, x):      self.set(self % x); return self
    #def __ipow__(self, x):      self.set(self **x); return self

    # Casts
    def __nonzero__(self):
        return self.__value__ != 0

    def __bool__(self):
        return self.__value__.__bool__()

    def __int__(self):
        return self.__value__.__int__()

    def __float__(self):
        return self.__value__.__float__()

    def __long__(self):
        return self.__value__.__long__()

    # Conversions

    def __oct__(self):
        return self.__value__.__oct__()

    def __hex__(self):
        return self.__value__.__hex__()

    # Random Ops

    def __index__(self):
        return self.__value__.__index__()

    def __trunc__(self):
        return self.__value__.__trunc__()

    def __coerce__(self, x):
        return self.__value__.__coerce__(x)

    # Represenation
    # ADW: This should probably be __str__ not __repr__
    def __repr__(self):
        if self.bounds is None:
            bounds = '[None, None]'
        else:
            bounds = '[%s, %s]' % (self.bounds[0], self.bounds[1])
        if self.errors is None:
            errors = '[None, None]'
        else:
            errors = '[%s, %s]' % (self.errors[0], self.errors[1])

        return "%s(%s, %s, %s, %s)" % (self.__class__.__name__,
                                       self.value, bounds, errors, self.free)

    @property
    def bounds(self):
        """Return the parameter bounds.

        None implies unbounded.
        """
        return self.__bounds__

    @property
    def free(self):
        """Return the fixd/free status """
        return self.__free__

    @property
    def errors(self):
        """Return the parameter uncertainties.

        None implies no error estimate.
        Single value implies symmetric errors.
        Two values implies low,high asymmetric errors.
        """
        return self.__errors__

    @property
    def symmetric_error(self):
        """Return the symmertic error

        Similar to above, but zero implies no error estimate,
        and otherwise this will either be the symmetric error,
        or the average of the low,high asymmetric errors.
        """
        # ADW: Should this be `np.nan`?
        if self.__errors__ is None:
            return 0.
        if np.isscalar(self.__errors__):
            return self.__errors__
        return 0.5 * (self.__errors__[0] + self.__errors__[1])

    def item(self):
        """For asscalar """
        return self.value

    def check_bounds(self, value):
        """Hook for bounds-checking, invoked during assignment.

        raises ValueError if value is outside of bounds.
        does nothing if bounds is set to None.
        """
        if self.__bounds__ is None:
            return
        if not self.__bounds__[0] <= value <= self.__bounds__[1]:
            msg = "Value outside bounds: %.2g [%.2g,%.2g]"
            msg = msg % (value, self.__bounds__[0], self.__bounds__[1])
            raise ValueError(msg)

    def set_bounds(self, bounds):
        """Set bounds """
        if bounds is None:
            self.__bounds__ = None
            return
        self.__bounds__ = [asscalar(b) for b in bounds]

    def set_free(self, free):
        """Set free/fixed status """
        if free is None:
            self.__free__ = False
            return
        self.__free__ = bool(free)

    def set_errors(self, errors):
        """Set parameter error estimate """
        if errors is None:
            self.__errors__ = None
            return
        self.__errors__ = [asscalar(e) for e in errors]

    def set(self, **kwargs):
        """Set the value,bounds,free,errors based on corresponding kwargs

        The invokes hooks for type-checking and bounds-checking that
        may be implemented by sub-classes.
        """
        # Probably want to reset bounds if set fails
        if 'bounds' in kwargs:
            self.set_bounds(kwargs.pop('bounds'))
        if 'free' in kwargs:
            self.set_free(kwargs.pop('free'))
        if 'errors' in kwargs:
            self.set_errors(kwargs.pop('errors'))
        if 'value' in kwargs:
            self.set_value(kwargs.pop('value'))

    def todict(self):
        """Convert to a '~collections.OrderedDict' object.

        This assigns {'value':self.value,'bounds'=self.bounds,
                      'free'=self.free,'errors'=self.errors}
        """
        return odict(value=self.value, bounds=self.bounds,
                     free=self.free, errors=self.errors)

    def dump(self):
        """Dump this object as a yaml string
        """
        return yaml.dump(self)

    @staticmethod
    def representer(dumper, data):
        """
        http://stackoverflow.com/a/14001707/4075339
        http://stackoverflow.com/a/21912744/4075339
        """
        tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG
        return dumper.represent_mapping(
            tag, data.todict().items(), flow_style=True)

Param = Parameter


def odict_representer(dumper, data):
    """ http://stackoverflow.com/a/21912744/4075339 """
    # Probably belongs in a util
    return dumper.represent_mapping(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, data.items())

yaml.add_representer(odict, odict_representer)
yaml.add_representer(Parameter, Parameter.representer)
