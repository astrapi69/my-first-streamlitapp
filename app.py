# Streamlit live coding script
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy

# First some MPG Data Exploration
@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df

mpg_df_raw = load_data(path="./data/mpg.csv")
mpg_df = deepcopy(mpg_df_raw)

# Add title and header
st.title("Introduction to Streamlit")
st.header("MPG Data Exploration")

# Introduction Text
st.markdown("""
This app provides an interactive way to explore the fuel efficiency of vehicles, represented through the miles per gallon (MPG) dataset. 
Utilize the widgets to filter the dataset by year, vehicle class, and to visualize the relationship between engine size (displacement) and highway fuel efficiency (MPG).
""")
# Widgets: checkbox (you can replace st.xx with st.sidebar.xx)
if st.checkbox("Show Dataframe"):
    st.subheader("This is my dataset:")
    # Explanation for the dataframe display
    st.markdown("""
    Below are the first few rows of the MPG dataset. This snapshot gives you a glimpse into the dataset's structure, including the various attributes like displacement, year, class, and MPG ratings for highway driving.
    """)
    st.dataframe(data=mpg_df.head())
    st.table(data=mpg_df.head())

st.markdown("""
### Data Filtering

Select a year and vehicle class from the dropdown menus below to filter the dataset accordingly. 
The 'All' option in each dropdown allows you to view the data across all years or classes.
""")
# Setting up columns
left_column, middle_column, right_column = st.columns([3, 1, 1])


# Widgets: selectbox
# years = sorted(pd.unique(mpg_df['year']))
years = ["All"]+sorted(pd.unique(mpg_df['year']))

year = left_column.selectbox("Choose a Year", years)

# Widgets: radio buttons
show_means = middle_column.radio(
    label='Show Class Means', options=['Yes', 'No'])

plot_types = ["Matplotlib", "Plotly"]
plot_type = right_column.radio("Choose Plot Type", plot_types)

# Flow control and plotting
if year == "All":
    reduced_df = mpg_df
else:
    reduced_df = mpg_df[mpg_df["year"] == year]

means = reduced_df.groupby('class').mean(numeric_only=True)

# Widgets: selectbox
# 
vehicle_classes = ["All"] + sorted(pd.unique(mpg_df['class']))
vehicle_class = left_column.selectbox("Choose a Vehicle Class", vehicle_classes)

if vehicle_class != "All":
    reduced_df = reduced_df[reduced_df["class"] == vehicle_class]

st.markdown("""
### Visualization

The charts below showcase the relationship between a vehicle's engine displacement and its highway fuel efficiency. 
You can customize the view by selecting a specific year, vehicle class, and whether to show class means in the plot. 
Choose between Matplotlib and Plotly visualizations to explore the data in different styles.
""")

# In Matplotlib
m_fig, ax = plt.subplots(figsize=(10, 8))
ax.scatter(reduced_df['displ'], reduced_df['hwy'], alpha=0.7)

if show_means == "Yes":
    ax.scatter(means['displ'], means['hwy'], alpha=0.7, color="red")

ax.set_title("Engine Size vs. Highway Fuel Mileage")
ax.set_xlabel('Displacement (Liters)')
ax.set_ylabel('MPG')

# In Plotly
p_fig = px.scatter(reduced_df, x='displ', y='hwy', opacity=0.5,
                   range_x=[1, 8], range_y=[10, 50],
                   width=750, height=600,
                   labels={"displ": "Displacement (Liters)",
                           "hwy": "MPG"},
                   title="Engine Size vs. Highway Fuel Mileage")
p_fig.update_layout(title_font_size=22)

if show_means == "Yes":
    p_fig.add_trace(go.Scatter(x=means['displ'], y=means['hwy'],
                               mode="markers"))
    p_fig.update_layout(showlegend=False)

# Select which plot to show
if plot_type == "Matplotlib":
    st.pyplot(m_fig)
else:
    st.plotly_chart(p_fig)

# We can write stuff
url = "https://archive.ics.uci.edu/ml/datasets/auto+mpg"
st.write("Data Source:", url)
# "This works too:", url

st.header("Geographic Data Visualization")
st.markdown("""
Explore the spatial distribution of car sharing data and unemployment rates across the United States. 
These maps offer a visual representation of geographical data points and statistical information, providing insights into regional trends and distributions.
""")
# Another header
st.header("Maps")
ds_geo = px.data.carshare()
st.dataframe(ds_geo.head())

# Sample Streamlit Map
st.subheader("Streamlit Map")
st.markdown("""
#### Car Sharing Data Overview

The map below displays car sharing data, highlighting the locations of car sharing stations and their usage intensity. 
Each point represents a car sharing station, with its size reflecting the number of cars available. 
This visualization helps identify areas with high or low availability of car sharing services.
""")
ds_geo = px.data.carshare()
ds_geo['lat'] = ds_geo['centroid_lat']
ds_geo['lon'] = ds_geo['centroid_lon']
st.map(ds_geo)

# Sample Choropleth mapbox using Plotly GO
st.subheader("Plotly Map")
st.markdown("""
#### Unemployment Rates by County

The interactive Choropleth map below visualizes unemployment rates across different counties in the United States. 
Hover over a county to see detailed information about its unemployment rate. 
The color gradient represents the range of unemployment rates, with darker colors indicating higher rates. 
This map offers insights into the economic health of various regions and can be used to analyze patterns of unemployment distribution across the country.
""")

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
                 dtype={"fips": str})

plotly_map = go.Figure(go.Choroplethmapbox(geojson=counties,
                                           locations=df.fips,
                                           z=df.unemp,
                                           colorscale="Viridis",
                                           zmin=0, zmax=12,
                                           marker={"opacity": 0.5, "line_width": 0}))
plotly_map.update_layout(mapbox_style="carto-positron",
                         mapbox_zoom=3,
                         mapbox_center={"lat": 37.0902, "lon": -95.7129},
                         margin={"r": 0, "t": 0, "l": 0, "b": 0})

st.plotly_chart(plotly_map)
st.markdown("""
### Insights and Conclusions

Through the interactive exploration of the MPG dataset, we can observe trends such as the impact of engine size on fuel efficiency and how this relationship varies across different vehicle classes and model years. 
Such insights can inform decisions around vehicle design, policy-making regarding fuel efficiency standards, and consumer choices in purchasing vehicles.
""")