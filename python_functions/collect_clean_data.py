"""
Data can be downloaded at the following links:

Government Health Data

U.S. Census Data

NOAA Data


Please put all data into the folder ../data for functions to work
"""
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')
%matplotlib inline
import scipy.stats as stats
import numpy as np

def read_in_heart_data():
    # Returns a list that contains all of the data frames saved as pandas.Dataframe objects
    heart_data = []

    # CSV files must be renamed to the format "heart_dis_<year of data>.csv" to be loaded this way
    for num in range(2013, 2019):
        df = pd.read_csv(f'../data/heart_dis_{num}.csv')
        df[f'{num}_mort_per_100k'] = df['Data_Value']

        # We are only interested in certain columns for every year
        if num != 2013:
            data_frames.append(df[[f'{num}_mort_per_100k', 
                               'LocationID', 'Stratification1', 'Stratification2', 'GeographicLevel']])
        else:
            data_frames.append(df)

    return heart_data

def remove_unwanted(df_list):
    # Removes columns and rows that we are not going to need
    cleaned = []
    for df in df_list:
        temp = df[(df['Stratification1'] == 'Overall') 
              & (df['Stratification2'] == 'Overall') 
              & (df['GeographicLevel'] == 'County')]
        temp = temp.drop(columns=['Stratification1', 'Stratification2', 'GeographicLevel'])
        cleaned.append(temp)
    
    return cleaned

def merge_health_data(df_list):
    # Merge all of the health data and return it in one panda.Dataframe object
    heath_data = df_list[0]
    
    for i in range(6):
        health_data = pd.merge(health_data, df_list[i], on='LocationID', how='inner')
    
    return health_data

