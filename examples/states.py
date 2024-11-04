# -*- coding: UTF-8 -*-
"""
States
======
@ Dash Picture Annotation

Author
------
Yuchen Jin (cainmagi)
cainmagi@gmail.com

License
-------
MIT License

Description
-----------
The demo for updating the annotator states from the server side.
"""

import os
import json

from typing import Optional

import dash
from dash import dcc, html
from dash import Output, Input, State


if __name__ == "__main__":
    import sys

    sys.path.append(os.path.dirname(os.path.dirname(__file__)))


import dash_picture_annotation as dpa


app = dash.Dash(
    __name__,
    assets_folder=os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "tests", "assets"
    ),
)

image_list = ["test_image.svg", "test_philips_PM5544.svg"]

default_data = {
    "timestamp": 0,
    "data": [
        {
            "id": "TestID",
            "mark": {
                "x": 200.87731048580005,
                "y": 78.57834993258817,
                "width": 196.74579219762532,
                "height": 198.54529639455487,
                "type": "RECT",
            },
            "comment": "Test-init",
        },
    ],
}

styles = {
    "mb1": {"marginBottom": "1rem"},
    "mr1": {"marginRight": "1rem"},
}

app.layout = html.Div(
    [
        dcc.Loading(
            dpa.DashPictureAnnotation(
                id="annotator",
                style={"height": "80vh"},
                data=default_data,
                image=None,
                options=None,
                clearable_dropdown=True,
            ),
            delay_show=1000,
        ),
        dcc.Loading(
            html.Div(
                id="output", children=json.dumps(default_data), style=styles["mb1"]
            ),
            delay_show=1000,
        ),
        html.Div(
            children=(
                html.Button(
                    children="Toggle disabled", id="btn-disabled", style=styles["mr1"]
                ),
                html.Button(
                    children="Toggle image", id="btn-image", style=styles["mr1"]
                ),
                html.Button(children="Reset data", id="btn-data"),
            ),
            style=styles["mb1"],
        ),
    ]
)


@app.callback(
    Output("annotator", "disabled"),
    Input("btn-disabled", "n_clicks"),
    State("annotator", "disabled"),
    prevent_initial_call=True,
)
def toggle_disabled(n_clicks: Optional[int], is_disabled: Optional[bool]):
    if n_clicks:
        return not bool(is_disabled)
    return dash.no_update


@app.callback(
    Output("annotator", "image"),
    Input("btn-image", "n_clicks"),
    State("annotator", "image"),
    prevent_initial_call=False,
)
def toggle_image(n_clicks: Optional[int], prev_image: Optional[str]) -> str:
    if n_clicks:
        if isinstance(prev_image, str):
            try:
                idx = image_list.index(os.path.split(prev_image)[-1])
            except ValueError:
                return "/assets/test_image.svg"
            next_idx = (idx + 1) % len(image_list)
            return "/assets/{0}".format(image_list[next_idx])
    return "/assets/test_image.svg"


@app.callback(
    Output("annotator", "data"),
    Input("btn-data", "n_clicks"),
    prevent_initial_call=False,
)
def reset_data(n_clicks: Optional[int]):
    if n_clicks:
        return default_data
    return dash.no_update


@app.callback(
    Output("output", "children"), Input("annotator", "data"), prevent_initial_call=False
)
def get_annotation(data) -> Optional[str]:
    if data is None:
        return None
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
