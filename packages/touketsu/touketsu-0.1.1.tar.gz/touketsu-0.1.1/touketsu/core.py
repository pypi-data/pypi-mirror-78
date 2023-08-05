__doc__ = """Core package code for ``touketsu``.

Contains the decorators and decorator factory that are the package's lifeblood.
"""

from abc import ABCMeta
from copy import deepcopy
from inspect import signature
from functools import wraps
import warnings

from .utils import classdocmod

# set up warnings
warnings.simplefilter("always")

def class_decorator_factory(dectype = None, docmod = None):
    """``touketsu`` class decorator factory.

    The returned decorator is able to automatically modify the docstrings of
    the wrapped class, provided they follow the docstring format specified in
    `PEP 257`__.

    .. note::

       It is possible to tell which classes have been wrapped a decorator
       returned by :func:`class_decorator_factory` because the decoration
       process introduces additional class attributes prepended by 
       ``_touketsu``. Using :func:`urt_class` on any of these decorated
       classes undos the decoration and returns the class to its original
       definition.

    .. __: https://www.python.org/dev/peps/pep-0257/

    :param dectype: The decorator type. Pass ``"immutable"`` to return a class
        decorator that makes a class instance immutable or ``"nondynamic"`` to
        make a class instance nondynamic.
    :type dectype: str
    :param docmod: How to modify the docstring of the class the returned
        decorator is applied to. Either ``"brief"``, or ``"identity"``. The
        default value is ``"brief"``.
    :type docmod: str, optional
    :returns: A class decorator that either makes disables dynamic attribute
        creation for class instances or makes class instances immutable.
    :type: function
    """
    _fn = class_decorator_factory.__name__
    # if dectype is not valid, raise error
    if (dectype != "immutable") and (dectype != "nondynamic"):
        raise ValueError(f"{_fn}: dectype must be \"immutable\" or "
                         f"\"nondynamic\"")

    # decorator for a class
    def wrapper(cls):
        # raise TypeError if this is not a type or abc.ABCMeta
        if cls.__class__ not in (type, ABCMeta):
            raise TypeError(f"{_fn}: expected type or abc.ABCMeta, received "
                            f"{type(cls)}")
        # class attribute indicating restriction imposed by touketsu
        cls._touketsu_restriction = None
        # original class docstring, original class __init__ and __setattr__
        cls._touketsu_orig__doc__ = cls.__doc__
        _orig__init__ = cls.__init__
        _orig__setattr__ = cls.__setattr__

        # new __setattr__. note: we could just use object.__setattr__, but since
        # self will have the _touketsu_orig__setattr__ pointing to the original
        # __setattr__ of the class, we use that instead. this is useful if the
        # class itself has an overriden __setattr__ method itself.
        def _touketsu_restricted_setattr(self, key, value):
            if self._touketsu_restriction == "immutable":
                raise AttributeError("Immutable class instance")
            elif (self._touketsu_restriction == "nondynamic") and \
                (not hasattr(self, key)):
                raise AttributeError("Nondynamic class instance")
            # use original __setattr__; see _orig__setattr__
            _orig__setattr__(self, key, value)

        # wrapper for class __init__ method
        def init_wrapper(init):
            # for "well-behaved" decoration (don't lose signature and docstring)
            @wraps(init)
            def _init_wrapper(self, *args, **kwargs):
                init(self, *args, **kwargs)
                self._touketsu_restriction = dectype

            return _init_wrapper
        
        # perform docstring modification
        classdocmod(cls, dectype, docmod = docmod)
        # override __setattr__ and __init__ of class + preserve original
        # signature. sphinx doesn't work well with functools.wraps.
        cls.__setattr__ = _touketsu_restricted_setattr
        # warn if the class doesn't override object __init__ method
        try: cls.__init__.__signature__ = signature(cls.__init__)
        except AttributeError:
            warnings.warn("Class without __init__ decorated. object.__init__ "
                          "signature will be displayed instead.")
        cls.__init__ = init_wrapper(cls.__init__)
        # bind original __init__ method to new __init__ so orig_init works
        cls.__init__._touketsu_orig__init__ = _orig__init__
        # bind original __setattr__ to new __setattr__
        cls.__setattr__._touketsu_orig__setattr__ = _orig__setattr__
        # retain original __setattr__ docstring, in case there was one
        cls.__setattr__.__doc__ = _orig__setattr__.__doc__
        # return class
        return cls

    # return decorator
    return wrapper


