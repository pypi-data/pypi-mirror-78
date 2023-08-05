__doc__ = "Various utilities for the ``touketsu`` package."

from textwrap import fill

# left and right formatting strings for identifier appended by _docmod_class to
# a docstring when docmod is "brief" or "fancy" (_RFMT should end with " ")
_LFMT = "**["
_RFMT = "]** "


def classdocmod(obj, class_type, docmod = None):
    """Modifies a class docstring.

    For the function to work properly, the docstring should be `PEP 257`__ 
    compliant. If ``docmod = "fancy"``, restructuredText will be injected into
    the docstring.

    .. note:: This function may be extended in future releases.

    .. __: https://www.python.org/dev/peps/pep-0257/

    :param obj: The class whose docstring is to be modified.
    :type obj: str
    :param class_type: Either ``"immutable"``, if the class docstring belongs to
        a class decorated by :func:`immutable`, or ``"nondynamic"`` if the
        docstring belongs to a class decorated by :func:`nondynamic`.
    :type class_type: str
    :param docmod: Specifies how to modify the docstring. As an example, suppose
        ``class_type = "immutable"``. If ``docmod = "brief"``, then the string
        ``"[Immutable] "`` will be prepended to the docstring. If ``docmod`` is
        ``None`` or ``"identity"``, then the docstring is returned unmodified.
    :type docmod: str, optional
    :param docwidth: The width of the fina
    :type docwidth: int, optional
    :rtype: None
    """
    _fn = classdocmod.__name__
    # if docstring is None, set to "" first
    odoc = obj.__doc__
    if odoc is None: odoc = ""
    # skip checks; supposed to be internal function
    if (docmod is None) or (docmod == "identity"): return None
    elif docmod == "brief":
        obj.__doc__ = _LFMT + class_type.title() + _RFMT + odoc
        return None
    raise ValueError(f"{classdocmod.__name__}: docmod must be \"brief\", or "
                     f"\"identity\"")