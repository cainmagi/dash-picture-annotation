# -*- coding: UTF-8 -*-
"""
Typehints
=========
@ Dash Picture Annotation

Author
------
Yuchen Jin (cainmagi)
cainmagi@gmail.com

Description
-----------
Extra typehints used by this project.
"""

import collections.abc

from typing import Union, Any, TypeVar

try:
    from typing import Sequence, Callable
    from typing import List, Type
except ImportError:
    from collections.abc import Sequence, Callable
    from builtins import list as List, type as Type

from typing_extensions import Literal, TypedDict, TypeGuard


T = TypeVar("T")

__all__ = (
    "AnnoMark",
    "AnnoItem",
    "Annotations",
    "is_sequence_of",
    "is_anno_mark",
    "is_anno_item",
    "is_annotations",
)


class AnnoMark(TypedDict):
    """The `mark` property in the annotation item.

    This property contains the position and the shape of the bounding box. Currently,
    we only support the rectangular annotation.
    """

    x: float
    """The x (horizontal) position of the upper left corner of the annotation item."""

    y: float
    """The y (vertical) position of the upper left corner of the annotation item."""

    width: float
    """The width of the bounding box."""

    height: float
    """The height of the bounding box."""

    type: Literal["RECT"]
    """The type of the annotation shape. Currently, we only support `"RECT"`
    (rectangle)."""


class _AnnoItem(TypedDict):
    """Annotation item. (private, internal)

    The internal and incomplete definition of `AnnoItem`
    """

    id: str
    """The ID of the annotation item. This ID is only used for locating which item
    is currently selected by users."""

    mark: AnnoMark
    """The boudning box and the shape information of thie annotation item."""


class AnnoItem(_AnnoItem, total=False):
    """Annotation item.

    This dictionary represents the definition of one annotation item with its bounding
    box information.
    """

    comment: str
    """The text attached to this annotation item. Typically, this value is the type of
    the label."""


class _Annotations(TypedDict):
    """The collection of annotations. (private, internal)

    The internal and incomplete definition of `Annotations`
    """

    data: List[AnnoItem]
    """A collection of annotation items. These items are decoded from JSON data and
    can be modified. Use these items to specify the annotations."""


class Annotations(_Annotations, total=False):
    """The collection of annotations.

    This dictionary contain the data of annotations.
    """

    timestamp: int
    """The time stamp recording when the user interaction changes the data. Note that
    this value is necessary for ensuring that the user triggered changes will not be
    omitted. From the server side, this value can be set by `0` because the user
    interaction will use a higher value to replace it."""


def is_sequence_of(
    data: Any, validator: Union[Type[T], Callable[[Any], TypeGuard[T]]]
) -> TypeGuard[Sequence[T]]:
    """Check whether `data` is `Sequence[T]`, where `T` is specified by `validator`."""
    if not isinstance(data, collections.abc.Sequence):
        return False
    if not data:
        return True
    if isinstance(validator, type):
        if isinstance(data, validator):
            return False
        return all(isinstance(ditem, validator) for ditem in data)
    else:
        return all(validator(ditem) for ditem in data)


def is_anno_mark(data: Any) -> TypeGuard[AnnoMark]:
    """Implementation of `isinstance(data, AnnoMark)`."""
    if not isinstance(data, collections.abc.Mapping):
        return False
    for key in ("x", "y", "width", "height", "type"):
        if key not in data:
            return False
    if data["type"] != "RECT":
        return False
    return True


def is_anno_item(data: Any) -> TypeGuard[AnnoItem]:
    """Implementation of `isinstance(data, AnnoItem)`."""
    if not isinstance(data, collections.abc.Mapping):
        return False
    for key in ("id", "mark"):
        if key not in data:
            return False
    if not is_anno_mark(data["mark"]):
        return False
    if not isinstance(data.get("comment", ""), str):
        return False
    return True


def is_annotations(data: Any) -> TypeGuard[Annotations]:
    """Implementation of `isinstance(data, Annotations)`."""
    if not isinstance(data, collections.abc.Mapping):
        return False
    timestamp = data.get("timestamp")
    if timestamp is not None and (not isinstance(timestamp, int)):
        return False
    anno_data = data.get("data")
    if not isinstance(anno_data, collections.abc.MutableSequence):
        return False
    for anno in anno_data:
        if not is_anno_item(anno):
            return False
    return True
