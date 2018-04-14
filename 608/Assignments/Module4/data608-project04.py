#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sudo kill $(sudo lsof -t -i:9001)
Created on Sat Nov 18 11:42:40 2017

@author:
        Duubar Villalobos Jimenez  - mydvtech@gmail.com

Project module 04:
    Data608
    CUNY SPS
    Masters in Data Science
    Spring 2018
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, Event
import dash_table_experiments as dt

from datetime import datetime as dtime

from plotly.offline import plot
import plotly.plotly as py
from plotly import graph_objs as go
from plotly.graph_objs import *

import pandas as pd
pd.options.mode.chained_assignment = None  # Pandas Copy Warning default='warn'

"""
################################### D A T A ###################################
"""
url = 'https://raw.githubusercontent.com/dvillalobos/MSDS/master/608/Assignments/Module4/'

# Reading the Riverkeeper Stations
df_stations = pd.read_csv(url+'Riverkeeper_Stations.csv')

# Reading the Riverkeeper Enterococcus levels readings
# data_set = 'riverkeeper_data_2013.csv'  # Original Data Set
data_set = 'EnteroCount2006-2017.csv'     # Updated Dataset
df_readings = pd.read_csv(url + data_set)


"""
################################### C L E A N S I N G #########################
"""
# Need to replace names from the 'MonitoringLocationIdentifier' in order to shortertn their field length.

df_stations['MonitoringLocationIdentifier'] = df_stations['MonitoringLocationIdentifier'].str.replace("RIVERKEEPER-", "")

# Need to define 'MonitoringLocationIdentifier' as categorical data

#df_stations['MonitoringLocationIdentifier'] = df_stations['MonitoringLocationIdentifier'].astype('category')


# Selecting specific columns from the Riverkeeper Station readings to join with our readings data

df_stations = df_stations.loc[:,['OrganizationFormalName',
                                   'MonitoringLocationIdentifier',
                                   'MonitoringLocationName',
                                   'MonitoringLocationTypeName',
                                   'MonitoringLocationDescriptionText',
                                   'HUCEightDigitCode',
                                   'LatitudeMeasure',
                                   'LongitudeMeasure',
                                   'CountryCode',
                                   'StateCode',
                                   'CountyCode']]

# Need to 'update' names in order to match mismatched station names.

df_readings['Site Name'].loc[df_readings['Site Name'] == 'Catskill Creek- First Bridge'] = "Catskill Creeku First Bridge"
df_readings['Site Name'].loc[df_readings['Site Name'] == 'Catskill Creek- East End'] = "Catskill Creeku East End"
df_readings['Site Name'].loc[df_readings['Site Name'] == 'Kingston STP Outfall'] = "Rondout Creek- Kingston STP Outfall"
df_readings['Site Name'].loc[df_readings['Site Name'] == 'Rondout- Kingston Public Dock'] = "Rondout Creek- Kingston Public Dock"
df_readings['Site Name'].loc[df_readings['Site Name'] == 'Rondout- Eddyville Anchorage'] = "Rondout Creek- Eddyville Anchorage"
df_readings['Site Name'].loc[df_readings['Site Name'] == 'Wappingers Creek'] = "Wappingers- New Hamburg"
df_readings['Site Name'].loc[df_readings['Site Name'] == 'Upper Sparkill Creek'] = "Sparkill- Route 340"
df_readings['Site Name'].loc[df_readings['Site Name'] == 'North River STP at 145th'] = "North River STP @145th"
df_readings['Site Name'].loc[df_readings['Site Name'] == 'East River mid-channel at Roosevelt Is.'] = "East River at Roosevelt Island"


#Creating Copy for reporting purposes

df_readings['EnteroCount'] = df_readings['Entero Count']


# Need to take care of inequalities in data

df_readings['EnteroCount'].loc[df_readings['EnteroCount'] == '<1'] = "0"
df_readings['EnteroCount'].loc[df_readings['EnteroCount'] == '<10'] = "5"
df_readings['EnteroCount'].loc[df_readings['EnteroCount'] == '>24196'] = "24200"
df_readings['EnteroCount'].loc[df_readings['EnteroCount'] == '>2420'] = "2425"

# Need to rename Column in order to perform join of data frames.

df_stations = df_stations.rename(index=str, columns={"MonitoringLocationName": "Site Name"})

# Joining/Merging dataframes.

df_readings = pd.merge(df_readings, df_stations, how='left', on=['Site Name'])

# Droping duplicates in order to plot 'active' stations with readings.

current_stations = df_readings.drop_duplicates(subset='MonitoringLocationIdentifier', keep='last')

# Need to define Data Types

df_readings['EnteroCount'] = df_readings['EnteroCount'].astype(int)

df_readings['Date'] = df_readings['Sample Date']

df_readings['Sample Date'] = pd.to_datetime(df_readings['Sample Date'])

# Need to sort by Alphabetically by Site

current_stations = current_stations.sort_values(by='Site Name', ascending=True)

# Need to set MonitoringLocationIdentifier as the index.

df_stations.set_index('MonitoringLocationIdentifier', drop=True, append=False, inplace=True, verify_integrity=False)
current_stations.set_index('MonitoringLocationIdentifier', drop=True, append=False, inplace=True, verify_integrity=False)
df_readings.set_index('MonitoringLocationIdentifier', drop=True, append=False, inplace=True, verify_integrity=False)

# Need to define the index as string

df_stations.index = df_stations.index.map(str)
current_stations.index = current_stations.index.map(str)
df_readings.index = df_readings.index.map(str)


# Need to define safety Calculations
df_readings['Geometric Mean'] =  df_readings['Geometric Mean'].astype(int)
df_readings['Water'] = 'Unsafe'
df_readings['Water'].loc[(df_readings['EnteroCount'] <= 110) & (df_readings['Geometric Mean'] <= 30)] = "Safe"



"""
################################### H E L P E R  F U N C T I O N S ############
"""

# Filter DataFrame by station code

def filter_dataframe(df, station):

    dff = df[df.index == str(station)]

    dff = dff.loc[:,['Sample Date',
                           'EnteroCount',
                           'Entero Count',
                           'Number of Samples',
                           'Geometric Mean',
                           'Site Name',
                           'Water',
                           'Date',
                           '4 Days Total Rain (in)'
                           ]]

    dff = dff.sort_values(by='Sample Date', ascending=False)

    return(dff)




