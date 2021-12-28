import altair as alt
import pandas as pd
import streamlit as st

alt.themes.enable('fivethirtyeight')

@st.cache
def load_dataset(fname: str):
    cols_to_read = ['text', 'CommentTime']
    out = pd.read_parquet(fname, columns=cols_to_read)
    comment_time = pd.to_datetime(out['CommentTime'])
    out['month'] = pd.to_datetime((comment_time + pd.offsets.MonthBegin(1)).dt.date)
    out = out[out.month.dt.year >= 2015]
    return out[['text', 'month']]


hiring = load_dataset('./data/hiring.parquet')
wants_to_be_hired = load_dataset('./data/wants_to_be_hired.parquet')
freelancer = load_dataset('./data/freelancer.parquet')

input_1 = st.text_input("First Search Term", value="Kubernetes")
input_2 = st.text_input("Second Search Term", value="CSS")
input_3 = st.text_input("Third Search Term", value="tensorflow")
input_4 = st.text_input("Fourth Search Term", value="")



st.markdown("***")
st.text("\n")
search_terms = [i.lower() for i in (input_1, input_2, input_3, input_4) if len(i.strip())>0]
groups = hiring.groupby('month')['text']
counts = pd.DataFrame({term: groups.apply(lambda x: x.str.lower().str.contains(term).sum()) for term in search_terms})

to_plot = pd.melt(counts.reset_index(), id_vars='month', value_vars=search_terms).rename(
    columns={'variable': 'Technology',
             'value': 'posts'})


plot = alt.Chart(to_plot).mark_line().encode(
    alt.X('month', title=''),
    alt.Y('posts', title=''),
    alt.Color('Technology')
).properties(
    width=620,
    height=400,
    title="Monthly Listings in HN Who Is Hiring Threads"
).configure_legend(
titleFontSize=15,
labelFontSize=15
).configure_title(
    fontSize=20,
)

st.write(plot)