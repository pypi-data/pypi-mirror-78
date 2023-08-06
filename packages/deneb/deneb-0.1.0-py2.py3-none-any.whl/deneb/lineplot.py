from typing import Any, Dict, List, Optional, Tuple, Union

import altair as alt
import pandas as pd

from .utils import Chart


def lineplot(
    df,
    x: str,
    y: str,
    c: Optional[str] = None,
    aggregate: Optional[str] = "mean",
    points: bool = True,
    lines: bool = True,
    errorbars: bool = True,
    error_extent: str = "stdev",
    spacing: int = 5,
    color: Optional[Union[str, alt.Color]] = None,
) -> Chart:
    """Produces lineplot with optional errorbars and facets

    Args:
        df: Dataframe
        x: Shorthand for x
        y: Shorthand for y
        c: Shorthand for columns (optional) which are faceted
        aggregate: Aggregation function for y values
        points: Whether to show points
        lines: Whether to show lines
        errorbars: Whether to show errorbars
        error_extent: Extent of errorbars, e.g., stdev or stderr
        spacing: Spacing between facets
        color: Colorscale

    Returns:
        Chart
    """
    if color is None:
        color_kwarg = {}
    else:
        color_kwarg = {"color": color}

    lines_layer = (
        alt.Chart()
        .mark_line()
        .encode(
            x=alt.X(x, title=""),
            y=alt.Y(y, scale=alt.Scale(zero=False), aggregate=aggregate),
            **color_kwarg
        )
    )

    points_layer = (
        alt.Chart()
        .mark_point(filled=True)
        .encode(
            x=alt.X(x, title=""),
            y=alt.Y(y, scale=alt.Scale(zero=False), aggregate=aggregate),
            **color_kwarg
        )
    )

    errorbars_layer = (
        alt.Chart()
        .mark_errorbar(extent=error_extent)
        .encode(
            x=alt.X(x, title=""), y=alt.Y(y, scale=alt.Scale(zero=False)), **color_kwarg
        )
    )

    layers = []
    if lines:
        layers.append(lines_layer)
    if points:
        layers.append(points_layer)
    if errorbars:
        layers.append(errorbars_layer)

    chart = alt.layer(*layers, data=df)

    if c is not None:
        chart = chart.facet(
            column=alt.Column(
                c, title="Number of simulations", header=alt.Header(labels=True)
            ),
            spacing=spacing,
        )
        chart = chart.configure_header(titleOrient="bottom", labelOrient="top")

    return chart