# Subsetting columns for data table initialization

def create_subset_dataframe(df_readings, station):

    stations = filter_dataframe(df_readings, station)

    stations = stations.loc[:,['Sample Date',
                               'EnteroCount',
                               'Entero Count',
                               'Geometric Mean',
                               'Site Name',
                               'Water',
                               'Date'
                               #'FourDayRainTotal'
                               ]]
    stations = stations.sort_values(by='Sample Date', ascending=False)

    return(stations)


# Subsetting columns for data table initialization

def create_subset_dataframe_table(df_readings, station):

    #df_readings['Geometric Mean'] =  df_readings['Geometric Mean'].astype(int)

    #df_readings['Water'] = 'Unsafe'
    #df_readings['Water'].loc[(df_readings['Geometric Mean'] <= 30) & (df_readings['EnteroCount'] <= 110)] = "Safe"


    stations = filter_dataframe(df_readings, station)

    stations = stations.loc[:,['Sample Date',
                               'Entero Count',
                               'Geometric Mean',
                               'Water'
                               #'FourDayRainTotal'
                               ]]
    stations = stations.sort_values(by='Sample Date', ascending=False)

    return(stations.to_dict('records'))


# Subsetting columns for data table initialization

def create_subset_dataframe_table_by_date(df_readings, date):

    df_readings['Geometric Mean'] =  df_readings['Geometric Mean'].astype(int)

    df_readings['Water'] = 'Unsafe'
    df_readings['Water'].loc[(df_readings['Geometric Mean'] <= 30) & (df_readings['EnteroCount'] <= 110)] = "Safe"


    stations = df_readings[df_readings['Sample Date'] == date]

    stations = stations.sort_values(by='EnteroCount', ascending=False)

    stations = stations.loc[:,['Site Name',
                               'EnteroCount',
                               'Geometric Mean',
                               'Water'
                               #'Entero Count'
                               ]]

    return(stations)



# Subsetting columns for data table initialization with 4 day Rain

def create_subset_dataframe_table_by_correlation(df_readings, station):

    df_readings['4 Days Total Rain (in)'] =  df_readings['4 Days Total Rain (in)'].astype(float)

    #stations = filter_dataframe(df_readings, station)
    stations = df_readings[df_readings.index == str(station)]

    stations = stations.sort_values(by='Sample Date', ascending=False)

    stations = stations.loc[:,['Sample Date',
                               'EnteroCount',
                               '4 Days Total Rain (in)',
                               'Water'
                               #'Entero Count'
                               ]]

    return(stations.to_dict('records'))



# Create a map display with Stations on it

def stations_map(df_stations):
    # Mapbox
    #mapbox_access_token = 'pk.eyJ1IjoiYWxpc2hvYmVpcmkiLCJhIjoiY2ozYnM3YTUxMDAxeDMzcGNjbmZyMmplZiJ9.ZjmQ0C2MNs1AzEBC_Syadg'
    mapbox_access_token = 'pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w' # noqa: E501

    # Global options

    zoom = 6.5
    latInitial = 41.60242
    lonInitial = -73.96115
    bearing = 0

    # Map figure
    figure = go.Figure(
        data=Data([
            Scattermapbox(
                lat=df_stations['LatitudeMeasure'],
                lon=df_stations['LongitudeMeasure'],
                customdata=df_stations.index,
                mode='markers',
                hoverinfo="text",
                text='Station: [ ' + df_stations.index + ' ] - ' + df_stations['Site Name']
            ),
        ]),
        layout=Layout(
            autosize=True,
            height=550,
            margin=Margin(l=0, r=0, t=0, b=0),
            showlegend=False,
            font=dict(color='#CCCCCC'),
            titlefont=dict(color='#CCCCCC', size='14'),
            hovermode='closest',
            plot_bgcolor='#191A1A',
            paper_bgcolor='#020202',
            legend=dict(font=dict(size=10), orientation='h'),
            title='Satellite Overview',
            mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(
                    lat=latInitial, # 40.7272
                    lon=lonInitial # -73.991251
                ),
                style='dark',
                bearing=bearing,
                zoom=zoom
            ),
            updatemenus=[
                dict(
                    buttons=([
                        dict(
                            args=[{
                                    'mapbox.zoom': 6.5,
                                    'mapbox.center.lon': lonInitial, # '-73.991251',
                                    'mapbox.center.lat': latInitial, # '40.7272',
                                    'mapbox.bearing': 0,
                                    'mapbox.style': 'dark'
                                }],
                            label='Reset Zoom',
                            method='relayout'
                        )
                    ]),
                    direction='left',
                    pad={'r': 0, 't': 0, 'b': 0, 'l': 0},
                    showactive=False,
                    type='buttons',
                    x=0.45,
                    xanchor='left',
                    yanchor='bottom',
                    bgcolor='#323130',
                    borderwidth=1,
                    bordercolor="#6d6d6d",
                    font=dict(
                        color="#FFFFFF"
                    ),
                    y=0.02
                ),
                dict(
                    buttons=([
                        dict(
                            args=[{
                                    'mapbox.zoom': 10,
                                    'mapbox.center.lon': '-73.74802',
                                    'mapbox.center.lat': '42.64242',
                                    'mapbox.bearing': 0,
                                    'mapbox.style': 'dark'
                                }],
                            label='Albany',
                            method='relayout'
                        ),
                        dict(
                            args=[{
                                    'mapbox.zoom': 9,
                                    'mapbox.center.lon': '-73.867',
                                    'mapbox.center.lat': '42.2169',
                                    'mapbox.bearing': 0,
                                    'mapbox.style': 'dark'
                                }],
                            label='Catskill',
                            method='relayout'
                        ),
                        dict(
                            args=[{
                                    'mapbox.zoom': 9,
                                    'mapbox.center.lon': '-73.94202',
                                    'mapbox.center.lat': '41.72289',
                                    'mapbox.bearing': 0,
                                    'mapbox.style': 'dark'
                                }],
                            label='Poughkeepsie',
                            method='relayout'
                        ),
                        dict(
                            args=[{
                                    'mapbox.zoom': 10,
                                    'mapbox.center.lon': '-73.965',
                                    'mapbox.center.lat': '41.2417',
                                    'mapbox.bearing': 0,
                                    'mapbox.style': 'dark'
                                }],
                            label='Stony Point',
                            method='relayout'
                        ),
                        dict(
                            args=[{
                                    'mapbox.zoom': 10,
                                    'mapbox.center.lon': '-73.91435',
                                    'mapbox.center.lat': '41.08838',
                                    'mapbox.bearing': 0,
                                    'mapbox.style': 'dark'
                                }],
                            label='Tarrytown',
                            method='relayout'
                        ),
                        dict(
                            args=[{
                                    'mapbox.zoom': 11,
                                    'mapbox.center.lon': '-73.95001',
                                    'mapbox.center.lat': '40.84838',
                                    'mapbox.bearing': 0,
                                    'mapbox.style': 'dark'
                                }],
                            label='GWB',
                            method='relayout'
                        ),
                        dict(
                            args=[{
                                    'mapbox.zoom': 10,
                                    'mapbox.center.lon': '-74.02237',
                                    'mapbox.center.lat': '40.74351',
                                    'mapbox.bearing': 0,
                                    'mapbox.style': 'dark'
                                }],
                            label='East River',
                            method='relayout'
                        )
                    ]),
                    direction="down",
                    pad={'r': 0, 't': 0, 'b': 0, 'l': 0},
                    showactive=False,
                    bgcolor="rgb(50, 49, 48, 0)",
                    type='buttons',
                    yanchor='bottom',
                    xanchor='left',
                    font=dict(
                        color="#FFFFFF"
                    ),
                    x=0,
                    y=0.05
                )
            ]
        )
    )
    return(figure)






