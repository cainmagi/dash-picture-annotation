# -*- coding: UTF-8 -*-
"""
Options
=======
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
The demo for using the selecting box to specify the annotation comments.
"""

import os
import json

from typing import Optional, Any

try:
    from typing import Sequence
except ImportError:
    from collections.abc import Sequence

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

default_data = {"timestamp": 0, "data": []}

default_options = [
    {"value": "type-1", "label": "Type 1"},
    {"value": "type-2", "label": "Type 2"},
]

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
                image="/assets/test_image.svg",
                options=None,
                clearable_dropdown=True,
                placeholder_input="Using free mode...",
                placeholder_dropdown="Using selection mode...",
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
                    children="Toggle options", id="btn-options", style=styles["mr1"]
                ),
                html.Button(children="Toggle options clearable", id="btn-optclear"),
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
    Output("annotator", "options"),
    Output("annotator", "clearable_dropdown"),
    Input("btn-options", "n_clicks"),
    Input("btn-optclear", "n_clicks"),
    State("annotator", "options"),
    State("annotator", "clearable_dropdown"),
    prevent_initial_call=True,
)
def toggle_options(
    n_clicks_options: Optional[int],
    n_clicks_optclear: Optional[int],
    options: Optional[Sequence[Any]],
    clearable_dropdown: Optional[bool],
):
    trigger = dash.ctx.triggered_id
    if trigger and trigger == "btn-options" and n_clicks_options:
        if options:
            return None, dash.no_update
        else:
            return default_options, dash.no_update
    if trigger and trigger == "btn-optclear" and n_clicks_optclear:
        return dash.no_update, not bool(clearable_dropdown)
    return dash.no_update, dash.no_update


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
