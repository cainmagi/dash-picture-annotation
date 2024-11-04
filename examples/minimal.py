# -*- coding: UTF-8 -*-
"""
Minimal
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
The minimal demo for the basic functionalities.
"""

import os
import json

from typing import Optional

import dash
from dash import dcc, html
from dash import Output, Input


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
            ),
            delay_show=1000,
        ),
        dcc.Loading(
            html.Div(
                id="output",
                children=json.dumps(default_data),
                style={"marginBottom": "1rem"},
            ),
            delay_show=1000,
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