# Create a time series
def time_series(stations):

    color = [{'Unsafe': 'Red', 'Safe': 'Green'}]

    df_color = pd.DataFrame(color)

    #stations['Geometric Mean'] =  stations['Geometric Mean'].astype(int)

    #stations['Water'] = 'Unsafe'
    #stations['Water'].loc[(stations['Geometric Mean'] <= 30) & (stations['EnteroCount'] <= 110)] = "Safe"


    figure = go.Figure(
        data=Data([
            Scatter(
                    #x=df[df['continent'] == i]['gdp per capita'],
                    x=stations[stations['Water'] == i]['Sample Date'],
                    y=stations[stations['Water'] == i]['EnteroCount'],
                    hoverinfo="text",
                    text='Date: '+ stations[stations['Water'] == i]['Date'] + '<br>Count = ' + stations[stations['Water'] == i]['Entero Count'] + '<br>Recomendation: ' + stations[stations['Water'] == i]['Water'] + ' to Swim',
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'},
                        'color': df_color[i][0]
                    },
                    name=i
                ) for i in stations['Water'].unique()
            #    ),
        ]),
        layout=Layout(
            autosize=True,
            height=450,
            title='Station: ' + stations['Site Name'][0:1][0],
            xaxis={'title': 'Date'},
            yaxis={'title': 'Enterococcus Count'},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    )
    return(figure)


# Create a Station readings Count series
def station_counts_series(stations):

    color = [{'Unsafe': 'Red', 'Safe': 'Green'}]

    df_color = pd.DataFrame(color)

    stations['Water'] = 'Unsafe'
    stations['Water'].loc[(stations['EnteroCount'] <= 110)] = 'Safe' #& (stations['Geometric Mean'] <= 30)] = "Safe"

    figure = go.Figure(
        data=Data([
            Scatter(
                    #x=df[df['continent'] == i]['gdp per capita'],
                    x=stations[stations['Water'] == i]['EnteroCount'],
                    y=stations[stations['Water'] == i]['Site Name'],
                    hoverinfo="text",
                    text='Date: '+ stations[stations['Water'] == i]['Date'] + '<br>Count = ' + stations[stations['Water'] == i]['Entero Count'], #+ ' it is ' + stations[stations['Water'] == i]['Water'] + ' to Swim',
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'},
                        'color': df_color[i][0]
                    },
                    name=i
                ) for i in stations['Water'].unique()
            #    ),
        ]),
        layout=Layout(
            autosize=True,
            height=1750,
            title="Station's Enterococcus Counts (log scale)",
            xaxis={'title': 'Enterococcus Counts', 'type':'log'},
            yaxis={'title': ''},
            # Line Vertical
            shapes=[{
            'type': 'line',
            'x0': 110,
            'y0': -1,
            'x1': 110,
            'y1': 75,
            'line': {
                'color': 'red',
                'width': 2,
            }}],
            margin={'r': 0, 't': 50, 'b': 40, 'l': 240},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    )
    return(figure)

# Create a Station Geometric Mean readings series
def station_gm_series(stations):

    color = [{'Unsafe': 'Red', 'Safe': 'Green'}]

    df_color = pd.DataFrame(color)

    stations['Geometric Mean'] =  stations['Geometric Mean'].astype(int)

    stations['Water'] = 'Unsafe'
    stations['Water'].loc[(stations['Geometric Mean'] <= 30)] = 'Safe' #& (stations['EnteroCount'] <= 110)] = "Safe"

    stations['Geometric Mean'] =  stations['Geometric Mean'].astype(str)

    figure = go.Figure(
        data=Data([
            Scatter(
                    #x=df[df['continent'] == i]['gdp per capita'],
                    x=stations[stations['Water'] == i]['Geometric Mean'],
                    y=stations[stations['Water'] == i]['Site Name'],
                    hoverinfo="text",
                    text='<br>Geometric Mean = ' + stations[stations['Water'] == i]['Geometric Mean'] + '<br>Recommendation: ' + stations[stations['Water'] == i]['Water'] + ' to Swim',
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'},
                        'color': df_color[i][0]
                    },
                    name=i
                ) for i in stations['Water'].unique()
            #    ),
        ]),
        layout=Layout(
            autosize=True,
            height=1750,
            title="Station's Geometric Mean",
            xaxis={'title': 'Geometric Mean'},
            yaxis={'title': ''},
            # Line Vertical
            shapes=[{
            'type': 'line',
            'x0': 30,
            'y0': -1,
            'x1': 30,
            'y1': 75,
            'line': {
                'color': 'red',
                'width': 2,
            }}],
            margin={'r': 0, 't': 50, 'b': 40, 'l': 240},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    )
    return(figure)


