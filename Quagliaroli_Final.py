"""
Name: Andrew Quagliaroli
CS230: Section 4
Data: 'volcanoes.csv'
URL:
Description:
"""
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np


# read in data
def read_data():
    df = pd.read_csv("volcanoes.csv").set_index("Volcano Number")
    return df


def all_countries():
    df = read_data()
    lst = []
    for ind, row in df.iterrows():
        if row['Country'] not in lst:
            lst.append(row['Country'])
    return lst


def all_regions():
    df = read_data()
    lst = []
    for ind, row in df.iterrows():
        if row['Region'] not in lst:
            lst.append(row['Region'])
    return lst


def region_subregion(df):
    lst = []
    for ind, row in df.iterrows():
        if row['Subregion'] not in lst:
            lst.append(row['Subregion'])
    return lst


def subregion_countries(df):
    lst = []
    for ind, row in df.iterrows():
        if row['Country'] not in lst:
            lst.append(row['Country'])
    return lst


def filter_data(df, column_filter, list):
    df = df.loc[df[column_filter].isin(list)]
    return df


# count frequency of countries
def count(col_name, lst, df):
    return [df.loc[df[col_name].isin([n])].shape[0] for n in lst]


def addlabels(x, y):
    for i in range(len(x)):
        plt.text(i, y[i] // 2, y[i], ha='center', fontsize=7.5, color='white', fontweight='bold')


def generate_bar_chart(list_of, graph_of, df, xlabel, ylabel, title):
    value = count(graph_of, list_of, df)
    x_pos = [i for i, _ in enumerate(list_of)]
    plt.bar(x_pos, value, color='firebrick')
    plt.xlabel(xlabel, fontweight='bold', fontsize=14, fontname='monospace')
    plt.ylabel(ylabel, fontweight='bold', fontsize=14, fontname='monospace')
    addlabels(list_of, value)
    plt.title(title, fontweight='bold', fontsize=20, fontname='monospace')
    if len(list_of) <= 3:
        rotation = 0
    elif 3 < len(list_of) <= 6:
        rotation = 45
    elif len(list_of) > 6:
        rotation = 90
    plt.xticks(rotation=rotation, fontsize=6, fontname='monospace')
    plt.xticks(x_pos, list_of)
    return plt


def run_bar_chart_program():
    select_type_barchart = st.sidebar.selectbox(
        'Would you like to compare volcano numbers by region, subregion, or country',
        ('<select>', 'Region', 'Subregion', 'Country'))
    if select_type_barchart == 'Region':
        st.sidebar.write('Please choose regions to explore and compare their data.')
        regions = st.sidebar.multiselect('Select a region: ', all_regions(), )
        df_regions = filter_data(read_data(), 'Region', regions)
        regions_bar_chart = generate_bar_chart(regions, 'Region', df_regions, "Regions", "Number of Volcanoes",
                                               "Frequency of Volcanoes by region")
        st.pyplot(regions_bar_chart)
    elif select_type_barchart == 'Subregion':
        st.sidebar.write('To start, select a region to view its various subregions')
        region = [st.sidebar.selectbox('Select a region: ', all_regions())]
        df_region = filter_data(read_data(), 'Region', region)

        list_subregions_given_region = region_subregion(df_region)
        st.sidebar.write(f'Please select Subregions within {region[0]} to compare volcano numbers')
        subregions = st.sidebar.multiselect('Please Select Subregions:', list_subregions_given_region)
        df_subregions = filter_data(df_region, 'Subregion', subregions)
        subregions_bar_chart = generate_bar_chart(subregions, 'Subregion', df_subregions, 'Subregions',
                                                  'Number of Volcanoes',
                                                  f'Number of Volcanoes by Selected Subregion')
        st.pyplot(subregions_bar_chart)
    elif select_type_barchart == 'Country':
        st.sidebar.write('To start, select a region to view its various subregions')
        region = [st.sidebar.selectbox('Select a region: ', all_regions())]
        df_region = filter_data(read_data(), 'Region', region)

        list_subregions_given_region = region_subregion(df_region)
        st.sidebar.write(f'Please select Subregions within {region[0]} to compare volcano numbers')
        subregions = [st.sidebar.selectbox('Please Select Subregions:', list_subregions_given_region)]
        df_subregions = filter_data(df_region, 'Subregion', subregions)

        list_countries_given_subregion = subregion_countries(df_subregions)
        st.sidebar.write(f'Please select Countries within {subregions[0]} to compare volcano numbers')
        countries = st.sidebar.multiselect('Please Select Countries', list_countries_given_subregion)
        df_countries = filter_data(df_subregions, 'Country', countries)

        countries_bar_chart = generate_bar_chart(countries, 'Country', df_countries,
                                                 'Countries', 'Number of Volcanoes',
                                                 f'Number of Volcanoes by Selected Countries')
        st.pyplot(countries_bar_chart)


def generate_pie_chart(counts, selected_countries):
    plt.figure()
    plt.pie(counts, labels=selected_countries, autopct="%.2f")
    plt.title(f'Volcano Frequency by Country: {", ".join(selected_countries)}')
    return plt


def dates_integers_sorted():
    df = read_data()
    df = df[df['Last Known Eruption'] != "Unknown"]
    df['Last Known Eruption'] = df['Last Known Eruption'].str.split()
    for x in df['Last Known Eruption']:
        if x[1] == "BCE":
            x[0] = -int(x[0])
        elif x[1] == "CE":
            x[0] = int(x[0])
    df = df.sort_values(by=['Last Known Eruption'])
    for x in df['Last Known Eruption']:
        x[0] = abs(x[0])
    df['Last Known Eruption'] = df['Last Known Eruption'].agg(lambda x: ' '.join(map(str, x)))
    return df


def dates_integers():
    df = dates_integers_sorted()
    lst = []
    for ind, row in df.iterrows():
        if row['Last Known Eruption'] not in lst:
            lst.append(row['Last Known Eruption'])
    return lst


def filter_df_by_date():
    df = read_data()
    df = df[df['Last Known Eruption'] != 'Unknown']
    df[['Last Known Eruption Int', 'Era']] = df['Last Known Eruption'].str.split(expand=True)
    df['Last Known Eruption Int'] = pd.to_numeric(df['Last Known Eruption Int'])
    df['Era'] = df['Era'].astype(str)
    for index, row in df.iterrows():
        if row['Era'] == 'BCE':
            df.at[index, 'Last Known Eruption Int'] = -row['Last Known Eruption Int']
    df = df.sort_values(by=['Last Known Eruption Int'])
    lst = []
    for ind, row in df.iterrows():
        if row['Last Known Eruption'] not in lst:
            lst.append(row['Last Known Eruption'])
    slider_time_range = st.sidebar.select_slider('Please Select a range of last known volcano eruptions to '
                                                 'display volcanoes', lst, ['10450 BCE', '2021 CE'])
    list_slider_1 = slider_time_range[0].split()
    list_slider_2 = slider_time_range[1].split()
    if list_slider_1[1] == 'BCE' and list_slider_2[1] == 'BCE':
        beginning_number = -int(list_slider_1[0])
        end_number = -int(list_slider_2[0])
    elif list_slider_1[1] == 'BCE' and list_slider_2[1] == 'CE':
        beginning_number = -int(list_slider_1[0])
        end_number = int(list_slider_2[0])
    elif list_slider_1[1] == 'CE' and list_slider_2[1] == 'CE':
        beginning_number = int(list_slider_1[0])
        end_number = int(list_slider_2[0])
    df.set_index('Last Known Eruption Int')
    df = df[(df['Last Known Eruption Int'] <= end_number) & (df['Last Known Eruption Int'] >= beginning_number)]
    return df


def generate_map(filtered_dataframe):
    df = filtered_dataframe
    fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", hover_name="Volcano Name",
                            hover_data=["Country", "Elevation (m)", "Link"],
                            color="Elevation (m)", zoom=0, height=500, width=850)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    st.plotly_chart(fig)


