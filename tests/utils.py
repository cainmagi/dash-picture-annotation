# -*- coding: UTF-8 -*-
"""
Utilities
=========
@ Dash Picture Annotation - Tests

Author
------
Yuchen Jin (cainmagi)
cainmagi@gmail.com

Description
-----------
Extra functionalities used for enhancing the tests.
"""

import os
import collections.abc

from typing import Optional, Any

try:
    from typing import Sequence, Mapping, Callable
except ImportError:
    from collections.abc import Sequence, Mapping, Callable

from dash.testing.composite import DashComposite
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import StaleElementReferenceException


__all__ = (
    "is_eq",
    "is_eq_mapping",
    "is_eq_sequence",
    "is_mapping_with_keys",
    "tst_folder",
    "asset_folder",
    "wait_func",
    "attribute_value_to_equal",
    "attribute_value_neq",
    "wait_for_the_attribute_value_to_equal",
    "wait_for_the_attribute_value_neq",
    "wait_for_dcc_loading",
    "wait_for",
)


def is_eq(val: Any, ref: Any) -> bool:
    """Safely check whether `val == ref`"""
    if isinstance(ref, (str, bytes)):
        return isinstance(val, ref.__class__) and val == ref
    if isinstance(ref, collections.abc.Sequence):
        return is_eq_sequence(val, ref)
    elif isinstance(ref, collections.abc.Mapping):
        return is_eq_mapping(val, ref)
    else:
        return isinstance(val, ref.__class__) and val == ref


def is_eq_mapping(val: Any, ref: Mapping[Any, Any]) -> bool:
    """Safely check whether `val == ref`, where `ref` is a mapping."""
    if not isinstance(val, collections.abc.Mapping):
        return False
    return val == ref


def is_eq_sequence(val: Any, ref: Sequence[Any]) -> bool:
    """Safely check whether `val == ref`, where `ref` is a sequence."""
    if isinstance(val, (str, bytes)) or (not isinstance(val, collections.abc.Sequence)):
        return False
    return tuple(val) == tuple(ref)


def is_mapping_with_keys(val: Any, keys: Sequence[Any]) -> bool:
    """Check whether `val` is mapping and this mapping has keys specified by `keys`.

    If `keys` is not a sequence, will treat it as one key.
    """
    if isinstance(keys, (str, bytes)) or (
        not isinstance(keys, collections.abc.Sequence)
    ):
        keys = (keys,)
    if not isinstance(val, collections.abc.Mapping):
        return False
    return set(val.keys()) == set(keys)


def tst_folder(file_name: Optional[str] = None) -> str:
    """Get the path of the testing folder.

    Arguments
    ---------
    file_name: `str`
        If specified, will view this value as the name of the file in the testing
        folder.

    Returns
    -------
    #1: `str`
        If `file_name` is provided, return the path of that file.
        Otherwise, return the testing folder path.
    """
    path = os.path.dirname(__file__)
    return (
        os.path.join(path, file_name)
        if isinstance(file_name, str) and file_name
        else path
    )


def asset_folder(file_name: Optional[str] = None) -> str:
    """Get the path of the asset folder.

    Arguments
    ---------
    file_name: `str`
        If specified, will view this value as the name of the file in the asset folder.

    Returns
    -------
    #1: `str`
        If `file_name` is provided, return the path of that file.
        Otherwise, return the asset folder path.
    """
    path = os.path.join(os.path.dirname(__file__), "assets")
    return (
        os.path.join(path, file_name)
        if isinstance(file_name, str) and file_name
        else path
    )


class wait_func:
    """Wait-for method: text value does not equal to something.

    The instance of this class serves as a method used by `DashComposite._waitfor`.
    It will listen to the state of the chosen element until its specific attribute
    value is not the specified value any more.
    """

    def __init__(self, func: Callable[[], bool]):
        """Initialization.

        Arguments
        ---------
        func: `() -> bool`
            The function to be waited. If `func()` returns `True`, the waiting will be
            finished.
        """
        self.func = func

    def __call__(self, driver):
        try:
            return self.func()
        except StaleElementReferenceException:
            return False


class attribute_value_to_equal:
    """Wait-for method: attribute value equals to something.

    The instance of this class serves as a method used by `DashComposite._waitfor`.
    It will listen to the state of the chosen element until its specific attribute
    value is not the specified value any more.
    """

    def __init__(self, element: WebElement, attribute: str, value: Any) -> None:
        """Initialization.

        Arguments
        ---------
        element: `WebElement`
            The selected selenium `WebElement` where the attribtue will be listened to.

        attribtue: `str`
            The attribute name to be checked. Normally, this name should starts with
            `"data-"`.

        value: `Any`
            The value that the attribute expects to be. Normally, this value
            should be a string.
        """
        self.element = element
        self.attribute = attribute
        self.value = value
        self.value_type = type(value)

    def __call__(self, driver: WebDriver):
        """Wait-for method."""
        try:
            element_attribute = self.element.get_attribute(self.attribute)
            return isinstance(element_attribute, self.value_type) and (
                element_attribute == self.value
            )
        except StaleElementReferenceException:
            return False