# Create a Station Geometric Mean readings series
def station_combined_count_gm_series(stations):

    color = [{'Unsafe': 'Red', 'Safe': 'Green'}]

    df_color = pd.DataFrame(color)

    stations['Geometric Mean'] =  stations['Geometric Mean'].astype(int)

    stations['Water'] = 'Unsafe'
    stations['Water'].loc[(stations['Geometric Mean'] <= 30) & (stations['EnteroCount'] <= 110)] = "Safe"

    stations['Geometric Mean'] =  stations['Geometric Mean'].astype(str)

    figure = go.Figure(
        data=Data([
            Scatter(
                    #x=df[df['continent'] == i]['gdp per capita'],
                    x=stations[stations['Water'] == i]['EnteroCount'],
                    y=stations[stations['Water'] == i]['Site Name'],
                    hoverinfo="text",
                    text='Date: '+ stations[stations['Water'] == i]['Date'] + '<br>Count = ' + stations[stations['Water'] == i]['Entero Count'] + '<br>Geometric Mean = ' + stations[stations['Water'] == i]['Geometric Mean'] + '<br>Recommendation: ' + stations[stations['Water'] == i]['Water'] + ' to Swim',
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'},
                        'color': df_color[i][0]
                    },
                    name=i
                ) for i in stations['Water'].unique()
            #    ),
        ]),
        layout=Layout(
            autosize=True,
            height=1750,
            title="Station's Counts & Geometric Means (log scale)",
            xaxis={'title': 'Geometric Mean', 'type':'log'},
            yaxis={'title': ''},
            # Line Vertical
            shapes=[{
            'type': 'line',
            'x0': 110,
            'y0': -1,
            'x1': 110,
            'y1': 75,
            'line': {
                'color': 'red',
                'width': 2,
            }}],
            margin={'r': 0, 't': 50, 'b': 40, 'l': 240},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    )
    return(figure)


def stations_map_by_safety(readings, picked_date):

    readings = readings[readings['Sample Date'] == picked_date]

    #    if (len(df_readings) == 0):{ }

    color = [{'Unsafe': 'Red', 'Safe': 'Green'}]

    df_color = pd.DataFrame(color)

    readings['Geometric Mean'] =  readings['Geometric Mean'].astype(int)

    readings['Water'] = 'Unsafe'
    readings['Water'].loc[(readings['Geometric Mean'] <= 30) & (readings['EnteroCount'] <= 110)] = "Safe"


    # Mapbox
    mapbox_access_token = 'pk.eyJ1IjoiYWxpc2hvYmVpcmkiLCJhIjoiY2ozYnM3YTUxMDAxeDMzcGNjbmZyMmplZiJ9.ZjmQ0C2MNs1AzEBC_Syadg'

    # Global options

    zoom = 6.5
    latInitial = 41.60242
    lonInitial = -73.96115
    bearing = 0

    # Map figure
    figure = go.Figure(
        data=Data([
            Scattermapbox(
                lat=readings[readings['Water'] == i]['LatitudeMeasure'],
                lon=readings[readings['Water'] == i]['LongitudeMeasure'],
                customdata=readings[readings['Water'] == i].index,
                mode='markers',
                hoverinfo="text",
                text='Station: [ ' + readings[readings['Water'] == i].index + ' ] - ' + readings[readings['Water'] == i]['Site Name'],
                marker={
                        'size': 15,
                        'color': df_color[i][0]
                    },
                    name=i
                ) for i in readings['Water'].unique()
        #    ),
        ]),
        layout=Layout(
            autosize=True,
            height=550,
            margin=Margin(l=0, r=0, t=0, b=0),
            showlegend=False,
            font=dict(color='#CCCCCC'),
            titlefont=dict(color='#CCCCCC', size='14'),
            hovermode='closest',
            plot_bgcolor='#191A1A',
            paper_bgcolor='#020202',
            legend=dict(font=dict(size=10), orientation='h'),
            title='Satellite Overview',
            mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(
                    lat=latInitial, # 40.7272
                    lon=lonInitial # -73.991251
                ),
                style='dark',
                bearing=bearing,
                zoom=zoom
            ),
            updatemenus=[
                dict(
                    buttons=([
                        dict(
                            args=[{
                                    'mapbox.zoom': 6.5,
                                    'mapbox.center.lon': lonInitial, # '-73.991251',
                                    'mapbox.center.lat': latInitial, # '40.7272',
                                    'mapbox.bearing': 0,
                                    'mapbox.style': 'dark'
                                }],
                            label='Reset Zoom',
                            method='relayout'
                        )
                    ]),
                    direction='left',
                    pad={'r': 0, 't': 0, 'b': 0, 'l': 0},
                    showactive=False,
                    type='buttons',
                    x=0.45,
                    xanchor='left',
                    yanchor='bottom',
                    bgcolor='#323130',
                    borderwidth=1,
                    bordercolor="#6d6d6d",
                    font=dict(
                        color="#FFFFFF"
                    ),
                    y=0.02
                ),
                dict(
                    buttons=([
                        dict(
                            args=[{
                                    'mapbox.zoom': 10,
                                    'mapbox.center.lon': '-73.74802',
                                    'mapbox.center.lat': '42.64242',
                                    'mapbox.bearing': 0,
                                    'mapbox.style': 'dark'
                                }],
                            label='Albany',
                            method='relayout'
                        ),
                        dict(
                            args=[{
                                    'mapbox.zoom': 9,
                                    'mapbox.center.lon': '-73.867',
                                    'mapbox.center.lat': '42.2169',
                                    'mapbox.bearing': 0,
                                    'mapbox.style': 'dark'
                                }],
                            label='Catskill',
                            method='relayout'
                        ),
                        dict(
                            args=[{
                                    'mapbox.zoom': 9,
                                    'mapbox.center.lon': '-73.94202',
                                    'mapbox.center.lat': '41.72289',
                                    'mapbox.bearing': 0,
                                    'mapbox.style': 'dark'
                                }],
                            label='Poughkeepsie',
                            method='relayout'
                        ),
                        dict(
                            args=[{
                                    'mapbox.zoom': 10,
                                    'mapbox.center.lon': '-73.965',
                                    'mapbox.center.lat': '41.2417',
                                    'mapbox.bearing': 0,
                                    'mapbox.style': 'dark'
                                }],
                            label='Stony Point',
                            method='relayout'
                        ),
                        dict(
                            args=[{
                                    'mapbox.zoom': 10,
                                    'mapbox.center.lon': '-73.91435',
                                    'mapbox.center.lat': '41.08838',
                                    'mapbox.bearing': 0,
                                    'mapbox.style': 'dark'
                                }],
                            label='Tarrytown',
                            method='relayout'
                        ),
                        dict(
                            args=[{
                                    'mapbox.zoom': 11,
                                    'mapbox.center.lon': '-73.95001',
                                    'mapbox.center.lat': '40.84838',
                                    'mapbox.bearing': 0,
                                    'mapbox.style': 'dark'
                                }],
                            label='GWB',
                            method='relayout'
                        ),
                        dict(
                            args=[{
                                    'mapbox.zoom': 10,
                                    'mapbox.center.lon': '-74.02237',
                                    'mapbox.center.lat': '40.74351',
                                    'mapbox.bearing': 0,
                                    'mapbox.style': 'dark'
                                }],
                            label='East River',
                            method='relayout'
                        )
                    ]),
                    direction="down",
                    pad={'r': 0, 't': 0, 'b': 0, 'l': 0},
                    showactive=False,
                    bgcolor="rgb(50, 49, 48, 0)",
                    type='buttons',
                    yanchor='bottom',
                    xanchor='left',
                    font=dict(
                        color="#FFFFFF"
                    ),
                    x=0,
                    y=0.05
                )
            ]
        )
    )
    return(figure)

