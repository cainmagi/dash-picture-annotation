# -*- coding: UTF-8 -*-
"""
Actions
=======
@ Dash Picture Annotation - Tests

Author
------
Yuchen Jin (cainmagi)
cainmagi@gmail.com

Description
-----------
Extra actions used for manipulating the browser's behavior.
"""

from typing import Union

try:
    from typing import Sequence
    from typing import Tuple
except ImportError:
    from collections.abc import Sequence
    from builtins import tuple as Tuple

from typing_extensions import Literal

from dash.testing.composite import DashComposite
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

from .utils import wait_for, attribute_value_neq


__all__ = (
    "drag_and_drop",
    "click_relatively",
    "get_input_element",
    "get_input_box",
    "get_input_del_button",
    "get_select_element",
    "get_select_expand",
    "get_select_del_button",
    "get_select_control_points",
    "get_select_item_by_label",
    "get_select_current_item",
    "get_canvas_image",
)


def drag_and_drop(
    dash_duo: DashComposite,
    element: WebElement,
    pos_start: Tuple[int, int] = (0, 0),
    pos_end: Tuple[int, int] = (0, 0),
) -> None:
    """Emulator behavior: Drag and drop.

    Arguments
    ---------
    dash_duo: `DashComposite`
        The dash emulator.

    element: `WebElement`
        The anchor of this event. The positions will be calculated as relative
        positions of the upper left corner of this element.

    pos_start: `(int, int)`
        The starting position. The mouse will press since here.

    pos_end: `(int, int)`
        The ending position. The mouse will release at here.
    """
    driver: WebDriver = dash_duo.driver
    action = ActionChains(driver)
    action.move_to_element_with_offset(element, pos_start[0], pos_start[1])
    action.click_and_hold()
    action.move_to_element_with_offset(element, pos_end[0], pos_end[1])
    action.release()
    action.perform()


def click_relatively(
    dash_duo: DashComposite, element: WebElement, pos: Tuple[int, int] = (0, 0)
) -> None:
    """Emulator behavior: Click a relative position of an element.

    Arguments
    ---------
    dash_duo: `DashComposite`
        The dash emulator.

    element: `WebElement`
        The anchor of this event. The positions will be calculated as relative
        positions of the upper left corner of this element.

    pos: `(int, int)`
        The position where the mouse will click.
    """
    driver: WebDriver = dash_duo.driver
    action = ActionChains(driver)
    action.move_to_element_with_offset(element, pos[0], pos[1])
    action.click()
    action.perform()


def get_input_element(
    dash_duo: DashComposite, annotator: Union[str, WebElement]
) -> WebElement:
    """Emulator behavior: Get the `<div class="rp-selected-input">` element of a
    selected annotation.

    If the element cannot be found, will throw a timeout error.

    Arguments
    ---------
    dash_duo: `DashComposite`
        The dash emulator.

    annotator: `str | WebElement`
        The CSS-selector or the element of the annotator. To obtain the annotator
        element, the following code can be used:
        ``` python
        dash_duo.find_element("#annotator")
        ```

    Returns
    -------
    #1: `WebElement`
        The `<div class="rp-selected-input">` element in the currently selected
        annotation.
    """
    if isinstance(annotator, str):
        dash_duo.wait_for_element_by_css_selector(
            "{0} > .rp-stage > .rp-selected-input".format(annotator),
        )
        element: WebElement = dash_duo.find_element(
            "{0} > .rp-stage > .rp-selected-input".format(annotator),
        )
    else:
        wait_for(
            dash_duo,
            lambda: annotator.find_element(
                By.CSS_SELECTOR, ".rp-stage > .rp-selected-input"
            ),
        )
        element: WebElement = annotator.find_element(
            By.CSS_SELECTOR,
            ".rp-stage > .rp-selected-input",
        )
    return element


def get_input_box(
    dash_duo: DashComposite, annotator: Union[str, WebElement]
) -> WebElement:
    """Emulator behavior: Get the `<input>` element of a selected annotation.

    If the element cannot be found, will throw a timeout error.

    Arguments
    ---------
    dash_duo: `DashComposite`
        The dash emulator.

    annotator: `str | WebElement`
        The CSS-selector or the element of the annotator. To obtain the annotator
        element, the following code can be used:
        ``` python
        dash_duo.find_element("#annotator")
        ```

    Returns
    -------
    #1: `WebElement`
        The `<input>` element in the currently selected annotation.
    """
    return get_input_element(dash_duo, annotator).find_element(By.TAG_NAME, "input")


