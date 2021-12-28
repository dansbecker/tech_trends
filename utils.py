import altair as alt
import pandas as pd
import streamlit as st
from dataclasses import dataclass
from typing import List

alt.themes.enable("fivethirtyeight")
data_path = "data"


@st.cache
def load_dataset(fname: str):
    cols_to_read = ["text", "CommentTime"]
    out = pd.read_parquet(fname, columns=cols_to_read)
    comment_time = pd.to_datetime(out["CommentTime"])
    out["month"] = pd.to_datetime((comment_time + pd.offsets.MonthBegin(1)).dt.date)
    out = out[out.month.dt.year > 2015]
    return out[["text", "month"]]


def make_plot(search_terms: List[str], data: pd.DataFrame, title: str, mobile_friendly_graphs: bool):
    graph_width = 380 if mobile_friendly_graphs else 660
    groups = data.groupby("month")["text"]
    counts = pd.DataFrame(
        {
            term: groups.apply(lambda x: x.str.lower().str.contains(term).sum())
            for term in search_terms
        }
    )
    to_plot = pd.melt(
        counts.reset_index(), id_vars="month", value_vars=search_terms,
    ).rename(columns={"variable": "Technology", "value": "posts"})

    plot = (
        alt.Chart(to_plot)
        .mark_line()
        .encode(
            alt.X("month", title=""), alt.Y("posts", title=""), alt.Color("Technology")
        )
        .properties(width=graph_width, height=400, title=title)
        .configure_legend(titleFontSize=15, labelFontSize=15)
        .configure_title(fontSize=20,)
    )
    return plot


@dataclass
class PlotInfo:
    title: str
    data_fname: pd.DataFrame


plot_info_set = (
    PlotInfo(
        title="Posts in HN Who Is Hiring Threads", data_fname="hiring.parquet"
    ),
    PlotInfo(
        title="Posts in HN Who Wants To Be Hired Threads",
        data_fname="wants_to_be_hired.parquet",
    ),
    PlotInfo(title="Posts in HN Freelancers Threads", data_fname="freelancer.parquet"),
)
