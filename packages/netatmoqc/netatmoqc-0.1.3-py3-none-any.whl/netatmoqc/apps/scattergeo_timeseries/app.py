import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from datetime import datetime as dt
from netatmoqc.config_parser import read_config
from netatmoqc.plots import init_fig_dict, generate_single_frame
from netatmoqc.load_data import read_netatmo_data_for_dtg, epoch2datetime
import pandas as pd

# TEST
import time
import numpy as np
import datetime
import pathlib

# END TEST

# app.config.suppress_callback_exceptions = True
from server import server

config = read_config(os.getenv("NETATMOQC_CONFIG_PATH", "config.toml"))

app = dash.Dash(
    name="scattergeo_timeseries",
    server=server,
    url_base_pathname="/scattergeo_timeseries/",
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
)


def description_card():
    """
    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            html.H5("NetAtmo Data Explorer"),
            html.H3("Welcome to the NetAtmo Data Explorer Dashboard"),
            html.Div(id="intro", children="An aid to explore NetAtmo data.",),
        ],
    )


variable_list = [
    "temperature",
    "pressure",
    "mslp",
    "alt",
    "humidity",
    "sum_rain_1",
]


def generate_control_card():
    """
    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[
            html.P("Select variable"),
            dcc.Dropdown(
                id="variable-select",
                options=[{"label": i, "value": i} for i in variable_list],
                value=variable_list[0],
            ),
            html.Br(),
            html.P("Select time range"),
            dcc.DatePickerRange(
                id="date-picker-select",
                minimum_nights=0,
                start_date=dt(2018, 4, 1),
                end_date=dt(2018, 4, 1),
                min_date_allowed=dt(2018, 4, 1),
                max_date_allowed=dt.today(),
                initial_visible_month=dt(2018, 4, 1),
            ),
            html.Br(),
            html.Br(),
            html.Div(
                id="plot-btn-outer",
                children=html.Button(
                    id="plot-btn", children="Make Plot", n_clicks=0
                ),
            ),
        ],
    )


app.layout = html.Div(
    id="app-container",
    children=[
        # Left column
        html.Div(
            id="left-column",
            className="four columns",
            children=[description_card(), generate_control_card()]
            + [
                html.Div(
                    ["initial child"],
                    id="output-clientside",
                    style={"display": "none"},
                )
            ],
        ),
        # Right column
        html.Div(
            id="right-column",
            className="eight columns",
            children=[
                # Patient Volume Heatmap
                html.Div(
                    id="scattergeo_plot_div",
                    children=[
                        html.B("My Plot"),
                        html.Hr(),
                        dcc.Graph(id="netatmo_data_plot"),
                    ],
                ),
                ## Patient Wait time by Department
                # html.Div(
                #    id="wait_time_card",
                #    children=[
                #        html.B("Patient Wait Time and Satisfactory Scores"),
                #        html.Hr(),
                #        html.Div(id="wait_time_table", children=initialize_table()),
                #    ],
                # ),
            ],
        ),
    ],
)


import plotly.graph_objects as go


@app.callback(
    Output("netatmo_data_plot", "figure"),
    [Input("plot-btn", "n_clicks")],
    [
        State("date-picker-select", "start_date"),
        State("date-picker-select", "end_date"),
        State("variable-select", "value"),
    ],
)
def prepare_animation(n_clicks, start_date, end_date, dataset_var):
    if n_clicks == 0:
        return go.Figure(go.Scattergeo())

    fig_dict, sliders_dict = init_fig_dict(dataset_var, frame_duration=300)
    # make frames
    min_dt_in_seconds = 120 * 60

    # Determine map boundaries and max/min plotted values
    min_lat = 360
    min_lon = 360
    max_lat = 0
    max_lon = 0
    minval_dataset_var = float("inf")
    maxval_dataset_var = -float("inf")

    for fmt in ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"]:
        try:
            start_date = dt.strptime(start_date, fmt).replace(hour=0)
            break
        except (ValueError):
            pass
    for fmt in ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"]:
        try:
            end_date = dt.strptime(end_date, fmt).replace(hour=21)
            break
        except (ValueError):
            pass

    for dtg in pd.date_range(start_date, end_date, freq="3H"):
        print("Reading data for {}".format(dtg))
        df = read_netatmo_data_for_dtg(dtg, rootdir=config.data_rootdir)
        print("    * Done. Now adding frame.")
        # Control of map boundaries
        df = df[df["lat"] > 50]  # Some cleaning
        min_lat = min(min_lat, min(df["lat"]))
        min_lon = min(min_lon, min(df["lon"]))
        max_lat = max(max_lat, max(df["lat"]))
        max_lon = max(max_lon, max(df["lon"]))
        minval_dataset_var = min(minval_dataset_var, min(df[dataset_var]))
        maxval_dataset_var = max(maxval_dataset_var, max(df[dataset_var]))

        frame, slider_step = generate_single_frame(
            df, dataset_var, dtg, frame_duration=300
        )

        fig_dict["frames"].append(frame)
        sliders_dict["steps"].append(slider_step)

    # Adjust colourbar
    cbar_minnval = 0
    cbar_maxval = maxval_dataset_var
    if minval_dataset_var * maxval_dataset_var < 0:
        cbar_maxval = max(np.abs((minval_dataset_var, maxval_dataset_var)))
        cbar_minnval = -cbar_maxval
    for iframe, frame in enumerate(fig_dict["frames"]):
        frame["data"]["marker"]["cmin"] = cbar_minnval
        frame["data"]["marker"]["cmax"] = cbar_maxval
        fig_dict["frames"][iframe] = frame

    # Adjust map boundaries
    fig_dict["layout"]["geo"]["lataxis"]["range"] = (
        min_lat - 0.1,
        max_lat + 0.1,
    )
    fig_dict["layout"]["geo"]["lonaxis"]["range"] = (
        min_lon - 0.1,
        max_lon + 0.1,
    )

    fig_dict["layout"]["sliders"] = [sliders_dict]

    fig_dict["data"] = fig_dict["frames"][0]["data"]

    fig = go.Figure(fig_dict)

    return fig


# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)