# Function that reurns the most recent Sample Date

def return_recent_date(df_readings):
    df_readings = df_readings.sort_values(by='Sample Date', ascending=False)
    recent_date = df_readings['Sample Date'][0]
    recent_date = pd.Timestamp(recent_date)
    recent_date = str(recent_date.month) + '-' + str(recent_date.day) + '-' +  str(recent_date.year)
    return(recent_date)


# Function that return an horizontal bar chart

def date_chart_h(df_readings, date):

    #date = '10-15-2017'
    #picked_date = "2017-10-19"
    #picked_date = dtime.now()
    #picked_date = dtime.date(picked_date)
    date = pd.Timestamp(date)
    date = '{:%m-%d-%Y}'.format(date) # str(date.year) + '-' + str(date.month) + '-' + str(date.day)
    date = pd.Timestamp(date)

    df_readings = create_subset_dataframe_table_by_date(df_readings, date)

    #color = [{'Unsafe': 'Red', 'Safe': 'Green'}]

    #df_color = pd.DataFrame(color)

    data = [
        go.Bar(
            x = df_readings[df_readings['Water'] == 'Unsafe']['EnteroCount'],
            y = df_readings[df_readings['Water'] == 'Unsafe']['Site Name'],
            orientation = 'h',
            marker = dict(
              color = 'Red'
            ),
            name = 'Unsafe'
        ),
        go.Bar(
            x = df_readings[df_readings['Water'] == 'Safe']['EnteroCount'],
            y = df_readings[df_readings['Water'] == 'Safe']['Site Name'],
            orientation = 'h',
            marker = dict(
              color = 'Green'
            ),
            name = 'Safe'
        )
    ]

    layout = go.Layout(
        title='Safe & Unsafe swiming areas on ' +  str(date.month) + '-' + str(date.day) + '-' + str(date.year),
        margin={'r': 0, 't': 50, 'b': 40, 'l': 240},
        xaxis={'title': 'Enterococcus Count'},
        yaxis={'title': ''},
        height=450,
    )

    figure = go.Figure(data=data, layout=layout)

    return(figure)

    #import plotly
    #plot_me = plotly.offline.plot(figure,auto_open=True)


# Calculate Statistical Threshold Value
def calculate_STV(readings):

    #readings = df_readings

    readings['Water'] = 'Unsafe'
    readings['Water'].loc[(readings['EnteroCount'] < 110) ] = "Safe"

    # Subset of data
    readings = readings.loc[:,['Site Name',
                               'Water'
                               #'FourDayRainTotal'
                           ]]

    readings = readings.groupby(['Site Name', 'Water'])[['Water']].count()

    readings = readings.rename(columns={"Water": "Count"})

    readings = readings.reset_index(level=['Site Name','Water'])

    readings = readings.pivot(index='Site Name', columns='Water', values='Count')

    readings = readings.reset_index(level=['Site Name'])

    readings.fillna(0,  inplace=True)

    readings['Total'] = readings['Safe'] + readings['Unsafe']

    readings['Safe %'] = round(readings['Safe'] /  readings['Total'] * 100,0)

    readings['Unsafe %'] = round(readings['Unsafe'] /  readings['Total'] * 100,0)

    readings['Safe %'] = readings['Safe %'].astype(int)

    readings['Insafe %'] = readings['Unsafe %'].astype(int)

    readings['Recommendation'] = "Safe"

    readings['Recommendation'].loc[(readings['Unsafe %'] >= 10) ] = "Unsafe"

    return(readings)


# Function that return an horizontal bar chart for the Statistical Treshold Value

def date_chart_STV_h(stations):

    #readings = df_readings
    #color = [{'Unsafe': 'Red', 'Safe': 'Green'}]

    #df_color = pd.DataFrame(color)

    readings = calculate_STV(stations)

    data = [
        go.Bar(
            x = readings['Unsafe %'],
            y = readings['Site Name'],
            orientation = 'h',
            marker = dict(
              color = 'Red'
            ),
            name = 'Unsafe'
        ),
        go.Bar(
            x = readings['Safe %'],
            y = readings['Site Name'],
            orientation = 'h',
            marker = dict(
              color = 'Green'
            ),
            name = 'Safe'
        )
    ]

    layout = go.Layout(
        title='Safe & Unsafe swiming areas based on Statistical Treshold Value',
        margin={'r': 0, 't': 50, 'b': 40, 'l': 240},
        xaxis={'title': 'Percentage of Readings'},
        yaxis={'title': ''},
        # Line Vertical
        shapes=[{
            'type': 'line',
            'x0': 10,
            'y0': -1,
            'x1': 10,
            'y1': 75,
            'line': {
                'color': 'red',
                'width': 2,
            }}],
        barmode='stack',
        height=1750,

    )

    figure = go.Figure(data=data, layout=layout)

    return(figure)

    #import plotly
    #plot_me = plotly.offline.plot(figure,auto_open=True)


