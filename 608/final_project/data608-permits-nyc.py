#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sudo kill $(sudo lsof -t -i:9001)
Created on Thu May 10 11:42:40 2018

@author:
        Duubar Villalobos Jimenez  - mydvtech@gmail.com

Final Project:
    Data608
    CUNY SPS
    Masters in Data Science
    Spring 2018
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, Event
import dash_table_experiments as dte

import calendar
from datetime import datetime 
from datetime import timedelta
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta # To create range slider

from plotly.offline import plot
import plotly.plotly as py
from plotly import graph_objs as go
from plotly.graph_objs import *
import plotly.figure_factory as ff

import pandas as pd
pd.options.mode.chained_assignment = None  # Pandas Copy Warning default='warn'


################################### D A T A ###################################

# url = 'https://raw.githubusercontent.com/dvillalobos/MSDS/master/608/Assignments/Module4/'
#url = '/home/mydvadmin/Dropbox/CUNY/Courses/DATA608/FinalProject/permits-app/data/'

url = '/usr/src/app/permits-nyc/data/'


sample_file = '24as-fxn4-SAMPLE.csv'

# Defining pandas types
pdtype={'address': 'str',
     'borough': 'str',
     'borough_block_lot': 'str', 
     'building_id': 'str',
     'city': 'str',
     'dob_skilled_trades_lic_type' : 'str',                                 
     'latitude_wgs84': 'float',
     'license_permit_holder': 'str',
     'license_permit_number': 'str',
     'longitude_wgs84': 'float',
     'permit_expiration_date': 'str',
     'permit_issuance_date': 'str',
     'permit_status_date': 'str',
     'permit_status_description': 'str',
     'permit_type_description': 'str',
     'source': 'str',
     'street': 'str',
     'zip_code': 'str',
     'dob_skilled_trades_lic_num': 'str',
     'permit_subtype_description': 'str',
     'business_description': 'str',
     'license_permit_holder_name': 'str'}

# Reading the Permits sample file
data_SAMPLE = pd.read_csv(url + sample_file, dtype=pdtype)

#Sampling smaller data for speed
#data_SAMPLE = data_SAMPLE.sample(frac=0.1, replace=False)

"""
file_BRONX = '24as-fxn4-BRONX.csv'
file_BROOOKLYN = '24as-fxn4-BROOKLYN.csv'
file_MANHATTAN = '24as-fxn4-MANHATTAN.csv'
file_QUEENS = '24as-fxn4-QUEENS.csv'
file_STATEN_ISLAND = '24as-fxn4-STATEN_ISLAND.csv'
file_NA = '24as-fxn4-NA.csv'

                       
data_BRONX = pd.read_csv(url + file_BRONX, dtype=pdtype)
data_BROOOKLYN = pd.read_csv(url + file_BROOOKLYN, dtype=pdtype)
data_MANHATTAN = pd.read_csv(url + file_MANHATTAN, dtype=pdtype)
data_QUEENS = pd.read_csv(url + file_QUEENS, dtype=pdtype)
data_STATEN_ISLAND = pd.read_csv(url + file_STATEN_ISLAND, dtype=pdtype)
data_NA = pd.read_csv(url + file_NA, dtype=pdtype)
    
data_SAMPLE = pd.concat([data_BRONX, data_BROOOKLYN, data_MANHATTAN, data_QUEENS, data_STATEN_ISLAND, data_NA], ignore_index=True)


#data_SAMPLE.shape
#data_SAMPLE.dtypes
#data_BROOOKLYN.memory_usage()   
# Need to sample smaller dataset for speed purposes while developing
data_SAMPLE = data_SAMPLE.sample(frac=0.25, replace=False)
    
# Need to convert to float values
# data_SAMPLE.dtypes
#data_SAMPLE['latitude_wgs84'] =  data_SAMPLE['latitude_wgs84'].astype(float)
#data_SAMPLE['longitude_wgs84'] =  data_SAMPLE['longitude_wgs84'].astype(float)

# Need to take care of unknown NA dates by assigning '1/1/1900' instead
data_SAMPLE['permit_issuance_date'] = data_SAMPLE['permit_issuance_date'].fillna('1/1/1900')    
data_SAMPLE['permit_expiration_date'] = data_SAMPLE['permit_expiration_date'].fillna('1/1/1900') 
data_SAMPLE['permit_status_date'] = data_SAMPLE['permit_status_date'].fillna('1/1/1900') 
    
# Need to Convert to date format
data_SAMPLE['permit_issuance_date'] = pd.to_datetime(data_SAMPLE['permit_issuance_date'], errors='coerce')
data_SAMPLE['permit_expiration_date'] = pd.to_datetime(data_SAMPLE['permit_expiration_date'], errors='coerce')
data_SAMPLE['permit_status_date'] = pd.to_datetime(data_SAMPLE['permit_status_date'], errors='coerce')

# Write Sample File
#data_SAMPLE.to_csv(url + '24as-fxn4-SAMPLE1.csv', header=True, index=False, index_label=None)
# Need to create a column State
#data_SAMPLE['state'] = 'NY'

# Need Full Address in single coulumn
#data_SAMPLE['permit_address'] = data_SAMPLE['address'] + ' ' \
#                                + data_SAMPLE['street'] + ', ' \
#                                + data_SAMPLE['city'] + ', ' \
#                                + data_SAMPLE['state'] + ' ' \
#                                + data_SAMPLE['zip_code']
"""
################################### F U N C T I O N S #########################
      
# Need to create Permit Count Summaries for each borough  
def get_total_permits_summary(df_permits):     
    permit_count_BRONX = df_permits[df_permits['borough'] == 'BRONX']['borough'].count()
    permit_count_BROOKLYN =  df_permits[df_permits['borough'] == 'BROOKLYN']['borough'].count()
    permit_count_MANHATTAN =  df_permits[df_permits['borough'] == 'MANHATTAN']['borough'].count()
    permit_count_QUEENS =  df_permits[df_permits['borough'] == 'QUEENS']['borough'].count()
    permit_count_STATEN_ISLAND =  df_permits[df_permits['borough'] == 'STATEN ISLAND']['borough'].count()
    
    permit_count_TOTAL = permit_count_BRONX + permit_count_BROOKLYN + permit_count_MANHATTAN + permit_count_QUEENS + permit_count_STATEN_ISLAND
    
    html_text = '**Number of permits randomly sampled for this analysis:** ' + str(permit_count_TOTAL) + '.'
                
    return(html_text)
                          
# Need to create Permit Count Summaries for each borough  
def get_borough_permits_summary(df_permits):     
    permit_count_BRONX = df_permits[df_permits['borough'] == 'BRONX']['borough'].count()
    permit_count_BROOKLYN =  df_permits[df_permits['borough'] == 'BROOKLYN']['borough'].count()
    permit_count_MANHATTAN =  df_permits[df_permits['borough'] == 'MANHATTAN']['borough'].count()
    permit_count_QUEENS =  df_permits[df_permits['borough'] == 'QUEENS']['borough'].count()
    permit_count_STATEN_ISLAND =  df_permits[df_permits['borough'] == 'STATEN ISLAND']['borough'].count()
    
    html_text = '**Bronx:** ' + str(permit_count_BRONX) + ', ' \
                + '**Brooklyn:** ' + str(permit_count_BROOKLYN) + ', ' \
                + '**Manahattan:** ' + str(permit_count_MANHATTAN) + ', ' \
                + '**Queens:** ' + str(permit_count_QUEENS) + ', ' \
                + '**Staten Island:** ' + str(permit_count_STATEN_ISLAND) + '.'
                
    return(html_text)                              

# Return split dates position
def getFirst(s):
  return s.split("-")[0]

def getSecond(s):
  return s.split("-")[1]

def getThird(s):
  return s.split("-")[2]

def getFirstSecond(s):
  return s.split("-")[1]+"-"+s.split("-")[0]

# Return minimum date available
def min_Date(df_permits):

    # Need to know how many days the permit is issued for
    df_permits['permit_issuance_date'] = pd.to_datetime(df_permits['permit_issuance_date'], errors='coerce')
    # Need to discard 1900 dates
    df_permits = df_permits[df_permits['permit_issuance_date'] != '1900-01-01']
    
    min_date = df_permits['permit_issuance_date'].min()
    return(min_date)
    
# Return minimum date available
def max_Date(df_permits):

    # Need to know how many days the permit is issued for
    df_permits['permit_issuance_date'] = pd.to_datetime(df_permits['permit_issuance_date'], errors='coerce')
    # Need to discard 1900 dates
    df_permits = df_permits[df_permits['permit_issuance_date'] != '1900-01-01']
    
    max_date = df_permits['permit_issuance_date'].max()
    return(max_date)
    
################################### P L O T L Y  ##############################

# Create Pie Chart for the Permits issued by day
def pie_chart_permits_by_day(df_permits):
    #df_permits = data_SAMPLE.copy()
    # Need to know how many days the permit is issued for
    df_permits['permit_issuance_date'] = pd.to_datetime(df_permits['permit_issuance_date'], errors='coerce')
       
    # Need to discard 1900 dates
    df_permits = df_permits[df_permits['permit_issuance_date'] != '1900-01-01']    

    df_permits['weekday_name'] = df_permits['permit_issuance_date'].dt.weekday_name
    df_permits['weekday'] = df_permits['permit_issuance_date'].dt.weekday
    
    # Need to group by the number of days
    permit_counts = df_permits.groupby(['weekday_name', 'weekday']).size().reset_index(name='counts')
    
    # Need to Sort sequentially
    permit_counts = permit_counts.sort_values(['weekday'], ascending=True)
    
    labels = permit_counts['weekday_name']
    values = permit_counts['counts']
    
    trace = go.Bar(
        x=labels,
        y=values,
        name='Day of the Week',
        orientation = 'v',
        marker = dict(
            color = 'rgba(232, 126, 4,1)',
            line = dict(
                color = 'rgba(232, 126, 4,1)',
                width = 3)
        )
    )

    data = [trace]
    layout = go.Layout(
                        barmode='stack',
                        title='Permits by day.'
                    )

    fig = go.Figure(data=data, layout=layout)

    return(fig)
    
# Create a permits by borough bar chart display on it
def bar_chart_permits_borough(df_permits):
    
    # Need to know how many days the permit is issued for
    df_permits['permit_issuance_date'] = pd.to_datetime(df_permits['permit_issuance_date'], errors='coerce')
    df_permits['permit_expiration_date'] = pd.to_datetime(df_permits['permit_expiration_date'], errors='coerce')    
    df_permits['permit_days'] = df_permits['permit_expiration_date'] - df_permits['permit_issuance_date']
    
    # Need to define color based on permit length
    df_permits['permit_length'] = 'Error'
    df_permits['permit_length'].loc[df_permits['permit_days'].dt.days == 1] = '1 Day'
    df_permits['permit_length'].loc[(df_permits['permit_days'].dt.days > 1) & (df_permits['permit_days'].dt.days <= 7)] = '<= 1 Week'
    df_permits['permit_length'].loc[(df_permits['permit_days'].dt.days > 7) & (df_permits['permit_days'].dt.days <= 30)] = '<= 1 Month'
    df_permits['permit_length'].loc[(df_permits['permit_days'].dt.days > 30) & (df_permits['permit_days'].dt.days <= 180)] = '<= 6 Months'
    df_permits['permit_length'].loc[df_permits['permit_days'].dt.days > 180] = '> 6 Months'
    
    # Need to group by
    permit_counts = df_permits.groupby(['borough','permit_length']).size().reset_index(name='counts')

    # Grouping by Error in order to plot stacked bar chart
    permit_error = permit_counts[permit_counts['permit_length'] == 'Error']
    permit_g6month = permit_counts[permit_counts['permit_length'] == '> 6 Months']
    permit_l6month = permit_counts[permit_counts['permit_length'] == '<= 6 Months']
    permit_l1month = permit_counts[permit_counts['permit_length'] == '<= 1 Month']    
    permit_l1week = permit_counts[permit_counts['permit_length'] == '<= 1 Week']  
    permit_l1day = permit_counts[permit_counts['permit_length'] == '1 Day']      

    # Unique Boroughs
    x = permit_counts['borough'].unique()
    
    trace1 = go.Bar(
        x=x,
        y=permit_error['counts'],
        name='Error',
        orientation = 'v',
        marker = dict(
            color = 'rgba(30, 139, 195,1)',
            line = dict(
                color = 'rgba(30, 139, 195,1)',
                width = 3)
        )
    )

    trace2 = go.Bar(
        x=x,
        y=permit_g6month['counts'],
        name='> 6 Month',
        orientation = 'v',
        marker = dict(
            color = 'rgba(30, 139, 195,1)',
            line = dict(
                color = 'rgba(30, 139, 195,10)',
                width = 3)
        )
    )
        
    trace3 = go.Bar(
        x=x,
        y=permit_l6month['counts'],
        name='<= 6 Months',
        orientation = 'v',
        marker = dict(
            color = 'rgba(30, 139, 195,1)',
            line = dict(
                color = 'rgba(30, 139, 195,1)',
                width = 3)
        )
    )

    trace4 = go.Bar(
        x=x,
        y=permit_l1month['counts'],
        name='<= 1 Month',
        orientation = 'v',
        marker = dict(
            color = 'rgba(30, 139, 195,1)',
            line = dict(
                color = 'rgba(30, 139, 195,1)',
                width = 3)
        )
    )         

    trace5 = go.Bar(
        x=x,
        y=permit_l1week['counts'],
        name='<= 1 Week',
        orientation = 'v',
        marker = dict(
            color = 'rgba(30, 139, 195,1)',
            line = dict(
                color = 'rgba(30, 139, 1954,1)',
                width = 3)
        )
    )      

    trace6 = go.Bar(
        x=x,
        y=permit_l1day['counts'],
        name='1 Day',
        orientation = 'v',
        marker = dict(
            color = 'rgba(30, 139, 195,1)',
            line = dict(
                color = 'rgba(30, 139, 195,1)',
                width = 3)
        )
    ) 
            
    data = [trace1, trace2, trace3, trace4, trace5, trace6]
    layout = go.Layout(
                        barmode='stack',
                        title='Permits by borough.'
                    )
    

    fig = go.Figure(data=data, layout=layout)

    return(fig)