class attribute_value_neq:
    """Wait-for method: attribute value does not equal to something.

    The instance of this class serves as a method used by `DashComposite._waitfor`.
    It will listen to the state of the chosen element until its specific attribute
    value is not the specified value any more.
    """

    def __init__(self, element: WebElement, attribute: str, value: Any) -> None:
        """Initialization.

        Arguments
        ---------
        element: `WebElement`
            The selected selenium `WebElement` where the attribtue will be listened to.

        attribtue: `str`
            The attribute name to be checked. Normally, this name should starts with
            `"data-"`.

        value: `Any`
            The value that the attribute needs to quit from. Normally, this value
            should be a string.
        """
        self.element = element
        self.attribute = attribute
        self.value = value
        self.value_type = type(value)

    def __call__(self, driver: WebDriver):
        """Wait-for method."""
        try:
            element_attribute = self.element.get_attribute(self.attribute)
            return (not isinstance(element_attribute, self.value_type)) or (
                element_attribute != self.value
            )
        except StaleElementReferenceException:
            return False


def wait_for(
    dash_duo: DashComposite,
    func: Optional[Callable[[], bool]] = None,
    timeout: Optional[int] = None,
) -> None:
    """The general `wait_for` method for `dash_duo`.

    Arguments
    ---------
    dash_duo: `DashComposite`
        The dash emulator providing the `_wait_for` method.

    func: `(() -> bool) | None`
        The validator function. The input value is the attribute value. If this
        function returns `True`, the check will pass.

        If this function is not specified, will not wait for anything and return
        immediately.

    timeout: `int | None`
        The customized time out (seconds) length that this method needs to wait.
    """
    if func is None:
        return
    dash_duo._wait_for(
        wait_func(func),
        timeout=timeout,
        msg=(
            "timeout {0}s => waiting for the function {1}.".format(
                timeout or dash_duo._wait_timeout, str(func)
            )
        ),
    )


def wait_for_the_attribute_value_to_equal(
    dash_duo: DashComposite,
    selector: str,
    by: str = "CSS_SELECTOR",
    attribute: str = "data-any",
    value: Any = "",
    timeout: Optional[int] = None,
) -> None:
    """Select an element, and wait until its attribute equals to the specific value.

    Arguments
    ---------
    dash_duo: `DashComposite`
        The dash emulator providing the `_wait_for` method.

    selector: `str`
        The selector used for locating the target element.

    by: `str`
        The method of using the selector.
        Valid values: "CSS_SELECTOR", "ID", "NAME", "TAG_NAME",
        "CLASS_NAME", "LINK_TEXT", "PARTIAL_LINK_TEXT", "XPATH".

    attribtue: `str`
        The attribute name to be checked. Normally, this name should starts with
        `"data-"`.

    value: `Any`
        The value that the attribute expects to be. Normally, this value should be a
        string.

    timeout: `int | None`
        The customized time out (seconds) length that this method needs to wait.
    """
    dash_duo._wait_for(
        attribute_value_to_equal(dash_duo.find_element(selector, by), attribute, value),
        timeout=timeout,
        msg=(
            "timeout {0}s => waiting for the element {1} until the attribute {2} is "
            "not {3}.".format(
                timeout or dash_duo._wait_timeout, selector, attribute, value
            )
        ),
    )


def wait_for_the_attribute_value_neq(
    dash_duo: DashComposite,
    selector: str,
    by: str = "CSS_SELECTOR",
    attribute: str = "data-any",
    value: Any = "",
    timeout: Optional[int] = None,
) -> None:
    """Select an element, and wait until its attribute does not equal to the specific
    value.

    Arguments
    ---------
    dash_duo: `DashComposite`
        The dash emulator providing the `_wait_for` method.

    selector: `str`
        The selector used for locating the target element.

    by: `str`
        The method of using the selector.
        Valid values: "CSS_SELECTOR", "ID", "NAME", "TAG_NAME",
        "CLASS_NAME", "LINK_TEXT", "PARTIAL_LINK_TEXT", "XPATH".

    attribtue: `str`
        The attribute name to be checked. Normally, this name should starts with
        `"data-"`.

    value: `Any`
        The value that the attribute needs to quit from. Normally, this value should
        be a string.

    timeout: `int | None`
        The customized time out (seconds) length that this method needs to wait.
    """
    dash_duo._wait_for(
        attribute_value_neq(dash_duo.find_element(selector, by), attribute, value),
        timeout=None,
        msg=(
            "timeout {0}s => waiting for the element {1} until the attribute {2} is "
            "not {3}.".format(
                timeout or dash_duo._wait_timeout, selector, attribute, value
            )
        ),
    )


def wait_for_dcc_loading(
    dash_duo: DashComposite,
    selector: str,
    by: str = "CSS_SELECTOR",
    timeout: Optional[int] = None,
) -> None:
    """Select an element, and wait until it quits from the is-loading state.

    Arguments
    ---------
    dash_duo: `DashComposite`
        The dash emulator providing the `_wait_for` method.

    selector: `str`
        The selector used for locating the target element.

    by: `str`
        The method of using the selector.
        Valid values: "CSS_SELECTOR", "ID", "NAME", "TAG_NAME",
        "CLASS_NAME", "LINK_TEXT", "PARTIAL_LINK_TEXT", "XPATH".

    timeout: `int | None`
        The customized time out (seconds) length that this method needs to wait.
    """
    dash_duo._wait_for(
        attribute_value_neq(
            dash_duo.find_element(selector, by), "data-dash-is-loading", "true"
        ),
        timeout=None,
        msg=(
            "timeout {0}s => waiting for the element {1} to be loaded.".format(
                timeout or dash_duo._wait_timeout, selector
            )
        ),
    )
