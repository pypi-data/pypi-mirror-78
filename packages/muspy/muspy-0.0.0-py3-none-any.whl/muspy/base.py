"""Base classes.

This module defines the bases classes for MusPy objects.

Classes
-------

- Base
- ComplexBase

"""
from collections import OrderedDict
from inspect import isclass
from operator import attrgetter
from typing import Any, Callable, List, Mapping, Optional, Type, TypeVar

import yaml

__all__ = ["Base", "ComplexBase"]

Base_ = TypeVar("Base_", bound="Base")
ComplexBase_ = TypeVar("ComplexBase_", bound="ComplexBase")


class _OrderedDumper(yaml.SafeDumper):
    """A dumper that supports OrderedDict."""

    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)


def _dict_representer(dumper, data):
    return dumper.represent_mapping(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, data.items()
    )


_OrderedDumper.add_representer(OrderedDict, _dict_representer)


def _yaml_dump(data):
    """Dump data to YAML, which supports OrderedDict.

    Code adapted from https://stackoverflow.com/a/21912744.
    """
    return yaml.dump(data, Dumper=_OrderedDumper, allow_unicode=True)


def _get_type_string(attr_cls):
    """Return a string represeting acceptable type(s)."""
    if isinstance(attr_cls, (list, tuple)):
        if len(attr_cls) > 1:
            return (
                ", ".join([x.__name__ for x in attr_cls[:-1]])
                + " or "
                + attr_cls[-1].__name__
            )
        return attr_cls[0].__name__
    return attr_cls.__name__


