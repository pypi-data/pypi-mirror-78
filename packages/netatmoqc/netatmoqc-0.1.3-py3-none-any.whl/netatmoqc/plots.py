#!/usr/bin/env python3
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import datetime
from netatmoqc.logs import get_logger

# Plotly page on scatter plots on maps: https://plotly.com/python/scatter-plots-on-maps/
# See colorscales at https://plotly.com/python/builtin-colorscales/
# For animations, see https://plotly.com/python/animations/#animated-figures-with-graph-objects


def generate_single_frame(df, dataset_var, dt, frame_duration):

    # Controlling colour schemes
    if dataset_var in ["temperature"]:
        color_scale = px.colors.diverging.RdBu_r
    else:
        color_scale = px.colors.sequential.haline_r

    frame = {"data": None, "name": str(dt)}
    frame["data"] = go.Scattergeo(
        lon=df["lon"],
        lat=df["lat"],
        text=df[dataset_var],
        marker=dict(
            color=df[dataset_var],
            colorscale=color_scale,
            opacity=0.5,
            # size = 8,
            line=dict(color="black", width=0.25),
            colorbar=dict(
                titleside="right", ticks="outside", showticksuffix="last",
            ),
        ),
    )

    slider_step = {
        "args": [
            [str(dt)],
            {
                "frame": {"duration": frame_duration, "redraw": True},
                "mode": "immediate",
                "transition": {"duration": frame_duration},
            },
        ],
        "label": str(dt),
        "method": "animate",
    }

    return frame, slider_step


def init_fig_dict(dataset_var, frame_duration):
    # We will make the figure by constructing a dictionary and passing it
    # to the final plotly method
    fig_dict = {"data": [], "layout": {}, "frames": []}

    # Figure layout
    fig_dict["layout"]["title"] = "NetAtmo Data: {}".format(dataset_var)

    fig_dict["layout"]["width"] = 800
    fig_dict["layout"]["height"] = fig_dict["layout"]["width"]

    fig_dict["layout"]["geo"] = dict(
        scope="europe",
        resolution=110,
        projection_type="stereographic",
        showland=True,
        showcountries=True,
        lataxis=dict(
            showgrid=True,
            dtick=10,
            # range=(min_lat-1, max_lat+1)
        ),
        lonaxis=dict(
            showgrid=True,
            dtick=15,
            # range=(min_lon-1, max_lon+1)
        ),
    )

    fig_dict["layout"]["updatemenus"] = [
        {
            "buttons": [
                {
                    "args": [
                        None,
                        {
                            "frame": {
                                "duration": frame_duration,
                                "redraw": True,
                            },
                            "fromcurrent": True,
                            "transition": {
                                "duration": frame_duration,
                                "easing": "quadratic-in-out",
                            },
                        },
                    ],
                    "label": "Play",
                    "method": "animate",
                },
                {
                    "args": [
                        [None],
                        {
                            "frame": {"duration": 0, "redraw": True},
                            "mode": "immediate",
                            "transition": {"duration": 0},
                        },
                    ],
                    "label": "Pause",
                    "method": "animate",
                },
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top",
        }
    ]

    sliders_dict = {
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 20},
            "prefix": "DT: ",
            "visible": True,
            "xanchor": "right",
        },
        "transition": {"duration": frame_duration, "easing": "cubic-in-out"},
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "steps": [],
    }

    return fig_dict, sliders_dict


# Make an animation
def make_map_animation(
    netatmo_data, dataset_var, min_dt_in_seconds=1.0, frame_duration=300
):
    # dts stand for dates and times
    dts = netatmo_data.keys()

    # Determine map boundaries and max/min plotted values
    min_lat = 360
    min_lon = 360
    max_lat = 0
    max_lon = 0
    minval_dataset_var = float("inf")
    maxval_dataset_var = -float("inf")
    for dt in dts:
        min_lat = min(min_lat, min(netatmo_data[dt]["lat"]))
        min_lon = min(min_lon, min(netatmo_data[dt]["lon"]))
        max_lat = max(max_lat, max(netatmo_data[dt]["lat"]))
        max_lon = max(max_lon, max(netatmo_data[dt]["lon"]))
        minval_dataset_var = min(
            minval_dataset_var, min(netatmo_data[dt][dataset_var])
        )
        maxval_dataset_var = max(
            maxval_dataset_var, max(netatmo_data[dt][dataset_var])
        )

    fig_dict, sliders_dict = init_fig_dict(dataset_var, frame_duration)

    # make frames
    previous_dt = datetime.datetime(2002, 2, 20)
    for dt in netatmo_data:
        if (dt - previous_dt).total_seconds() < min_dt_in_seconds:
            continue
        previous_dt = dt

        frame, slider_step = generate_single_frame(
            netatmo_data[dt], dataset_var, dt, frame_duration
        )

        fig_dict["frames"].append(frame)
        sliders_dict["steps"].append(slider_step)

    fig_dict["layout"]["sliders"] = [sliders_dict]
    fig_dict["data"] = fig_dict["frames"][0]["data"]

    fig = go.Figure(fig_dict)

    return fig


