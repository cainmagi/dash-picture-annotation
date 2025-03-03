# -*- coding: UTF-8 -*-
"""
Utilities
=========
@ Dash Picture Annotation

Author
------
Yuchen Jin (cainmagi)
cainmagi@gmail.com

Description
-----------
Utilities used for managing the data of the annotation results.
"""

import re
import uuid
import hashlib
import datetime
import collections.abc

from typing import Union, Optional, TypeVar

try:
    from typing import Sequence, AbstractSet
    from typing import List, Tuple, Set, FrozenSet
except ImportError:
    from collections.abc import Sequence, Set as AbstractSet
    from builtins import (
        list as List,
        tuple as Tuple,
        set as Set,
        frozenset as FrozenSet,
    )

from typing_extensions import Literal

from . import typehints as th


T = TypeVar("T")

__all__ = (
    "get_data_item",
    "get_data_item_with_default",
    "get_data_items",
    "get_data_items_by_regex",
    "get_all_ids",
    "get_all_comments",
    "compare_anno_marks",
    "sanitize_data_item",
    "sanitize_data",
    "sanitize_scale",
)


def get_data_item(
    data: Union[th.Annotations, Sequence[th.AnnoItem]], id: str
) -> th.AnnoItem:
    """Get an annotation item by its unique ID.

    Note that this method will not validate the format of `data`. If the item cannot
    be found, will raise a `KeyError`.

    Arguments
    ---------
    data: `Annotations | [AnnoItem]`
        The annotation data that is queried.

    id: `str`
        The ID of the annotation item to be found.

    Returns
    -------
    #1: `AnnoItem`
        The queried value. If not found, raise an `KeyError`.
    """
    val = get_data_item_with_default(data, id)
    if val is None:
        raise KeyError('The ID "{0}" is not found in the data.'.format(id))
    return val


def get_data_item_with_default(
    data: Union[th.Annotations, Sequence[th.AnnoItem]], id: str, default: T = None
) -> Union[th.AnnoItem, T]:
    """Get an annotation item by its unique ID with a default value provided.

    Note that this method will not validate the format of `data`. If the item cannot
    be found, will return the default value.

    Arguments
    ---------
    data: `Annotations | [AnnoItem]`
        The annotation data that is queried.

    id: `str`
        The ID of the annotation item to be found.

    default: `T`
        If the ID is not found in the data, return this value.

    Returns
    -------
    #1: `AnnoItem | T`
        The queried value or the default value given by this method.
    """
    if isinstance(data, collections.abc.Mapping):
        data = data["data"]
    if not isinstance(data, collections.abc.Sequence):
        raise TypeError(
            "Cannot iterate the given `data` which type is: "
            "{0}".format(data.__class__.__name__)
        )
    for ditem in data:
        if not isinstance(ditem, collections.abc.Mapping):
            continue
        if "id" not in ditem:
            continue
        val_id = ditem["id"]
        if not isinstance(val_id, str):
            continue
        if val_id == id:
            return ditem
    return default


def get_data_items(
    data: Union[th.Annotations, Sequence[th.AnnoItem]],
    comment: Optional[str] = None,
    n: Optional[int] = None,
) -> Tuple[th.AnnoItem, ...]:
    """Get one or several annotation items by exactly matching the comment.

    Note that this method will not validate the format of each returned annotation
    items. Not well-formatted items will STILL be returned.

    Arguments
    ---------
    data: `Annotations | [AnnoItem]`
        The annotation data that is queried.

    comment: `str | None`
        The comment of the annoatations to be selected. This value will be exactly
        matched in the data, which means that it is space- and case-sensitive.

        If using `None`, will return the annotations without comments.

    n: `int | None`
        Limit the maximal number of the items to be found. If not provided, will try
        to return all annotation items with a specified `comment`.

        Specifying a non-positive value will cause this number to be ignored.

    Returns
    -------
    #1: `[AnnoItem]`
        The located annotation items. Modifying the content of these items will
        cause the `data` to be modified.
    """
    if isinstance(data, collections.abc.Mapping):
        data = data["data"]
    if not isinstance(data, collections.abc.Sequence):
        raise TypeError(
            "Cannot iterate the given `data` which type is: "
            "{0}".format(data.__class__.__name__)
        )
    res: List[th.AnnoItem] = list()
    n_has = 0
    if isinstance(n, int) and n <= 0:
        n = None
    for ditem in data:
        if not isinstance(ditem, collections.abc.Mapping):
            continue
        _comment = ditem.get("comment")
        if _comment == comment:
            res.append(ditem)
            n_has += 1
        if n is not None and n_has >= n:
            break
    return tuple(res)