def get_input_del_button(
    dash_duo: DashComposite, annotator: Union[str, WebElement]
) -> WebElement:
    """Emulator behavior: Get the delete button, i.e. the
    `<div class="rp-default-input-section_delete">` element of a selected annotation.

    This element appears only when the `<input>` element is available. It should appear
    near the `<input>` element.

    If the element cannot be found, will throw a timeout error.

    Arguments
    ---------
    dash_duo: `DashComposite`
        The dash emulator.

    annotator: `str | WebElement`
        The CSS-selector or the element of the annotator. To obtain the annotator
        element, the following code can be used:
        ``` python
        dash_duo.find_element("#annotator")
        ```

    Returns
    -------
    #1: `WebElement`
        The `<div class="rp-default-input-section_delete">` element in the currently
        selected annotation.
    """
    return get_input_element(dash_duo, annotator).find_element(
        By.CSS_SELECTOR, ".rp-default-input-section_delete"
    )


def get_select_element(
    dash_duo: DashComposite, annotator: Union[str, WebElement]
) -> WebElement:
    """Emulator behavior: Get the React-selector, i.e. the
    `<div class="dpa-dropdown...">` element of a selected annotation.

    If the element cannot be found, will throw a timeout error.

    Arguments
    ---------
    dash_duo: `DashComposite`
        The dash emulator.

    annotator: `str | WebElement`
        The CSS-selector or the element of the annotator. To obtain the annotator
        element, the following code can be used:
        ``` python
        dash_duo.find_element("#annotator")
        ```

    Returns
    -------
    #1: `WebElement`
        The selector element in the currently selected annotation.
    """
    if isinstance(annotator, str):
        dash_duo.wait_for_element_by_css_selector(
            "{0} > .rp-stage > .rp-selected-input > "
            "div[class^='dpa-dropdown']".format(annotator),
        )
        element: WebElement = dash_duo.find_element(
            "{0} > .rp-stage > .rp-selected-input > "
            "div[class^='dpa-dropdown']".format(annotator)
        )
    else:
        wait_for(
            dash_duo,
            lambda: annotator.find_element(
                By.CSS_SELECTOR,
                ".rp-stage > .rp-selected-input > div[class^='dpa-dropdown']",
            ),
        )
        element: WebElement = annotator.find_element(
            By.CSS_SELECTOR,
            ".rp-stage > .rp-selected-input > div[class^='dpa-dropdown']",
        )
    return element


def get_select_expand(
    dash_duo: DashComposite, annotator: Union[str, WebElement]
) -> WebElement:
    """Emulator behavior: Get the control region of the selector. The control region
    is an element that will trigger the dropdown menu when being clicked.

    If the element cannot be found, will throw a timeout error.

    Arguments
    ---------
    dash_duo: `DashComposite`
        The dash emulator.

    annotator: `str | WebElement`
        The CSS-selector or the element of the annotator. To obtain the annotator
        element, the following code can be used:
        ``` python
        dash_duo.find_element("#annotator")
        ```

    Returns
    -------
    #1: `WebElement`
        The control region of the selector element in the currently selected
        annotation.
    """
    return get_select_element(dash_duo, annotator).find_element(
        By.CSS_SELECTOR, "div[class$='-control']"
    )


def get_select_del_button(
    dash_duo: DashComposite, annotator: Union[str, WebElement]
) -> WebElement:
    """Emulator behavior: Get the delete button of the selector.

    This element appears only when the selector element is available. It should appear
    near the control region of the selector element.

    If the element cannot be found, will throw a timeout error.

    Arguments
    ---------
    dash_duo: `DashComposite`
        The dash emulator.

    annotator: `str | WebElement`
        The CSS-selector or the element of the annotator. To obtain the annotator
        element, the following code can be used:
        ``` python
        dash_duo.find_element("#annotator")
        ```

    Returns
    -------
    #1: `WebElement`
        The delete button of the selector element in the currently selected
        annotation.
    """
    return get_select_element(dash_duo, annotator).find_element(
        By.CSS_SELECTOR, "div[class^='dpa-btn-delete']"
    )


def get_select_control_points(
    dash_duo: DashComposite, annotator: Union[str, WebElement]
) -> Sequence[WebElement]:
    """Emulator behavior: Get the control points of the selector. The control points
    represent icons in the selector that will trigger special behaviors. For example,
    a "clear" icon will make the currently selected item cleared.

    If the element cannot be found, will throw a timeout error.

    Arguments
    ---------
    dash_duo: `DashComposite`
        The dash emulator.

    annotator: `str | WebElement`
        The CSS-selector or the element of the annotator. To obtain the annotator
        element, the following code can be used:
        ``` python
        dash_duo.find_element("#annotator")
        ```

    Returns
    -------
    #1: `[WebElement]`
        All clickable control point icons detected in the selector.
    """
    return get_select_element(dash_duo, annotator).find_elements(
        By.CSS_SELECTOR,
        "div[class$='-control'] > div:nth-child(2) > div[class$='-indicatorContainer']",
    )