# Function that return a vertical correlation bar chart

def date_chart_correlation(df_readings, station):

    df_readings['4 Days Total Rain (in)'] =  df_readings['4 Days Total Rain (in)'].astype(float)
    #station = '0'
    #stations = filter_dataframe(df_readings, station)
    stations = df_readings[df_readings.index == str(station)]

    stations = stations.sort_values(by='Sample Date', ascending=False)

    stations = stations.loc[:,['Site Name',
                               'Sample Date',
                               'EnteroCount',
                               '4 Days Total Rain (in)',
                               'Water',
                               'Entero Count'
                               ]]

    correlation = stations['EnteroCount'].corr(stations['4 Days Total Rain (in)'])

    #color = [{'Unsafe': 'Red', 'Safe': 'Green'}]

    #df_color = pd.DataFrame(color)

    data = [
        go.Scatter(
            x = stations[stations['Water'] == 'Unsafe']['Sample Date'],
            y = stations[stations['Water'] == 'Unsafe']['EnteroCount'],
            #orientation = 'v',
            marker = dict(
              color = 'Red',
              symbol = 'x'
            ),
            mode = 'markers',
            name = 'Unsafe'
        ),
        go.Scatter(
            x = stations[stations['Water'] == 'Safe']['Sample Date'],
            y = stations[stations['Water'] == 'Safe']['EnteroCount'],
            #orientation = 'v',
            marker = dict(
              color = 'Green',
              symbol = 'x'
            ),
            mode = 'markers',
            name = 'Safe'
        ),
        go.Scatter(
            x = stations['Sample Date'],
            y = stations['4 Days Total Rain (in)'],
            marker = dict(
              color = 'blue',
              symbol = 'x'
            ),
            mode = 'markers',
            name = '4 Days Total Rain (in)'
        )

    ]

    layout = go.Layout(
        title='Station: ' + stations['Site Name'].unique()[0] + "<br>Correlation for the last '4 Days Total Rain (in)' vs 'Enteroccocus' is: " + str(round(correlation,4)),
        margin={'r': 0, 't': 50, 'b': 40, 'l': 50},
        xaxis={'title': 'Sample Date'},
        yaxis={'title': 'Enteroccocus Count', 'type':'log'},
        height=450,
    )

    figure = go.Figure(data=data, layout=layout)

    return(figure)



"""
################################### D A S H  L A Y O U T ######################
"""
app = dash.Dash()

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

background_text = '''
                 Enterococcus is a fecal indicating bacteria that lives in the
                 intestines of humans and other warm-blooded animals. Enterococcus (“Entero”)
                 counts are useful as a water quality indicator due to their abundance in human
                 sewage, correlation with many human pathogens and low abundance in sewage free
                 environments. The United States Environmental Protection Agency (EPA) reports
                 Entero counts as colonies (or cells) per 100 ml of water.
                 >>
                 Riverkeeper has based its assessment of acceptable water quality on the 2012
                 Federal Recreational Water Quality Criteria from the US EPA. Unacceptable water
                 is based on an illness rate of 32 per 1000 swimmers.
                 >>
                 The federal standard for unacceptable water quality is a single sample
                 value of greater than 110 Enterococcus/100 mL, or five or more samples
                 with a geometric mean (a weighted average) greater than 30 Enterococcus/100 mL.
                 >>
                 Data provided by the [Riverkeeper](http://www.riverkeeper.org).

    '''
#https://www.riverkeeper.org/water-quality/hudson-river/
#https://www.riverkeeper.org/wp-content/uploads/2017/11/Riverkeeper_WQReport_2017_final-1.pdf
project_text = '''
                 To create an app prototype that allows an user to pick a date, and will give its
                 recommendations for that particular date and provide some information
                 explaining why a particular site is flagged as unsafe.
    '''

instructions_text = '''
                 **HOVER** over a station in the graph to see the readings.
                 >>
                 **SELECT** a date from the date picker to visualize the readings of the stations for that single day.
                 >>
                 **COLOR CODES** for the most part, I have decided to denote as follows:
                     + **Red:** Unsafe to Swim
                     + **Green:** Safe to Swim
                >>
                **When is considered safe to swim?** (Green) otherwise Unsafe (Red).
                    + If the **EnteroCount** <= 110
                    + If the **Geometric Mean** <= 30
                    + If the **Statistical Threshold Value** < 10%:

                If the number of samples that exceed 110 is equal or more than 10%; the
                water is not considered safe for swimming due the frequency of contamination
                events, even if "average" levels are low.
    '''

created_by_text = '''
        Duubar Villalobos Jimenez

        CUNY MSDS

        DATA 608

        Project 4

        Spring 2018

        [mydvtech@gmail.com](mailto:mydvtech@gmail.com)
    '''