def get_data_items_by_regex(
    data: Union[th.Annotations, Sequence[th.AnnoItem]],
    comment_regex: Optional[Union[str, re.Pattern]] = None,
    n: Optional[int] = None,
) -> Tuple[th.AnnoItem, ...]:
    """Get one or several annotation items by matching the comment with a regular
    expression.

    The regex is done by `re.match`.

    Note that this method will not validate the format of each returned annotation
    items. Not well-formatted items will STILL be returned.

    Arguments
    ---------
    data: `Annotations | [AnnoItem]`
        The annotation data that is queried.

    comment_regex: `str | re.Pattern | None`
        The regular expression used for matching the comment of the annoatations.
        All comments matching the regex can be returned.

        If using `None`, will return the annotations without comments.

    n: `int | None`
        Limit the maximal number of the items to be found. If not provided, will try
        to return all annotation items with the `comment` matched.

        Specifying a non-positive value will cause this number to be ignored.

    Returns
    -------
    #1: `[AnnoItem]`
        The located annotation items. Modifying the content of these items will
        cause the `data` to be modified.
    """
    if isinstance(data, collections.abc.Mapping):
        data = data["data"]
    if not isinstance(data, collections.abc.Sequence):
        raise TypeError(
            "Cannot iterate the given `data` which type is: "
            "{0}".format(data.__class__.__name__)
        )
    res: List[th.AnnoItem] = list()
    if isinstance(comment_regex, str):
        comment_regex = re.compile(comment_regex)
    if comment_regex is not None and (not isinstance(comment_regex, re.Pattern)):
        raise TypeError(
            'The argument "comment_regex" is not a valid regular expression '
            "pattern: {0}".format(comment_regex)
        )
    n_has = 0
    if isinstance(n, int) and n <= 0:
        n = None
    for ditem in data:
        if not isinstance(ditem, collections.abc.Mapping):
            continue
        _comment = ditem.get("comment")
        if (comment_regex is None and _comment is None) or (
            comment_regex is not None
            and _comment is not None
            and re.match(comment_regex, _comment) is not None
        ):
            res.append(ditem)
            n_has += 1
        if n is not None and n_has >= n:
            break
    return tuple(res)


def get_all_ids(data: Union[th.Annotations, Sequence[th.AnnoItem]]) -> Tuple[str, ...]:
    """Get the list of all IDs in the annotation data. The returne IDs are ordered
    as the order of the items in `data`.

    Arguments
    ---------
    data: `Annotations | [AnnoItem]`
        The annotation data that is queried.

    Returns
    -------
    #1: `[str]`
        The ordered IDs of the annotation items in the data.
    """
    if isinstance(data, collections.abc.Mapping):
        data = data["data"]
    if not isinstance(data, collections.abc.Sequence):
        raise TypeError(
            "Cannot iterate the given `data` which type is: "
            "{0}".format(data.__class__.__name__)
        )
    return tuple(
        ditem["id"]
        for ditem in data
        if isinstance(ditem, collections.abc.Mapping)
        and isinstance(ditem.get("id"), str)
    )


def get_all_comments(
    data: Union[th.Annotations, Sequence[th.AnnoItem]]
) -> FrozenSet[str]:
    """Get the set of all comments in the annotation data. The returned comments are
    unordered.

    Arguments
    ---------
    data: `Annotations | [AnnoItem]`
        The annotation data that is queried.

    Returns
    -------
    #1: `{str}`
        The unordered set of comments appearing in the annotation data. If the data
        does not contain any comment, will return an empty set.
    """
    if isinstance(data, collections.abc.Mapping):
        data = data["data"]
    if not isinstance(data, collections.abc.Sequence):
        raise TypeError(
            "Cannot iterate the given `data` which type is: "
            "{0}".format(data.__class__.__name__)
        )
    res: Set[str] = set()
    for ditem in data:
        if not isinstance(ditem, collections.abc.Mapping):
            continue
        _comment = ditem.get("comment")
        if isinstance(_comment, str):
            res.add(_comment)
    return frozenset(res)


