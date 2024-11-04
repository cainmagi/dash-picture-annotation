# -*- coding: UTF-8 -*-
"""
Size Control
============
@ Dash Picture Annotation - Tests

Author
------
Yuchen Jin (cainmagi)
cainmagi@gmail.com

Description
-----------
The tests for the `size_control.py` application. These tests will run a browser emulator
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
from .actions import drag_and_drop, click_relatively


__all__ = ("TestSizeControl",)


@pytest.mark.with_dash
class TestSizeControl:
    """Test the rendering the Dash app: Size Control"""

    @pytest.fixture(scope="class")
    def dash_app(self) -> Generator[dash.Dash, None, None]:
        log = logging.getLogger("dash_picture_annotation.test")
        log.info("Initialize the Dash app.")
        app = import_app("examples.size_control")
        yield app
        log.info("Remove the Dash app.")
        del app

    def test_sizecontrol_create_new_annotation(
        self, dash_duo: DashComposite, dash_app: dash.Dash
    ) -> None:
        """Test the size_control app and create a new annotation box.

        The release of the mouse will trigger the callbacks.
        """
        log = logging.getLogger("dash_picture_annotation.test")

        # Start a dash app contained as the variable `app` in `usage.py`
        dash_duo.start_server(dash_app)

        annotator: WebElement = dash_duo.find_element("#annotator")
        output: WebElement = dash_duo.find_element("#output")

        data_init = output.text
        log.info("Initial annotation: {0}".format(data_init))
        assert data_init.casefold().strip() == ""

        drag_and_drop(dash_duo, annotator, pos_start=(100, 100), pos_end=(300, 300))
        drag_and_drop(dash_duo, annotator, pos_start=(400, 100), pos_end=(600, 300))

        wait_for_dcc_loading(dash_duo, "#output")
        data_updated = output.text
        log.info("Updated annotation: {0}".format(data_updated))
        annotations_updated = json.loads(data_updated)
        assert len(annotations_updated["data"]) == 2
        for anno in annotations_updated["data"]:
            assert (
                abs(anno["mark"]["width"] - anno["mark"]["height"])
                / max(1, abs(anno["mark"]["width"]))
                < 0.05
            )

        drag_and_drop(dash_duo, annotator, pos_start=(100, 400), pos_end=(300, 410))
        click_relatively(dash_duo, annotator, (50, 50))
        drag_and_drop(dash_duo, annotator, pos_start=(400, 400), pos_end=(600, 410))
        click_relatively(dash_duo, annotator, (50, 50))
        wait_for_dcc_loading(dash_duo, "#output")
        data_updated = output.text
        log.info("Updated annotation: {0}".format(data_updated))
        annotations_updated = json.loads(data_updated)
        assert len(annotations_updated["data"]) == 2
        log.info("Confirm that creating a small annotation box will be disallowed.")

        drag_and_drop(dash_duo, annotator, pos_start=(100, 400), pos_end=(300, 600))
        drag_and_drop(dash_duo, annotator, pos_start=(400, 400), pos_end=(600, 600))
        wait_for_dcc_loading(dash_duo, "#output")
        data_updated = output.text
        log.info("Updated annotation: {0}".format(data_updated))
        annotations_updated = json.loads(data_updated)
        assert len(annotations_updated["data"]) == 4
        log.info("Allowed to create annotations as long as they are big enough.")

        click_relatively(dash_duo, annotator, (450, 450))
        drag_and_drop(dash_duo, annotator, pos_start=(600, 600), pos_end=(600, 410))
        click_relatively(dash_duo, annotator, (50, 50))
        wait_for_dcc_loading(dash_duo, "#output")
        data_updated = output.text
        log.info("Updated annotation: {0}".format(data_updated))
        annotations_updated = json.loads(data_updated)
        assert len(annotations_updated["data"]) == 3
        log.info(
            "Confirm the auto-delete caused by resizing the annotation box to a "
            "small size."
        )
