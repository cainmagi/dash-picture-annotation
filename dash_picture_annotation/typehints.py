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
    from typing import Sequence, Callable, Mapping
    from typing import List, Type
except ImportError:
    from collections.abc import Sequence, Callable, Mapping
    from builtins import list as List, type as Type

from typing_extensions import Literal, TypedDict, TypeGuard


T = TypeVar("T")

__all__ = (
    "AnnoMark",
    "AnnoItem",
    "Annotations",
    "AnnoStyle",
    "DashSelectOptionItem",
    "Size",
    "NSAnnoItem",
    "NSAnnotations",
    "is_sequence_of",
    "is_anno_mark",
    "is_anno_item",
    "is_annotations",
    "is_dash_select_option_item",
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

    The internal and incomplete definition of `AnnoItem`.
    """

    id: str
    """The ID of the annotation item. This ID is only used for locating which item
    is currently selected by users."""

    mark: AnnoMark
    """The boudning box and the shape information of this annotation item."""


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

    The internal and incomplete definition of `Annotations`.
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


class AnnoStyle(TypedDict, total=False):
    """The css-styles of the annotation marker (box).

    If this value is specified as a string, the string will be parsed as the default
    color of the annotation boxes.
    """

    padding: float
    """Text padding."""

    fontSize: float
    """Text font size."""

    fontColor: str
    """Text font color."""

    fontBackground: str
    """Text background color."""

    fontFamily: str
    """Text font name."""

    lineWidth: float
    """Stroke width."""

    shapeBackground: str
    """Background color in the middle of the marker."""

    shapeStrokeStyle: str
    """Shape stroke color."""

    shadowBlur: float
    """Stroke shadow blur."""

    shapeShadowStyle: str
    """Stroke shape shadow color."""

    transformerBackground: str
    """Color of the scalable dots around the selected box."""

    transformerSize: float
    """Size of the scalable dots around the selected box."""


class _DashSelectOptionItem(TypedDict):
    """The option item of a Dash selectable component. (private, internal)

    The internal and incomplete definition of `DashSelectOptionItem`.
    """

    label: str
    """Label (displayed text) of the option."""

    value: Any
    """The value of the option which will be applied to the annotation data."""


class DashSelectOptionItem(_DashSelectOptionItem, total=False):
    """The option item of a Dash selectable component.

    The available options of the annotator. The usage is like the selector component
    `dcc.Dropdown(options=...)`. Each item represents an available choice of the
    annotation type.
    """

    disabled: bool
    """A flag. If specified, this option item will be not selectable."""


class Size(TypedDict, total=False):
    """The requirement of the minimal annotation size. Any newly created annotation
    with a size smaller than this size will be dropped.

    If this value is configured as a scalar, will use it for both `width` and `height`.

    If any of the value is not set or configured as invalid values, will use `0`.
    """

    width: float
    """Requirement of the minimal width of an annotation."""

    height: float
    """Requirement of the minimal height of an annotation."""


NSAnnoItem = Union[AnnoItem, AnnoMark, Mapping[str, Any]]
"""The type of a not sanitized annotation item."""


class _NSAnnotations(TypedDict):
    """The type of a not sanitized annotation collection. (private, internal)

    The internal and incomplete definition of `NSAnnotations`.
    """

    data: Sequence[NSAnnoItem]
    """A sequence of not sanitized data items. These items will be sanitized can
    put into a sanitized data item list."""


class NSAnnotations(_NSAnnotations, total=False):
    """The type of a not sanitized annotation collection."""


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


def is_dash_select_option_item(obj: Any) -> TypeGuard[DashSelectOptionItem]:
    """Implementation of `isinstance(data, DashSelectOptionItem)`."""
    if not isinstance(obj, collections.abc.Mapping):
        return False
    if "label" in obj and "value" in obj:
        return True
    return False