##################################################################################
def empty_scattergeo():
    fig = go.Figure(go.Scattergeo())
    fig.update_layout(
        height=500,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        geo=dict(
            # scope='europe',
            showcountries=True,
            # showsubunits = True,
            projection_type="stereographic",
            # center=dict(lon=63, lat=17),
            # projection_rotation=dict(lon=63, lat=17, roll=0),
            lataxis_range=[55, 72],
            lonaxis_range=[4.5, 31.85],
        ),
    )
    return fig


def make_simple_scatter_geo(
    df, min_lat=None, max_lat=None, min_lon=None, max_lon=None, **kwargs
):
    fig = px.scatter_geo(
        df,
        lat="lat",
        lon="lon",
        hover_data=df.columns,
        projection="stereographic",
        height=500,
        **kwargs
    )

    if min_lat is None:
        min_lat = min(df["lat"])
    if max_lat is None:
        max_lat = max(df["lat"])
    if min_lon is None:
        min_lon = min(df["lon"])
    if max_lon is None:
        max_lon = max(df["lon"])

    fig.update_layout(
        clickmode="event+select",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        geo=dict(
            showland=True,
            showcountries=True,
            # showsubunits = True,
            lataxis=dict(
                showgrid=True, dtick=10, range=[min_lat - 0.5, max_lat + 0.5],
            ),
            lonaxis=dict(
                showgrid=True, dtick=15, range=[min_lon - 0.5, max_lon + 0.5],
            ),
        ),
    )

    return fig