# Describe the layout
app.layout = html.Div(children=[


    # Header Row
    html.Div([
            html.Img(src="https://www.riverkeeper.org/wp-content/uploads/2010/03/new_logo_500-450x116.gif"),
            html.H2(children="Riverkeeper's Enterococcus Data App", style={'font-family': 'Dosis',
                                                                                'textAlign': 'center',
                                                                                'position': 'relative',
                                                                                'left': '5px'}),
    ], className='banner'),


    # Text Descriptions
    html.Div([
            # Backgound Row
         html.Div([
                html.H1(children="Background:"),
            ], className='Title'),

        # Background Description Row
        html.Div([
            dcc.Markdown(children=background_text.replace('  ', ''), className='eight columns offset-by-two'),
        ], className='row', style={'text-align': 'left', 'margin-bottom': '15px'}),

        # Project Row
        html.Div([
            html.H1(children="Project:"),
        ], className='Title'),

         # Project Description Row
        html.Div([
            dcc.Markdown(children=project_text.replace('  ', ''), className='eight columns offset-by-two'),
        ], className='row', style={'text-align': 'left', 'margin-bottom': '15px'}),



        # App Row
        html.Div([
                html.H1(children="App:"),
        ], className='Title'),

        # App Instructions
        html.Div([
                html.H3(children="Instructions"),
        ]),

         # App instructions description
        html.Div([
            dcc.Markdown(children=instructions_text.replace('  ', ''), className='eight columns offset-by-two'),
        ], className='row', style={'text-align': 'left', 'margin-bottom': '15px'}),

    ], style={'padding': '0px 10px 15px 10px',
    'marginLeft': 'auto', 'marginRight': 'auto', "width": "900px",
    'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'}),


    # Main Charts display area
    html.Div([

        # Chart type options
        html.Div([
                html.H3(children="Chart type"),
        ]),

        # Radio button selector
        dcc.RadioItems(id='chart-type-selector',
            options=[
                {'label': 'Counts Only', 'value': 'counts'},
                {'label': 'Geometric Mean Only', 'value': 'gmean'},
                {'label': 'Combined', 'value': 'combined'},
                {'label': 'Statistical Threshold Value', 'value': 'STV'}
            ],
            value='counts',
           labelStyle={'display': 'inline-block'}
        ),


        html.Div(
            [
                dcc.Graph(id='main-chart-types', figure=station_counts_series(df_readings)),
            ],
            className='twelve columns',
            style={'margin-top': '20'}
        ),

    ], className='row', style={'padding': '0px 10px 15px 10px',
    'marginLeft': 'auto', 'marginRight': 'auto', "width": "900px",
    'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'}),




    html.Div([
        # Main Graphs section
        html.Div([

            # By Location
            html.Div([
                    html.H1(children="Exploring by Location"),
            ], className='Title'),

            html.H3(id='selected-station-id', children="The selected station ID is 0"),

            html.H4(id='selected-station-name', children="Location: The Battery mid-channel"),


            # Riverkeeper's Stations Map and Table
            html.Div([
                # Riverkeeper's Sations Map
                html.Div(
                    [
                        dcc.Graph(id='main_graph', figure=stations_map(current_stations)),
                    ],
                    className='ten columns offset-by-one',
                    style={'margin-top': '20'}
                ),


            ],className='row'),


            # Riverkeeper's Readings Graphs
            html.Div([
                # Riverkeeper's Stations Time Series
                html.Div(
                    [
                        dcc.Graph(id='station-time-series', figure=time_series(create_subset_dataframe(df_readings, '0'))),
                    ],
                    className='twelve columns',
                    style={'margin-top': '20'}
                ),
            ],className='row'),

        ]),
    ], style={'padding': '0px 10px 15px 10px',
    'marginLeft': 'auto', 'marginRight': 'auto', "width": "900px",
    'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'}),




    html.Div([
        # Graphs section by Date
        html.Div([

            # By Date
            html.Div([
                    html.H1(children="Exploring by Date"),
            ], className='Title'),

            html.H3(id='most-recent-date', children="The most recent Sample's Date was {}".format(return_recent_date(df_readings))),


            html.H3(id='selected-date', children=""),

            # Date picker
            html.Div(
                [   html.P('Pick your Choice:'),
                    dcc.DatePickerSingle(
                        id='date-picker',
                        date=return_recent_date(df_readings),
                    ),
                ],className='row'),

            # Riverkeeper's Stations Map and Table
            html.Div([
                # Riverkeeper's Sations Map
                html.Div(
                    [
                        dcc.Graph(id='main_date_map_graph', figure=stations_map_by_safety(df_readings, return_recent_date(df_readings) )),
                    ],
                    className='five columns',
                    style={'margin-top': '20'}
                ),
                #Riverkeeper's Station's Readings Table
                html.Div(
                    [
                        dt.DataTable(
                            id='table_recomended',
                            # Initialise the rows
                            #rows=[{}],
                            rows=create_subset_dataframe_table(df_readings, '0'),
                            row_selectable=False,
                            filterable=True,
                            sortable=True,
                            min_height=500,
                            editable=False,
                            #selected_row_indices=[],
                        )
                    ],
                    className='seven columns',
                    style={'margin-top': '20'}
                ),
            ],className='row'),

            # Riverkeeper's Stations Charts
            html.Div([
                # Riverkeeper's Sations Map
                html.Div(
                    [
                        dcc.Graph(id='stations-results-chart', figure=date_chart_h(df_readings, return_recent_date(df_readings))),
                    ],
                    className='twelve columns',
                    style={'margin-top': '20'}
                ),

            ],className='row'),


        ]),
    ], style={'padding': '0px 10px 15px 10px',
    'marginLeft': 'auto', 'marginRight': 'auto', "width": "900px",
    'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'}),


    # Main Charts rain and water quality area
    html.Div([

                # Rain vs Water Quality
                html.Div([
                        html.H3(children="Exploring Rain vs Water Quality"),
                ]),

                html.H4(id='selected-station-correlation-name', children="Location: The Battery mid-channel"),

                # Chart
            html.Div([
               # Riverkeeper's Sations Map
                html.Div(
                        [
                            dcc.Graph(id='main_correlation_map_graph', figure=stations_map(current_stations)),
                        ],
                        className='five columns',
                        style={'margin-top': '20'}
                ),
                #Riverkeeper's Station's Readings Table
                html.Div(
                    [
                        dt.DataTable(
                            id='table_correlations',
                            # Initialise the rows
                            #rows=[{}],
                            rows=create_subset_dataframe_table_by_correlation(df_readings, '0'),
                            row_selectable=False,
                            filterable=True,
                            sortable=True,
                            min_height=500,
                            editable=False,
                            #selected_row_indices=[],
                        )
                    ],
                    className='seven columns',
                    style={'margin-top': '20'}
                ),
            ],className='row'),

            # Riverkeeper's Stations Correlations Charts
            html.Div([
                # Riverkeeper's Sations Correlations
                html.Div(
                    [
                        dcc.Graph(id='stations-correlations-results-chart', figure=date_chart_correlation(df_readings, '0')),
                    ],
                    className='twelve columns',
                    style={'margin-top': '20'}
                ),

            ],className='row'),

    ], className='row', style={'padding': '0px 10px 15px 10px',
    'marginLeft': 'auto', 'marginRight': 'auto', "width": "900px",
    'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'}),


    html.Div([
        # Created By Description Row
         html.Div([
                html.H1(children="Created by", style={'font-family': 'Dosis'}),
            ]),

        # Description Row
        html.Div([
            dcc.Markdown(children=created_by_text.replace('  ', ''), className='eight columns offset-by-two'),
        ], className='row', style={'text-align': 'left', 'margin-bottom': '15px'}),


    ], style={'padding': '0px 10px 15px 10px',
      'marginLeft': 'auto', 'marginRight': 'auto', "width": "900px",
      'boxShadow': '0px 0px 5px 5px rgba(204,204,204,0.4)'}),

], className='ten columns offset-by-one')



