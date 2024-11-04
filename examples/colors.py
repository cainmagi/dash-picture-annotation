# -*- coding: UTF-8 -*-
"""
Colors
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
The demo for configuring colors of the annotation boxes.
"""

import os
import json

from typing import Optional

try:
    from typing import Mapping
except ImportError:
    from collections.abc import Mapping

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

with open(
    os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "tests", "data-colors.json"
    ),
    "r",
) as fobj:
    example_data = json.load(fobj)

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
                data=example_data,
                image="/assets/test_image.svg",
                options=None,
                clearable_dropdown=True,
            ),
            delay_show=1000,
        ),
        dcc.Loading(
            html.Div(id="output", children=None, style={"marginBottom": "1rem"}),
            delay_show=1000,
        ),
        html.Div(
            children=(
                html.Button(
                    children="Toggle default color",
                    id="btn-default",
                    style=styles["mr1"],
                ),
                html.Button(
                    children="Toggle specific color",
                    id="btn-specific",
                    style=styles["mr1"],
                ),
                html.Button(
                    children="Toggle dynamic color",
                    id="btn-dynamic",
                    style=styles["mr1"],
                ),
            ),
            style=styles["mb1"],
        ),
    ]
)


@app.callback(
    Output("output", "children"), Input("annotator", "data"), prevent_initial_call=False
)
def get_annotation(data) -> Optional[str]:
    if data is None:
        return None
    return json.dumps(data)


@app.callback(
    Output("annotator", "style_annotation"),
    Input("btn-default", "n_clicks"),
    State("annotator", "style_annotation"),
    prevent_initial_call=True,
)
def toggle_default_color(n_clicks: Optional[int], style_annotation: Optional[str]):
    if n_clicks:
        if not isinstance(style_annotation, str):
            return "#000"
        if style_annotation == "#fff":
            return "#000"
        else:
            return "#fff"
    return dash.no_update


@app.callback(
    Output("annotator", "colors"),
    Input("btn-specific", "n_clicks"),
    State("annotator", "colors"),
    prevent_initial_call=True,
)
def toggle_specific_colors(
    n_clicks: Optional[int], colors: Optional[Mapping[str, str]]
):
    if n_clicks:
        if colors:
            return None
        else:
            return dict(
                zip(
                    (ditem["comment"] for ditem in example_data["data"]),
                    ("hsl(180, 100%, 50%)", "rgb(255, 0, 255)", "#ff0"),
                )
            )
    return dash.no_update


@app.callback(
    Output("annotator", "is_color_dynamic"),
    Input("btn-dynamic", "n_clicks"),
    State("annotator", "is_color_dynamic"),
    prevent_initial_call=True,
)
def toggle_dynamic_color(n_clicks: Optional[int], is_color_dynamic: Optional[bool]):
    if n_clicks:
        return not bool(is_color_dynamic)
    return dash.no_update


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
