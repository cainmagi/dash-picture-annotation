# -*- coding: UTF-8 -*-
"""
States
======
@ Dash Picture Annotation - Tests

Author
------
Yuchen Jin (cainmagi)
cainmagi@gmail.com

Description
-----------
The tests for the `states.py` application. These tests will run a browser emulator
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

from .utils import wait_for_dcc_loading, asset_folder
from .imgutils import decode_base64_image, compare_images, ImageLoader
from .actions import drag_and_drop, get_canvas_image


__all__ = ("TestStates",)


@pytest.mark.with_dash
class TestStates:
    """Test the rendering the Dash app: States"""

    @pytest.fixture(scope="class")
    def dash_app(self) -> Generator[dash.Dash, None, None]:
        """Fixture of the dash application."""
        log = logging.getLogger("dash_picture_annotation.test")
        log.info("Initialize the Dash app.")
        app = import_app("examples.states")
        yield app
        log.info("Remove the Dash app.")
        del app

    @pytest.fixture(scope="class")
    def ref_images(self) -> Generator[ImageLoader, None, None]:
        """Fixture of the testing images."""
        log = logging.getLogger("dash_picture_annotation.test")
        log.info("Use the reference images.")
        yield ImageLoader(root=asset_folder())

    def test_states_toggle_disabled(
        self, dash_duo: DashComposite, dash_app: dash.Dash
    ) -> None:
        """Test the states app and toggle the `disabled` property of the annotator..

        The release of the mouse will trigger the callbacks.
        """
        log = logging.getLogger("dash_picture_annotation.test")

        # Start a dash app contained as the variable `app` in `usage.py`
        dash_duo.start_server(dash_app)

        annotator: WebElement = dash_duo.find_element("#annotator")
        btn_disabled: WebElement = dash_duo.find_element("#btn-disabled")
        output: WebElement = dash_duo.find_element("#output")

        drag_and_drop(dash_duo, annotator, pos_start=(100, 100), pos_end=(300, 300))

        wait_for_dcc_loading(dash_duo, "#output")
        annotation_ids = tuple(
            anno["id"] for anno in json.loads(output.text).get("data", tuple())
        )
        log.info("Updated annotation IDs: {0}".format(annotation_ids))
        assert len(annotation_ids) == 2

        btn_disabled.click()
        dash_duo.wait_for_element_by_css_selector(
            "#annotator > div[class^='dpa-overlay-container']"
        )
        drag_and_drop(dash_duo, annotator, pos_start=(400, 100), pos_end=(600, 300))
        wait_for_dcc_loading(dash_duo, "#output")
        annotation_ids = tuple(
            anno["id"] for anno in json.loads(output.text).get("data", tuple())
        )
        log.info("Updated annotation IDs: {0}".format(annotation_ids))
        assert len(annotation_ids) == 2

        btn_disabled.click()
        dash_duo.wait_for_element_by_css_selector("#annotator > .rp-stage > .rp-image")
        drag_and_drop(dash_duo, annotator, pos_start=(400, 100), pos_end=(600, 300))
        wait_for_dcc_loading(dash_duo, "#output")
        annotation_ids = tuple(
            anno["id"] for anno in json.loads(output.text).get("data", tuple())
        )
        log.info("Updated annotation IDs: {0}".format(annotation_ids))
        assert len(annotation_ids) == 3

    def test_states_toggle_image(
        self,
        dash_duo: DashComposite,
        dash_app: dash.Dash,
        ref_images: ImageLoader,
    ) -> None:
        """Test the states app and toggle the `image` property of the annotator.

        The release of the mouse will trigger the callbacks.
        """
        log = logging.getLogger("dash_picture_annotation.test")

        # Start a dash app contained as the variable `app` in `usage.py`
        dash_duo.start_server(dash_app)

        annotator: WebElement = dash_duo.find_element("#annotator")
        btn_image: WebElement = dash_duo.find_element("#btn-image")
        output: WebElement = dash_duo.find_element("#output")

        drag_and_drop(dash_duo, annotator, pos_start=(100, 100), pos_end=(300, 300))

        wait_for_dcc_loading(dash_duo, "#output")
        anno_ids_before = tuple(
            anno["id"] for anno in json.loads(output.text).get("data", tuple())
        )
        log.info("Current annotation IDs: {0}".format(anno_ids_before))
        assert len(anno_ids_before) == 2

        for img_name in ("test_philips_PM5544", "test_image"):
            btn_image.click()
            res = get_canvas_image(dash_duo, annotator)
            img = decode_base64_image(res)
            ssim = compare_images(img, ref_images["ref_" + img_name])
            log.info('SSIM of the image "{0}": {1}'.format(img_name, ssim))

            anno_ids = tuple(
                anno["id"] for anno in json.loads(output.text).get("data", tuple())
            )
            log.info("Current annotation IDs: {0}".format(anno_ids))
            assert len(anno_ids) == 2
            assert len(set(anno_ids).difference(anno_ids_before)) == 0
            assert ssim > 0.85

    def test_states_reset_data(
        self,
        dash_duo: DashComposite,
        dash_app: dash.Dash,
    ) -> None:
        """Test the states app and reset the data of the annotator from the server side.

        The release of the mouse will trigger the callbacks.
        """
        log = logging.getLogger("dash_picture_annotation.test")

        # Start a dash app contained as the variable `app` in `usage.py`
        dash_duo.start_server(dash_app)

        annotator: WebElement = dash_duo.find_element("#annotator")
        btn_data: WebElement = dash_duo.find_element("#btn-data")
        output: WebElement = dash_duo.find_element("#output")

        drag_and_drop(dash_duo, annotator, pos_start=(100, 100), pos_end=(300, 300))
        drag_and_drop(dash_duo, annotator, pos_start=(400, 100), pos_end=(600, 300))

        wait_for_dcc_loading(dash_duo, "#output")
        anno_ids_before = tuple(
            anno["id"] for anno in json.loads(output.text).get("data", tuple())
        )
        log.info("Current annotation IDs: {0}".format(anno_ids_before))
        assert len(anno_ids_before) == 3

        btn_data.click()
        wait_for_dcc_loading(dash_duo, "#output")
        annotations = json.loads(output.text).get("data", tuple())
        anno_ids = tuple(anno["id"] for anno in annotations)
        log.info("Current annotation IDs: {0}".format(anno_ids))
        assert len(anno_ids) == 1
        assert annotations[0]["id"] == "TestID"