def urt_class(cls):
    """Remove the ``touketsu`` restriction from a ``touketsu`` decorated class.

    For any class decorated by a decorator returned by 
    :func:`~touketsu.core.class_decorator_factory`, :func:`urt_class` removes
    the decorator's effect, restoring the original :meth:`__init__` and
    :meth:`.__setattr__` methods.

    Useful for removing a ``touketsu`` decorator restriction from a decorated
    class during runtime or a subclass that does not override :meth:`__init__`,
    which results in a superclass :meth:`__init__` beind used instead according
    to the method resolution order.
    
    .. note::

       If the class is undecorated, then :func:`urt_class` will have no
       effect.

    .. note::

       Calling :func:`urt_class` on subclasses of classes decorated by a
       decorator returned from :func:`~touketsu.core.class_decorator_factory`
       will result in warnings being raised, as the ``_touketsu_restriction``
       and ``_touketsu_orig__doc__`` attributes cannot be deleted from the
       subclass, as they are superclass attributes. These warnings can be
       safely ignored, however.

    :param cls: Class decorated by
        :func:`~touketsu.core.class_decorator_factory` decorator
    :type cls: type
    :returns: The original class, without decoration
    :rtype: type
    """
    # try to delete restriction; doesn't work if superclass is also restricted
    if hasattr(cls, "_touketsu_restriction"):
        try: delattr(cls, "_touketsu_restriction")
        except AttributeError:
            warnings.warn("Unable to delete _touketsu_restriction; likely a "
                          "superclass attribute")
    # restore original docstring if necessary and delete _touketsu_orig__doc__
    # note we do delattr before doc assignment since this may be the superclass
    # __doc__, which we do not want
    if hasattr(cls, "_touketsu_orig__doc__"):
        try:
            _orig__doc__ = cls._touketsu_orig__doc__
            delattr(cls, "_touketsu_orig__doc__")
            cls.__doc__ = _orig__doc__
        except AttributeError:
            warnings.warn("Unable to delete _touketsu_orig__doc__; likely a "
                          "superclass attribute")
    # use original __init__ method if necessary. no need for try statement as
    # the __init__ method does not have a direct superclass with the same attr
    if hasattr(cls.__init__, "_touketsu_orig__init__"):
        cls.__init__ = cls.__init__._touketsu_orig__init__
    # override __setattr__ with original __setattr__ if necessary
    if hasattr(cls.__setattr__, "_touketsu_orig__setattr__"):
        cls.__setattr__ = cls.__setattr__._touketsu_orig__setattr__
    # return class
    return cls


def urt_method(meth):
    """Decorate instance methods to temporarily allow attribute creation.
    
    Apply :func:`urt_method` to instance methods to temporarily remove the class
    restriction during the execution of the instance method. For example,
    suppose we have a class ``a_class``, where
    
    .. code:: python
    
       from touketsu import nondynamic, urt_method
       
       @nondynamic
       class a_class:
       
           def __init__(self, a = "a"):
               self.a = a
               
           @classmethod
           def a_class_method(cls):
               cls.aa = 1000
               return cls(a = "A")

           @urt_method
           def method_one(self, val):
               self.b = val
               
           def method_two(self):
               if hasattr(self, "b"):
                   return f"{self.a} UwU {self.b}"
               return f"{self.a} T^T"

    ``method_one`` needs to be decorated with :func:`urt_method` since it will
    create an instance attribute ``b`` when called. However, ``method_two``
    does not need to be decorated since it is not creating or modifying any
    instance attributes. The :func:`classmethod` ``a_class_method`` also does
    not need to be decorated since ``touketsu`` restrictions only apply to class
    *instances*, not the classes themselves.
    
    :param meth: An unbound instance method
    :type meth: function
    :returns: A decorated unbound instance method that allows instance attribute
        modification and creation during its execution.
    :rtype: function
    """
    # wrapper for the method
    @wraps(meth)
    def meth_wrapper(obj, *args, **kwargs):
        # temporarily unrestrict class instance
        restriction = obj._touketsu_restriction
        object.__setattr__(obj, "_touketsu_restriction", None)
        # note try-catch since if an exception is thrown and not caught the
        # restriction will not be reapplied
        try:
            res = meth(obj, *args, **kwargs)
            # restore original restriction (don't need object.__setattr__)
            obj._touketsu_restriction = restriction
            return res
        except Exception as e:
            # restore restriction and raise (don't need object.__setattr__)
            obj._touketsu_restriction = restriction
            raise e

    # make it identifiable as an urt_method
    meth_wrapper.is_urt_method = True

    return meth_wrapper