# Create a permits by borough bar chart display on it
def bar_chart_permits_length(df_permits):

    # Need to know how many days the permit is issued for
    df_permits['permit_issuance_date'] = pd.to_datetime(df_permits['permit_issuance_date'], errors='coerce')
    df_permits['permit_expiration_date'] = pd.to_datetime(df_permits['permit_expiration_date'], errors='coerce')    
    df_permits['permit_days'] = df_permits['permit_expiration_date'] - df_permits['permit_issuance_date']
    
    # Need to define color based on permit length
    df_permits['permit_length'] = 'Error'
    df_permits['permit_length'].loc[df_permits['permit_days'].dt.days == 1] = '1 Day'
    df_permits['permit_length'].loc[(df_permits['permit_days'].dt.days > 1) & (df_permits['permit_days'].dt.days <= 7)] = '<= 1 Week'
    df_permits['permit_length'].loc[(df_permits['permit_days'].dt.days > 7) & (df_permits['permit_days'].dt.days <= 30)] = '<= 1 Month'
    df_permits['permit_length'].loc[(df_permits['permit_days'].dt.days > 30) & (df_permits['permit_days'].dt.days <= 180)] = '<= 6 Months'
    df_permits['permit_length'].loc[df_permits['permit_days'].dt.days > 180] = '> 6 Months'
    
    # Need to group by
    permit_counts = df_permits.groupby(['borough','permit_length']).size().reset_index(name='counts')

    # Grouping by Error in order to plot stacked bar chart
    permit_BRONX = permit_counts[permit_counts['borough'] == 'BRONX']
    permit_BROOKLYN = permit_counts[permit_counts['borough'] == 'BROOKLYN']
    permit_MANHATTAN = permit_counts[permit_counts['borough'] == 'MANHATTAN']
    permit_QUEENS = permit_counts[permit_counts['borough'] == 'QUEENS']    
    permit_STATEN_ISLAND = permit_counts[permit_counts['borough'] == 'STATEN ISLAND']  
    
    # Unique Boroughs
    x = permit_counts['permit_length'].unique()
    
    trace1 = go.Bar(
        x=x,
        y=permit_BRONX['counts'],
        name='BRONX',
        orientation = 'v',
        marker = dict(
            color = 'rgba(222,45,38,1)',
            line = dict(
                color = 'rgba(222,45,38,1)',
                width = 3)
        )
    )

    trace2 = go.Bar(
        x=x,
        y=permit_BROOKLYN['counts'],
        name='BROOKLYN',
        orientation = 'v',
        marker = dict(
            color = 'rgba(222,45,38, 1)',
            line = dict(
                color = 'rgba(222,45,38,1)',
                width = 3)
        )
    )
        
    trace3 = go.Bar(
        x=x,
        y=permit_MANHATTAN['counts'],
        name='MANHATTAN',
        orientation = 'v',
        marker = dict(
            color = 'rgba(222,45,38, 1)',
            line = dict(
                color = 'rgba(222,45,38,1)',
                width = 3)
        )
    )

    trace4 = go.Bar(
        x=x,
        y=permit_QUEENS['counts'],
        name='QUEENS',
        orientation = 'v',
        marker = dict(
            color = 'rgba(222,45,38, 1)',
            line = dict(
                color = 'rgba(222,45,38,1)',
                width = 3)
        )
    )         

    trace5 = go.Bar(
        x=x,
        y=permit_STATEN_ISLAND['counts'],
        name='STATEN ISLAND',
        orientation = 'v',
        marker = dict(
            color = 'rgba(222,45,38, 1)',
            line = dict(
                color = 'rgba(222,45,38,1)',
                width = 3)
        )
    )      

            
    data = [trace1, trace2, trace3, trace4, trace5]
    layout = go.Layout(
                            barmode='stack',
                            title='Permits by length.'
                        )

    fig = go.Figure(data=data, layout=layout)

    return(fig)   


# Create Chart for the length of the Permit by day
def time_series_table_permits_by_day_long_chart(df_permits):
 
    #df_permits = data_SAMPLE.copy()
    # Need to know how many days the permit is issued for
    df_permits['permit_issuance_date'] = pd.to_datetime(df_permits['permit_issuance_date'], errors='coerce')
       
    # Need to discard 1900 dates
    df_permits = df_permits[df_permits['permit_issuance_date'] != '1900-01-01']    

    # Need to group by the number of days
    permit_counts = df_permits.groupby(['permit_issuance_date']).size().reset_index(name='counts')
    
    permit_counts['permit_issuance_date'] = pd.to_datetime(permit_counts['permit_issuance_date'], errors='coerce')
    
    # Need to Sort sequentially
    permit_counts = permit_counts.sort_values(['counts', 'permit_issuance_date'], ascending=False)
    
    permit_counts = permit_counts.head()
    
    permit_counts.rename(columns={'permit_issuance_date': 'Date',
                                  'counts': 'Count'},
                        inplace=True)
    
    return(permit_counts.to_dict('records'))
    
# Create Chart for the length of the Permit by day
def time_series_plot_permits_by_day_long_chart(df_permits):
 
    # Need to know how many days the permit is issued for
    df_permits['permit_issuance_date'] = pd.to_datetime(df_permits['permit_issuance_date'], errors='coerce')
       
    # Need to discard 1900 dates
    df_permits = df_permits[df_permits['permit_issuance_date'] != '1900-01-01']    

    # Need to group by the number of days
    permit_counts = df_permits.groupby(['permit_issuance_date']).size().reset_index(name='counts')
    
    permit_counts['permit_issuance_date'] = pd.to_datetime(permit_counts['permit_issuance_date'], errors='coerce')
    
    # Need to Sort sequentially
    permit_counts = permit_counts.sort_values('permit_issuance_date')
    
    x = permit_counts['permit_issuance_date']# + ' - ' + permit_counts['year']
    trace1 = go.Scatter(
    #trace1 = go.Bar(
        x=x,
        y=permit_counts['counts'],
        name='Counts',
        mode = 'lines',
        #orientation = 'v',
        marker = dict(
            color = 'rgba(108, 122, 137,1)',
            line = dict(
                color = 'rgba(108, 122, 137, .8)',
                width = 3)
        )
    )

    data = [trace1]
    layout = go.Layout(
                        #barmode='stack',
                        title='<b>Time Series:</b> Number of permits issued by day.',
                        xaxis = dict(
                                        rangeselector=dict(
                                            buttons=list([
                                                dict(count=6,
                                                     label='6m',
                                                     step='month',
                                                     stepmode='backward'),
                                                dict(count=1,
                                                    label='1y',
                                                    step='year',
                                                    stepmode='backward'),
                                                dict(count=2,
                                                    label='2y',
                                                    step='year',
                                                    stepmode='todate'),   
                                                dict(count=5,
                                                    label='5y',
                                                    step='year',
                                                    stepmode='todate'),   
                                                dict(count=10,
                                                    label='10y',
                                                    step='year',
                                                    stepmode='todate'),                                                      
                                                dict(step='all')
                                            ])
                                        ),
                                        rangeslider=dict(),
                                        type='date'
                                    )
                                )
    

    fig = go.Figure(data=data, layout=layout)

    return(fig)

# Create Chart for the length of the Permit by day
def time_series_table_permits_by_month_long_chart(df_permits):
 
    #df_permits = data_SAMPLE.copy()
    # Need to know how many days the permit is issued for
    df_permits['permit_issuance_date'] = pd.to_datetime(df_permits['permit_issuance_date'], errors='coerce')

    df_permits['year'] = df_permits['permit_issuance_date'].dt.year
    df_permits['month'] = df_permits['permit_issuance_date'].dt.month
    #df_permits['day'] = df_permits['permit_issuance_date'].dt.day    
    #df_permits['weekday_name'] = df_permits['permit_issuance_date'].dt.weekday_name
    
    df_permits['month'] = df_permits['month'].astype(str)
    df_permits['year'] = df_permits['year'].astype(str)
    
    df_permits['YearMonth'] = df_permits['year'] + '-'+  df_permits['month'] + '-01'
    
    # Need to discard 1900 dates
    df_permits = df_permits[df_permits['permit_issuance_date'] != '1900-01-01']    

    # Need to group by the number of days
    permit_counts = df_permits.groupby(['YearMonth']).size().reset_index(name='counts')
    
    
    permit_counts['YearMonth'] = pd.to_datetime(permit_counts['YearMonth'], errors='coerce')
    
    permit_counts['year'] = permit_counts['YearMonth'].dt.year
    permit_counts['month'] = permit_counts['YearMonth'].dt.month
    
    permit_counts['month_name'] = permit_counts['month'].astype(int)
    permit_counts['month_name'] = permit_counts['month_name'].apply(lambda x: calendar.month_abbr[x])    
    
    permit_counts['year']  =  permit_counts['year'].astype(str)
    permit_counts['month_name']  =  permit_counts['month_name'].astype(str)
    
    permit_counts['Month'] = permit_counts['month_name'] + ', ' + permit_counts['year']
    
    # Need to Sort sequentially
    permit_counts = permit_counts.sort_values(['counts', 'YearMonth'], ascending=False)
    
    permit_counts = permit_counts.head()
    
    permit_counts.rename(columns={'Month': 'Month',
                                  'counts': 'Count'},
                        inplace=True)
    
    permit_counts = permit_counts[['Month', 'Count']]
    
    return(permit_counts.to_dict('records'))

     
# Create Chart for the length of the Permit in months
def time_series_plot_permits_by_month_long_chart(df_permits):
   
    # Need to know how many days the permit is issued for
    df_permits['permit_issuance_date'] = pd.to_datetime(df_permits['permit_issuance_date'], errors='coerce')

    df_permits['year'] = df_permits['permit_issuance_date'].dt.year
    df_permits['month'] = df_permits['permit_issuance_date'].dt.month
    #df_permits['day'] = df_permits['permit_issuance_date'].dt.day    
    #df_permits['weekday_name'] = df_permits['permit_issuance_date'].dt.weekday_name
    
    df_permits['month'] = df_permits['month'].astype(str)
    df_permits['year'] = df_permits['year'].astype(str)
    
    df_permits['YearMonth'] = df_permits['year'] + '-'+  df_permits['month'] + '-01'
    
    # Need to discard 1900 dates
    df_permits = df_permits[df_permits['permit_issuance_date'] != '1900-01-01']    

    # Need to group by the number of days
    permit_counts = df_permits.groupby(['YearMonth']).size().reset_index(name='counts')
    
    permit_counts['YearMonth'] = pd.to_datetime(permit_counts['YearMonth'], errors='coerce')
    
    # Need to Sort sequentially
    permit_counts = permit_counts.sort_values('YearMonth')
    
    x = permit_counts['YearMonth']# + ' - ' + permit_counts['year']
    trace1 = go.Scatter(
    #trace1 = go.Bar(
        x=x,
        y=permit_counts['counts'],
        name='Counts',
        mode = 'lines',
        #orientation = 'v',
        marker = dict(
            color = 'rgba(239, 72, 54,1)',
            line = dict(
                color = 'rgba(152, 0, 0, .8)',
                width = 3)
        )
    )

    data = [trace1]
    layout = go.Layout(
                        #barmode='stack',
                        title='<b>Time Series:</b> Number of permits issued by month.',
                        xaxis = dict(
                                        rangeselector=dict(
                                            buttons=list([
                                                dict(count=6,
                                                     label='6m',
                                                     step='month',
                                                     stepmode='backward'),
                                                dict(count=1,
                                                    label='1y',
                                                    step='year',
                                                    stepmode='backward'),
                                                dict(count=2,
                                                    label='2y',
                                                    step='year',
                                                    stepmode='todate'),   
                                                dict(count=5,
                                                    label='5y',
                                                    step='year',
                                                    stepmode='todate'),   
                                                dict(count=10,
                                                    label='10y',
                                                    step='year',
                                                    stepmode='todate'),                                                      
                                                dict(step='all')
                                            ])
                                        ),
                                        rangeslider=dict(),
                                        type='date'
                                    )
                                )
    

    fig = go.Figure(data=data, layout=layout)

    return(fig)

# Heat Map Month vs Day of the Week
def heat_map_table_weekday_month_chart(df_permits):
    #df_permits = data_SAMPLE.copy()
    
    # Need to know how many days the permit is issued for
    df_permits['permit_issuance_date'] = pd.to_datetime(df_permits['permit_issuance_date'], errors='coerce')
      
    #df_permits['year'] = df_permits['permit_issuance_date'].dt.year
    df_permits['month'] = df_permits['permit_issuance_date'].dt.month
    df_permits['day'] = df_permits['permit_issuance_date'].dt.day    
    df_permits['weekday_name'] = df_permits['permit_issuance_date'].dt.weekday_name
    df_permits['weekday'] = df_permits['permit_issuance_date'].dt.weekday
   
    df_permits['month'] = df_permits['permit_issuance_date'].dt.month
          
    #df_permits[df_permits['month'].isnull()]
    df_permits = df_permits.dropna(subset=['month'])

    df_permits['month_name'] = df_permits['month'].astype(int)
    df_permits['month_name'] = df_permits['month_name'].apply(lambda x: calendar.month_abbr[x])    
    
    # Need to discard 1900 dates
    df_permits = df_permits[df_permits['permit_issuance_date'] != '1900-01-01']
    
    # Need to Group
    df_permits['weekday'] = df_permits['weekday'].astype(str) 
    df_permits['month'] = df_permits['month'].astype(str)
    
    df_permits['MonthWeekDay'] = df_permits['weekday'] + '-'+  df_permits['month']

    # Need to group by the number of days
    permit_counts = df_permits.groupby(['MonthWeekDay']).size().reset_index(name='counts')
    
    # Need to sort sequentially (Need to switch order in order to pull correct values)
    permit_counts['weekday']= permit_counts['MonthWeekDay'].apply(lambda x: getFirst(x)) 
    permit_counts['month']= permit_counts['MonthWeekDay'].apply(lambda x: getSecond(x)) 

    # Need to change Month Number to Month Name
    permit_counts['month_name'] = permit_counts['month'].astype(int)
    permit_counts['month_name'] = permit_counts['month_name'].apply(lambda x: calendar.month_abbr[x])

    permit_counts['weekday_name'] = permit_counts['weekday'].astype(int)
    permit_counts['weekday_name'] = permit_counts['weekday_name'].apply(lambda x: calendar.day_name[x])
    
    # Need to Map Days of the Week
    
    permit_counts['month'] = permit_counts['month'].astype(int)
    permit_counts = permit_counts.sort_values(['weekday','month'])
    
    # Need to Sort sequentially
    permit_counts = permit_counts.sort_values(['counts', 'weekday_name', 'month_name'], ascending=False)
    
    permit_counts = permit_counts.head()
    
    permit_counts.rename(columns={'weekday_name': 'Day',
                                  'month_name': 'Month',
                                  'counts': 'Count'},
                        inplace=True)
    
    permit_counts = permit_counts[['Day', 'Month', 'Count']]
    
    return(permit_counts.to_dict('records'))
    
    
