import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy

# First some MPG Data Exploration

#@st.cache
df_raw = pd.read_csv("./data/raw/renewable_power_plants_CH.csv")
df = deepcopy(df_raw)


# Add title and header
st.title("Clean Energy Sources in Switzerland")
st.header("Sources per municipality")

# Widgets: checkbox (you can replace st.xx with st.sidebar.xx)
if st.checkbox("Show Dataframe"):
    st.subheader("This is my dataset:")
    st.dataframe(data=df)


# Setting up columns
left_column, right_column = st.columns([3, 1])

# Widgets: selectbox
municipality = ["All"]+sorted(pd.unique(df['municipality']))
canton = left_column.selectbox("Choose a municipality", municipality)



with open("data/gemeinden-geojson.geojson", encoding='utf-8') as response:
    munis = json.load(response)

sources_per_muni = df.groupby("municipality").size().reset_index(name="count")
sources_per_muni.head()


for f in munis['features']:
    f['properties']['gemeinde_NAME'] = f['properties']['gemeinde.NAME']
    del f['properties']['gemeinde.NAME']

fig = px.choropleth_mapbox(
    sources_per_muni,
    color="count",
    geojson=munis,
    locations="municipality",
    featureidkey="properties.gemeinde_NAME",
    center={"lat": 46.8, "lon": 8.3},
    mapbox_style="open-street-map",
    zoom=6.3,
    opacity=0.8,
    width=900,
    height=500,
    labels={"canton_name":"Canton",
            "municipality": "Municipality",
           "count":"Number of Sources"},
    title="<b>Number of Clean Energy Sources per municipality</b>",
    color_continuous_scale="Cividis",
)
fig.update_layout(margin={"r":0,"t":35,"l":0,"b":0},
                  font={"family":"Sans",
                       "color":"maroon"},
                  hoverlabel={"bgcolor":"white",
                              "font_size":12,
                             "font_family":"Sans"},
                  title={"font_size":20,
                        "xanchor":"left", "x":0.01,
                        "yanchor":"bottom", "y":0.95}
                 )

st.plotly_chart(fig)