def make_clustering_fig(df, quiet=True):
    # Knowing whether the scan method was dbscan or hdbscan
    if "is_core_point" in df.columns:
        clustering_method = "dbscan"
    else:
        clustering_method = "hdbscan"
    # Getting member counts for every label
    unique_labels, member_counts = np.unique(
        df["cluster_label"], return_counts=True
    )
    label2count = {
        label: count for label, count in zip(unique_labels, member_counts)
    }

    # Get labels of obs removed due to post-clustering refinement
    # See clustering.py for an explanation about the meaning of
    # rm_obs_label_offset and the convention employed to calculate it
    # and determine these labels.
    try:
        max_abs_rm_label = abs(min(l for l in unique_labels if l < -1))
        rm_obs_label_offset = 1
        while max_abs_rm_label % rm_obs_label_offset != max_abs_rm_label:
            rm_obs_label_offset *= 10
        rm_obs_label_offset //= 10
    except (ValueError):
        rm_obs_label_offset = None

    # Construct array with some descriptive labels for plot
    plot_labels = []
    label_to_legend_label = {}
    for index, row in df.iterrows():
        label = row["cluster_label"]
        if label == -1:
            legend_label = "Rejected obs: "
        elif label < -1:
            orig_cluster_label = int(-(label + rm_obs_label_offset))
            legend_label = "Cluster {}, obs removed due to refining: ".format(
                orig_cluster_label
            )
        else:
            legend_label = "Cluster {}, accepted obs: ".format(int(label))
        legend_label += "{} obs".format(int(label2count[label]))
        plot_labels.append(legend_label)
        label_to_legend_label[label] = legend_label

    # Define colours and symbols
    color_discrete_sequence = [
        px.colors.qualitative.Light24,
        px.colors.qualitative.Alphabet,
        px.colors.qualitative.Dark24,
    ][0]
    # See all symbols at
    # <https://plotly.com/python/marker-style/#custom-marker-symbols>
    symbols = [
        "circle",
        "octagon",
        "hexagon2",
        "circle-dot",
        "octagon-dot",
        "circle-cross",
        "circle-x",
    ]
    # Assign colous and synbols for the legend entries corresponding
    # to every cluster
    color_discrete_map = {-1: "black"}
    leg2symbol = {}
    for ilabel, label in enumerate(l for l in unique_labels if l >= 0):
        # Change colour for every cluster, cycle when all have been used
        color = color_discrete_sequence[ilabel % len(color_discrete_sequence)]
        # Change symbols every len(color_discrete_sequence) time. Cycle when
        # all symbols have been used.
        i_symb = (ilabel // len(color_discrete_sequence)) % len(symbols)
        symbol = symbols[i_symb]
        leg_label = label_to_legend_label[label]
        color_discrete_map[leg_label] = color
        leg2symbol[leg_label] = symbol
        if rm_obs_label_offset is not None:
            try:
                # Make sure points removed by clusters at the refinement stage
                # keep the colours of their parent clusters
                rm_ob_label = int(-(label + rm_obs_label_offset))
                leg_label_of_removed = label_to_legend_label[rm_ob_label]
                color_discrete_map[leg_label_of_removed] = color
                leg2symbol[leg_label_of_removed] = symbol
            except (KeyError):
                if rm_ob_label in unique_labels:
                    raise
                else:
                    # Some clusters do not have any observation removed
                    # after refining
                    pass

    # Preparing plot
    # Zoom in based on coords of accepted obs
    coords_of_accepted_obs = df[df["cluster_label"] > -1][["lat", "lon"]]
    max_lat = max(coords_of_accepted_obs["lat"]) + 0.5
    min_lat = min(coords_of_accepted_obs["lat"]) - 0.5
    max_lon = max(coords_of_accepted_obs["lon"]) + 0.5
    min_lon = min(coords_of_accepted_obs["lon"]) - 0.5
    fig = make_simple_scatter_geo(
        df,
        min_lat=min_lat,
        max_lat=max_lat,
        min_lon=min_lon,
        max_lon=max_lon,
        color=plot_labels,
        color_discrete_map=color_discrete_map,
        hover_name=plot_labels,  # column added to hover information
    )

    fig.update_layout(
        legend_title=(
            "<b> Clustering of Observations </b> <br>"
            + "<b> Method: {} </b>".format(clustering_method)
        ),
    )

    def config_trace_markers(trace):
        tracename_lower = trace.name.lower()
        if "rejected" in tracename_lower:
            trace.update(
                visible="legendonly",
                marker=dict(
                    symbol="x-open",
                    size=5,
                    color="black",
                    opacity=0.25,
                    line=dict(width=1,),
                ),
            )
        elif "removed" in tracename_lower:
            trace.update(
                marker=dict(
                    # Keep colour of original cluster in this case
                    symbol="x-open",
                    size=5,
                    opacity=0.25,
                    line=dict(width=1,),
                )
            )
        else:
            trace.update(
                marker=dict(
                    # symbol="circle",
                    symbol=leg2symbol[trace.name],
                    size=8,
                    opacity=0.75,
                    line=dict(
                        # color=color_discrete_map[trace.name],
                        width=1.0,
                    ),
                )
            )

    fig.for_each_trace(lambda trace: config_trace_markers(trace),)

    return fig


def show_cmd_get_fig_from_dataframes(args, dataframes):
    logger = get_logger(__name__, args.loglevel)

    df = (
        pd.concat(dataframes, names=["fname"])
        .reset_index(level=0)
        .reset_index(drop=True)
    )

    if "accepted_stations.csv" in df["fname"].unique():
        df_accepted = df[df["fname"] == "accepted_stations.csv"]
        max_lat = max(df_accepted["lat"]) + 0.5
        min_lat = min(df_accepted["lat"]) - 0.5
        max_lon = max(df_accepted["lon"]) + 0.5
        min_lon = min(df_accepted["lon"]) - 0.5
        fig = make_simple_scatter_geo(
            df,
            color="fname",
            min_lat=min_lat,
            max_lat=max_lat,
            min_lon=min_lon,
            max_lon=max_lon,
        )
    else:
        fig = make_simple_scatter_geo(df, color="fname")

    return fig
