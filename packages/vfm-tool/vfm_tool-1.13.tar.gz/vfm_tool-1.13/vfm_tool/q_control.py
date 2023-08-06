'''Nicolas Trinephi - acse-nt719

Module with quality control functions

Functions:
  c_desc
    Adds and removes rows to make a custom description dataframe
  qc_list(input, ids)
    creates dataframe of concatenated custom describe dataframes from a list of dataframes
  qc_data
    Provides statistical analysis of data in file_location

'''

from vfm_tool.Utils import *
from vfm_tool.Pandas_data import *
from vfm_tool.Spark_data import *
import copy
import pandas as pd

def c_desc(input, desc):
  '''
  Creates a custom description dataframe

  Parameters:
    pandf: pd.DataFrame
      input dataframe
    df_l: pd.DataFrame
      description dataframe of pandf
  Output:
    df_l: pd.DataFrame
      custom description dataframe
  '''
  
  # make new rows
  df = desc.copy()
  df.loc['range'] = df.loc['min'].round(2).apply(str) + ' - ' + df.loc['max'].round(2).apply(str)
  df.loc['% null'] = (input == 0).astype(int).sum(axis=0) * 100 / len(input)
  # keep useful rows
  df = df.loc[['count', 'mean', 'range', '% null']].round(2)
  return df

def qc_list(input, ids):
  '''
  creates dataframe of concatenated custom describe dataframes from a list of dataframes.

  Parameter:
    df_list: list of pd.DataFrames
  Output:
    df: pd.DataFrames
  '''

  df = []
  for i in range(len(input)):
    df.append(input[i].describe())
    df[i] = c_desc(input[i], df[i])
  df = pd.concat(df, keys=ids, sort=True)
  return df

def qc_data(obj):
  '''
  Provides statistical analysis of data in file_location. Accepts daily, monthly and test data with units.
  
  Parameters:
    obj: data object, spark_data() or pandas_data()
      location of data file.

  Outputs:
    df: pd.DataFrame
      Contains statistical elements necessary for quality control of the data.
  '''

  # check object type and create pd.DataFrame if spark_data is used.
  if isinstance(obj, spark_data):
    tmp_list = utils.to_pandas(obj.list_df)
    df = qc_list(tmp_list, obj.list_ids)
  elif isinstance(obj, pandas_data):
    df = qc_list(obj.list_df, obj.list_ids)
  else:
    raise TypeError('The input is not a valid type, please input a spark_data() or pandas_data() object.')

  # add units
  if '_DAY.' in obj.file_location:
    print('It would be better to choose a more recent file.')
    return
  elif '_DAY_' in obj.file_location:
    print('*********** qc day data ***********')
    # add units heading
    df.loc[('units', ''),:] = ('hours', '   bar', '\N{DEGREE SIGN}C', 'bar', 'bar', '%', 'm\u00b3/day', 'bar', '\N{DEGREE SIGN}C', '$ US', '%', 'm\u00b3/day', 'm\u00b3/day', \
                                     'm\u00b3/day', 'm\u00b3/day', 'm\u00b3/day', 'm\u00b3/day', 'bar', '\N{DEGREE SIGN}C', '%', '%', 'bar', 'bar', '\N{DEGREE SIGN}C', '\N{DEGREE SIGN}C')

  elif 'MONTH' in obj.file_location: # month data
    print('*********** qc month data ***********')
    # add units heading
    df.loc[('units', ''),:] = ('m\u00b3/day', 'm\u00b3/day', 'm\u00b3/day', 'm\u00b3/day', 'hours', 'bar', '\N{DEGREE SIGN}C', 'bar', 'bar', 'm\u00b3', '$ US', '%', \
                                     'm\u00b3/day', '%', '%', '%', 'bar', 'bar', 'bar', '\N{DEGREE SIGN}C', '\N{DEGREE SIGN}C', '\N{DEGREE SIGN}C')

  elif '_TEST_' in obj.file_location: # well test data
    print('*********** qc test data ***********')
    # add units heading
    df.loc[('units', ''),:] = ('%', 'm\u00b3/day', 'bar', 'm\u00b3/day', 'm\u00b3/day', 'm\u00b3/day', '$ US', '$ US', 'bar', \
                                     '\N{DEGREE SIGN}C', '$ US', 'm\u00b3/day', 'm\u00b3/day', 'm\u00b3/day', 'metric', 'm\u00b3', 'm\u00b3', 'm\u00b3', 'm\u00b3',\
                                     'metric', '$ US', 'bar', '\N{DEGREE SIGN}C', '$ US', 'bar', '\N{DEGREE SIGN}C', 'm\u00b3/day')
  else:
    raise TypeError('Not a valid data file.')
  df = df.T.set_index('units', append=1).T
  return df

def qc_high_freq(high_freq, sheet_names):
  '''
  Obtains statistical analysis of the high frequency data.

  Parameters:
    high_freq: list pd.DataFrame
      Dataframe containing high frequency data  
    sheet_names: list str
      well tail names
    Outputs:
      desc_well: pd.DataFrame
        Dataframe containing custom description of pressures at each tail
      desc_oil: pd.DataFrame
        Dataframe containing custom description of oil rate at well head.
  '''

  df = copy.deepcopy(high_freq) # deep copy of the list of df

  # for pressures
  df_l = []
  for i in range(len(df)-1):
    df[i].drop(df[i].columns[2], axis=1, inplace=True)
    df[i].columns = ['*DATE', 'Pressure']
    df_l.append(df[i].describe())
    df_l[i] = c_desc(df[i], df_l[i])
  desc_well = pd.concat(df_l, keys=sheet_names)
  # add units heading
  desc_well.loc[('units', ''),:] = ('bar')
  desc_well = desc_well.T.set_index('units', append=1).T

  # for oil rate
  desc_oil = df[3].describe()
  desc_oil = c_desc(df[3], desc_oil)
  desc_oil.loc[('units')] = ('m\u00b3/day')
  desc_oil = desc_oil.T.set_index('units', append=1).T
  return desc_well, desc_oil