# Heat Map Month vs Day of the Week
def heat_map_permits_weekday_month_chart(df_permits):
    #df_permits = data_SAMPLE.copy()
    
    # Need to know how many days the permit is issued for
    df_permits['permit_issuance_date'] = pd.to_datetime(df_permits['permit_issuance_date'], errors='coerce')
      
    #df_permits['year'] = df_permits['permit_issuance_date'].dt.year
    df_permits['month'] = df_permits['permit_issuance_date'].dt.month
    df_permits['day'] = df_permits['permit_issuance_date'].dt.day    
    df_permits['weekday_name'] = df_permits['permit_issuance_date'].dt.weekday_name
    df_permits['weekday'] = df_permits['permit_issuance_date'].dt.weekday
   
    df_permits['month'] = df_permits['permit_issuance_date'].dt.month
          
    #df_permits[df_permits['month'].isnull()]
    df_permits = df_permits.dropna(subset=['month'])

    df_permits['month_name'] = df_permits['month'].astype(int)
    df_permits['month_name'] = df_permits['month_name'].apply(lambda x: calendar.month_abbr[x])    
    
    # Need to discard 1900 dates
    df_permits = df_permits[df_permits['permit_issuance_date'] != '1900-01-01']
    
    # Need to Group
    df_permits['weekday'] = df_permits['weekday'].astype(str) 
    df_permits['month'] = df_permits['month'].astype(str)
    
    df_permits['MonthWeekDay'] = df_permits['weekday'] + '-'+  df_permits['month']

    # Need to group by the number of days
    permit_counts = df_permits.groupby(['MonthWeekDay']).size().reset_index(name='counts')
    
    # Need to sort sequentially (Need to switch order in order to pull correct values)
    permit_counts['weekday']= permit_counts['MonthWeekDay'].apply(lambda x: getFirst(x)) #Had to swtich order in order to pull correct values
    permit_counts['month']= permit_counts['MonthWeekDay'].apply(lambda x: getSecond(x)) #Had to swtich order in order to pull correct values

    # Need to change Month Number to Month Name
    permit_counts['month_name'] = permit_counts['month'].astype(int)
    permit_counts['month_name'] = permit_counts['month_name'].apply(lambda x: calendar.month_abbr[x])

    permit_counts['weekday_name'] = permit_counts['weekday'].astype(int)
    permit_counts['weekday_name'] = permit_counts['weekday_name'].apply(lambda x: calendar.day_name[x])
    
    # Need to Map Days of the Week
    
    permit_counts['month'] = permit_counts['month'].astype(int)
    permit_counts = permit_counts.sort_values(['weekday','month'])
    
    x = permit_counts['month_name']
    y = permit_counts['weekday_name']
    z = permit_counts['counts'] 

    permit_counts['counts'] = permit_counts['counts'].astype(str)  
    
    data = [
        go.Heatmap(
            z=z,
            x=x,
            y=y,
            colorscale='matter',
            hoverinfo = "text",
            text = 'Month: ' + permit_counts['month_name'] + '<br>' \
                    + 'Week Day: ' + permit_counts['weekday_name'] + '<br>' \
                    + 'Total Permits Issued: ' + permit_counts['counts'],  
        )
    ]
    
    layout = go.Layout(
        title='<b>Heat Map:</b> Number of permits issued by day of the week & month.',
        xaxis = dict(ticks='', nticks=36),
        yaxis = dict(ticks='' )
    )
    
    fig = go.Figure(data=data, layout=layout)
    
    return(fig)
    
    
# Heat Map Month vs Day
def heat_map_table_day_month_chart(df_permits):
    #df_permits = data_SAMPLE.copy()
    # Need to know how many days the permit is issued for
    df_permits['permit_issuance_date'] = pd.to_datetime(df_permits['permit_issuance_date'], errors='coerce')

    #df_permits['year'] = df_permits['permit_issuance_date'].dt.year
    df_permits['month'] = df_permits['permit_issuance_date'].dt.month
    df_permits['day'] = df_permits['permit_issuance_date'].dt.day    
    #df_permits['weekday_name'] = df_permits['permit_issuance_date'].dt.weekday_name
    #df_permits['weekday'] = df_permits['permit_issuance_date'].dt.weekday
    
    # Need to discard 1900 dates
    df_permits = df_permits[df_permits['permit_issuance_date'] != '1900-01-01']
    
    # Need to Group
    df_permits['monthday'] = df_permits['day'].astype(str) 
    df_permits['month'] = df_permits['month'].astype(str)
    
    df_permits['MonthDay'] = df_permits['monthday'] + '-'+  df_permits['month']
    
    # Need to group by the number of days
    permit_counts = df_permits.groupby(['MonthDay']).size().reset_index(name='counts')   

    # Need to sort sequentially (Need to switch order in order to pull correct values)
    permit_counts['day']= permit_counts['MonthDay'].apply(lambda x: getFirst(x)) #Had to swtich order in order to pull correct values
    permit_counts['month']= permit_counts['MonthDay'].apply(lambda x: getSecond(x)) #Had to swtich order in order to pull correct values
    
    permit_counts['month_name'] = permit_counts['month'].astype(int)
    
    permit_counts = permit_counts.sort_values('month_name')
    
    permit_counts['month_name'] = permit_counts['month_name'].apply(lambda x: calendar.month_abbr[x])

    # Need to Sort sequentially
    permit_counts = permit_counts.sort_values(['counts', 'month', 'day'], ascending=False)
    
    permit_counts = permit_counts.head()
    
    permit_counts['month'] = permit_counts['month'].astype(str)
    
    permit_counts['Date'] = permit_counts['month_name'] + ', ' + permit_counts['day']
    
    permit_counts.rename(columns={'Date': 'Date',
                                  'counts': 'Count'},
                        inplace=True)
    
    permit_counts = permit_counts[['Date', 'Count']]
    
    return(permit_counts.to_dict('records'))    
    
    
# Heat Map Month vs Day
def heat_map_permits_day_month_chart(df_permits):
    
    # Need to know how many days the permit is issued for
    df_permits['permit_issuance_date'] = pd.to_datetime(df_permits['permit_issuance_date'], errors='coerce')

    #df_permits['year'] = df_permits['permit_issuance_date'].dt.year
    df_permits['month'] = df_permits['permit_issuance_date'].dt.month
    df_permits['day'] = df_permits['permit_issuance_date'].dt.day    
    #df_permits['weekday_name'] = df_permits['permit_issuance_date'].dt.weekday_name
    #df_permits['weekday'] = df_permits['permit_issuance_date'].dt.weekday
    
    # Need to discard 1900 dates
    df_permits = df_permits[df_permits['permit_issuance_date'] != '1900-01-01']
    
    # Need to Group
    df_permits['monthday'] = df_permits['day'].astype(str) 
    df_permits['month'] = df_permits['month'].astype(str)
    
    df_permits['MonthDay'] = df_permits['monthday'] + '-'+  df_permits['month']
    
    # Need to group by the number of days
    permit_counts = df_permits.groupby(['MonthDay']).size().reset_index(name='counts')   

    # Need to sort sequentially (Need to switch order in order to pull correct values)
    permit_counts['day']= permit_counts['MonthDay'].apply(lambda x: getFirst(x)) #Had to swtich order in order to pull correct values
    permit_counts['month']= permit_counts['MonthDay'].apply(lambda x: getSecond(x)) #Had to swtich order in order to pull correct values
    
    permit_counts['month_name'] = permit_counts['month'].astype(int)
    
    permit_counts = permit_counts.sort_values('month_name')
    
    permit_counts['month_name'] = permit_counts['month_name'].apply(lambda x: calendar.month_abbr[x])
    
    x = permit_counts['day']
    y = permit_counts['month_name']
    z = permit_counts['counts'] 
    
    permit_counts['counts'] = permit_counts['counts'].astype(str)  
        
    data = [
        go.Heatmap(
            z=z,
            x=x,
            y=y,
            colorscale='matter',
            hoverinfo = "text",
            text = 'Month: ' + permit_counts['month_name'] + '<br>' \
                    + 'Day: ' + permit_counts['day'] + ' of the month <br>' \
                    + 'Total Permits Issued: ' + permit_counts['counts'],  
        )
    ]
    
    layout = go.Layout(
        title="<b>Heat Map:</b> Number of permits issued by month & day of the month.",
        xaxis = dict(ticks='', nticks=36),
        yaxis = dict(ticks='' )
    )
    
    fig = go.Figure(data=data, layout=layout)
    
    return(fig)

# Heat Map Year vs Day
def heat_map_table_monthday_year_chart(df_permits):
    #permits = data_SAMPLE.copy()
    # Need to know how many days the permit is issued for
    df_permits['permit_issuance_date'] = pd.to_datetime(df_permits['permit_issuance_date'], errors='coerce')

    df_permits['year'] = df_permits['permit_issuance_date'].dt.year
    #df_permits['month'] = df_permits['permit_issuance_date'].dt.month
    df_permits['day'] = df_permits['permit_issuance_date'].dt.day    
    #df_permits['weekday_name'] = df_permits['permit_issuance_date'].dt.weekday_name
    
    df_permits['day'] = df_permits['day'].astype(str)
    df_permits['year'] = df_permits['year'].astype(str)
    
    df_permits['YearDay'] = df_permits['day'] + '-'+  df_permits['year']
    
    # Need to discard 1900 dates
    df_permits = df_permits[df_permits['permit_issuance_date'] != '1900-01-01']    

    # Need to group by the number of days
    permit_counts = df_permits.groupby(['YearDay']).size().reset_index(name='counts')
    
    # Need to sort sequentially (Need to switch order in order to pull correct values)
    permit_counts['day']= permit_counts['YearDay'].apply(lambda x: getFirst(x)) #Had to swtich order in order to pull correct values
    permit_counts['year']= permit_counts['YearDay'].apply(lambda x: getSecond(x)) #Had to swtich order in order to pull correct values

    permit_counts['year'] = permit_counts['year'].astype(str)
    
    # Need to Sort sequentially
    permit_counts = permit_counts.sort_values(['counts', 'year', 'day'], ascending=False)
    
    permit_counts = permit_counts.head()
    
    permit_counts['year'] = permit_counts['year'].astype(str)
    
    permit_counts = permit_counts[['year', 'day', 'counts']]
    
    permit_counts.rename(columns={'year': 'Year',
                                  'day': "Month's day",
                                  'counts': 'Count'},
                        inplace=True) 

    return(permit_counts.to_dict('records'))    
    
    
    
# Heat Map Year vs Day
def heat_map_permits_monthday_year_chart(df_permits):
    
    # Need to know how many days the permit is issued for
    df_permits['permit_issuance_date'] = pd.to_datetime(df_permits['permit_issuance_date'], errors='coerce')

    df_permits['year'] = df_permits['permit_issuance_date'].dt.year
    #df_permits['month'] = df_permits['permit_issuance_date'].dt.month
    df_permits['day'] = df_permits['permit_issuance_date'].dt.day    
    #df_permits['weekday_name'] = df_permits['permit_issuance_date'].dt.weekday_name
    
    df_permits['day'] = df_permits['day'].astype(str)
    df_permits['year'] = df_permits['year'].astype(str)
    
    df_permits['YearDay'] = df_permits['day'] + '-'+  df_permits['year']
    
    # Need to discard 1900 dates
    df_permits = df_permits[df_permits['permit_issuance_date'] != '1900-01-01']    

    # Need to group by the number of days
    permit_counts = df_permits.groupby(['YearDay']).size().reset_index(name='counts')
    
    # Need to sort sequentially (Need to switch order in order to pull correct values)
    permit_counts['day']= permit_counts['YearDay'].apply(lambda x: getFirst(x)) #Had to swtich order in order to pull correct values
    permit_counts['year']= permit_counts['YearDay'].apply(lambda x: getSecond(x)) #Had to swtich order in order to pull correct values

    permit_counts['year'] = permit_counts['year'].astype(str)
    
    x = permit_counts['year']
    y = permit_counts['day']
    z = permit_counts['counts'] 
    
    permit_counts['counts'] = permit_counts['counts'].astype(str)   
    
    data = [
        go.Heatmap(
            z=z,
            x=x,
            y=y,
            colorscale='matter',
            hoverinfo = "text",
            text = 'Year: ' + permit_counts['year'] + '<br>' \
                    + 'Day: ' + permit_counts['day'] + ' of the month <br>' \
                    + 'Total Permits Issued: ' + permit_counts['counts'],  
        )
    ]
    
    layout = go.Layout(
        title='<b>Heat Map:</b> Number of permits issued by day of the month & year.',
        xaxis = dict(ticks='', 
                     nticks=36, 
                     autorange = True,
                     categoryorder = "category ascending",
                     type = "category"),
        yaxis = dict(ticks='' )
    )
    
    
    fig = go.Figure(data=data, layout=layout)
    
    
    return(fig)

