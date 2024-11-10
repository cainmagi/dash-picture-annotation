# -*- coding: UTF-8 -*-
"""
Dash Picture Annotation
=======================

Author
------
Yuchen Jin (cainmagi)
cainmagi@gmail.com

Description
-----------
Dash porting version of the React project React Picture Annotation. Provide a simple
annotation window for a single picture.

Thanks to
---------
Kunduin/react-picture-annotation

https://github.com/Kunduin/react-picture-annotation
"""

import os as _os
import sys as _sys
import json

import dash as _dash

# noinspection PyUnresolvedReferences
from ._imports_ import DashPictureAnnotation
from ._imports_ import __all__ as __import_all__

from . import typehints
from . import utilities

from .typehints import (
    AnnoMark,
    AnnoItem,
    Annotations,
    AnnoStyle,
    DashSelectOptionItem,
    Size,
    NSAnnoItem,
    NSAnnotations,
    is_sequence_of,
    is_anno_mark,
    is_anno_item,
    is_annotations,
    is_dash_select_option_item,
)
from .utilities import (
    get_data_item,
    get_data_item_with_default,
    get_data_items,
    get_data_items_by_regex,
    get_all_ids,
    get_all_comments,
    compare_anno_marks,
    sanitize_data_item,
    sanitize_data,
)

__all__ = (
    "typehints",
    "utilities",
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
    "get_data_item",
    "get_data_item_with_default",
    "get_data_items",
    "get_data_items_by_regex",
    "get_all_ids",
    "get_all_comments",
    "compare_anno_marks",
    "sanitize_data_item",
    "sanitize_data",
    "DashPictureAnnotation",
)

if not hasattr(_dash, "__plotly_dash") and not hasattr(_dash, "development"):
    print(
        "Dash was not successfully imported. "
        "Make sure you don't have a file "
        'named \n"dash.py" in your current directory.',
        file=_sys.stderr,
    )
    _sys.exit(1)

_basepath = _os.path.dirname(__file__)
_filepath = _os.path.abspath(_os.path.join(_basepath, "package-info.json"))
with open(_filepath) as f:
    package = json.load(f)

package_name = package["name"].replace(" ", "_").replace("-", "_")
__version__ = package["version"]

_current_path = _os.path.dirname(_os.path.abspath(__file__))

_this_module = _sys.modules[__name__]

async_resources = [
    "DashPictureAnnotation",
]

_js_dist = []

_js_dist.extend(
    [
        {
            "relative_package_path": "async-{}.js".format(async_resource),
            "external_url": ("https://unpkg.com/{0}@{2}" "/{1}/async-{3}.js").format(
                package_name, __name__, __version__, async_resource
            ),
            "namespace": package_name,
            "async": True,
        }
        for async_resource in async_resources
    ]
)

# TODO: Figure out if unpkg link works
_js_dist.extend(
    [
        {
            "relative_package_path": "async-{}.js.map".format(async_resource),
            "external_url": (
                "https://unpkg.com/{0}@{2}" "/{1}/async-{3}.js.map"
            ).format(package_name, __name__, __version__, async_resource),
            "namespace": package_name,
            "dynamic": True,
        }
        for async_resource in async_resources
    ]
)

_js_dist.extend(
    [
        {
            "relative_package_path": "dash_picture_annotation.min.js",
            "namespace": package_name,
        },
        {
            "relative_package_path": "dash_picture_annotation.min.js.map",
            "namespace": package_name,
            "dynamic": True,
        },
    ]
)

_css_dist = []


for _component in __import_all__:
    setattr(locals()[_component], "_js_dist", _js_dist)
    setattr(locals()[_component], "_css_dist", _css_dist)