def get_select_item_by_label(
    dash_duo: DashComposite, annotator: Union[str, WebElement], item_label: str
) -> WebElement:
    """Emulator behavior: Get a selectable item from the menu by checking its label.

    This element can be located only when the dropdown menu is activated by clicking
    the control region of the selector.

    If the element cannot be found, will throw a timeout error.

    Arguments
    ---------
    dash_duo: `DashComposite`
        The dash emulator.

    annotator: `str | WebElement`
        The CSS-selector or the element of the annotator. To obtain the annotator
        element, the following code can be used:
        ``` python
        dash_duo.find_element("#annotator")
        ```

    Returns
    -------
    #1: `WebElement`
        The selectable item in the menu. Click this value will make the currently
        selected item switched to this one.
    """
    element: WebElement = get_select_element(dash_duo, annotator).find_element(
        By.CSS_SELECTOR, "div[class$='-menu']"
    )
    element: WebElement = element.find_element(
        By.XPATH, "//*[text()='{0}']".format(item_label)
    )
    return element


def get_select_current_item(
    dash_duo: DashComposite,
    annotator: Union[str, WebElement],
    expect_to_be: Literal["item", "placeholder"] = "item",
) -> WebElement:
    """Emulator behavior: Get the currently selected item. The selected item is an
    element in the control region of the selector. Its `text` property is the label
    of the currently selected item.

    If the element cannot be found, will throw a timeout error.

    Arguments
    ---------
    dash_duo: `DashComposite`
        The dash emulator.

    annotator: `str | WebElement`
        The CSS-selector or the element of the annotator. To obtain the annotator
        element, the following code can be used:
        ``` python
        dash_duo.find_element("#annotator")
        ```

    Returns
    -------
    #1: `WebElement`
        The currently selected item of the selector element in the currently selected
        annotation.
    """
    element = get_select_element(dash_duo, annotator)
    if expect_to_be == "item":
        wait_for(
            dash_duo,
            lambda: (
                isinstance(
                    element.find_element(
                        By.CSS_SELECTOR,
                        "div[class$='-control'] > div > div[class$=-singleValue]",
                    ),
                    WebElement,
                )
            ),
        )
        element: WebElement = element.find_element(
            By.CSS_SELECTOR, "div[class$='-control'] > div > div[class$=-singleValue]"
        )
    elif expect_to_be == "placeholder":
        wait_for(
            dash_duo,
            lambda: isinstance(
                element.find_element(
                    By.CSS_SELECTOR,
                    "div[class$='-control'] > div > div[id$=-placeholder]",
                ),
                WebElement,
            ),
        )
        element: WebElement = element.find_element(
            By.CSS_SELECTOR, "div[class$='-control'] > div > div[id$=-placeholder]"
        )
    else:
        raise TypeError(
            'The arugment "expect_to_be" is not recognizable: {0}'.format(expect_to_be)
        )
    return element


def get_canvas_image(
    dash_duo: DashComposite,
    annotator: Union[str, WebElement],
    canvas_selector: Literal[".rp-image", ".rp-shapes"] = ".rp-image",
) -> str:
    """Emulator behavior: Get the canvas image.

    This method will returns a base64-encoded and png-format snapshot of a canvas.
    This snapshot can be processed by the image utilities to validate the visualized
    results.

    Arguments
    ---------
    dash_duo: `DashComposite`
        The dash emulator.

    annotator: `str | WebElement`
        The CSS-selector or the element of the annotator. To obtain the annotator
        element, the following code can be used:
        ``` python
        dash_duo.find_element("#annotator")
        ```

    canvas_selector: `".rp-image" | ".rp-shapes"`
        The CSS-selector used for locating the canvas. `".rp-image"` and `".rp-shapes"`
        represent the displayed image and the annotations, respectively.

    Returns
    -------
    #1: `str`
        The base64-encoded and png-format snapshot of the selected canvas.
    """
    driver: WebDriver = dash_duo.driver
    element: WebElement = (
        annotator
        if isinstance(annotator, WebElement)
        else dash_duo.find_element(annotator)
    )
    dash_duo._wait_for(
        attribute_value_neq(element, "data-dash-is-loading", "true"),
        timeout=None,
        msg=(
            "timeout {0}s => waiting for the element {1} to be loaded.".format(
                dash_duo._wait_timeout,
                (
                    annotator
                    if isinstance(annotator, str)
                    else (element.tag_name + element.id)
                ),
            )
        ),
    )
    selector = ".rp-stage > {0}".format(canvas_selector)
    wait_for(
        dash_duo,
        lambda: isinstance(element.find_element(By.CSS_SELECTOR, selector), WebElement),
    )
    element = element.find_element(By.CSS_SELECTOR, selector)
    assert isinstance(element, WebElement)
    res = str(
        driver.execute_script(
            "return {data: arguments[0].toDataURL('image/png')}", element
        ).get("data", "")
    )
    assert res.startswith("data:image/png;base64,")
    return res
