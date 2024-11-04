# -*- coding: UTF-8 -*-
"""
Usage
=====
@ Dash Picture Annotation

Author
------
Yuchen Jin (cainmagi)
cainmagi@gmail.com

Description
-----------
A demo for the project. Run the following command to view the performance:
``` shell
python usage.py
```
"""

import os

from typing import Optional, Any

try:
    from typing import Sequence
except ImportError:
    from collections.abc import Sequence

import dash
import json
from dash import Dash, dcc, callback, html, Input, Output, State
import dash_picture_annotation as dpa

app = Dash(
    __name__, assets_folder=os.path.join(os.path.dirname(__file__), "tests/assets")
)


default_data = {
    "timestamp": None,
    "data": [
        {
            "id": "AYAder",
            "mark": {
                "x": 200.87731048580005,
                "y": 78.57834993258817,
                "width": 196.74579219762532,
                "height": 198.54529639455487,
                "type": "RECT",
            },
            "comment": "Title",
        },
    ],
}

default_options = [
    {"value": "Title", "label": "Title"},
    {"value": "Label", "label": "Label"},
]

image_list = ["test_image.svg", "test_philips_PM5544.svg"]

styles = {
    "mr1": {"marginRight": "1rem"},
    "mb1": {"marginBottom": "1rem"},
}

app.layout = html.Div(
    [
        dcc.Loading(
            dpa.DashPictureAnnotation(
                id="annotator",
                style={"height": "80vh", "marginBottom": "1rem"},
                data=default_data,
                image="/assets/test_image.svg",
                options=default_options,
                clearable_dropdown=True,
            ),
            delay_show=1000,
        ),
        html.Div(
            (
                html.Button(
                    children="Toggle disabled", id="btn-disabled", style=styles["mr1"]
                ),
                html.Button(
                    children="Toggle color", id="btn-color", style=styles["mr1"]
                ),
                html.Button(
                    children="Toggle options", id="btn-options", style=styles["mr1"]
                ),
                html.Button(
                    children="Reset Annotations", id="btn-reset", style=styles["mr1"]
                ),
                html.Button(
                    children="Change Image", id="btn-changeimg", style=styles["mr1"]
                ),
            ),
            style=styles["mb1"],
        ),
        dcc.Loading(
            html.Div(
                id="output", children=json.dumps(default_data), style=styles["mb1"]
            ),
            delay_show=1000,
        ),
    ]
)


@callback(
    Output("annotator", "disabled"),
    Input("btn-disabled", "n_clicks"),
    State("annotator", "disabled"),
)
def toggle_disabled(n_clicks: Optional[int], disabled: Optional[bool]):
    if n_clicks:
        return not bool(disabled)
    return dash.no_update


@callback(
    Output("annotator", "is_color_dynamic"),
    Input("btn-color", "n_clicks"),
    State("annotator", "is_color_dynamic"),
)
def toggle_color(n_clicks: Optional[int], is_color_dynamic: Optional[bool]):
    if n_clicks:
        return not bool(is_color_dynamic)
    return dash.no_update


@callback(
    Output("annotator", "options"),
    Input("btn-options", "n_clicks"),
    State("annotator", "options"),
)
def toggle_options(n_clicks: Optional[int], options: Optional[Sequence[Any]]):
    if n_clicks:
        if options:
            return None
        else:
            return default_options
    return dash.no_update


@app.callback(
    Output("annotator", "data"),
    Input("btn-reset", "n_clicks"),
    prevent_initial_call=False,
)
def reset_data(n_clicks: Optional[int]):
    if n_clicks:
        return default_data
    return dash.no_update


@callback(
    Output("annotator", "image"),
    Input("btn-changeimg", "n_clicks"),
    State("annotator", "image"),
    prevent_initial_call=False,
)
def reset_img(n_clicks: Optional[int], prev_image: Optional[str]) -> str:
    if n_clicks:
        if isinstance(prev_image, str):
            try:
                idx = image_list.index(os.path.split(prev_image)[-1])
            except ValueError:
                return "/assets/test_image.svg"
            next_idx = (idx + 1) % len(image_list)
            return "/assets/{0}".format(image_list[next_idx])
    return "/assets/test_image.svg"


@callback(
    Output("output", "children"), Input("annotator", "data"), prevent_initial_call=False
)
def get_annotation(data) -> str:
    return json.dumps(data)


if __name__ == "__main__":
    import socket

    def get_ip(method: str = "broadcast") -> str:
        """Detect the IP address of this device."""
        s_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            if method == "broadcast":
                s_socket.connect(("10.255.255.255", 1))
                ip_value = s_socket.getsockname()[0]
            elif method == "udp":
                s_socket.connect(("8.8.8.8", 1))
                ip_value = s_socket.getsockname()[0]
            elif method == "host":
                ip_value = socket.gethostbyname(socket.gethostname())
            else:
                raise ConnectionError
        except Exception:  # pylint: disable=broad-except
            ip_value = "localhost"
        finally:
            s_socket.close()
        return ip_value

    app.run(host=get_ip(), port="8080", debug=False)
