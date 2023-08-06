'''Nicolas Trinephi - acse-nt719

Utility modules

This module contains necessary imports for the VFM_Main file. This file requires all libraries from
requirements.txt to be installed on the cluster.

Contains utils class and InputError class
'''

import numpy as np
import copy
import datetime
import math

# data loading
from pyspark.sql.types import *
from pyspark.sql.functions import col
import pandas as pd

# interactive plotting
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as pyo
import panel as pn
import hvplot
import hvplot.pandas
import holoviews as hv
import panel as pn

class utils:
  '''
  Class with utility functions that are all public.
  
  Methods:
    list_flat() lambda function
      flattens a list
    list_deep() lambda fuinction
      nests elements of a list
    to_pandas(df_list)
      Converts PySpark DataFrame to Pandas DataFrame
    re_writer(file)
      Rewrites data file removing and editing unusable text
    dynamic_filter(df, bin_size, col_name, r_lim)
      Smoothens the curve of the data within df[col_name]
    find_well(well_name, day, month, test)
      Find dataframes of well named well_name
    keep_param(day, month, test)
      Keep useful paramters for the LSTM model
    un_accum(month)
      calculates and adds columns for the unaccumulated rates in monthly historic data
    nan_exc(df_day, df_month, df_test)
      Clears data that are out of the limits set after quality control
    rmv_exc(target, *args)
      Removes 0 values of the rates
    hf_prep_input(high_freq)
      Merges high frequency datasets together and removes none useful columns
    prep_input(target, lets_keep)
      creates DATE dataframe with time stamp of kept values and removes unwanted columns from target
  '''

  list_flat = lambda l: [item for sublist in l for item in sublist]
  list_flat.__doc__ = '''lamda function to flatten a nested list'''

  list_deep = lambda lst: [[i] for i in lst]
  list_deep.__doc__ = '''lambda function to nest a list'''

  def to_pandas(df_list):
    '''
    Converts PySpark DataFrame to Pandas DataFrame
    
    Parameters: 
      df_list: list of PySpark DataFrames
    '''

    df = []
    for i in range(len(df_list)):
      tmp = df_list[i].toPandas()
      tmp['*DATE'] =  pd.to_datetime(tmp['*DATE'], infer_datetime_format=True)
      df.append(tmp)
    return df

  def re_writer(file): # pythonexamples.org
    '''
    Rewrites data file removing and editing unusable text.
    
    Parameters:
      file: string
        text file to edit
    '''
    if 'FileStore' in  file:
      f = '/dbfs/' + file # to access DataBricks file system
    else:
      pass
    fin = open(f, "rt", encoding='cp1252') # this encoding can open special characters
    data = fin.read()
    data = data.replace(' -99999', '0')
    data = data.replace('null', '0')
    data = data.replace('Null', '0')
    data = data.replace('NO 6', 'NO_6')
    data = data.replace(' A', '_A')
    data = data.replace(' C', '_C')
    data = data.replace(' B', '_B')
    data = data.replace(' H', '_H')
    data = data.replace('OIL,CHOKE_SIZE_GI', 'rOIL *CHOKE_SIZE_GI')
    data = data.replace('GAS_RATE,PRODUCTIVITY_INDEX', 'rGAS *PRODUCTIVITY_INDEX')
    data = data.replace('Date', 'DATE')

    fin.close()
    #open the input file in write mode
    fin = open(f, "wt")
    #overrite the input file with the resulting data
    fin.write(data)
    fin.close()
    
  def dynamic_filter(df, bin_size, col_name, r_lim): # try different spread for day and month
    '''
    Smoothens the curve of the data within df[col_name]. 
    
    Smaller bin_size and r_lim will result in tighter, smoother curve.
    
    Parameters:
      df: pd.DataFrame
      bin_size: int
        size of bin where the current value will be compared to values inside the bin
      col_name: str
        name of column where studied data is stored
      r_lim: int
        limit which will determine if the current value is to be adjusted
    Outputs:
      dfilter: pd.DataFrame
        dataframe containing adjusted values
    '''
    dfilter = df.copy()
    for row in range(1, len(df)-1):
      cur = df.loc[row, col_name] # current value
      if cur == np.nan:
        continue

      # calculate past and futur means
      if row < bin_size:
        past = df.iloc[0:row,:].loc[:, col_name]
        fut = df.iloc[row+1:row+bin_size,:].loc[:, col_name]
        m_past = past.mean()
        m_fut = fut.mean()
      elif row > len(df)-bin_size:
        past = df.iloc[row-bin_size:row,:].loc[:, col_name]
        fut = df.iloc[row+1:len(df),:].loc[:, col_name]
        m_past = past.mean()
        m_fut = fut.mean()
      else:
        past = df.iloc[row-bin_size:row,:].loc[:, col_name]
        fut = df.iloc[row+1:row+bin_size,:].loc[:, col_name]
        m_past = past.mean()
        m_fut = fut.mean()

      # filter if nan
      if m_past == np.nan: # can change the default value
        if abs(cur-m_fut) > r_lim:
          dfilter.loc[row, col_name] = m_fut
          continue
        else:
          continue

      if m_fut == np.nan:
        if abs(cur-m_past) > r_lim:
          dfilter.loc[row, col_name] = m_past
          continue
        else:
          continue

      # now compare means to current value
      if abs(cur-m_past) < r_lim or abs(cur-m_fut) < r_lim:
        continue
      else:
        # look at m_diff
        m_array = np.array([m_past, m_fut])
        tmp = np.isnan(m_array) # np.isnan because bin may contain nan
        m_array[tmp] = 0.0
        m_diff = abs(np.diff(m_array))[0]
        if m_diff < r_lim:
          b_mean = np.nanmean(m_array)
          if abs(cur-b_mean) > r_lim:
            dfilter.loc[row, col_name] = b_mean
            continue
          else:
            continue
        else: # check choppy bins
          max_past = past.max()
          min_past = past.min()
          max_fut = fut.max()
          min_fut = fut.min()
          if max_fut - min_fut > r_lim*2:
            dfilter.loc[row, col_name] = m_past
            continue
          if max_past - min_past > r_lim*2:
            dfilter.loc[row, col_name] = m_fut
            continue
    return dfilter
    
  def find_well(well_name, day, month, test):
    '''
    Find dataframes of well named well_name
    
    Parameters:
      well_name: str            
        name of well of interest            
      day: data object  
      month: data object  
      test: data object   
    Outputs:   
      l_day: list of day dataframes  
      l_month: list of month dataframes  
      l_test: list of test dataframes  
      well_ids: list of well tail names  
      test_ids: list of well head names  
    '''
    l_day = []
    l_month = []
    l_test = []
    assert (month.list_ids == day.list_ids)
    print('month and day ids are identical.')
    
    # monthly and daily have same well ids
    index = [index for index, name in enumerate(day.list_ids) if well_name in name]
    well_ids = [day.list_ids[i] for i in index]
    l_day.append([day.list_df[i] for i in index])
    l_month.append([month.list_df[i] for i in index])
    
    # test well ids
    index = [index for index, name in enumerate(test.list_ids) if well_name in name]
    test_ids = [test.list_ids[i] for i in index]
    l_test.append([test.list_df[i] for i in index])

    l_day = utils.list_flat(l_day)
    l_month = utils.list_flat(l_month)
    l_test = utils.list_flat(l_test)
    return l_day, l_month, l_test, well_ids, test_ids
  
  def keep_param(day, month, test):
    '''
    Keep useful paramters for the LSTM model
    
    Parameters:
      day: list pd.DataFrame
         day data
      month: list pd.DataFrame
         month data
      test: list pd.DataFrame
        test data
      '''
    all_df = [day, month, test]
    for df in all_df:
      for i in range(len(df)):
        df[i] = df[i][['*DATE', '*BHP_AVG', '*BHT_AVG', '*WHP_AVG_P', '*WHT_AVG_P', '*rOIL', '*rGAS', '*WATER']].reset_index(drop=True)
        
  def un_accum(month):
    '''
    calculates and adds columns for the unaccumulated rates in monthly historic data.
    
    Parameters:
      month: pd.DataFrame
        Dataframe of monthly historic data
    Outputs:
      month: pd.DataFrame
        Dataframe of monthly historic data with unaccumulated rates
    '''
    month = month.sort_values('*DATE').reset_index()

    month['days_in_month'] = month['*DATE'].dt.daysinmonth
    month = month.rename(columns={'*rOIL': '*OIL_ACCUM', '*rGAS': '*GAS_ACCUM',
                                                    '*WATER': '*WAT_ACCUM'})
    month['*rOIL'] = month['*OIL_ACCUM']/month['days_in_month']
    month['*rGAS'] = month['*GAS_ACCUM']/month['days_in_month']
    month['*WATER'] = month['*WAT_ACCUM']/month['days_in_month']
    return month
  
  def nan_exc(df_day, df_month, df_test):
    '''
    Clears data that are out of the limits set after quality control
    
    Parameters:
      df_day: pd.DataFrame
        dataframes containing day data
      df_month: pd.DataFrame
        dataframes containing month data
      df_test: pd.DataFrame
        dataframes containing test data
    '''
    df_list = [df_day, df_month, df_test]
  # remove exceptional data
    for df in df_list:
      df.loc[df['*WHP_AVG_P'] < 50, '*WHP_AVG_P'] = np.nan
      df.loc[df['*WHT_AVG_P'] < 20, '*WHT_AVG_P'] = np.nan
      df.loc[df['*BHP_AVG'] < 20, '*BHP_AVG'] = np.nan
      df.loc[df['*BHT_AVG'] < 20, '*BHT_AVG'] = np.nan
      df.loc[df['*WHP_AVG_P'] > 400, '*WHP_AVG_P'] = np.nan
      df.loc[df['*WHT_AVG_P'] > 200, '*WHT_AVG_P'] = np.nan
      df.loc[df['*BHP_AVG'] > 400, '*BHP_AVG'] = np.nan
      df.loc[df['*BHT_AVG'] > 200, '*BHT_AVG'] = np.nan
        
  def rmv_exc(target, *args):
    '''
    Removes 0 values of the rates
    
    Shut in values are not interesting.
    
    target: list pd.DataFrame
      list of dataframes containing data of the well of interest
    *args: list
      strings of parameter to remove from target dataframe
        expected: 'remove_oil', 'remove_gas', 'remove_water', '*BHP_AVG',
                  '*BHT_AVG', '*WHP_AVG_P', '*WHT_AVG_P'
    '''
    
    for i in range(len(target)):
      if 'remove_oil' in args:
        target[i] = target[i][(target[i]['*rOIL'] > 0)] 
      elif 'remove_gas' in args:
        target[i] = target[i][target[i]['*rGAS'] > 0]
      elif 'remove_water' in args:
        target[i] = target[i][target[i]['*WATER'] > 0]
        
      # remove nans if obj are processed
      elif '*BHP_AVG' in args:
        target[i].dropna(subset=['*BHP_AVG'], inplace=True)
      elif '*BHT_AVG' in args:
        target[i].dropna(subset=['*BHT_AVG'], inplace=True)
      elif '*WHP_AVG_P' in args:
        target[i].dropna(subset=['*WHP_AVG_P'], inplace=True)
      elif '*WHT_AVG_P' in args:
        target[i].dropna(subset=['*WHT_AVG_P'], inplace=True)
      elif args[i] not in ['remove_oil', 'remove_gas', 'remove_water', '*BHP_AVG',\
                  '*BHT_AVG', '*WHP_AVG_P', '*WHT_AVG_P']:
        try:
          raise InputError(args[i])
        except InputError as e:
          print('InputError: ', e.val, 'is not an expected input.')
    return target

  def hf_prep_input(high_freq):
    '''
    Merges high frequency datasets together and removes none useful columns
  
    Saves DATE dataframe with dates of each kept value
    
    Parameters:
      high_freq: list of pd.DataFrames
        high frequency dataframes 
    Output:
      hf_data: pd.DataFrame
        high frequency data ready for to be input into keras model
      DATE: pd.DataFrame
        date indexes
    '''
    # merge high frequency datasets
    hf_data = pd.merge_ordered(high_freq[0], high_freq[1], on=['*DATE'], how='outer').interpolate()
    hf_data = pd.merge_ordered(hf_data, high_freq[2], on=['*DATE'], how='outer').interpolate()
    hf_data = pd.merge_ordered(hf_data, high_freq[3], on=['*DATE'], how='outer').interpolate()

    # we want to use the data while there is no shut in, before July 26, 2013
    hf_data = hf_data[(hf_data['*DATE'] < datetime.datetime(2013,7,26))]
    hf_data = hf_data.fillna(0)

    DATE = pd.DataFrame(hf_data['*DATE']).reset_index(drop=True)

    hf_data.drop(hf_data.columns[[0,2,4,6]], axis=1, inplace=True) # remove date and non usable columns
    hf_data = hf_data.reset_index(drop=True)
    return hf_data, DATE
  
  def prep_input(target, lets_keep):
    '''
    creates DATE dataframe with time stamp of kept values and removes unwanted columns from target
    
    Parameters:
      target: pd.DataFrame
      lets_keep: list of str
        column names of cols that will be kept
    Outputs:
      target: list pd.DataFrame
        Dataframe with usable columns
      DATE: list pd.DataFrame
        date indexes
    '''
    DATE = [pd.DataFrame(target[i]['*DATE']).reset_index(drop=True) for i in range(len(target))]
    target = [target[i][lets_keep].reset_index(drop=True) for i in range(len(target))] # keep useful columns
    return target, DATE
  
class InputError(Exception):
  '''
  Error class inheriting form Exception class
  
  Attributes:
    val
      Variable causing exception
  '''
  def __init__(self, val):
    '''
    Paramaters:
      val:
        Variable causing exception
      '''

    self.val = val
  def __str__(self):
    '''
    Print val
    '''

    return repr(self.val)

# COMMAND ----------