# Heat Map Year vs Month
def heat_map_table_month_year_chart(df_permits):
    #df_permits = data_SAMPLE.copy()
    # Need to know how many days the permit is issued for
    df_permits['permit_issuance_date'] = pd.to_datetime(df_permits['permit_issuance_date'], errors='coerce')
    
    df_permits['permit_issuance_date'] = df_permits['permit_issuance_date'].astype(str)

    # Need to get Month and Year
    df_permits['YearMonth']= df_permits['permit_issuance_date'].apply(lambda x: getFirstSecond(x))

    # Need to discard 1900 dates
    df_permits = df_permits[df_permits['permit_issuance_date'] != '1900-01-01']    

    # Need to group by the number of days
    permit_counts = df_permits.groupby(['YearMonth']).size().reset_index(name='counts')
    
    # Need to sort sequentially (Need to switch order in order to pull correct values)
    permit_counts['month']= permit_counts['YearMonth'].apply(lambda x: getFirst(x)) #Had to swtich order in order to pull correct values
    permit_counts['year']= permit_counts['YearMonth'].apply(lambda x: getSecond(x)) #Had to swtich order in order to pull correct values

    permit_counts = permit_counts.sort_values('month')
    
    permit_counts['month_name'] = permit_counts['month'].astype(int)
    permit_counts['month_name'] = permit_counts['month_name'].apply(lambda x: calendar.month_abbr[x])

    # Need to Sort sequentially
    permit_counts = permit_counts.sort_values(['counts', 'year', 'month'], ascending=False)
    
    permit_counts = permit_counts.head()
    
    permit_counts['year'] = permit_counts['year'].astype(str)
    
    permit_counts['Month'] = permit_counts['month_name'] + ', ' +  permit_counts['year']
    
    permit_counts = permit_counts[['Month', 'counts']]
    
    permit_counts.rename(columns={'Month': 'Month',
                                  'counts': 'Count'},
                        inplace=True) 

    return(permit_counts.to_dict('records'))  

    
# Heat Map Year vs Month
def heat_map_permits_month_year_chart(df_permits):

    # Need to know how many days the permit is issued for
    df_permits['permit_issuance_date'] = pd.to_datetime(df_permits['permit_issuance_date'], errors='coerce')
    
    df_permits['permit_issuance_date'] = df_permits['permit_issuance_date'].astype(str)

    # Need to get Month and Year
    df_permits['YearMonth']= df_permits['permit_issuance_date'].apply(lambda x: getFirstSecond(x))

    # Need to discard 1900 dates
    df_permits = df_permits[df_permits['permit_issuance_date'] != '1900-01-01']    

    # Need to group by the number of days
    permit_counts = df_permits.groupby(['YearMonth']).size().reset_index(name='counts')
    
    # Need to sort sequentially (Need to switch order in order to pull correct values)
    permit_counts['month']= permit_counts['YearMonth'].apply(lambda x: getFirst(x)) #Had to swtich order in order to pull correct values
    permit_counts['year']= permit_counts['YearMonth'].apply(lambda x: getSecond(x)) #Had to swtich order in order to pull correct values

    permit_counts = permit_counts.sort_values('month')
    
    permit_counts['month_name'] = permit_counts['month'].astype(int)
    permit_counts['month_name'] = permit_counts['month_name'].apply(lambda x: calendar.month_abbr[x])
    
    x = permit_counts['year']
    y = permit_counts['month_name']
    z = permit_counts['counts'] 
    
    permit_counts['counts'] = permit_counts['counts'].astype(str)
    
    data = [
        go.Heatmap(
            z=z,
            x=x,
            y=y,
            colorscale='matter',
            hoverinfo = "text",
            text = 'Year: ' + permit_counts['year'] + '<br>' \
                    + 'Month: ' + permit_counts['month_name'] + '<br>' \
                    + 'Total Permits Issued: ' + permit_counts['counts'],            
        )
    ]
    
    layout = go.Layout(
        title='<b>Heat Map:</b> Number of permits issued by month & year.',
        xaxis = dict(ticks='', 
                     nticks=36, 
                     autorange = True,
                     categoryorder = "category ascending",
                     type = "category"),
        yaxis = dict(ticks='' )
    )
    
    
    fig = go.Figure(data=data, layout=layout)
    
    
    return(fig)


# Heat Map City vs Permit Type
def heat_map_table_city_permit_type_chart(df_permits):
    #df_permits = data_SAMPLE.copy()
    # Need to discard 1900 dates
    df_permits = df_permits[df_permits['permit_issuance_date'] != '1900-01-01']    

    # Need to group by the number of days
    permit_counts = df_permits.groupby(['city', 'permit_type_description']).size().reset_index(name='counts')
    
    # Need to Sort sequentially
    permit_counts = permit_counts.sort_values(['counts', 'city', 'permit_type_description'], ascending=False)
    
    permit_counts = permit_counts.head()
    
    #permit_counts['year'] = permit_counts['year'].astype(str)
    
    #permit_counts['Month'] = permit_counts['month_name'] + ', ' +  permit_counts['year']
    
    #permit_counts = permit_counts[['Month', 'counts']]
    
    permit_counts.rename(columns={'city': 'City',
                                  'permit_type_description': 'Permit Type',
                                  'counts': 'Count'},
                        inplace=True) 

    return(permit_counts.to_dict('records'))  
    
    
# Heat Map City vs Permit Type
def heat_map_permits_city_permit_type_chart(df_permits):
 
    # Need to discard 1900 dates
    df_permits = df_permits[df_permits['permit_issuance_date'] != '1900-01-01']    

    # Need to group by the number of days
    permit_counts = df_permits.groupby(['city', 'permit_type_description']).size().reset_index(name='counts')
    
    x = permit_counts['permit_type_description'].str.upper()
    y = permit_counts['city'].str.upper()
    z = permit_counts['counts'] 
    
    permit_counts['counts'] = permit_counts['counts'].astype(str)
    
    data = [
        go.Heatmap(
            z=z,
            x=x,
            y=y,
            colorscale='matter',
            hoverinfo = "text",
            text = 'City: ' + permit_counts['city'].str.upper() + '<br>' \
                    + 'Permit Type: ' + permit_counts['permit_type_description'].str.upper() + '<br>' \
                    + 'Total Permits Issued: ' + permit_counts['counts'],
        )
    ]
    
    layout = go.Layout(
        title='<b>Heat Map:</b> Number of permits issued by city & permit type.',
        xaxis = dict(ticks='', nticks=36),
        yaxis = dict(ticks='' ),
        margin = dict(
            r = 80,
            t = 100,
            b = 140,
            l = 150
        ),

    )
    
    fig = go.Figure(data=data, layout=layout)
    
    return(fig)


# Heat Map City vs Permit Type
def heat_map_table_source_permit_type_chart(df_permits):
    #df_permits = data_SAMPLE.copy()
    # Need to discard 1900 dates
    df_permits = df_permits[df_permits['permit_issuance_date'] != '1900-01-01']    

    # Need to group by the number of days
    permit_counts = df_permits.groupby(['source', 'permit_type_description']).size().reset_index(name='counts')

    # Need to Sort sequentially
    permit_counts = permit_counts.sort_values(['counts', 'permit_type_description', 'source'], ascending=False)
    
    permit_counts = permit_counts.head()
    
    #permit_counts['year'] = permit_counts['year'].astype(str)
    
    #permit_counts['Month'] = permit_counts['month_name'] + ', ' +  permit_counts['year']
    
    #permit_counts = permit_counts[['Month', 'counts']]
    
    permit_counts.rename(columns={'source': 'Issuer',
                                  'permit_type_description': 'Permit Type',
                                  'counts': 'Count'},
                        inplace=True) 

    return(permit_counts.to_dict('records'))  
    
# Heat Map City vs Permit Type
def heat_map_permits_source_permit_type_chart(df_permits):

    # Need to discard 1900 dates
    df_permits = df_permits[df_permits['permit_issuance_date'] != '1900-01-01']    

    # Need to group by the number of days
    permit_counts = df_permits.groupby(['source', 'permit_type_description']).size().reset_index(name='counts')
    
    x = permit_counts['permit_type_description'].str.upper()
    y = permit_counts['source'].str.upper()
    z = permit_counts['counts'] 
    
    permit_counts['counts'] = permit_counts['counts'].astype(str)
    
    data = [
        go.Heatmap(
            z=z,
            x=x,
            y=y,
            colorscale='matter',
            hoverinfo = "text",
            text = 'Source: ' + permit_counts['source'].str.upper() + '<br>' \
                    + 'Permit Type: ' + permit_counts['permit_type_description'].str.upper() + '<br>' \
                    + 'Total Permits Issued: ' + permit_counts['counts'],
        )
    ]
    
    layout = go.Layout(
        title='<b>Heat Map:</b> Number of permits issued by source & permit type.',
        xaxis = dict(ticks='', nticks=36),
        yaxis = dict(ticks='' ),
        margin = dict(
            r = 80,
            t = 100,
            b = 140,
            l = 150
        ),

    )
    
    fig = go.Figure(data=data, layout=layout)
    
    return(fig)

# Heat Map City vs Source
def heat_map_table_city_permit_source_chart(df_permits):
    #df_permits = data_SAMPLE.copy()
    # Need to discard 1900 dates
    df_permits = df_permits[df_permits['permit_issuance_date'] != '1900-01-01']    

    # Need to group by the number of days
    permit_counts = df_permits.groupby(['city', 'source']).size().reset_index(name='counts')
    
    # Need to Sort sequentially
    permit_counts = permit_counts.sort_values(['counts', 'city', 'source'], ascending=False)
    
    permit_counts = permit_counts.head()
    
    #permit_counts['year'] = permit_counts['year'].astype(str)
    
    #permit_counts['Month'] = permit_counts['month_name'] + ', ' +  permit_counts['year']
    
    #permit_counts = permit_counts[['Month', 'counts']]
    
    permit_counts.rename(columns={'source': 'Issuer',
                                  'city': 'City',
                                  'counts': 'Count'},
                        inplace=True) 

    return(permit_counts.to_dict('records'))  

      
# Heat Map City vs Source
def heat_map_permits_city_permit_source_chart(df_permits):
    
    # Need to discard 1900 dates
    df_permits = df_permits[df_permits['permit_issuance_date'] != '1900-01-01']    

    # Need to group by the number of days
    permit_counts = df_permits.groupby(['city', 'source']).size().reset_index(name='counts')
    
    x = permit_counts['city'].str.upper()
    y = permit_counts['source'].str.upper()
    z = permit_counts['counts'] 
    
    permit_counts['counts'] = permit_counts['counts'].astype(str)
    
    data = [
        go.Heatmap(
            z=z,
            x=x,
            y=y,
            colorscale='matter',
            hoverinfo = "text",
            text = 'City: ' + permit_counts['city'].str.upper() + '<br>' \
                    + 'Source : ' + permit_counts['source'].str.upper() + '<br>' \
                    + 'Total Permits Issued: ' + permit_counts['counts'],
        )
    ]
    
    layout = go.Layout(
        title='<b>Heat Map:</b> Number of permits issued by source & city.',
        xaxis = dict(ticks='', nticks=36),
        yaxis = dict(ticks='' ),
        margin = dict(
            r = 80,
            t = 100,
            b = 140,
            l = 150
        ),

    )
    
    fig = go.Figure(data=data, layout=layout)

    return(fig)

# Heat Map City vs Source
def heat_map_table_holder_permit_type_chart(df_permits):
    #df_permits = data_SAMPLE.copy()
    # Need to discard 1900 dates
    df_permits = df_permits[df_permits['permit_issuance_date'] != '1900-01-01']    

    # Need to group by the number of days
    permit_counts = df_permits.groupby(['license_permit_holder', 'permit_type_description']).size().reset_index(name='counts')
        
    # Need to Sort sequentially
    permit_counts = permit_counts.sort_values(['counts', 'license_permit_holder', 'permit_type_description'], ascending=False)
    
    permit_counts = permit_counts.head()
    
    #permit_counts['year'] = permit_counts['year'].astype(str)
    
    #permit_counts['Month'] = permit_counts['month_name'] + ', ' +  permit_counts['year']
    
    #permit_counts = permit_counts[['Month', 'counts']]
    
    permit_counts.rename(columns={'license_permit_holder': 'Company',
                                  'permit_type_description': 'Permit Type',
                                  'counts': 'Count'},
                        inplace=True) 

    return(permit_counts.to_dict('records'))  

    
# Heat Map City vs Source
def heat_map_permits_holder_permit_type_chart(df_permits):
    #df_permits = data_SAMPLE.copy()
    # Need to discard 1900 dates
    df_permits = df_permits[df_permits['permit_issuance_date'] != '1900-01-01']    

    # Need to group by the number of days
    permit_counts = df_permits.groupby(['license_permit_holder', 'permit_type_description']).size().reset_index(name='counts')
    
    #permit_counts = permit_counts.sort_values('counts')
    #permit_counts = permit_counts[permit_counts['counts'] > permit_counts['counts'].mean()]
    permit_counts = permit_counts.sort_values(['counts'], ascending=False)
    
    
    permit_counts = permit_counts.head(20)
    # Need to sort sequentially (Need to switch order in order to pull correct values)

    x = permit_counts['license_permit_holder'].str.upper()
    y = permit_counts['permit_type_description'].str.upper()
    z = permit_counts['counts'] 
    
    permit_counts['counts'] = permit_counts['counts'].astype(str)
    
    data = [
        go.Heatmap(
            z=z,
            x=x,
            y=y,
            colorscale='matter',
            hoverinfo = "text",
            text = 'Permit Holder: ' + permit_counts['license_permit_holder'].str.upper() + '<br>' \
                    + 'Permit Type : ' + permit_counts['permit_type_description'].str.upper() + '<br>' \
                    + 'Total Permits Issued: ' + permit_counts['counts'],
        )
    ]
    
    layout = go.Layout(
        title='<b>Heat Map:</b> Top 20 companies that have the most by permits issued by type.',
        xaxis = dict(ticks='', nticks=36),
        yaxis = dict(ticks='' ),
        margin = dict(
            r = 80,
            t = 100,
            b = 140,
            l = 150
        ),

    )
    
    fig = go.Figure(data=data, layout=layout)
    
    return(fig)

