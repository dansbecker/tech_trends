import streamlit as st

from utils import load_dataset, make_plot, plot_info_set
from os.path import join

st.header('Tech Job Posting Trends on HackerNews')
st.write(
'''
HN has monthly threads for job listings, job searchers, and freelancers. This app lets you track trends in these HN threads.
Find interesting trends with this app? Share it with the app author [here](https://twitter.com/dan_s_becker).

\n
'''
)

input_1 = st.text_input("First Search Term", value="Kubernetes")
input_2 = st.text_input("Second Search Term", value="CSS")
input_3 = st.text_input("Third Search Term", value="tensorflow")
input_4 = st.text_input("Fourth Search Term", value="")

mobile_friendly_graphs = st.checkbox(label="Show mobile friendly graphs")

search_terms = [
    i.lower() for i in (input_1, input_2, input_3, input_4) if len(i.strip()) > 0
]

for plot_info in plot_info_set:
    data_path = join("data", plot_info.data_fname)
    data = load_dataset(data_path)
    plot = make_plot(search_terms, data, plot_info.title, mobile_friendly_graphs)
    st.markdown("***")
    st.markdown("\n")
    st.write(plot)
