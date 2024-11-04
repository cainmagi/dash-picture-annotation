# -*- coding: UTF-8 -*-
"""
Sanitize
========
@ Dash Picture Annotation - Tests

Author
------
Yuchen Jin (cainmagi)
cainmagi@gmail.com

Description
-----------
The tests for sanitizing and querying the annotation data.
"""

import json
import logging

try:
    from typing import Generator
except ImportError:
    from collections.abc import Generator

import pytest

import dash_picture_annotation as dpa

from .utils import tst_folder


__all__ = ("TestSanitize",)


class TestSanitize:
    """Test the sanitizing the querying of the annotation data."""

    @pytest.fixture(scope="class")
    def data(self) -> Generator[dpa.Annotations, None, None]:
        """Fixture of the testing data."""
        log = logging.getLogger("dash_picture_annotation.test")
        file_name = "data-sanitize"
        with open(tst_folder("{0}.json".format(file_name)), "r") as fobj:
            _data = json.load(fobj)
        log.info("Use testing data: {0}".format(file_name))
        yield _data

    def test_sanitize_get_data(self, data: dpa.Annotations) -> None:
        """Test the methods for getting data items."""
        log = logging.getLogger("dash_picture_annotation.test")

        anno = dpa.get_data_item(data, "ZxdA2p")
        assert anno["id"] == "ZxdA2p"
        assert abs(anno["mark"]["x"] - 152.14361702127658) < 1e-3
        log.info("Get data: {0}".format(anno))

        with pytest.raises(KeyError):
            dpa.get_data_item(data, "not-exist")

        anno = dpa.get_data_item_with_default(data, "not-exist")
        assert anno is None

        annos = dpa.get_data_items(data, "type-1")
        assert len(annos) == 0
        log.info("Get data: {0}".format(annos))

        annos = dpa.get_data_items(data, "type-2")
        assert len(annos) == 1
        assert annos[0].get("comment") == "type-2"
        log.info("Get data: {0}".format(annos))

        annos = dpa.get_data_items(data, "type-7")
        assert len(annos) == 2
        anno = dpa.get_data_item(annos, "yJwGxK")
        assert anno.get("comment") == "type-7"
        log.info("Get data: {0}".format(annos))

        annos = dpa.get_data_items_by_regex(data, r"type-[678]")
        assert len(annos) == 3
        anno = dpa.get_data_item(annos, "yJwGxK")
        assert anno.get("comment") in ("type-6", "type-7", "type-8")
        log.info("Get data: {0}".format(annos))

    def test_sanitize_all_info(self, data: dpa.Annotations) -> None:
        """Test the methods for gathering high-level information."""
        log = logging.getLogger("dash_picture_annotation.test")

        anno_ids = dpa.get_all_ids(data)
        assert not set(anno_ids).difference(
            ("ZxdA2p", "hCC6Gi", "yJwGxK", "EWCEpN", "3Pb3rh")
        )
        anno_ids_2 = dpa.get_all_ids(data["data"])
        assert not set(anno_ids).difference(set(anno_ids_2))
        log.info("Get all IDs: {0}".format(anno_ids))

        anno_comments = dpa.get_all_comments(data)
        assert not anno_comments.difference(("type-2", "type-6", "type-7", ""))
        anno_comments_2 = dpa.get_all_comments(data["data"])
        assert not set(anno_comments).difference(anno_comments_2)
        log.info("Get all comments: {0}".format(anno_comments))

    def test_sanitize_compare(self, data: dpa.Annotations) -> None:
        """Test the methods for gathering high-level information."""
        log = logging.getLogger("dash_picture_annotation.test")

        anno_0 = data["data"][0]
        anno_1 = data["data"][1]

        assert dpa.compare_anno_marks(anno_0, anno_0)
        assert dpa.compare_anno_marks(anno_1, anno_1)
        assert not dpa.compare_anno_marks(anno_0, anno_1)
        log.info("Distinguish the difference two annotations.")

        assert dpa.compare_anno_marks(anno_0["mark"], anno_0)
        assert dpa.compare_anno_marks(anno_1, anno_1["mark"])
        assert not dpa.compare_anno_marks(anno_0["mark"], anno_1["mark"])
        log.info("Confirm the compatibility of using marks directly.")

        anno_mark = anno_0["mark"].copy()
        anno_mark["width"] = -anno_mark["width"]
        assert not dpa.compare_anno_marks(anno_0, anno_mark)
        log.info("Negative width causes the mark to move.")

        anno_mark["x"] = anno_mark["x"] - anno_mark["width"]
        assert dpa.compare_anno_marks(anno_0, anno_mark)
        log.info("Correct the mark poistion back by changing x.")

        anno_copy = anno_0.copy()
        anno_copy["mark"] = anno_copy["mark"].copy()
        anno_copy["comment"] = "changed-comment"
        assert dpa.compare_anno_marks(anno_0, anno_copy)
        log.info("Change comment does not influence the comparison.")

    def test_sanitize_data(self, data: dpa.Annotations) -> None:
        """Test the methods for gathering high-level information."""
        log = logging.getLogger("dash_picture_annotation.test")

        anno_bad = data["data"][4]
        assert anno_bad["id"] == "yJwGxK"
        assert anno_bad["mark"]["width"] < 0
        log.info("Get the bad item: {0}".format(anno_bad))

        anno_good = dpa.sanitize_data_item(anno_bad)
        assert anno_good is not None
        assert dpa.compare_anno_marks(anno_bad, anno_good)
        log.info("Get the sanitized item: {0}".format(anno_good))

        assert anno_bad["mark"]["width"] < 0
        assert anno_good["mark"]["width"] > 0
        log.info("Confirm that the bad item is not changed: {0}".format(anno_bad))

        bad_ids = dpa.get_all_ids(data)
        bad_comments = dpa.get_all_comments(data)
        assert not set(bad_ids).difference(
            ("ZxdA2p", "hCC6Gi", "yJwGxK", "EWCEpN", "3Pb3rh")
        )
        assert not bad_comments.difference(("type-2", "type-6", "type-7", ""))
        log.info("IDs of bad data: {0}".format(bad_ids))
        log.info("Comments of bad data: {0}".format(bad_comments))

        s_data = dpa.sanitize_data(data, deduplicate="add")
        good_ids = dpa.get_all_ids(s_data)
        good_comments = dpa.get_all_comments(s_data)
        log.info("IDs of sanitized data: {0}".format(good_ids))
        log.info("Comments of sanitized data: {0}".format(good_comments))

        assert (
            not set(good_ids)
            .intersection(bad_ids)
            .difference(("ZxdA2p", "hCC6Gi", "yJwGxK", "EWCEpN", "3Pb3rh"))
        )
        assert len(set(good_ids)) == len(s_data["data"])
        log.info("Confirm that the IDs are sanitized.")

        assert not good_comments.difference(bad_comments)
        log.info("Confirm that the comments are not changed in the sanitized data.")

        _bad_ids = dpa.get_all_ids(data)
        _bad_comments = dpa.get_all_comments(data)
        assert not set(_bad_ids).difference(bad_ids)
        assert not bad_comments.difference(_bad_comments)
        log.info("Confirm that the bad data is not changed: {0}".format(anno_bad))

        _s_data = dpa.sanitize_data(data, deduplicate="drop")
        log.info(
            "Use the drop mode to sanitize data: len(sdata_drop_mode)={0} < {1}="
            "len(sdata_add_mode)".format(len(_s_data["data"]), len(s_data["data"]))
        )
        assert len(_s_data["data"]) < len(s_data["data"])