def compare_anno_marks(
    anno_item_1: Union[th.AnnoItem, th.AnnoMark],
    anno_item_2: Union[th.AnnoItem, th.AnnoMark],
    tolearance: float = 0.1,
) -> bool:
    """Compare whether two annotation marks are equivalent or not.

    The comparison is only performed on the positions. The ID and the comment of the
    annotation items will not be compared.

    Arguments
    ---------
    anno_item_1: `AnnoItem | AnnoMark`
    anno_item_2: `AnnoItem | AnnoMark`
        The annotation items to be compared.

    tolearance: `float`
        The tolerance used for checking whether positions are the same or not.

    Returns
    -------
    #1: `bool`
        A flag. Returns `True` if the two items are in the same position and share the
        same size.

        Will return `False` if any of them is not an annotation item or mark.
    """
    if not (
        isinstance(anno_item_1, collections.abc.Mapping)
        and isinstance(anno_item_2, collections.abc.Mapping)
    ):
        return False
    if "mark" in anno_item_1:
        anno_item_1 = anno_item_1["mark"]
    if "mark" in anno_item_2:
        anno_item_2 = anno_item_2["mark"]
    if not (th.is_anno_mark(anno_item_1) and th.is_anno_mark(anno_item_2)):
        return False
    if abs(abs(anno_item_1["width"]) - abs(anno_item_2["width"])) > tolearance:
        return False
    if abs(abs(anno_item_1["height"]) - abs(anno_item_2["height"])) > tolearance:
        return False
    if (
        abs(
            (
                anno_item_1["x"]
                if anno_item_1["width"] > 0
                else (anno_item_1["x"] + anno_item_1["width"])
            )
            - (
                anno_item_2["x"]
                if anno_item_2["width"] > 0
                else (anno_item_2["x"] + anno_item_2["width"])
            )
        )
        > tolearance
    ):
        return False
    if (
        abs(
            (
                anno_item_1["y"]
                if anno_item_1["height"] > 0
                else (anno_item_1["y"] + anno_item_1["height"])
            )
            - (
                anno_item_2["y"]
                if anno_item_2["height"] > 0
                else (anno_item_2["y"] + anno_item_2["height"])
            )
        )
        > tolearance
    ):
        return False
    return True


def _generate_id(n: int = 3) -> str:
    """Generate the random ID. (private method)

    Arguments
    ---------
    n: `int`
        The number of characters of the ID.

    Returns
    -------
    #1: `str`
        The randomly generated ID.
    """
    hash_code = hashlib.shake_256()
    hash_code.update(uuid.uuid4().bytes)
    return hash_code.hexdigest(n)


def sanitize_data_item(data_item: th.NSAnnoItem) -> Optional[th.AnnoItem]:
    """Perform the full sanitization on an annotation item.

    The sanitization will ensure that:
    1. The result is a dictionary typed by `AnnoItem`.
    2. A `None` value comment will be removed.
    3. The position of the annotation mark will always have positive width and height.
       (Negative values means that the starting location is reversed.)
    4. If no ID is specified, will return a randomly generated 6-character ID.

    Arguments
    ---------
    data_item: `AnnoItem | AnnoMark | {str: Any}`
        The annotation item data to be sanitized. If the `data_item` is just a mark,
        will add ID for it.

    Returns
    -------
    #1: `AnnoItem | None`
        The sanitized copy of the data item. Will return `None` if the given data
        cannot be sanitized.
    """
    if not isinstance(data_item, collections.abc.Mapping):
        return None
    if "mark" not in data_item:
        if th.is_anno_mark(data_item):
            data_item = th.AnnoItem(id=_generate_id(), mark=data_item)
        else:
            return None
    else:
        if not th.is_anno_mark(data_item["mark"]):
            return None
    sanitized_id = data_item.get("id")
    comment = data_item.get("comment")
    if not sanitized_id:
        sanitized_id = _generate_id()
    data_item = th.AnnoItem(id=sanitized_id, mark=data_item["mark"].copy())
    if isinstance(comment, str):
        data_item["comment"] = comment
    mark = data_item["mark"]
    width = mark["width"]
    height = mark["height"]
    if width < 0:
        mark["width"] = -width
        mark["x"] = mark["x"] + width
    if height < 0:
        mark["height"] = -height
        mark["y"] = mark["y"] + height
    return data_item


