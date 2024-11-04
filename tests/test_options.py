# -*- coding: UTF-8 -*-
"""
Options
=======
@ Dash Picture Annotation - Tests

Author
------
Yuchen Jin (cainmagi)
cainmagi@gmail.com

Description
-----------
The tests for the `options.py` application. These tests will run a browser emulator
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

from .utils import wait_for_the_attribute_value_to_equal, wait_for_dcc_loading, wait_for
from .actions import (
    drag_and_drop,
    click_relatively,
    get_select_expand,
    get_select_del_button,
    get_select_control_points,
    get_select_item_by_label,
    get_select_current_item,
)


__all__ = ("TestOptions",)


@pytest.mark.with_dash
class TestOptions:
    """Test the rendering the Dash app: Options"""

    @pytest.fixture(scope="class")
    def dash_app(self) -> Generator[dash.Dash, None, None]:
        log = logging.getLogger("dash_picture_annotation.test")
        log.info("Initialize the Dash app.")
        app = import_app("examples.options")
        yield app
        log.info("Remove the Dash app.")
        del app

    def test_options_toggle_options(
        self, dash_duo: DashComposite, dash_app: dash.Dash
    ) -> None:
        """Test the options app and toggle the option box.

        The release of the mouse will trigger the callbacks.
        """
        log = logging.getLogger("dash_picture_annotation.test")

        # Start a dash app contained as the variable `app` in `usage.py`
        dash_duo.start_server(dash_app)

        annotator: WebElement = dash_duo.find_element("#annotator")
        btn_options: WebElement = dash_duo.find_element("#btn-options")

        drag_and_drop(dash_duo, annotator, pos_start=(100, 100), pos_end=(300, 300))
        click_relatively(dash_duo, annotator, (150, 150))

        dash_duo.wait_for_element_by_css_selector(
            "#annotator > .rp-stage > .rp-selected-input > "
            "div.rp-default-input-section > input"
        )
        log.info("Current annotation is controlled by <input>.")

        btn_options.click()
        dash_duo.wait_for_element_by_css_selector(
            "#annotator > .rp-stage > .rp-selected-input > div[class^='dpa-dropdown']",
        )
        log.info("Current annotation is controlled by <Select>.")

        btn_options.click()
        dash_duo.wait_for_element_by_css_selector(
            "#annotator > .rp-stage > .rp-selected-input > "
            "div.rp-default-input-section > input"
        )
        log.info("Current annotation is controlled by <input>.")

    def test_options_toggle_option_clearable(
        self, dash_duo: DashComposite, dash_app: dash.Dash
    ) -> None:
        """Test the options app and toggle the option box.

        The release of the mouse will trigger the callbacks.
        """
        log = logging.getLogger("dash_picture_annotation.test")

        # Start a dash app contained as the variable `app` in `usage.py`
        dash_duo.start_server(dash_app)

        annotator: WebElement = dash_duo.find_element("#annotator")
        btn_options: WebElement = dash_duo.find_element("#btn-options")
        btn_optclear: WebElement = dash_duo.find_element("#btn-optclear")
        output: WebElement = dash_duo.find_element("#output")

        drag_and_drop(dash_duo, annotator, pos_start=(100, 100), pos_end=(300, 300))
        click_relatively(dash_duo, annotator, (150, 150))

        dash_duo.wait_for_element_by_css_selector(
            "#annotator > .rp-stage > .rp-selected-input > "
            "div.rp-default-input-section > input"
        )
        log.info("Current annotation is controlled by <input>.")

        btn_options.click()
        dash_duo.wait_for_element_by_css_selector(
            "#annotator > .rp-stage > .rp-selected-input > div[class^='dpa-dropdown']",
        )
        log.info("Current annotation is controlled by <Select>.")

        # Open the menu
        element = get_select_expand(dash_duo, annotator)
        element.click()

        # Find the first item
        element = get_select_item_by_label(dash_duo, annotator, item_label="Type 1")
        element.click()

        # Validate the currently selected value.
        element = get_select_current_item(dash_duo, annotator, expect_to_be="item")
        wait_for(dash_duo, lambda: (element.text == "Type 1"))
        log.info("Currently selected option: {0}".format(element.text))

        # Validate that it is clearable now or not.
        elements = get_select_control_points(dash_duo, annotator)
        assert len(elements) == 2
        log.info("Currently selected option is clerable.")

        btn_optclear.click()
        elements = get_select_control_points(dash_duo, annotator)
        assert len(elements) == 1
        log.info("Currently selected option is not clerable.")

        btn_optclear.click()
        elements = get_select_control_points(dash_duo, annotator)
        assert len(elements) == 2
        log.info("Currently selected option is clerable.")

        click_relatively(dash_duo, annotator, (50, 50))
        wait_for_dcc_loading(dash_duo, "#output")
        data_updated = output.text
        log.info("Updated annotation: {0}".format(data_updated))
        annotations_updated = json.loads(data_updated)
        assert len(annotations_updated["data"]) == 1
        assert annotations_updated["data"][0]["comment"] == "type-1"

        # Remove the comment
        click_relatively(dash_duo, annotator, (150, 150))
        elements = get_select_control_points(dash_duo, annotator)
        assert len(elements) == 2
        elements[0].click()
        get_select_current_item(dash_duo, annotator, expect_to_be="placeholder")

        click_relatively(dash_duo, annotator, (50, 50))
        wait_for_dcc_loading(dash_duo, "#output")
        data_updated = output.text
        log.info("Updated annotation: {0}".format(data_updated))
        annotations_updated = json.loads(data_updated)
        assert len(annotations_updated["data"]) == 1
        assert not annotations_updated["data"][0].get("comment")

    def test_options_placeholders(
        self, dash_duo: DashComposite, dash_app: dash.Dash
    ) -> None:
        """Test the options app and validate the customized placeholders.

        The release of the mouse will trigger the callbacks.
        """
        log = logging.getLogger("dash_picture_annotation.test")

        # Start a dash app contained as the variable `app` in `usage.py`
        dash_duo.start_server(dash_app)

        annotator: WebElement = dash_duo.find_element("#annotator")
        btn_options: WebElement = dash_duo.find_element("#btn-options")

        drag_and_drop(dash_duo, annotator, pos_start=(100, 100), pos_end=(300, 300))
        click_relatively(dash_duo, annotator, (150, 150))

        wait_for_the_attribute_value_to_equal(
            dash_duo,
            "#annotator > .rp-stage > .rp-selected-input > "
            "div.rp-default-input-section > input",
            attribute="placeholder",
            value="Using free mode...",
        )
        log.info("Confirm the placeholder of <input>.")

        btn_options.click()
        element = get_select_current_item(
            dash_duo, annotator, expect_to_be="placeholder"
        )
        assert element.text == "Using selection mode..."
        log.info("Confirm the placeholder of <Select>.")

    def test_options_delete_annotation(
        self, dash_duo: DashComposite, dash_app: dash.Dash
    ) -> None:
        """Test the options app and remove the annotation box by the button of selector.

        The events of the mouse will trigger the callbacks.
        """
        log = logging.getLogger("dash_picture_annotation.test")

        # Start a dash app contained as the variable `app` in `usage.py`
        dash_duo.start_server(dash_app)

        annotator: WebElement = dash_duo.find_element("#annotator")
        btn_options: WebElement = dash_duo.find_element("#btn-options")
        output: WebElement = dash_duo.find_element("#output")

        drag_and_drop(dash_duo, annotator, pos_start=(100, 100), pos_end=(300, 300))

        click_relatively(dash_duo, annotator, (150, 150))
        btn_options.click()
        dash_duo.wait_for_element_by_css_selector(
            "#annotator > .rp-stage > .rp-selected-input > div[class^='dpa-dropdown']",
        )
        log.info("Current annotation is controlled by <Select>.")

        click_relatively(dash_duo, annotator, (50, 50))
        wait_for_dcc_loading(dash_duo, "#output")
        data_updated = output.text
        log.info("Updated annotation: {0}".format(data_updated))
        annotations_updated = json.loads(data_updated)
        assert len(annotations_updated["data"]) == 1

        click_relatively(dash_duo, annotator, (150, 150))
        element = get_select_del_button(dash_duo, annotator)
        element.click()

        wait_for_dcc_loading(dash_duo, "#output")
        data_updated = output.text
        log.info("Updated annotation: {0}".format(data_updated))
        annotations_updated = json.loads(data_updated)
        assert not annotations_updated.get("data")