def orig_init(init):
    """Return original :meth:`__init__` from decorated :meth:`__init__`.

    If ``init`` is not the :meth:`__init__` of a decorated class, then ``init``
    itself is returned.

    :param init: The unbound :meth:`__init__` of the decorated class.
    :type init: function
    :returns: The unbound original :meth:`__init__` of the decorated class or
        ``init``, if ``init`` is not the :meth:`__init__` of a decorated class.
    :rtype: function
    """
    _fn = orig_init.__name__
    # should be a function
    if init.__class__.__name__ == "function":
        # if it contains original init, return that
        if hasattr(init, "_touketsu_orig__init__"):
            return getattr(init, "_touketsu_orig__init__")
        # else return init itself
        return init
    # raise TypeError if necessary
    raise TypeError("{0}: init must be a method or function".format(_fn))


def immutable(cls):
    """Makes a class immutable and modifies the class docstring.

    Equivalent to :func:`class_decorator_factory` with ``dectype = "immutable"``
    and ``docmod = "brief"``. The standard decorator to use for making a class
    immutable.

    .. note::

       Do not apply to a previously decorated class. Instead, use
       :func:`urt_class` first to return the class to its original state before
       applying :func:`immutable`.

    :param cls: The class to decorate.
    :type cls: type
    :returns: A decorated version of the original class with immutable
        instances.
    :rtype: type
    """
    return class_decorator_factory("immutable", "brief")(cls)


def identity_immutable(cls):
    """Makes a class immutable without modifying the class docstring.

    .. caution::

       Since :func:`identity_immutable` does not modify the docstring of the
       class it decorates, it is easy to mistake the decorated class for the
       undecorated class.

    .. note::

       Do not apply to a previously decorated class. Instead, use
       :func:`urt_class` first to return the class to its original state before
       applying :func:`identity_immutable`.

    :param cls: The class to decorate.
    :type cls: type
    :returns: A decorated version of the original class with immutable
        instances.
    :rtype: type
    """
    return class_decorator_factory("immutable", "identity")(cls)


def nondynamic(cls):
    """Makes a class nondynamic and modifies the class docstring.

    Equivalent to :func:`class_decorator_factory` with
    ``dectype = "nondynamic"`` and ``docmod = "brief"``. The standard decorator
    to use for making a class nondynamic.

    .. note::

       Do not apply to a previously decorated class. Instead, use
       :func:`urt_class` first to return the class to its original state before
       applying :func:`nondynamic`.

    :param cls: The class to decorate.
    :type cls: type
    :returns: A decorated version of the original class with immutable
        instances.
    :rtype: type
    """
    return class_decorator_factory("nondynamic", "brief")(cls)


def identity_nondynamic(cls):
    """Makes a class nondynamic without modifying the class docstring.

    .. caution::

       Since :func:`identity_nondynamic` does not modify the docstring of the
       class it decorates, it is easy to mistake the decorated class for the
       undecorated class.

    .. note::

       Do not apply to a previously decorated class. Instead, use
       :func:`urt_class` first to return the class to its original state before
       applying :func:`identity_nondynamic`.

    :param cls: The class to decorate.
    :type cls: type
    :returns: A decorated version of the original class with immutable
        instances.
    :rtype: type
    """
    return class_decorator_factory("nondynamic", "identity")(cls)