# Create a permits map display on it
def permits_map(df_permits):
    # Mapbox
    mapbox_access_token = 'pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w' # noqa: E501

    # Global options
    
    # Need to define how many days the permit is issued for
    df_permits['permit_issuance_date'] = pd.to_datetime(df_permits['permit_issuance_date'], errors='coerce')
    df_permits['permit_expiration_date'] = pd.to_datetime(df_permits['permit_expiration_date'], errors='coerce')       
    
    df_permits['permit_days'] = df_permits['permit_expiration_date'] - df_permits['permit_issuance_date'] #+ timedelta(days=1)
    
    # Need to change date fromat to MM/DD/YYYY
    df_permits['permit_issuance_date'] = df_permits['permit_issuance_date'].dt.strftime('%m/%d/%Y')
    df_permits['permit_expiration_date'] = df_permits['permit_expiration_date'].dt.strftime('%m/%d/%Y')
    
    df_permits['permit_issuance_date'] = df_permits['permit_issuance_date'].astype(str)
    df_permits['permit_expiration_date'] = df_permits['permit_expiration_date'].astype(str)

    zoom = 9
    latInitial = df_permits['latitude_wgs84'].mean()
    lonInitial = df_permits['longitude_wgs84'].mean()
    
    lat_BRONX = df_permits[df_permits['borough'] == 'BRONX']['latitude_wgs84'].mean()
    lon_BRONX = df_permits[df_permits['borough'] == 'BRONX']['longitude_wgs84'].mean()
    
    lat_BROOKLYN = df_permits[df_permits['borough'] == 'BROOKLYN']['latitude_wgs84'].mean()
    lon_BROOKLYN = df_permits[df_permits['borough'] == 'BROOKLYN']['longitude_wgs84'].mean()  
    
    lat_MANHATTAN = df_permits[df_permits['borough'] == 'MANHATTAN']['latitude_wgs84'].mean()
    lon_MANHATTAN = df_permits[df_permits['borough'] == 'MANHATTAN']['longitude_wgs84'].mean()      
    
    lat_QUEENS = df_permits[df_permits['borough'] == 'QUEENS']['latitude_wgs84'].mean()
    lon_QUEENS = df_permits[df_permits['borough'] == 'QUEENS']['longitude_wgs84'].mean() 
    
    lat_STATEN_ISLAND = df_permits[df_permits['borough'] == 'STATEN ISLAND']['latitude_wgs84'].mean()
    lon_STATEN_ISLAND = df_permits[df_permits['borough'] == 'STATEN ISLAND']['longitude_wgs84'].mean()     
    
    bearing = 0
    map_style = 'satellite-streets' #options are: ['satellite-streets', 'satellite', 'dark',  'outdoors', 'streets']

    # Need to define color dictionary based on permit length  
    permit_color = [{'1 Day': 'rgb(0,128,0)',  # Green
                     '<= 1 Week': 'rgb(173,255,47)', # Green Yellow
                     '<= 1 Month': 'rgb(255,255,51)', # Light Yellow
                     '<= 6 Months': 'rgb(255,140,0)', # Dark Orange
                     '> 6 Months': 'rgb(139,0,0)',  # Dark Red
                     'Error': 'rgb(69,10,243)'}]
    permit_color = pd.DataFrame(permit_color)
    
    # Need to define color based on permit length
    df_permits['permit_length'] = 'Error'
    df_permits['permit_length'].loc[df_permits['permit_days'].dt.days == 1] = '1 Day'
    df_permits['permit_length'].loc[(df_permits['permit_days'].dt.days > 1) & (df_permits['permit_days'].dt.days <= 7)] = '<= 1 Week'
    df_permits['permit_length'].loc[(df_permits['permit_days'].dt.days > 7) & (df_permits['permit_days'].dt.days <= 30)] = '<= 1 Month'
    df_permits['permit_length'].loc[(df_permits['permit_days'].dt.days > 30) & (df_permits['permit_days'].dt.days <= 180)] = '<= 6 Months'
    df_permits['permit_length'].loc[df_permits['permit_days'].dt.days > 180] = '> 6 Months'
    
    df_permits['permit_days'] =  df_permits['permit_days'].dt.days.astype(str)
    
    # Map figure
    figure = go.Figure(
        data=Data([
            Scattermapbox(
  
                lat = df_permits[df_permits['permit_length'] == i]['latitude_wgs84'],
                lon = df_permits[df_permits['permit_length'] == i]['longitude_wgs84'],
                customdata = df_permits[df_permits['permit_length'] == i]['building_id'],
                hoverinfo = "text",
                text = 'Building ID:' + df_permits[df_permits['permit_length'] == i]['building_id'] + '<br>' \
                        + 'Address: ' + df_permits[df_permits['permit_length'] == i]['permit_address'] + '<br>' \
                        + 'Permit Issued: ' + df_permits[df_permits['permit_length'] == i]['permit_issuance_date']  + '<br>' \
                        + 'Permit Expiration: ' + df_permits[df_permits['permit_length'] == i]['permit_expiration_date']  + '<br>' \
                        + 'Permit length: ' + df_permits[df_permits['permit_length'] == i]['permit_days'] + ' days <br>' \
                        + 'Permit Description: ' + df_permits[df_permits['permit_length'] == i]['permit_type_description']  + '<br>' \
                        + 'Permit Source: ' + df_permits[df_permits['permit_length'] == i]['source'],
                mode = 'markers',
                marker=dict(
                    size = 15,
                    color = permit_color[i][0],
                    opacity=0.7
                ),
                name=i
                ) for i in df_permits['permit_length'].unique() 
                       
            #),
        ]),
        layout=Layout(
            autosize=True,
            height=550,
            margin=Margin(l=0, r=0, t=40, b=0),
            showlegend=True,
            font=dict(color='#f7f7f7'),
            titlefont=dict(color='#f7f7f7', size='20'),
            hovermode='closest',
            plot_bgcolor='#191A1A',
            paper_bgcolor='#191A1A',
            legend=dict(font=dict(size=10), orientation='v'),
            title='Satellite Overview',
            mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(
                    lat=latInitial, # 40.7272
                    lon=lonInitial # -73.991251
                ),
                style=map_style, # Define the map style
                bearing=bearing,
                zoom=zoom
            ),
            updatemenus=[
                dict(
                    buttons=([
                        dict(
                            args=[{
                                    'mapbox.zoom': 9,
                                    'mapbox.center.lon': lonInitial,
                                    'mapbox.center.lat': latInitial, 
                                    'mapbox.bearing': 0,
                                    'mapbox.style': map_style, # Define the map style
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
                    bgcolor='rgb(32,31,30, 0)',
                    borderwidth=1,
                    bordercolor="#6d6d6d",
                    font=dict(
                        color="#666666"
                    ),
                    y=0.02
                ),
                dict(
                    buttons=([
                        dict(
                            args=[{
                                    'mapbox.zoom': 10.5,
                                    'mapbox.center.lon': lon_BRONX,
                                    'mapbox.center.lat': lat_BRONX,
                                    'mapbox.bearing': 0,
                                    'mapbox.style': map_style, # Define the map style
                                }],
                            label='Bronx',
                            method='relayout'
                        ),
                        dict(
                            args=[{
                                    'mapbox.zoom': 10.5,
                                    'mapbox.center.lon': lon_BROOKLYN,
                                    'mapbox.center.lat': lat_BROOKLYN,
                                    'mapbox.bearing': 0,
                                    'mapbox.style': map_style, # Define the map style
                                }],
                            label='Brooklyn',
                            method='relayout'
                        ),
                        dict(
                            args=[{
                                    'mapbox.zoom': 10.5,
                                    'mapbox.center.lon': lon_MANHATTAN,
                                    'mapbox.center.lat': lat_MANHATTAN,
                                    'mapbox.bearing': 0,
                                    'mapbox.style': map_style, # Define the map style
                                }],
                            label='Manhattan',
                            method='relayout'
                        ),
                        dict(
                            args=[{
                                    'mapbox.zoom': 10.5,
                                    'mapbox.center.lon': lon_QUEENS,
                                    'mapbox.center.lat': lat_QUEENS,
                                    'mapbox.bearing': 0,
                                    'mapbox.style': map_style, # Define the map style
                                }],
                            label='Queens',
                            method='relayout'
                        ),
                        dict(
                            args=[{
                                    'mapbox.zoom': 10.5,
                                    'mapbox.center.lon': lon_STATEN_ISLAND,
                                    'mapbox.center.lat': lat_STATEN_ISLAND,
                                    'mapbox.bearing': 0,
                                    'mapbox.style': map_style, # Define the map style
                                }],
                            label='Staten Island',
                            method='relayout'
                        )
                    ]),
                    direction="down",
                    pad={'r': 0, 't': 0, 'b': 0, 'l': 0},
                    showactive=False,
                    bgcolor="rgb(32,31,30, 0)",
                    type='buttons',
                    yanchor='bottom',
                    xanchor='left',
                    font=dict(
                        color="#666666"
                    ),
                    x=0,
                    y=0.05
                )
            ]
        )
    )
    return(figure)
    
# Create a permits map display on it for last months
def permits_map_filter(df_permits, filter_period):
    # Mapbox
    mapbox_access_token = 'pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w' # noqa: E501

    # Global options
    #df_permits = data_SAMPLE.copy()
    # Need to define how many days the permit is issued for
    df_permits['permit_issuance_date'] = pd.to_datetime(df_permits['permit_issuance_date'], errors='coerce')
    df_permits['permit_expiration_date'] = pd.to_datetime(df_permits['permit_expiration_date'], errors='coerce')       
    
    # Need to calculate number of permit days
    df_permits['permit_days'] = df_permits['permit_expiration_date'] - df_permits['permit_issuance_date']   
    
    # Need to find the most recent permits that were issued
    df_permits['now_issued_date_difference'] = datetime.now() - df_permits['permit_issuance_date']

    df_permits['now_issued_date_difference'] = df_permits['now_issued_date_difference'].dt.days
    
    # Need to filter
    #filter_period = '7'
    df_permits = df_permits[df_permits['now_issued_date_difference'] <= int(filter_period)]
    

    # Need to change date fromat to MM/DD/YYYY
    #df_permits['permit_issuance_date'] = df_permits['permit_issuance_date'].dt.strftime('%m/%d/%Y')
    #df_permits['permit_expiration_date'] = df_permits['permit_expiration_date'].dt.strftime('%m/%d/%Y')
    
    df_permits['permit_issuance_date'] = df_permits['permit_issuance_date'].astype(str)
    df_permits['permit_expiration_date'] = df_permits['permit_expiration_date'].astype(str)

    zoom = 9
    latInitial = df_permits['latitude_wgs84'].mean()
    lonInitial = df_permits['longitude_wgs84'].mean()
    
    lat_BRONX = df_permits[df_permits['borough'] == 'BRONX']['latitude_wgs84'].mean()
    lon_BRONX = df_permits[df_permits['borough'] == 'BRONX']['longitude_wgs84'].mean()
    
    lat_BROOKLYN = df_permits[df_permits['borough'] == 'BROOKLYN']['latitude_wgs84'].mean()
    lon_BROOKLYN = df_permits[df_permits['borough'] == 'BROOKLYN']['longitude_wgs84'].mean()  
    
    lat_MANHATTAN = df_permits[df_permits['borough'] == 'MANHATTAN']['latitude_wgs84'].mean()
    lon_MANHATTAN = df_permits[df_permits['borough'] == 'MANHATTAN']['longitude_wgs84'].mean()      
    
    lat_QUEENS = df_permits[df_permits['borough'] == 'QUEENS']['latitude_wgs84'].mean()
    lon_QUEENS = df_permits[df_permits['borough'] == 'QUEENS']['longitude_wgs84'].mean() 
    
    lat_STATEN_ISLAND = df_permits[df_permits['borough'] == 'STATEN ISLAND']['latitude_wgs84'].mean()
    lon_STATEN_ISLAND = df_permits[df_permits['borough'] == 'STATEN ISLAND']['longitude_wgs84'].mean()     
    
    bearing = 0
    map_style = 'satellite-streets' #options are: ['satellite-streets', 'satellite', 'dark',  'outdoors', 'streets']

    # Need to define color dictionary based on permit length  
    permit_color = [{'1 Day': 'rgb(0,128,0)',  # Green
                     '<= 1 Week': 'rgb(173,255,47)', # Green Yellow
                     '<= 1 Month': 'rgb(255,255,51)', # Light Yellow
                     '<= 6 Months': 'rgb(255,140,0)', # Dark Orange
                     '> 6 Months': 'rgb(139,0,0)',  # Dark Red
                     'Error': 'rgb(69,10,243)'}]
    permit_color = pd.DataFrame(permit_color)
    
    # Need to define color based on permit length
    df_permits['permit_length'] = 'Error'
    df_permits['permit_length'].loc[df_permits['permit_days'].dt.days == 1] = '1 Day'
    df_permits['permit_length'].loc[(df_permits['permit_days'].dt.days > 1) & (df_permits['permit_days'].dt.days <= 7)] = '<= 1 Week'
    df_permits['permit_length'].loc[(df_permits['permit_days'].dt.days > 7) & (df_permits['permit_days'].dt.days <= 30)] = '<= 1 Month'
    df_permits['permit_length'].loc[(df_permits['permit_days'].dt.days > 30) & (df_permits['permit_days'].dt.days <= 180)] = '<= 6 Months'
    df_permits['permit_length'].loc[df_permits['permit_days'].dt.days > 180] = '> 6 Months'
    
    df_permits['permit_days'] =  df_permits['permit_days'].dt.days.astype(str)
    
    # Map figure
    figure = go.Figure(
        data=Data([
            Scattermapbox(
  
                lat = df_permits[df_permits['permit_length'] == i]['latitude_wgs84'],
                lon = df_permits[df_permits['permit_length'] == i]['longitude_wgs84'],
                customdata = df_permits[df_permits['permit_length'] == i]['building_id'],
                hoverinfo = "text",
                text = 'Building ID:' + df_permits[df_permits['permit_length'] == i]['building_id'] + '<br>' \
                        + 'Address: ' + df_permits[df_permits['permit_length'] == i]['permit_address'] + '<br>' \
                        + 'Permit Issued: ' + df_permits[df_permits['permit_length'] == i]['permit_issuance_date']  + '<br>' \
                        + 'Permit Expiration: ' + df_permits[df_permits['permit_length'] == i]['permit_expiration_date']  + '<br>' \
                        + 'Permit length: ' + df_permits[df_permits['permit_length'] == i]['permit_days'] + ' days <br>' \
                        + 'Permit Description: ' + df_permits[df_permits['permit_length'] == i]['permit_type_description']  + '<br>' \
                        + 'Permit Source: ' + df_permits[df_permits['permit_length'] == i]['source'],
                mode = 'markers',
                marker=dict(
                    size = 15,
                    color = permit_color[i][0],
                    opacity=0.7
                ),
                name=i
                ) for i in df_permits['permit_length'].unique() 
                       
            #),
        ]),
        layout=Layout(
            autosize=True,
            height=850,
            margin=Margin(l=0, r=0, t=40, b=0),
            showlegend=True,
            font=dict(color='#f7f7f7'),
            titlefont=dict(color='#f7f7f7', size='20'),
            hovermode='closest',
            plot_bgcolor='#191A1A',
            paper_bgcolor='#191A1A',
            legend=dict(font=dict(size=10), orientation='v'),
            title='Satellite Overview',
            mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(
                    lat=latInitial, # 40.7272
                    lon=lonInitial # -73.991251
                ),
                style=map_style, # Define the map style
                bearing=bearing,
                zoom=zoom
            ),
            updatemenus=[
                dict(
                    buttons=([
                        dict(
                            args=[{
                                    'mapbox.zoom': 9,
                                    'mapbox.center.lon': lonInitial,
                                    'mapbox.center.lat': latInitial, 
                                    'mapbox.bearing': 0,
                                    'mapbox.style': map_style, # Define the map style
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
                    bgcolor='rgb(32,31,30, 0)',
                    borderwidth=1,
                    bordercolor="#6d6d6d",
                    font=dict(
                        color="#666666"
                    ),
                    y=0.02
                ),
                dict(
                    buttons=([
                        dict(
                            args=[{
                                    'mapbox.zoom': 10.5,
                                    'mapbox.center.lon': lon_BRONX,
                                    'mapbox.center.lat': lat_BRONX,
                                    'mapbox.bearing': 0,
                                    'mapbox.style': map_style, # Define the map style
                                }],
                            label='Bronx',
                            method='relayout'
                        ),
                        dict(
                            args=[{
                                    'mapbox.zoom': 10.5,
                                    'mapbox.center.lon': lon_BROOKLYN,
                                    'mapbox.center.lat': lat_BROOKLYN,
                                    'mapbox.bearing': 0,
                                    'mapbox.style': map_style, # Define the map style
                                }],
                            label='Brooklyn',
                            method='relayout'
                        ),
                        dict(
                            args=[{
                                    'mapbox.zoom': 10.5,
                                    'mapbox.center.lon': lon_MANHATTAN,
                                    'mapbox.center.lat': lat_MANHATTAN,
                                    'mapbox.bearing': 0,
                                    'mapbox.style': map_style, # Define the map style
                                }],
                            label='Manhattan',
                            method='relayout'
                        ),
                        dict(
                            args=[{
                                    'mapbox.zoom': 10.5,
                                    'mapbox.center.lon': lon_QUEENS,
                                    'mapbox.center.lat': lat_QUEENS,
                                    'mapbox.bearing': 0,
                                    'mapbox.style': map_style, # Define the map style
                                }],
                            label='Queens',
                            method='relayout'
                        ),
                        dict(
                            args=[{
                                    'mapbox.zoom': 10.5,
                                    'mapbox.center.lon': lon_STATEN_ISLAND,
                                    'mapbox.center.lat': lat_STATEN_ISLAND,
                                    'mapbox.bearing': 0,
                                    'mapbox.style': map_style, # Define the map style
                                }],
                            label='Staten Island',
                            method='relayout'
                        )
                    ]),
                    direction="down",
                    pad={'r': 0, 't': 0, 'b': 0, 'l': 0},
                    showactive=False,
                    bgcolor="rgb(32,31,30, 0)",
                    type='buttons',
                    yanchor='bottom',
                    xanchor='left',
                    font=dict(
                        color="#666666"
                    ),
                    x=0,
                    y=0.05
                )
            ]
        )
    )
    return(figure)    

# Create a permits map display on it
def permits_map_v1(df_permits):
    # Mapbox
    mapbox_access_token = 'pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w' # noqa: E501

    # Global options
   
    # Need to change date fromat to MM/DD/YYYY
    df_permits['permit_issuance_date'] = df_permits['permit_issuance_date'].dt.strftime('%m/%d/%Y')
    df_permits['permit_expiration_date'] = df_permits['permit_expiration_date'].dt.strftime('%m/%d/%Y')
    
    df_permits['permit_issuance_date'] = df_permits['permit_issuance_date'].astype(str)
    df_permits['permit_expiration_date'] = df_permits['permit_expiration_date'].astype(str)

    zoom = 9
    latInitial = df_permits['latitude_wgs84'].mean()
    lonInitial = df_permits['longitude_wgs84'].mean()
    
    lat_BRONX = df_permits[df_permits['borough'] == 'BRONX']['latitude_wgs84'].mean()
    lon_BRONX = df_permits[df_permits['borough'] == 'BRONX']['longitude_wgs84'].mean()
    
    lat_BROOKLYN = df_permits[df_permits['borough'] == 'BROOKLYN']['latitude_wgs84'].mean()
    lon_BROOKLYN = df_permits[df_permits['borough'] == 'BROOKLYN']['longitude_wgs84'].mean()  
    
    lat_MANHATTAN = df_permits[df_permits['borough'] == 'MANHATTAN']['latitude_wgs84'].mean()
    lon_MANHATTAN = df_permits[df_permits['borough'] == 'MANHATTAN']['longitude_wgs84'].mean()      
    
    lat_QUEENS = df_permits[df_permits['borough'] == 'QUEENS']['latitude_wgs84'].mean()
    lon_QUEENS = df_permits[df_permits['borough'] == 'QUEENS']['longitude_wgs84'].mean() 
    
    lat_STATEN_ISLAND = df_permits[df_permits['borough'] == 'STATEN ISLAND']['latitude_wgs84'].mean()
    lon_STATEN_ISLAND = df_permits[df_permits['borough'] == 'STATEN ISLAND']['longitude_wgs84'].mean()     
    
    bearing = 0
    map_style = 'satellite-streets' #options are: ['satellite-streets', 'satellite', 'dark',  'outdoors', 'streets']

    # Map figure
    figure = go.Figure(
        data=Data([
            Scattermapbox(
                lat = df_permits['latitude_wgs84'],
                lon = df_permits['longitude_wgs84'],
                customdata = df_permits['building_id'],
                mode = 'markers',
                marker=dict(
                    size=17,
                    color='rgb(127, 216, 19)',
                    opacity=0.7
                ),
                hoverinfo = "text",
                text = 'Building ID:' + df_permits['building_id'] + '<br>' \
                        + 'Address: ' + df_permits['permit_address'] + '<br>' \
                        + 'Permit Issued: ' + df_permits['permit_issuance_date']  + '<br>' \
                        + 'Permit Expiration: ' + df_permits['permit_expiration_date']  + '<br>' \
                        + 'Permit Description: ' + df_permits['permit_type_description']  + '<br>' \
                        + 'Permit Source: ' + df_permits['source']
                        
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
                style=map_style, # Define the map style
                bearing=bearing,
                zoom=zoom
            ),
            updatemenus=[
                dict(
                    buttons=([
                        dict(
                            args=[{
                                    'mapbox.zoom': 9,
                                    'mapbox.center.lon': lonInitial,
                                    'mapbox.center.lat': latInitial, 
                                    'mapbox.bearing': 0,
                                    'mapbox.style': map_style, # Define the map style
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
                                    'mapbox.zoom': 10.5,
                                    'mapbox.center.lon': lon_BRONX,
                                    'mapbox.center.lat': lat_BRONX,
                                    'mapbox.bearing': 0,
                                    'mapbox.style': map_style, # Define the map style
                                }],
                            label='Bronx',
                            method='relayout'
                        ),
                        dict(
                            args=[{
                                    'mapbox.zoom': 10.5,
                                    'mapbox.center.lon': lon_BROOKLYN,
                                    'mapbox.center.lat': lat_BROOKLYN,
                                    'mapbox.bearing': 0,
                                    'mapbox.style': map_style, # Define the map style
                                }],
                            label='Brooklyn',
                            method='relayout'
                        ),
                        dict(
                            args=[{
                                    'mapbox.zoom': 10.5,
                                    'mapbox.center.lon': lon_MANHATTAN,
                                    'mapbox.center.lat': lat_MANHATTAN,
                                    'mapbox.bearing': 0,
                                    'mapbox.style': map_style, # Define the map style
                                }],
                            label='Manhattan',
                            method='relayout'
                        ),
                        dict(
                            args=[{
                                    'mapbox.zoom': 10.5,
                                    'mapbox.center.lon': lon_QUEENS,
                                    'mapbox.center.lat': lat_QUEENS,
                                    'mapbox.bearing': 0,
                                    'mapbox.style': map_style, # Define the map style
                                }],
                            label='Queens',
                            method='relayout'
                        ),
                        dict(
                            args=[{
                                    'mapbox.zoom': 10.5,
                                    'mapbox.center.lon': lon_STATEN_ISLAND,
                                    'mapbox.center.lat': lat_STATEN_ISLAND,
                                    'mapbox.bearing': 0,
                                    'mapbox.style': map_style, # Define the map style
                                }],
                            label='Staten Island',
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

################################### D A S H  L A Y O U T ######################

app = dash.Dash()

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

author = '''**Developer:** Duubar Villalobos Jimenez.
        >>
        **Final Project:** Knowledge and Visual Analytics (Multi Agency Permits in NYC).
        >>
        **Master in data science:** CUNY SPS, Data 608.
        >>
        **Period:** Spring 2018.
        >>
        **Contact:** [mydvtech@gmail.com](mailto:mydvtech@gmail.com)
        >>
        **github:** /dvillalobos   **docker:** /dvillalobos   **linkedin:** Duubar Villalobos.
    '''

app.title='Exploring NYC Permits'

# Describe the layout
app.layout = html.Div(children=[

    html.Div([
        # Main Graphs section
        html.Div([

            # By Location
            html.Div([
                    html.H1(children="Exploring NYC Permits"),
            ], className='Title', style={'text-align': 'center', 'margin-bottom': '15px'}),

            # Pick date range
            #html.Div([
            #    dcc.DatePickerRange(
            #        id='date-picker-range',
            #        start_date=dt(2016, 12, 1),
            #        end_date='Select a date!'
            #    ), 
            #], className='Title', style={'text-align': 'center', 'margin-bottom': '15px'}),            
                                       
            # Total Summary
            html.Div([
 
                dcc.Markdown(id='total-sumary',children=get_total_permits_summary(data_SAMPLE).replace('  ', ''), className='eight columns offset-by-two'),
                dcc.Markdown(id='borough-sumary',children=get_borough_permits_summary(data_SAMPLE).replace('  ', ''), className='eight columns offset-by-two'),
            ], className='row', style={'text-align': 'center', 'margin-bottom': '15px'}),


                            
## First Block
            # NYC Permits Bar Charts
            html.Div([
                html.Div([
                    # NYC Permits by Borough
                    html.Div(
                        [
                            dcc.Graph(id='bar-chart-borough', figure=bar_chart_permits_borough(data_SAMPLE)),
                        ],
                        className='four columns',
                        style={'margin-top': '20'}
                    ),
                    # NYC Permits Separator
                    html.Div(
                        [
                                dcc.Graph(id='pie-chart-days', figure=pie_chart_permits_by_day(data_SAMPLE)),
                        ],
                        className='four columns',
                        style={'margin-top': '20'}
                    ),
                    # NYC Permits by Permit Length
                    html.Div(
                        [
                            dcc.Graph(id='bar-chart-length', figure=bar_chart_permits_length(data_SAMPLE)),
                        ],
                        className='four columns',
                        style={'margin-top': '20'}
                    ),
                ], className='twelve columns'),
            ], className='row', style={'text-align': 'center', 'margin-bottom': '15px'}),


## Second Block
            # Time Series by Day Chart Summary
            html.Div([
                html.Div([
                    html.Div(
                        [
                            dcc.Markdown(id='question-1-table-1',
                                         children='**Question:** Which day had the highest number of permits issued?'.replace('  ', ''), 
                                         className='twelve columns'
                                         ), 
                            html.Br([]),
                            html.Br([]),
                            dte.DataTable(
                                id='time_series_table_permits_by_day_top5',
                                rows=time_series_table_permits_by_day_long_chart(data_SAMPLE),
                                row_selectable=False,
                                filterable=False,
                                sortable=False,
                                min_height=212,
                                min_width=350,
                                editable=False,
                            )
                            ],
                        className='four columns', style={'text-align': 'left', 'margin-top': '75px'}
                    ),
                    html.Div(
                        [
                            dcc.Graph(id='time-series-by-day-chart', figure=time_series_plot_permits_by_day_long_chart(data_SAMPLE)),
                        ],
                        className='eight columns', style={'text-align': 'center', 'margin-bottom': '15px'}
                    ),                        
                ], className='twelve columns'),
            ], className='row', style={'text-align': 'center', 'margin-bottom': '15px',  'margin-left': '50px'}),

           
            
 
## Third Block
            # Time Series by Month Chart Summary
            html.Div([
                html.Div([
                    html.Div(
                        [
                            dcc.Markdown(id='question-2-table-2',
                                         children='**Question:** Which month had the highest number of permits issued?'.replace('  ', ''), 
                                         className='twelve columns'
                                         ), 
                            html.Br([]),
                            html.Br([]),
                            dte.DataTable(
                                id='time_series_table_permits_by_month_top5',
                                rows=time_series_table_permits_by_month_long_chart(data_SAMPLE),
                                row_selectable=False,
                                filterable=False,
                                sortable=False,
                                min_height=212,
                                min_width=350,
                                editable=False,
                            )
                            ],
                        className='four columns', style={'table-align': 'right','text-align': 'left', 'margin-top': '75px'}
                    ),  
                    html.Div(
                        [
                            dcc.Graph(id='time-series-by-month-chart', figure=time_series_plot_permits_by_month_long_chart(data_SAMPLE)),
                        ],
                        className='eight columns', style={'text-align': 'center', 'margin-bottom': '15px'}
                    ),                        

                ], className='twelve columns'),
            ], className='row', style={'text-align': 'center', 'margin-bottom': '15px',  'margin-left': '50px'}),

            ###################################################################
            
            
## Fourth Block
            # Heat Map Month vs Day Chart Summary
            html.Div([
                html.Div([
                    html.Div(
                        [
                            dcc.Markdown(id='question-3-table-3',
                                         children='**Question:** Which day of the week had the highest number of permits issued and which month?'.replace('  ', ''), 
                                         className='twelve columns'
                                         ), 
                            html.Br([]),
                            html.Br([]),
                            html.Br([]),                            
                            dte.DataTable(
                                id='heat-map-weekday-month_top5',
                                rows=heat_map_table_weekday_month_chart(data_SAMPLE),
                                row_selectable=False,
                                filterable=False,
                                sortable=False,
                                min_height=212,
                                min_width=350,
                                editable=False,
                            )
                            ],
                        className='four columns', style={'text-align': 'left', 'margin-top': '75px'}
                    ),
                    html.Div(
                        [
                            dcc.Graph(id='heat-map-weekday-month', figure=heat_map_permits_weekday_month_chart(data_SAMPLE)),
                        ],
                        className='eight columns', style={'text-align': 'center', 'margin-bottom': '15px'}
                    ),                        
                ], className='twelve columns'),
            ], className='row', style={'text-align': 'center', 'margin-bottom': '15px',  'margin-left': '50px'}),


## Fift Block
            # Time Series by Month Chart Summary
            html.Div([
                html.Div([
                    # NYC Permits by Borough
                    html.Div(
                        [
                            dcc.Markdown(id='question-4-table-4',
                                         children='**Question:** Which day of the month had the highest number of permits issued and which month?'.replace('  ', ''), 
                                         className='twelve columns'
                                         ), 
                            html.Br([]),
                            html.Br([]),
                            html.Br([]),                             
                            dte.DataTable(
                                id='heat_map_permits_day_month_top5',
                                rows=heat_map_table_day_month_chart(data_SAMPLE),
                                row_selectable=False,
                                filterable=False,
                                sortable=False,
                                min_height=212,
                                min_width=350,
                                editable=False,
                            )
                            ],
                        className='four columns', style={'table-align': 'right','text-align': 'left', 'margin-top': '75px'}
                    ),
                        
                    html.Div(
                        [
                            dcc.Graph(id='heat-map-day-month', figure=heat_map_permits_day_month_chart(data_SAMPLE)),
                        ],
                        className='eight columns', style={'text-align': 'center', 'margin-bottom': '15px'}
                    ),
                ], className='twelve columns'),
            ], className='row', style={'text-align': 'center', 'margin-bottom': '15px',  'margin-left': '50px'}),


## sixth Block
            # Heat Map Year vs Day Chart Summary
            html.Div([
                html.Div([
                    html.Div(
                        [
                            dcc.Markdown(id='question-5-table-5',
                                         children='**Question:** Which day of the month had the highest number of permits issued and which year?'.replace('  ', ''), 
                                         className='twelve columns'
                                         ), 
                            html.Br([]),
                            html.Br([]),
                            html.Br([]),                            
                            dte.DataTable(
                                id='heat-map-monthday_year_top5',
                                rows=heat_map_table_monthday_year_chart(data_SAMPLE),
                                row_selectable=False,
                                filterable=False,
                                sortable=False,
                                min_height=212,
                                min_width=350,
                                editable=False,
                            )
                            ],
                        className='four columns', style={'text-align': 'left', 'margin-top': '75px'}
                    ),
                    html.Div(
                        [
                            dcc.Graph(id='heat-map-monthday-year', figure=heat_map_permits_monthday_year_chart(data_SAMPLE)),
                        ],
                        className='eight columns', style={'text-align': 'center', 'margin-bottom': '15px'}
                    ),                        
                ], className='twelve columns'),
            ], className='row', style={'text-align': 'center', 'margin-bottom': '15px',  'margin-left': '50px'}),


## Seventh Block
            # Heat Map Year vs Month Chart Summary
            html.Div([
                html.Div([
                    html.Div(
                        [
                            dcc.Markdown(id='question-6-table-6',
                                         children='**Question:** Which month had the highest number of permits issued and which year?'.replace('  ', ''), 
                                         className='twelve columns'
                                         ), 
                            html.Br([]),
                            html.Br([]),
                            html.Br([]),                             
                            dte.DataTable(
                                id='heat_map_permits_month_year_top5',
                                rows=heat_map_table_month_year_chart(data_SAMPLE),
                                row_selectable=False,
                                filterable=False,
                                sortable=False,
                                min_height=212,
                                min_width=350,
                                editable=False,
                            )
                            ],
                        className='four columns', style={'table-align': 'right','text-align': 'left', 'margin-top': '75px'}
                    ),                        
                    html.Div(
                        [
                            dcc.Graph(id='heat-map-month-year', figure=heat_map_permits_month_year_chart(data_SAMPLE)),
                        ],
                        className='eight columns', style={'text-align': 'center', 'margin-bottom': '15px'}
                    ),
                ], className='twelve columns'),
            ], className='row', style={'text-align': 'center', 'margin-bottom': '15px',  'margin-left': '50px'}),

## Eigth Block
            # Heat Map City vs Permit Type Chart Summary
            html.Div([
                html.Div([
                    html.Div(
                        [
                            dcc.Markdown(id='question-7-table-7',
                                         children='**Question:** Which permit type has been issued the most and in what city?'.replace('  ', ''), 
                                         className='twelve columns'
                                         ), 
                            html.Br([]),
                            html.Br([]),                            
                            dte.DataTable(
                                id='heat_map_permits_city_permit_type_top5',
                                rows=heat_map_table_city_permit_type_chart(data_SAMPLE),
                                row_selectable=False,
                                filterable=False,
                                sortable=False,
                                min_height=212,
                                min_width=350,
                                editable=False,
                            )
                            ],
                        className='four columns', style={'table-align': 'right','text-align': 'left', 'margin-top': '75px'}
                    ),                        
                    html.Div(
                        [
                            dcc.Graph(id='heat-map-city-permit-type', figure=heat_map_permits_city_permit_type_chart(data_SAMPLE)),
                        ],
                        className='eight columns', style={'text-align': 'center', 'margin-bottom': '15px'}
                    ),
                ], className='twelve columns'),
            ], className='row', style={'text-align': 'center', 'margin-bottom': '15px',  'margin-left': '50px'}),

## 9th Block
            # Heat Map Source vs Permit Type Chart Summary
            html.Div([
                html.Div([
                    html.Div(
                        [
                            dcc.Markdown(id='question-8-table-8',
                                         children='**Question:** Which permit type has been issued the most and by which department?'.replace('  ', ''), 
                                         className='twelve columns'
                                         ), 
                            html.Br([]),
                            html.Br([]),    
                            html.Br([]), 
                            dte.DataTable(
                                id='heat_map_permits_source_permit_type_top5',
                                rows=heat_map_table_source_permit_type_chart(data_SAMPLE),
                                row_selectable=False,
                                filterable=False,
                                sortable=False,
                                min_height=212,
                                min_width=350,
                                editable=False,
                            ),
                            html.Br([]),         
                            dcc.Markdown(children='**DOB:** New York City Department of Buildings.'.replace('  ', '')),
                            dcc.Markdown(children='**DOHMH:** New York City Department of Health and Mental Hygiene.'.replace('  ', '')),                            
                            ],
                        className='four columns', style={'table-align': 'right','text-align': 'left', 'margin-top': '75px'}
                    ),                        
                    html.Div(
                        [
                            dcc.Graph(id='heat-map-source-permit-type', figure=heat_map_permits_source_permit_type_chart(data_SAMPLE)),
                        ],
                        className='eight columns', style={'text-align': 'center', 'margin-bottom': '15px'}
                    ),
                ], className='twelve columns'),
            ], className='row', style={'text-align': 'center', 'margin-bottom': '15px',  'margin-left': '50px'}),


## 10th Block

            # Heat Map City vs Permit Type Chart Summary
            html.Div([
                html.Div([
                    html.Div(
                        [
                            dcc.Markdown(id='question-9-table-9',
                                         children='**Question:** Which city has the most permits issued and by which department?'.replace('  ', ''), 
                                         className='twelve columns'
                                         ), 
                            html.Br([]),
                            html.Br([]),    
                            html.Br([]), 
                            dte.DataTable(
                                id='heat_map_permits_city_permit_source_top5',
                                rows=heat_map_table_city_permit_source_chart(data_SAMPLE),
                                row_selectable=False,
                                filterable=False,
                                sortable=False,
                                min_height=212,
                                min_width=350,
                                editable=False,
                            ),
                            html.Br([]),         
                            #dcc.Markdown(children='**DOB:** New York City Department of Buildings.'.replace('  ', '')),
                            #dcc.Markdown(children='**DOHMH:** New York City Department of Health and Mental Hygiene.'.replace('  ', '')),                            
                            ],
                        className='four columns', style={'table-align': 'right','text-align': 'left', 'margin-top': '75px'}
                    ),                        
                    html.Div(
                        [
                            dcc.Graph(id='heat-map-city-permit-source', figure=heat_map_permits_city_permit_source_chart(data_SAMPLE)),
                        ],
                        className='eight columns', style={'text-align': 'center', 'margin-bottom': '15px'}
                    ),
                ], className='twelve columns'),
            ], className='row', style={'text-align': 'center', 'margin-bottom': '15px',  'margin-left': '50px'}),

## 11th Block

            # Heat Map Permit Holder vs Permit Type Chart Summary
            html.Div([
                html.Div([
                    html.Div(
                        [
                            dcc.Markdown(id='question-10-table-10',
                                         children='**Question:** Which company has the most permits issued and which type?'.replace('  ', ''), 
                                         className='twelve columns'
                                         ), 
                            html.Br([]),
                            html.Br([]),    
                            html.Br([]), 
                            dte.DataTable(
                                id='heat_map_permits_holder_permit_type_top5',
                                rows=heat_map_table_holder_permit_type_chart(data_SAMPLE),
                                row_selectable=False,
                                filterable=False,
                                sortable=False,
                                min_height=212,
                                min_width=350,
                                editable=False,
                            ),
                            html.Br([]),         
                            #dcc.Markdown(children='**DOB:** New York City Department of Buildings.'.replace('  ', '')),
                            #dcc.Markdown(children='**DOHMH:** New York City Department of Health and Mental Hygiene.'.replace('  ', '')),                            
                            ],
                        className='four columns', style={'table-align': 'right','text-align': 'left', 'margin-top': '75px'}
                    ),                        
                    html.Div(
                        [
                            dcc.Graph(id='heat-map-permit-holder-permit-type', figure=heat_map_permits_holder_permit_type_chart(data_SAMPLE)),
                        ],
                        className='eight columns', style={'text-align': 'center', 'margin-bottom': '15px'}
                    ),
                ], className='twelve columns'),
            ], className='row', style={'text-align': 'center', 'margin-bottom': '15px',  'margin-left': '50px'}),




            ###################################################################
 
         
            
            
            # Time Series by Day Chart Summary
            #html.Div([ 
            #    html.Div(
            #            [
            #                dcc.Graph(id='time-series-by-day-chart', figure=time_series_plot_permits_by_day_long_chart(data_SAMPLE)),
            #            ],
            #            className='eight columns offset-by-two',
            #            style={'margin-top': '20'}
            #        ),
            #], className='row', style={'text-align': 'center', 'margin-bottom': '15px'}),

            # Time Series by Month Chart Summary
            #html.Div([ 
            #    html.Div(
            #            [
            #                dcc.Graph(id='time-series-by-month-chart', figure=time_series_plot_permits_by_month_long_chart(data_SAMPLE)),
            #            ],
            #            className='eight columns offset-by-two',
            #            style={'margin-top': '20'}
            #        ),
            #], className='row', style={'text-align': 'center', 'margin-bottom': '15px'}),
  
            # Heat Map Month vs Day Chart Summary
            #html.Div([ 
            #    html.Div(
            #            [
            #                dcc.Graph(id='heat-map-weekday-month', figure=heat_map_permits_weekday_month_chart(data_SAMPLE)),
            #            ],
            #            className='eight columns offset-by-two',
            #            style={'margin-top': '20'}
            #        ),
            #], className='row', style={'text-align': 'center', 'margin-bottom': '15px'}),    
                
            # Heat Map Month vs Day Chart Summary
            #html.Div([ 
            #    html.Div(
            #            [
            #                dcc.Graph(id='heat-map-day-month', figure=heat_map_permits_day_month_chart(data_SAMPLE)),
            #            ],
            #            className='eight columns offset-by-two',
            #            style={'margin-top': '20'}
            #        ),
            #], className='row', style={'text-align': 'center', 'margin-bottom': '15px'}),       
                
            # Heat Map Year vs Day Chart Summary
            #html.Div([ 
            #    html.Div(
            #            [
            #                dcc.Graph(id='heat-map-monthday-year', figure=heat_map_permits_monthday_year_chart(data_SAMPLE)),
            #            ],
            #            className='eight columns offset-by-two',
            #            style={'margin-top': '20'}
            #        ),
            #], className='row', style={'text-align': 'center', 'margin-bottom': '15px'}),                  
                
            # Heat Map Year vs Month Chart Summary
            #html.Div([ 
            #    html.Div(
            #            [
            #                dcc.Graph(id='heat-map-month-year', figure=heat_map_permits_month_year_chart(data_SAMPLE)),
            #            ],
            #            className='eight columns offset-by-two',
            #            style={'margin-top': '20'}
            #        ),
            #], className='row', style={'text-align': 'center', 'margin-bottom': '15px'}),       

             # Heat Map City vs Permit Type Chart Summary
            #html.Div([ 
            #    html.Div(
            #            [
            #                dcc.Graph(id='heat-map-city-permit-type', figure=heat_map_permits_city_permit_type_chart(data_SAMPLE)),
            #            ],
            #            className='eight columns offset-by-two',
            #            style={'margin-top': '20'}
            #        ),
            #], className='row', style={'text-align': 'center', 'margin-bottom': '15px'}),   

             # Heat Map Source vs Permit Type Chart Summary
            #html.Div([ 
            #    html.Div(
            #            [
            #                dcc.Graph(id='heat-map-source-permit-type', figure=heat_map_permits_source_permit_type_chart(data_SAMPLE)),
            #            ],
            #            className='eight columns offset-by-two',
            #            style={'margin-top': '20'}
            #        ),
            #], className='row', style={'text-align': 'center', 'margin-bottom': '15px'}),   

             # Heat Map City vs Permit Type Chart Summary
            #html.Div([ 
            #    html.Div(
            #            [
            #                dcc.Graph(id='heat-map-city-permit-source', figure=heat_map_permits_city_permit_source_chart(data_SAMPLE)),
            #            ],
            #            className='eight columns offset-by-two',
            #            style={'margin-top': '20'}
            #        ),
            #], className='row', style={'text-align': 'center', 'margin-bottom': '15px'}),   

            # Heat Map Permit Holder vs Permit Type Chart Summary
            #html.Div([ 
            #    html.Div(
            #            [
            #                dcc.Graph(id='heat-map-permit-holder-permit-type', figure=heat_map_permits_holder_permit_type_chart(data_SAMPLE)),
            #            ],
            #            className='eight columns offset-by-two',
            #            style={'margin-top': '20'}
            #        ),
            #], className='row', style={'text-align': 'center', 'margin-bottom': '15px'}), 
 
            html.Br([]),
            
            html.Div([  
                dcc.Markdown(id='question-11-map-1',
                             children='**Question:** Can I see these locations in a map and visualize the length of the permit?'.replace('  ', ''), 
                             className='twelve columns'
                ), 
            ], className='row', style={'text-align': 'left', 'margin-bottom': '15px',  'margin-left': '50px'}),

            html.Br([]),
                            
             # NYC Permits Map - Filter
            html.Div([  
                    html.Div(
                    [                           
                        dcc.Dropdown(
                            id='permit-map-filter-dropdown',
                            options=[
                                {'label': 'Last 7 days', 'value': '7'},
                                {'label': 'Last 2 Weeks', 'value': '15'},
                                {'label': 'Last 3 Weeks', 'value': '21'},
                                {'label': 'Last Month', 'value': '30'},
                                {'label': 'Last 3 Months', 'value': '90'},
                                {'label': 'Last 6 Months', 'value': '180'},   
                                {'label': 'Last Year', 'value': '365'},
                                {'label': 'Last 2 Years', 'value': '730'},
                                {'label': 'All Years', 'value': '100000'},
                            ],
                            value='7',
                            clearable=False
                        ),
                    ],
                    className='two columns offset-by-five',
                    style={'margin-top': '20'}
                ),
                    
            ],className='row'),  
      
            # NYC Permits Map - Filter
            html.Div([
                # NYC Map
                html.Div(
                    [
                        dcc.Graph(id='permits-map-filter', figure=permits_map_filter(data_SAMPLE,7)),
                    ],
                    className='ten columns offset-by-one',
                    style={'margin-top': '20'}
                ),
            ],className='row'),  

        ]),
    ]),
                
    html.Br([]),
    html.Br([]),
    html.Br([]),
           
    # Developer
      
    html.H6('Copyright © Spring 2018 by Duubar Villalobos Jimenez. | \
            Final Project: Knowledge and Visual Analytics (Multi Agency Permits in NYC). | \
            Master in data science: CUNY SPS, Data 608. | \
            Contact: mydvtech@gmail.com github: /dvillalobos docker: /dvillalobos',
            className="gs-header gs-text-header padded", 
            style={'text-align': 'center', 'margin-bottom': '45px'}),         

])

################################### D A S H  F U N C T I O N S ################

# Filtering Permit issue date with Date picker

#Filter Section too slow!
"""
# Update total number of permits
@app.callback(
    dash.dependencies.Output('total-sumary', 'children'),
    [dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date')])
def update_total_sumary_output(start_date, end_date):
    
    global data_SAMPLE

    df_permits = data_SAMPLE.copy()
    
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    df_permits['permit_issuance_date'] = pd.to_datetime(df_permits['permit_issuance_date'], errors='coerce')
    
    if (start_date is not None) and (end_date is not None):
        df_permits = df_permits[(df_permits['permit_issuance_date'] >= start_date) & 
                                (df_permits['permit_issuance_date'] <= end_date)]
        
    return(get_total_permits_summary(df_permits))

# Update borough total number of permits
@app.callback(
    dash.dependencies.Output('borough-sumary', 'children'),
    [dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date')])
def update_borough_sumary_output(start_date, end_date):
    
    global data_SAMPLE

    df_permits = data_SAMPLE.copy()
    
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    df_permits['permit_issuance_date'] = pd.to_datetime(df_permits['permit_issuance_date'], errors='coerce')
    
    if (start_date is not None) and (end_date is not None):
        df_permits = df_permits[(df_permits['permit_issuance_date'] >= start_date) & 
                                (df_permits['permit_issuance_date'] <= end_date)]
        
    return(get_borough_permits_summary(df_permits))

# Update borough bar chart
@app.callback(
    dash.dependencies.Output('bar-chart-borough', 'figure'),
    [dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date')])
def update_output_borough_bar_chart(start_date, end_date):
    
    global data_SAMPLE

    df_permits = data_SAMPLE.copy()
    
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    df_permits['permit_issuance_date'] = pd.to_datetime(df_permits['permit_issuance_date'], errors='coerce')
    
    if (start_date is not None) and (end_date is not None):
        days = end_date - start_date
        if (days.days > 180):
            
            df_permits = df_permits[(df_permits['permit_issuance_date'] >= start_date) & 
                                    (df_permits['permit_issuance_date'] <= end_date)]
            
            return(bar_chart_permits_borough(df_permits))
        else: 
            return('')
    else: 
        return('')

# Update time-series-by-day-chart
@app.callback(
    dash.dependencies.Output('time-series-by-day-chart', 'figure'),
    [dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date')])
def update_output_ts_by_day(start_date, end_date):
    
    global data_SAMPLE

    df_permits = data_SAMPLE.copy()
    
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    df_permits['permit_issuance_date'] = pd.to_datetime(df_permits['permit_issuance_date'], errors='coerce')
    
    if (start_date is not None) and (end_date is not None):
        df_permits = df_permits[(df_permits['permit_issuance_date'] >= start_date) & 
                                (df_permits['permit_issuance_date'] <= end_date)]
     
    return(time_series_plot_permits_by_day_long_chart(df_permits))
    
# Update time-series-by-month-chart
@app.callback(
    dash.dependencies.Output('time-series-by-month-chart', 'figure'),
    [dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date')])
def update_output_ts_by_month(start_date, end_date):
    
    global data_SAMPLE

    df_permits = data_SAMPLE.copy()
    
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    df_permits['permit_issuance_date'] = pd.to_datetime(df_permits['permit_issuance_date'], errors='coerce')
    
    if (start_date is not None) and (end_date is not None):
        df_permits = df_permits[(df_permits['permit_issuance_date'] >= start_date) & 
                                (df_permits['permit_issuance_date'] <= end_date)]
        
    return(time_series_plot_permits_by_month_long_chart(df_permits))   

# Update heat-map-weekday-month
@app.callback(
    dash.dependencies.Output('heat-map-weekday-month', 'figure'),
    [dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date')])
def update_output_hm_by_weekday_month(start_date, end_date):
    
    global data_SAMPLE

    df_permits = data_SAMPLE.copy()
   
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    df_permits['permit_issuance_date'] = pd.to_datetime(df_permits['permit_issuance_date'], errors='coerce')
    
    if (start_date is not None) and (end_date is not None):
        df_permits = df_permits[(df_permits['permit_issuance_date'] >= start_date) & 
                                (df_permits['permit_issuance_date'] <= end_date)]
        
    return(heat_map_permits_weekday_month_chart(df_permits))
    
# Update heat-ma-by-day-month-chart
@app.callback(
    dash.dependencies.Output('heat-map-day-month', 'figure'),
    [dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date')])
def update_output_hm_by_day_month(start_date, end_date):
    
    global data_SAMPLE

    df_permits = data_SAMPLE.copy()
   
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    df_permits['permit_issuance_date'] = pd.to_datetime(df_permits['permit_issuance_date'], errors='coerce')
    
    if (start_date is not None) and (end_date is not None):
        df_permits = df_permits[(df_permits['permit_issuance_date'] >= start_date) & 
                                (df_permits['permit_issuance_date'] <= end_date)]
        
    return(heat_map_permits_day_month_chart(df_permits))    

# Update heat-ma-by-monthday-year-chart
@app.callback(
    dash.dependencies.Output('heat-map-monthday-year', 'figure'),
    [dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date')])
def update_output_hm_by_monthday_year(start_date, end_date):
    
    global data_SAMPLE

    df_permits = data_SAMPLE.copy()
   
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    df_permits['permit_issuance_date'] = pd.to_datetime(df_permits['permit_issuance_date'], errors='coerce')
    
    if (start_date is not None) and (end_date is not None):
        df_permits = df_permits[(df_permits['permit_issuance_date'] >= start_date) & 
                                (df_permits['permit_issuance_date'] <= end_date)]
        
    return(heat_map_permits_monthday_year_chart(df_permits))  

# Update heat-ma-by-month-year-chart
@app.callback(
    dash.dependencies.Output('heat-map-month-year', 'figure'),
    [dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date')])
def update_output_hm_by_month_year(start_date, end_date):
    
    global data_SAMPLE

    df_permits = data_SAMPLE.copy()
   
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    df_permits['permit_issuance_date'] = pd.to_datetime(df_permits['permit_issuance_date'], errors='coerce')
    
    if (start_date is not None) and (end_date is not None):
        df_permits = df_permits[(df_permits['permit_issuance_date'] >= start_date) & 
                                (df_permits['permit_issuance_date'] <= end_date)]
        
    return(heat_map_permits_month_year_chart(df_permits))  

# Update heat-map-by-city-permit-type-chart
@app.callback(
    dash.dependencies.Output('heat-map-city-permit-type', 'figure'),
    [dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date')])
def update_output_hm_by_city_permit_type(start_date, end_date):
    
    global data_SAMPLE

    df_permits = data_SAMPLE.copy()
   
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    df_permits['permit_issuance_date'] = pd.to_datetime(df_permits['permit_issuance_date'], errors='coerce')
    
    if (start_date is not None) and (end_date is not None):
        df_permits = df_permits[(df_permits['permit_issuance_date'] >= start_date) & 
                                (df_permits['permit_issuance_date'] <= end_date)]
        
    return(heat_map_permits_city_permit_type_chart(df_permits))  

# Update heat-map-by-source-permit-type-chart
@app.callback(
    dash.dependencies.Output('heat-map-source-permit-type', 'figure'),
    [dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date')])
def update_output_hm_by_source_permit_type(start_date, end_date):
    
    global data_SAMPLE

    df_permits = data_SAMPLE.copy()
   
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    df_permits['permit_issuance_date'] = pd.to_datetime(df_permits['permit_issuance_date'], errors='coerce')
    
    if (start_date is not None) and (end_date is not None):
        df_permits = df_permits[(df_permits['permit_issuance_date'] >= start_date) & 
                                (df_permits['permit_issuance_date'] <= end_date)]
        
    return(heat_map_permits_source_permit_type_chart(df_permits))  

# Update heat-map-by-city-permit-source-chart
@app.callback(
    dash.dependencies.Output('heat-map-city-permit-source', 'figure'),
    [dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date')])
def update_output_hm_by_city_permit_source(start_date, end_date):
    
    global data_SAMPLE

    df_permits = data_SAMPLE.copy()
   
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    df_permits['permit_issuance_date'] = pd.to_datetime(df_permits['permit_issuance_date'], errors='coerce')
    
    if (start_date is not None) and (end_date is not None):
        df_permits = df_permits[(df_permits['permit_issuance_date'] >= start_date) & 
                                (df_permits['permit_issuance_date'] <= end_date)]
        
    return(heat_map_permits_city_permit_source_chart(df_permits))  

# Update heat-map-by-holder-permit-type-chart
@app.callback(
    dash.dependencies.Output('heat-map-permit-holder-permit-type', 'figure'),
    [dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date')])
def update_output_hm_by_holder_permit_type(start_date, end_date):
    
    global data_SAMPLE

    df_permits = data_SAMPLE.copy()
   
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    df_permits['permit_issuance_date'] = pd.to_datetime(df_permits['permit_issuance_date'], errors='coerce')
    
    if (start_date is not None) and (end_date is not None):
        df_permits = df_permits[(df_permits['permit_issuance_date'] >= start_date) & 
                                (df_permits['permit_issuance_date'] <= end_date)]
        
    return(heat_map_permits_holder_permit_type_chart(df_permits))  

# Update permits-map
@app.callback(
    dash.dependencies.Output('permits-map', 'figure'),
    [dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date')])
def update_output_permits_map(start_date, end_date):
    
    global data_SAMPLE

    df_permits = data_SAMPLE.copy()
   
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    df_permits['permit_issuance_date'] = pd.to_datetime(df_permits['permit_issuance_date'], errors='coerce')
    
    if (start_date is not None) and (end_date is not None):
        df_permits = df_permits[(df_permits['permit_issuance_date'] >= start_date) & 
                                (df_permits['permit_issuance_date'] <= end_date)]
        
    return(permits_map(df_permits))  

""" 

# Update permits-map-filter
@app.callback(
    dash.dependencies.Output('permits-map-filter', 'figure'),
    [dash.dependencies.Input('permit-map-filter-dropdown', 'value')])
def update_output_permits_map_filter(value):
    
    global data_SAMPLE

    df_permits = data_SAMPLE.copy()
 
    return(permits_map_filter(df_permits, value )) 
    
################################### E X T E R N A L  C A L L S ################

# External css
external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "//fonts.googleapis.com/css?family=Dosis:Medium",
                "//fonts.googleapis.com/css?family=Tangerine:Medium",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/62f0eb4f1fadbefea64b2404493079bf848974e8/dash-uber-ride-demo.css",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
                #"https://codepen.io/bcd/pen/KQrXdb.css",
                'https://cdn.rawgit.com/chriddyp/0247653a7c52feb4c48437e1c1837f75/raw/a68333b876edaf62df2efa7bac0e9b3613258851/dash.css']

for css in external_css:
    app.css.append_css({"external_url": css})

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