"""
################################### D A S H  F U N C T I O N S ################
"""


# Displaying the selected Stations ID of the visualized data
@app.callback(Output('selected-station-id', 'children'),
              [Input('main_graph', 'hoverData')])
def update_station_id(hoverData):

    return('The selected station ID is {}'.format(hoverData['points'][0]['customdata']))



# Displaying the selected Stations Name of the visualized data

@app.callback(Output('selected-station-name', 'children'),
              [Input('main_graph', 'hoverData')])
def update_station_name(hoverData):

    station_name = filter_dataframe(df_stations, hoverData['points'][0]['customdata'])

    return('Location: {}'.format(station_name['Site Name'][0]))

# Trying to figure it out
#@app.callback(Output('button-clicks', 'children'),
#              [Input('my-dropdown', 'value')])
#def clicks(dropdown_properties):
#    return 'The selected station is {}'.format(dropdown_properties)




"""
# Creating a table based on selections from the Stations Map

@app.callback(Output('table1', 'rows'),
              [Input('main_graph', 'hoverData')])
def update_table(hoverData):

    #station = '0' # Default Station
    station = hoverData['points'][0]['customdata']

    stations = create_subset_dataframe_table(df_readings, station)

    return(stations)

# this is hoover data holds
#hoverData = {'points': [{'curveNumber': 0, 'pointNumber': 75, 'lon': -73.96303, 'lat': 41.93158, 'customdata': '92W', 'text': 'Station: [ 92W ] - Kingston Point Beach'}]}
"""



# Presenting Timeseries for the Stations based on the Main Map

@app.callback(Output('station-time-series', 'figure'),
              [Input('main_graph', 'hoverData')])
def update_graph(hoverData):

    #station = '0'
    station = hoverData['points'][0]['customdata']

    stations = filter_dataframe(df_readings, station)

    figure = time_series(stations)

    return(figure)


# Updating Map with Date picker
@app.callback(Output('main_date_map_graph', 'figure'),
              [Input('date-picker', 'date')])
def update_filtered_map_output(date):
    #date = '2017-10-15'
    #picked_date = "2017-10-19"
    #picked_date = dtime.now()
    #picked_date = dtime.date(picked_date)
    picked_date = pd.Timestamp(date)
    picked_date = str(picked_date.year) + '-' + str(picked_date.month) + '-' + str(picked_date.day)
    picked_date = pd.Timestamp(picked_date)

    figure = stations_map_by_safety(df_readings, picked_date)

    return(figure)


# Displaying the selected Stations ID of the visualized data
@app.callback(Output('selected-date', 'children'),
              [Input('date-picker', 'date')])
def update_date(date):
    date = pd.Timestamp(date)
    return('The selected date is {:%m-%d-%Y}'.format(date)) #{}.format(date))


# Creating a table based on Date selections from Date Picker

@app.callback(Output('table_recomended', 'rows'),
             [Input('date-picker', 'date')])
def update_table_by_date(date):
    #date = '10/19/2017'
    date = pd.Timestamp(date)
    date = '{:%m-%d-%Y}'.format(date) #str(date.year) + '-' + str(date.month) + '-' + str(date.day)
    date = pd.Timestamp(date)

    stations = create_subset_dataframe_table_by_date(df_readings, date)

    return(stations.to_dict('records'))




# Updating Stations with Date picker
@app.callback(Output('stations-results-chart', 'figure'),
              [Input('date-picker', 'date')])
def update_filtered_map_date_output(date):
    #date = return_recent_date(df_readings)
    figure = date_chart_h(df_readings, date)

    return(figure)


# Updating Main charts display based on chart selection
@app.callback(Output('main-chart-types', 'figure'),
              [Input('chart-type-selector', 'value')])
def update_chart_type(value):
    #date = return_recent_date(df_readings)

    if (value == 'counts'):
        figure = station_counts_series(df_readings)

    if (value == 'gmean'):
        figure = station_gm_series(df_readings)

    if (value == 'combined'):
        figure = station_combined_count_gm_series(df_readings)

    if (value == 'STV'):
        figure = date_chart_STV_h(df_readings)


    return(figure)



# Creating a table based on Correlations from Map

@app.callback(Output('table_correlations', 'rows'),
              [Input('main_correlation_map_graph', 'hoverData')])
def update_table(hoverData):

    #station = '0' # Default Station
    station = hoverData['points'][0]['customdata']

    stations = create_subset_dataframe_table_by_correlation(df_readings, station)

    return(stations)



# Displaying the selected Stations Name of the correlation data

@app.callback(Output('selected-station-correlation-name', 'children'),
              [Input('main_correlation_map_graph', 'hoverData')])
def update_station_name(hoverData):

    station_name = filter_dataframe(df_stations, hoverData['points'][0]['customdata'])

    return('Location: {}'.format(station_name['Site Name'][0]))


# Presenting Timeseries for the Stations Correlations based on the Main Map

@app.callback(Output('stations-correlations-results-chart', 'figure'),
              [Input('main_correlation_map_graph', 'hoverData')])
def update_correlation_graph(hoverData):

    #station = '0'
    station = hoverData['points'][0]['customdata']

    figure = date_chart_correlation(df_readings, station)

    return(figure)

"""
################################### E X T E R N A L  C A L L S ################
"""

# External css
external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "//fonts.googleapis.com/css?family=Dosis:Medium",
                "//fonts.googleapis.com/css?family=Tangerine:Medium",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/62f0eb4f1fadbefea64b2404493079bf848974e8/dash-uber-ride-demo.css",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
                'https://cdn.rawgit.com/chriddyp/0247653a7c52feb4c48437e1c1837f75/raw/a68333b876edaf62df2efa7bac0e9b3613258851/dash.css']


for css in external_css:
    app.css.append_css({"external_url": css})

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
