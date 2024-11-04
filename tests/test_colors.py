# -*- coding: UTF-8 -*-
"""
Colors
======
@ Dash Picture Annotation - Tests

Author
------
Yuchen Jin (cainmagi)
cainmagi@gmail.com

Description
-----------
The tests for the `colors.py` application. These tests will run a browser emulator
powered by `selenium` and `dash.testing`. The basic functionalities of the demo
will be checked one by one.
"""

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
from .imgutils import decode_base64_image, compare_images_with_alpha, ImageLoader
from .actions import get_canvas_image


__all__ = ("TestColors",)


@pytest.mark.with_dash
class TestColors:
    """Test the rendering the Dash app: Colors"""

    @pytest.fixture(scope="class")
    def dash_app(self) -> Generator[dash.Dash, None, None]:
        log = logging.getLogger("dash_picture_annotation.test")
        log.info("Initialize the Dash app.")
        app = import_app("examples.colors")
        yield app
        log.info("Remove the Dash app.")
        del app

    @pytest.fixture(scope="class")
    def ref_images(self) -> Generator[ImageLoader, None, None]:
        """Fixture of the testing images."""
        log = logging.getLogger("dash_picture_annotation.test")
        log.info("Use the reference images.")
        yield ImageLoader(root=asset_folder())

    @staticmethod
    def get_check_function_for_current_shape_ssim(
        dash_duo: DashComposite, ref_images: ImageLoader, annotator: WebElement
    ):
        """Get the check function for the ssim of the current shape.

        This factory method will be used to create the shape validator in the tests.
        It is internally used.

        Arguments
        ---------
        dash_duo: `DashComposite`
        ref_images: `ref_images`
            Fixtures used in the test.

        annotator: `WebElement`
            The annotator box gotten by
            ``` python
            dash_duo.find_element("#annotator")
            ```

        Returns
        -------
        #1: `(name: str) -> float`
            A validator function. It accepts the name of the figure that is used for
            validating the results. If the ssim score is lower than 0.9, throw an
            error. If the check succeeds, return the ssim score.
        """

        def check_function(name: str, validate: bool = True) -> float:
            """Check function for the current shapes.

            Arguments
            ---------
            name: `str`
                The name of the reference image used for performing the check.

            validate: `bool`
                A flag. If specified, will validate the score by `> 0.9`.

            Returns
            -------
            #1: `float`
                If the check succeeds, return the ssim score. Otherwise, throw an
                error.
            """
            wait_for_dcc_loading(dash_duo, "#annotator")
            img = decode_base64_image(
                get_canvas_image(dash_duo, annotator, canvas_selector=".rp-shapes"),
                use_rgba=True,
            )
            ssim = compare_images_with_alpha(img, ref_images[name], fine_mode=True)
            if validate:
                assert ssim > 0.9
            return ssim

        return check_function

    def test_colors_set_color(
        self, dash_duo: DashComposite, dash_app: dash.Dash, ref_images: ImageLoader
    ) -> None:
        """Test the colors app and change the default color of annotations.

        The release of the mouse will trigger the callbacks.
        """
        log = logging.getLogger("dash_picture_annotation.test")

        # Start a dash app contained as the variable `app` in `usage.py`
        dash_duo.start_server(dash_app)

        wait_for_dcc_loading(dash_duo, "#annotator")

        annotator: WebElement = dash_duo.find_element("#annotator")
        btn_default: WebElement = dash_duo.find_element("#btn-default")
        btn_specific: WebElement = dash_duo.find_element("#btn-specific")

        checker = self.get_check_function_for_current_shape_ssim(
            dash_duo, ref_images, annotator
        )

        wait_for_dcc_loading(dash_duo, "#annotator")
        ssim = checker("ref_color_init")
        log.info("SSIM of the initial annotations: {0:.3g}".format(ssim))

        btn_default.click()
        wait_for_dcc_loading(dash_duo, "#annotator")
        ssim = checker("ref_color_change_default")
        log.info("SSIM of changing the default color: {0:.3g}".format(ssim))

        btn_specific.click()
        wait_for_dcc_loading(dash_duo, "#annotator")
        ssim = checker("ref_color_specific")
        log.info("SSIM of specifying colors of some types: {0:.3g}".format(ssim))

        btn_specific.click()
        wait_for_dcc_loading(dash_duo, "#annotator")
        ssim = checker("ref_color_change_default")
        log.info("SSIM of reverting the specific colors: {0:.3g}".format(ssim))

        btn_default.click()
        wait_for_dcc_loading(dash_duo, "#annotator")
        ssim = checker("ref_color_init")
        log.info("SSIM of reverting the default color: {0:.3g}".format(ssim))

    def test_colors_dynamic_color(
        self, dash_duo: DashComposite, dash_app: dash.Dash, ref_images: ImageLoader
    ) -> None:
        """Test the colors app and toggle the dynamic colors.

        The release of the mouse will trigger the callbacks.
        """
        log = logging.getLogger("dash_picture_annotation.test")

        # Start a dash app contained as the variable `app` in `usage.py`
        dash_duo.start_server(dash_app)

        wait_for_dcc_loading(dash_duo, "#annotator")

        annotator: WebElement = dash_duo.find_element("#annotator")
        btn_default: WebElement = dash_duo.find_element("#btn-default")
        btn_specific: WebElement = dash_duo.find_element("#btn-specific")
        btn_dynamic: WebElement = dash_duo.find_element("#btn-dynamic")

        checker = self.get_check_function_for_current_shape_ssim(
            dash_duo, ref_images, annotator
        )

        wait_for_dcc_loading(dash_duo, "#annotator")
        ssim = checker("ref_color_init")
        log.info("SSIM of the initial annotations: {0:.3g}".format(ssim))

        btn_dynamic.click()
        wait_for_dcc_loading(dash_duo, "#annotator")
        ssim = checker("ref_color_dynamic")
        log.info("SSIM of changing the dynamic color: {0:.3g}".format(ssim))

        btn_default.click()
        wait_for_dcc_loading(dash_duo, "#annotator")
        _ssim = checker("ref_color_dynamic")
        assert abs(ssim - _ssim) < 1e-3
        log.info(
            "Confirm that default color will not override dynamic "
            "color: {0:.3g}".format(_ssim)
        )

        btn_specific.click()
        wait_for_dcc_loading(dash_duo, "#annotator")
        _ssim = checker("ref_color_dynamic", validate=False)
        assert _ssim < ssim
        assert abs(ssim - _ssim) > 1e-3
        log.info(
            "Confirm that specific color will override dynamic color: "
            "{0:.3g}".format(_ssim)
        )
        ssim = checker("ref_color_dynamic_specific")
        assert _ssim < ssim
        assert abs(ssim - _ssim) > 1e-3
        log.info(
            "Confirm that dynamic color with specified color matches the target: "
            "{0:.3g}".format(ssim)
        )

        btn_specific.click()
        btn_dynamic.click()
        btn_default.click()
        wait_for_dcc_loading(dash_duo, "#annotator")
        ssim = checker("ref_color_init")
        log.info("SSIM of reverting the dynamic colors: {0:.3g}".format(ssim))
