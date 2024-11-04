# -*- coding: UTF-8 -*-
"""
Minimal
=======
@ Dash Picture Annotation - Tests

Author
------
Yuchen Jin (cainmagi)
cainmagi@gmail.com

Description
-----------
The tests for the `minimal.py` application. These tests will run a browser emulator
powered by `selenium` and `dash.testing`. The basic functionalities of the demo
will be checked one by one.
"""

import json
import logging

try:
    from typing import Generator
except ImportError:
    from collections.abc import Generator

import pytest

import dash
from dash.testing.application_runners import import_app
from dash.testing.composite import DashComposite
from selenium.webdriver.remote.webelement import WebElement

from .utils import wait_for_dcc_loading
from .actions import (
    drag_and_drop,
    click_relatively,
    get_input_box,
    get_input_del_button,
)


__all__ = ("TestMinimal",)


@pytest.mark.with_dash
class TestMinimal:
    """Test the rendering the Dash app: Minimal"""

    @pytest.fixture(scope="class")
    def dash_app(self) -> Generator[dash.Dash, None, None]:
        log = logging.getLogger("dash_picture_annotation.test")
        log.info("Initialize the Dash app.")
        app = import_app("examples.minimal")
        yield app
        log.info("Remove the Dash app.")
        del app

    def test_minimal_create_new_annotation(
        self, dash_duo: DashComposite, dash_app: dash.Dash
    ) -> None:
        """Test the minimal app and create a new annotation box.

        The release of the mouse will trigger the callbacks.
        """
        log = logging.getLogger("dash_picture_annotation.test")

        # Start a dash app contained as the variable `app` in `usage.py`
        dash_duo.start_server(dash_app)

        annotator: WebElement = dash_duo.find_element("#annotator")
        output: WebElement = dash_duo.find_element("#output")

        data_init = output.text
        log.info("Initial annotation: {0}".format(data_init))
        annotations_init = json.loads(data_init)
        assert len(annotations_init["data"]) == 1
        assert annotations_init["data"][0]["id"] == "TestID"

        drag_and_drop(dash_duo, annotator, pos_start=(100, 100), pos_end=(300, 300))

        wait_for_dcc_loading(dash_duo, "#output")
        data_updated = output.text
        log.info("Updated annotation: {0}".format(data_updated))
        annotations_updated = json.loads(data_updated)
        assert annotations_updated["timestamp"] > annotations_init["timestamp"]
        assert len(annotations_updated["data"]) == 2
        anno_new = next(
            anno for anno in annotations_updated["data"] if anno["id"] != "TestID"
        )
        assert (
            abs(anno_new["mark"]["width"] - anno_new["mark"]["height"])
            / max(1, abs(anno_new["mark"]["width"]))
            < 0.05
        )

    def test_minimal_change_size(
        self, dash_duo: DashComposite, dash_app: dash.Dash
    ) -> None:
        """Test the minimal app and change the size of an annotation box.

        The release of the mouse will trigger the callbacks.
        """
        log = logging.getLogger("dash_picture_annotation.test")

        # Start a dash app contained as the variable `app` in `usage.py`
        dash_duo.start_server(dash_app)

        annotator: WebElement = dash_duo.find_element("#annotator")
        output: WebElement = dash_duo.find_element("#output")

        drag_and_drop(dash_duo, annotator, pos_start=(100, 100), pos_end=(300, 300))
        click_relatively(dash_duo, annotator, pos=(150, 150))
        wait_for_dcc_loading(dash_duo, "#output")
        drag_and_drop(dash_duo, annotator, pos_start=(300, 300), pos_end=(500, 500))

        wait_for_dcc_loading(dash_duo, "#output")
        data_updated = output.text
        log.info("Updated annotation: {0}".format(data_updated))
        annotations_updated = json.loads(data_updated)
        assert len(annotations_updated["data"]) == 2
        anno_new = next(
            anno for anno in annotations_updated["data"] if anno["id"] != "TestID"
        )
        assert (
            abs(anno_new["mark"]["width"] - anno_new["mark"]["height"])
            / max(1, abs(anno_new["mark"]["width"]))
            < 0.05
        )

    def test_minimal_change_annotation(
        self, dash_duo: DashComposite, dash_app: dash.Dash
    ) -> None:
        """Test the minimal app and change an annotation box.

        The events of the mouse will trigger the callbacks.
        """
        log = logging.getLogger("dash_picture_annotation.test")

        # Start a dash app contained as the variable `app` in `usage.py`
        dash_duo.start_server(dash_app)

        annotator: WebElement = dash_duo.find_element("#annotator")
        output: WebElement = dash_duo.find_element("#output")

        drag_and_drop(dash_duo, annotator, pos_start=(100, 100), pos_end=(300, 300))
        wait_for_dcc_loading(dash_duo, "#output")
        data_updated = output.text
        log.info("Updated annotation (add): {0}".format(data_updated))
        annotations_updated = json.loads(data_updated)
        assert len(annotations_updated["data"]) == 2

        click_relatively(dash_duo, annotator, pos=(150, 150))
        get_input_box(dash_duo, annotator).send_keys("New Annotation")
        click_relatively(dash_duo, annotator, pos=(50, 50))

        wait_for_dcc_loading(dash_duo, "#output")
        data_updated = output.text
        log.info("Updated annotation (name): {0}".format(data_updated))
        annotations_updated = json.loads(data_updated)
        assert len(annotations_updated["data"]) == 2
        anno_new = next(
            anno for anno in annotations_updated["data"] if anno["id"] != "TestID"
        )
        assert anno_new["comment"] == "New Annotation"

        click_relatively(dash_duo, annotator, pos=(150, 150))
        get_input_del_button(dash_duo, annotator).click()

        wait_for_dcc_loading(dash_duo, "#output")
        data_updated = output.text
        log.info("Updated annotation (delete): {0}".format(data_updated))
        annotations_updated = json.loads(data_updated)
        assert len(annotations_updated["data"]) == 1
        assert annotations_updated["data"][0]["id"] == "TestID"

    def test_minimal_switch_between(
        self, dash_duo: DashComposite, dash_app: dash.Dash
    ) -> None:
        """Test the minimal app and switch between two input boxes.

        The events of the mouse will trigger the callbacks.
        """
        log = logging.getLogger("dash_picture_annotation.test")

        # Start a dash app contained as the variable `app` in `usage.py`
        dash_duo.start_server(dash_app)

        annotator: WebElement = dash_duo.find_element("#annotator")
        output: WebElement = dash_duo.find_element("#output")

        # Create boxes
        drag_and_drop(dash_duo, annotator, pos_start=(100, 100), pos_end=(300, 300))
        drag_and_drop(dash_duo, annotator, pos_start=(400, 100), pos_end=(600, 300))
        wait_for_dcc_loading(dash_duo, "#output")
        data_updated = output.text
        log.info("Updated annotation (add): {0}".format(data_updated))
        annotations_updated = json.loads(data_updated)
        assert len(annotations_updated["data"]) == 3

        # Add text comments
        click_relatively(dash_duo, annotator, pos=(150, 150))
        get_input_box(dash_duo, annotator).send_keys("Box1")
        click_relatively(dash_duo, annotator, pos=(50, 50))

        click_relatively(dash_duo, annotator, pos=(450, 150))
        get_input_box(dash_duo, annotator).send_keys("Box2")
        click_relatively(dash_duo, annotator, pos=(50, 50))

        # Check the switching between boxes
        click_relatively(dash_duo, annotator, pos=(150, 150))
        box_text = get_input_box(dash_duo, annotator).get_attribute("value")
        assert box_text == "Box1"
        log.info("Validate the comment text: {0}".format(box_text))
        click_relatively(dash_duo, annotator, pos=(450, 150))
        box_text = get_input_box(dash_duo, annotator).get_attribute("value")
        assert box_text == "Box2"
        log.info("Validate the comment text: {0}".format(box_text))
        click_relatively(dash_duo, annotator, pos=(150, 150))
        box_text = get_input_box(dash_duo, annotator).get_attribute("value")
        assert box_text == "Box1"
        log.info("Validate the comment text: {0}".format(box_text))