class Base:
    """The base class of MusPy objects.

    It provides the following features.

    - Intuitive and meaningful `__repr__` in the form of
      `class_name(attr_1=value_1, attr_2=value_2,...)`.
    - Method `from_dict`: Instantiate an object whose attributes and the
      the corresponding values are given as a dictionary.
    - Method `to_ordered_dict`: Returns the object as an OrderedDict.
    - Method `validate_type`: Raise TypeError if any attribute of the object
      is of the wrong type according to `_attributes` (see Notes).
    - Method `validate`: Raise TypeError or ValueError if any attribute of
      the object is of the wrong type according to `_attributes` (see
      Notes) or having an invalid value.
    - Method `is_valid_type`: Return True if each attribute of the object is
      of the correct type according to `_attributes` (see Notes).
    - Method `is_valid`: Return True if each attribute of the object is
      of the correct type according to `_attributes` (see Notes) and having
      a valid value.
    - Method `adjust_time`: Adjust the timing of time-stamped objects. For
      example, if `tempo` is an instance of the :class:`muspy.Tempo` class
      and `func` is a callable, then calling `tempo.adjust_time(func)` leads
      to `tempo.time = func(tempo.time)`.

    Notes
    -----
    This is the base class for MusPy objects. To add a new class, please
    inherit from this class and set the following class variables properly.

    - `_attributes`: An OrderedDict with all the attributes (both required
      and optional ones) of the object as keys and their types as values.
    - `_optional_attributes`: A list containing optional attributes. An
      attribute in this list is allowed to be None.
    - _list_attributes: A list containing attributes that are lists.

    """

    _attributes: Mapping[str, Any] = {}
    _optional_attributes: List[str] = []
    _list_attributes: List[str] = []
    _sort_attributes: List[str] = []

    def _init(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __init__(self, **kwargs):
        self._init(**kwargs)

    def __repr__(self):
        to_join = []
        for attr in self._attributes:
            value = getattr(self, attr)
            if attr in self._list_attributes:
                if not value:
                    continue
                if len(value) > 3:
                    to_join.append(
                        attr + "=" + repr(value[:3])[:-1] + ", ...]"
                    )
                else:
                    to_join.append(attr + "=" + repr(value))
            elif value is not None:
                to_join.append(attr + "=" + repr(value))
        return type(self).__name__ + "(" + ", ".join(to_join) + ")"

    def __eq__(self, other) -> bool:
        for attr in self._attributes:
            if getattr(self, attr) != getattr(other, attr):
                return False
        return True

    @classmethod
    def from_dict(cls: Type[Base_], dict_: Mapping) -> Base_:
        """Return an instance constructed from a dictionary.

        Parameters
        ----------
        dict_ : dict
            A dictionary that stores the attributes and their values as
            key-value pairs.

        """
        kwargs = {}
        for attr, attr_cls in cls._attributes.items():
            value = dict_.get(attr)
            if value is None:
                if attr in cls._optional_attributes:
                    continue
                raise TypeError("`{}` must not be None.".format(attr))
            if isclass(attr_cls) and issubclass(attr_cls, Base):
                if attr in cls._list_attributes:
                    kwargs[attr] = [attr_cls.from_dict(v) for v in value]
                else:
                    kwargs[attr] = attr_cls.from_dict(value)
            else:
                kwargs[attr] = value
        return cls(**kwargs)

    def to_ordered_dict(self, ignore_null: bool = True) -> OrderedDict:
        """Return the object as an OrderedDict."""
        ordered_dict: OrderedDict = OrderedDict()
        for attr, attr_cls in self._attributes.items():
            value = getattr(self, attr)
            if attr in self._list_attributes:
                if not value and ignore_null:
                    continue
                if isclass(attr_cls) and issubclass(attr_cls, Base):
                    ordered_dict[attr] = [v.to_ordered_dict() for v in value]
                else:
                    ordered_dict[attr] = value
            elif value is None:
                if not ignore_null:
                    ordered_dict[attr] = None
            elif isclass(attr_cls) and issubclass(attr_cls, Base):
                ordered_dict[attr] = value.to_ordered_dict()
            else:
                ordered_dict[attr] = value
        return ordered_dict

    def pretty_str(self) -> str:
        """Return the content as a string in pretty YAML-like format."""
        return _yaml_dump(self.to_ordered_dict())

    def print(self):
        """Print the content in a pretty YAML-like format."""
        print(self.pretty_str())

    def _validate_attr_type(self, attr: str):
        attr_cls = self._attributes[attr]
        value = getattr(self, attr)
        if value is None:
            if attr in self._optional_attributes:
                return
            raise TypeError("`{}` must not be None".format(attr))
        if attr in self._list_attributes:
            if not isinstance(value, list):
                raise TypeError("`{}` must be a list.".format(attr))
            for v in value:
                if not isinstance(v, attr_cls):
                    raise TypeError(
                        "`{}` must be a list of type {}.".format(
                            attr, _get_type_string(attr_cls)
                        )
                    )
        elif not isinstance(value, attr_cls):
            raise TypeError(
                "`{}` must be of type {}.".format(
                    attr, _get_type_string(attr_cls)
                )
            )

    def validate_type(self: Base_, attr: Optional[str] = None) -> Base_:
        """Raise proper errors if a certain attribute is of wrong type.

        This will apply recursively to an attribute's attributes.

        Parameters
        ----------
        attr : str
            Attribute to validate. If None, validate all attributes. Defaults
            to None.

        """
        if attr is None:
            for attribute in self._attributes:
                self._validate_attr_type(attribute)
        else:
            self._validate_attr_type(attr)
        return self

    def _validate(self, attr: str):
        attr_cls = self._attributes[attr]
        if isclass(attr_cls) and issubclass(attr_cls, Base):
            if attr in self._list_attributes:
                if getattr(self, attr):
                    for item in getattr(self, attr):
                        item.validate()
            else:
                getattr(self, attr).validate()
        else:
            self._validate_attr_type(attr)
            if attr == "time" and getattr(self, "time") < 0:
                raise ValueError("`time` must be nonnegative.")

    def validate(self: Base_, attr: Optional[str] = None) -> Base_:
        """Raise proper errors if a certain attribute is invalid.

        This will apply recursively to an attribute's attributes.

        Parameters
        ----------
        attr : str
            Attribute to validate. If None, validate all attributes. Defaults
            to None.

        """
        if attr is None:
            for attribute in self._attributes:
                self._validate(attribute)
        else:
            self._validate(attr)
        return self

    def is_type_valid(self, attr: Optional[str] = None) -> bool:
        """Return True if a certain attribute is valid, otherwise False.

        This will apply recursively to an attribute's attributes.

        Parameters
        ----------
        attr : str
            Attribute to validate. If None, validate all attributes. Defaults
            to None.

        """
        try:
            self.validate_type(attr)
        except TypeError:
            return False
        return True

    def is_valid(self, attr: Optional[str] = None) -> bool:
        """Return True if a certain attribute is valid, otherwise False.

        This will recursively apply to an attribute's attributes.

        Parameters
        ----------
        attr : str
            Attribute to validate. If None, validate all attributes. Defaults
            to None.

        """
        try:
            self.validate(attr)
        except (TypeError, ValueError):
            return False
        return True

    def _adjust_time(self, func: Callable[[int], int], attr: str):
        attr_cls = self._attributes[attr]
        if attr == "time":
            if "time" in self._list_attributes:
                new_list = [func(item) for item in getattr(self, "time")]
                setattr(self, "time", new_list)
            else:
                setattr(self, "time", func(getattr(self, attr)))
        else:
            if isclass(attr_cls) and issubclass(attr_cls, Base):
                if attr in self._list_attributes:
                    for item in getattr(self, attr):
                        item.adjust_time(func)
                elif getattr(self, attr) is not None:
                    getattr(self, attr).adjust_time(func)

    def adjust_time(
        self: Base_, func: Callable[[int], int], attr: Optional[str] = None
    ) -> Base_:
        """Adjust the timing of time-stamped objects.

        This will apply recursively to an attribute's attributes.

        Parameters
        ----------
        func : callable
            The function used to compute the new timing from the old timing,
            i.e., `new_time = func(old_time)`.
        attr : str
            Attribute to adjust. If None, adjust all attributes. Defaults to
            None.

        """
        if attr is None:
            for attribute in self._attributes:
                self._adjust_time(func, attribute)
        else:
            self._adjust_time(func, attr)
        return self


class ComplexBase(Base):
    """A base class that supports operations on list attributes.

    The supported operations are

    - Method `remove_invalid`: Remove invalid items from list attributes.
    - Method `append`: Automatically append the object to the corresponding
      list. For example, if `track` is an instance of the
      :class:`muspy.Track` class and `note` is an instance of the
      :class:`muspy.Note` class, then calling `track.append(note)` leads to
      `track.notes.append(note)`.
    - Method `sort`: Sort the time-stamped objects with respect to the
      `time` attribute. For example, if `track` is an instance of the
      :class:`muspy.Track` class, then calling `track.sort()` leads to
      `track.notes.sort(lambda x: x.time)`.

    """

    def _append(self, obj):
        for attr in self._list_attributes:
            attr_cls = self._attributes[attr]
            if isinstance(obj, attr_cls):
                if isclass(attr_cls) and issubclass(attr_cls, Base):
                    if getattr(self, attr) is None:
                        setattr(self, attr, [obj])
                    else:
                        getattr(self, attr).append(obj)
                    return
        raise TypeError(
            "Cannot find a list of type {}.".format(type(obj).__name__)
        )

    def append(self: ComplexBase_, obj) -> ComplexBase_:
        """Append an object to the correseponding list."""
        self._append(obj)
        return self

    def _remove_invalid(self, attr: str):
        if not getattr(self, attr):
            return
        attr_cls = self._attributes[attr]
        new_value = []
        if isclass(attr_cls) and issubclass(attr_cls, Base):
            for item in getattr(self, attr):
                if item.is_valid():
                    new_value.append(item)
        else:
            for item in getattr(self, attr):
                if isinstance(item, self._attributes[attr]):
                    new_value.append(item)
        setattr(self, attr, new_value)

    def remove_invalid(
        self: ComplexBase_, attr: Optional[str] = None
    ) -> ComplexBase_:
        """Remove invalid items from list attributes, others left unchanged.

        This will apply recursively to an attribute's attributes.

        Parameters
        ----------
        attr : str
            Attribute to check. If None, check all attributes. Defaults to
            None.

        """
        if attr is not None and attr not in self._list_attributes:
            raise TypeError("`{}` must be a list attribute.")

        if attr is None:
            for attribute in self._list_attributes:
                self._remove_invalid(attribute)
        else:
            self._remove_invalid(attr)

        return self

    def _remove_duplicate(self, attr: str):
        if not getattr(self, attr):
            return

        attr_cls = self._attributes[attr]
        if isclass(attr_cls) and issubclass(attr_cls, ComplexBase):
            getattr(self, attr).remove_duplicate()
        else:
            value = getattr(self, attr)
            new_value = [value[0]]
            for item, next_item in zip(value[:-1], value[1:]):
                if item != next_item:
                    new_value.append(next_item)
            setattr(self, attr, new_value)

    def remove_duplicate(
        self: ComplexBase_, attr: Optional[str] = None
    ) -> ComplexBase_:
        """Remove duplicate items.

        Parameters
        ----------
        attr : str
            Attribute to check. If None, check all attributes. Defaults to
            None.

        """
        if attr is not None and attr not in self._list_attributes:
            raise TypeError("`{}` must be a list attribute.")

        if attr is None:
            for attribute in self._list_attributes:
                self._remove_duplicate(attribute)
        else:
            self._remove_duplicate(attr)

        return self

    def _sort(self, attr: str):
        if not getattr(self, attr):
            return

        attr_cls = self._attributes[attr]
        if isclass(attr_cls) and issubclass(attr_cls, Base):
            # pylint: disable=protected-access
            if issubclass(attr_cls, ComplexBase):
                getattr(self, attr).sort()
            elif attr_cls._sort_attributes:
                getattr(self, attr).sort(
                    attrgetter(*attr_cls._sort_attributes)
                )

    def sort(self: ComplexBase_, attr: Optional[str] = None) -> ComplexBase_:
        """Sort the time-stamped objects recursively.

        This will apply recursively to an attribute's attributes.

        Parameters
        ----------
        attr : str
            Attribute to sort. If None, sort all attributes. Defaults to None.

        """
        if attr is not None and attr not in self._list_attributes:
            raise TypeError("`{}` must be a list attribute.")

        if attr is None:
            for attribute in self._list_attributes:
                self._sort(attribute)
        else:
            self._sort(attr)

        return self
