from typing import TypeVar, cast

T = TypeVar("T")


def named(obj: T, name: str) -> T:
    """Python magic to override discreetly __str__ of an object"""

    class NamedMeta(type):
        def __instancecheck__(self, instance):
            return isinstance(type(obj), instance)

        def __subclasscheck__(self, subclass):
            return issubclass(type(obj), subclass)

        def __getattribute__(self, attr):
            return getattr(type(obj), attr)

        def __setattr__(self, attr, value):
            return setattr(type(obj), attr, value)

        def __delattr__(self, attr):
            del type(obj).attr

    class Named(metaclass=NamedMeta):
        def __getattribute__(self, attr):
            return getattr(obj, attr)

        def __setattr__(self, attr, value):
            setattr(obj, attr, value)

        def __delattr__(self, attr):
            del obj.attr

        def __str__(self):
            return name

    return cast(T, Named())