def _deduplicate_id_by_add(seen_ids: AbstractSet[str], anno_id: str) -> str:
    """Ensure that the given `anno_id` is not duplicated by the "add" rule.
    (private method)

    Arguments
    ---------
    seen_ids: `{str}`
        The collection of seen IDs.

    anno_id: `str`
        The new ID to be checked.

    Returns
    -------
    #1: `str`
        If `anno_id` is not in `seen_ids`, return it as it is. Otherwise, return a
        modified ID that is not in `seen_ids`.
    """
    _anno_id = anno_id
    while _anno_id in seen_ids:
        _anno_id = anno_id + _generate_id()
    return _anno_id


def sanitize_data(
    data: Union[th.NSAnnotations, Sequence[th.NSAnnoItem]],
    deduplicate: Literal["add", "drop"] = "drop",
) -> th.Annotations:
    """Perform the full sanitization on the annotation data.

    The sanitization will ensure that:
    1. The current timestamp is the time when this method is used.
    2. All items in `data` are dictionaries typed by `AnnoItem`.
    3. Any item with a `None` comment will be sanitized as an item without the comment.
    4. The position of the annotation mark will always have positive width and height.
       (Negative values means that the starting location is reversed.)
    4. Annotation items will be deduplicated, i.e. the IDs will be sanitized.

    This method can be used when the annotations need to be saved as a file. It may
    take time to run, so it may not be suitable to sanitize the annotations in the
    real time.

    Arguments
    ---------
    data: `Annotations | [AnnoItem | {str: Any}]`
        The annotation data that will be sanitized. Note that this method will not
        change the input data.

    deduplicate: `"add" | "drop"`
        The deduplicate method for the annotation IDs. `"add"` means that preserving
        the duplicated ID by adding a postfix. `"drop"` means that dropping all
        annotation items with duplicated IDs after the first found item.

    Returns
    -------
    #1: `Annotations`
        The sanitized copy of the data.
    """
    if isinstance(data, collections.abc.Mapping):
        data = data["data"]
    if not isinstance(data, collections.abc.Sequence):
        return th.Annotations(
            timestamp=int(datetime.datetime.now().timestamp() * 1000), data=list()
        )
    new_data: List[th.AnnoItem] = list()
    seen_ids: Set[str] = set()
    for ditem in data:
        new_anno = sanitize_data_item(ditem)
        if new_anno is None:
            continue
        anno_id = new_anno.get("id")
        if not anno_id:
            anno_id = _generate_id()
        if anno_id in seen_ids:
            if deduplicate == "add":
                anno_id = _deduplicate_id_by_add(seen_ids, anno_id)
            else:
                continue
        new_anno["id"] = anno_id
        seen_ids.add(anno_id)
        new_data.append(new_anno)
    return th.Annotations(
        timestamp=int(datetime.datetime.now().timestamp() * 1000), data=new_data
    )


def sanitize_scale(
    scale: Union[float, th.Mapping[str, th.Any]],
    offset_x: Optional[float] = None,
    offset_y: Optional[float] = None,
) -> th.Scale:
    """Perform the sanitization on the annotated image scaling factor.

    The sanitization will ensure that:
    1. A dictionary containing at least the scaling ratio will be returned.
    2. Optional offsets can be configured.
    3. A timestamp will be attached to the sanitized configuration. It ensures that the
       scaling event will be always triggered even if the configuration does not
       change.

    Arguments
    ---------
    scale: `float | Mapping[str, Any]`
        The scaling factor value (float) or a full scaling configuration dictionary.

    offset_x: `float`
        The relative offset ratio along the X axis. This value will be added to the
        returned value only when it is configured and `"offset_x"` is not configured
        in `scale`.

    offset_y: `float`
        The relative offset ratio along the Y axis. This value will be added to the
        returned value only when it is configured and `"offset_y"` is not configured
        in `scale`.

    Returns
    -------
    #1: `Scale`
        The santized scaling factor with a newly configured timestamp.
    """
    if isinstance(scale, collections.abc.Mapping):
        res = th.Scale(scale=(float(scale["scale"]) if "scale" in scale else 1.0))
        if "offset_x" in scale:
            res["offset_x"] = float(scale["offset_x"])
        if "offset_y" in scale:
            res["offset_y"] = float(scale["offset_y"])
    else:
        res = th.Scale(scale=float(scale))
    if "offset_x" not in res and isinstance(offset_x, float):
        res["offset_x"] = offset_x
    if "offset_y" not in res and isinstance(offset_y, float):
        res["offset_y"] = offset_y
    res["timestamp"] = int(datetime.datetime.now().timestamp() * 1000)
    return res