def streamlit_theme():
    st.set_page_config('Andrew Q. • Python Project', page_icon=":volcano:", initial_sidebar_state='collapsed')
    original_title = '<p style="font-family:Didot; color:#D98880; font-size: 60px;"><b>Visualizing Volcano Data with Python</b></p>'
    st.markdown(original_title, unsafe_allow_html=True)
    subheader = '<p style="font-family:Didot; color:#F2D7D5; font-size: 30px;"><i>by Andrew Quagliaroli</i></p>'
    st.markdown(subheader, unsafe_allow_html=True)
    st.markdown(
        """
    <style>
    .reportview-container {
        background: url("https://imgs.michaels.com/MAM/assets/1/5E3C12034D34434F8A9BAAFDDF0F8E1B/img/C919E20AE7944696A952CF0D5FFD18FF/10594175_1.jpg?fit=inside|1024:1024")
    }
   .sidebar .sidebar-content {
        background: url("https://images.unsplash.com/photo-1619266465172-02a857c3556d?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxleHBsb3JlLWZlZWR8MXx8fGVufDB8fHx8&w=1000&q=80")
    }
    </style>
    """,
        unsafe_allow_html=True
    )


def main():
    streamlit_theme()
    st.sidebar.write('Please choose one of the three data visualization options')
    choose_app = st.sidebar.radio('Please select a data app to run', ['Map', 'Bar Chart', 'Pie Chart'])
    if choose_app == 'Map':
        st.sidebar.subheader('Welcome to the map app.')
        df1 = filter_df_by_date()
        generate_map(df1)
    elif choose_app == 'Bar Chart':
        run_bar_chart_program()
    elif choose_app == 'Pie Chart':
        countries = st.sidebar.multiselect('Select Countries', all_countries())
        st.pyplot(generate_pie_chart(count('Country', countries, read_data()), countries))


main()
