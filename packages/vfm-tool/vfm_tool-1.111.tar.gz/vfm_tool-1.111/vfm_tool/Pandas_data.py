'''Nicolas Trinephi - acse-nt719

Pandas DataFrame creator and manipulator

This module allows the user to load data into pd.DataFrames.

This module accepts space separated value files (.dat).

Contains pandas_data class
'''

from vfm_tool.Utils import *
import pandas as pd
import copy

class pandas_data:
  '''
  Class for data loading and manipulation with pandas
  
  Attributes:
    df: dataframe containing data
    list_df: list of dataframes
      contains dataframes per well name
    list_ids: list of str
      contains well names
      
  Methods:
    make_df()
      Creates pandas dataframes from historic data files
    df_lister(id_col)
      Makes list of pd.DataFrames, one for each unique entre of id_col
    make_stack(day, month, test)   static method
      Combines pd.DataFrames for plotting. The dataframe sizes and well names must match for plotting
    process(o_day, o_month, o_test, smooth=False)
      Processes the data using combination of filtering functions
    high_freq_local_only()
      Loads high frequency pressure data into dataframes using excel, usable on local machines but not on databricks
  '''
  
  def __init__(self, file_location):
    self.file_location = file_location
    self.df = None
    self.list_df = None
    self.list_ids = None
    
  def make_df(self):
    '''
    Creates pandas dataframes from historic data files
    
    Parameters:
      file_location: str
        directory of file
      datatype: str
        type of historic data
    Outputs:
      df: pd.DataFrame
        dataframe containing the loaded data
    '''

    if 'FileStore' in self.file_location: # check if local or on databricks
      file = '/dbfs' + self.file_location
    else:
      file = self.file_location

    if '_TEST_' in self.file_location:
      print('***********Accepted test data***********')
      utils.re_writer(self.file_location)
      self.df = pd.read_csv(file, header=0, sep=' ', engine='python', skiprows=2, index_col=False)
      self.df.drop(['Unnamed: 32', '*RESULT_NO'], axis=1, inplace=True)
      self.df['*DATE'] = pd.to_datetime(self.df['*DATE'])
      self.df = self.df.rename(columns={'*OIL_RATE': '*rOIL'})
      self.df = self.df.rename(columns={'*WAT_RATE': '*WATER'})
      self.df = self.df.rename(columns={'*WHP': '*WHP_AVG_P'})
      self.df = self.df.rename(columns={'*WHT': '*WHT_AVG_P'}).sort_values('*WELL_CODE')

    elif 'MONTH' in self.file_location:
      print('***********Accepted month data***********')
      utils.re_writer(self.file_location)
      self.df = pd.read_csv(file, header=0, sep=' ', engine='python', skiprows=2, index_col=False)
      self.df.drop(['Unnamed: 24'], axis=1, inplace=True)
      self.df['*DATE'] = pd.to_datetime(self.df['*DATE'])
      self.df = self.df.rename(columns={'*GAS': '*rGAS'})
      self.df = self.df.rename(columns={'*WHP_P': '*WHP_AVG_P'})
      self.df = self.df.rename(columns={'*WHT_P': '*WHT_AVG_P'}).sort_values('*WELL_BORE_CODE')

    elif '_DAY_' in self.file_location:
      print('***********Accepted day data***********')
      utils.re_writer(self.file_location)
      self.df = pd.read_csv(file, header=0, sep=' ', engine='python', skiprows=2, index_col=False)
      self.df.drop(['Unnamed: 28'], axis=1, inplace=True)
      self.df['*DATE'] = pd.to_datetime(self.df['*DATE'])
      self.df = self.df.rename(columns={'*GAS': '*rGAS'})
      self.df = self.df.rename(columns={'*OIL': '*rOIL'}).sort_values('*WELL_BORE_CODE')

    elif 'DAY.' in self.file_location:
      print('Choose a more recent file.')
      return
    else:
      try:
        raise InputError(self.file_location)
      except:
        print('InputError,', self.file_location, 'is not a good file.')
        
  def df_lister(self, id_col):
    '''
    Makes list of pd.DataFrames, one for each unique entre of id_col
    
    Paramters:
      df: pd.DataFrame
        original dataframe to be made into list
      id_col: str
        column with entries to be listed
      date: str
        date column
    Output:
      df_list: list of pd.DataFrames
        list containing data frames of each id_col
      list_ids: list of str
        list containing unique entries of id_col     
    '''
    dict_ids = self.df[id_col].unique().tolist()
    self.list_ids = []
    for i in range(len(dict_ids)):
      self.list_ids.append(str(dict_ids[i])) # keep str values
    # create list of DataFrames
    self.list_df = [self.df.where(self.df[id_col] == x) for x in self.list_ids]
    for i in range(len(self.list_df)):
      self.list_df[i] = self.list_df[i].dropna(subset=[id_col])
      self.list_df[i] = self.list_df[i].sort_values(['*DATE'])

  def make_stack(o_day, o_month, o_test):
    '''
    Combines pd.DataFrames for plotting. The dataframe sizes and well names must match for plotting.
    
    day, month and test objects must be created
    
    Parameters:
      day: data object
        list of day dataframes    
      month: data object
        list of month dataframes    
      test: data object
        list of test dataframes
    Outputs:
      day: pd.DataFrame
        day dataframes together by tail name
      month: pd.DataFrame
        month dataframes together by tail name
      test: pd.DataFrame
        test dataframes together by tail name
    '''

    day = o_day # shallow copy for spark compatibility
    month = o_month
    test = o_test
    # change to pd.DataFrame if spark_data uses this method
    if not isinstance(o_day.df, pd.DataFrame):
      if not isinstance(o_day.list_df[0], pd.DataFrame):
        day.list_df = utils.to_pandas(o_day.list_df)
    if not isinstance(o_month.df, pd.DataFrame):
      if not isinstance(o_month.list_df[0], pd.DataFrame):
        month.list_df = utils.to_pandas(o_month.list_df)
    if not isinstance(o_test.df, pd.DataFrame):
      if not isinstance(o_test.list_df[0], pd.DataFrame):
        test.list_df = utils.to_pandas(o_test.list_df)


    # restack data and prepare for plotting
    index = []
    day_bore = []
    month_bore = []
    test_copies = []
    cnt = 0
    for n in range(len(test.list_ids)):
      index.append([index for index, name in enumerate(day.list_ids) if test.list_ids[n] in name]) # get index of test_wells
      # stack dataframes for each well
      day_bore.append([day.list_df[index[n][i]] for i in range(len(index[n]))])
      month_bore.append([month.list_df[index[n][i]] for i in range(len(index[n]))])
      day_bore[n] = pd.concat(day_bore[n], ignore_index=True)
      month_bore[n] = pd.concat(month_bore[n], ignore_index=True)
      # expand test data for plotting, add well bore names 
      tmp = [] # refresh temp to match day and month bore names
      tmp_df = test.list_df[n].copy()
      tmp_df['*WELL_BORE_CODE'] = day.list_ids[cnt]
      tmp.append(tmp_df)
      cnt += 1
      for k in range(len(index[n])-1):
        tmp_df = test.list_df[n].copy()
        tmp_df['*WELL_BORE_CODE'] = day.list_ids[cnt]
        tmp.append(tmp_df)
        cnt += 1
      test_copies.append(tmp)
      test_copies[n] = pd.concat(test_copies[n], ignore_index=True)
    # stack wells together for plotting
    day_ = pd.concat(day_bore, ignore_index=True)
    month_ = pd.concat(month_bore, ignore_index=True)
    test_ = pd.concat(test_copies, ignore_index=True)
    return day_, month_, test_

  def process(o_day, o_month, o_test, smooth=False):
    '''
    Processes the data using combination of filtering functions
    
    Previous functions:clear data outside of limits, make list of dataframes, 
    calculate unaccumulated monthly rates, apply filter if needed, concat dataframes
    together for plotting.
    
    Parameters:
      o_day: pandas_data object
        object containing original day data
      o_month: pandas_data object
        object containing original month data
      o_test: pandas_data object
        object containing original test data
    Outputs:
      day: pandas_data object
        object containing processed day data
      month: pandas_data object
        object containing processed month data
      test: pandas_data object
        object containing processed test data
    '''
    # deep copy of the original objects
    if isinstance(o_day.df, pd.DataFrame) and isinstance(o_day.list_df[0], pd.DataFrame): # makes copy
      day = copy.deepcopy(o_day)
    if isinstance(o_month.df, pd.DataFrame) and isinstance(o_month.list_df[0], pd.DataFrame):
      month = copy.deepcopy(o_month)
    if isinstance(o_test.df, pd.DataFrame) and isinstance(o_test.list_df[0], pd.DataFrame):
      test = copy.deepcopy(o_test)

    # change to pd.DataFrame if spark_data uses this method, deep copy not available
    if not isinstance(o_day.df, pd.DataFrame):
      day = o_day
      day.df  = o_day.df.toPandas()
      if not isinstance(o_day.list_df[0], pd.DataFrame):
        day.list_df = utils.to_pandas(o_day.list_df)
    if not isinstance(o_month.df, pd.DataFrame):
      month = o_month
      month.df  = o_month.df.toPandas()
      if not isinstance(o_month.list_df[0], pd.DataFrame):
        month.list_df = utils.to_pandas(o_month.list_df)
    if not isinstance(o_test.df, pd.DataFrame):
      test = o_test
      test.df = o_test.df.toPandas()
      if not isinstance(o_test.list_df[0], pd.DataFrame):
        test.list_df = utils.to_pandas(o_test.list_df)

    utils.nan_exc(day.df, month.df, test.df)

    for i in range(len(test.list_df)):
      test.list_df[i] = test.list_df[i].sort_values('*DATE')

    for i, df in enumerate(month.list_df):
      month.list_df[i] = utils.un_accum(df)

    for i in range(len(day.list_df)):
      day.list_df[i] = day.list_df[i].sort_values('*DATE').reset_index(drop=True)

      if smooth:
        month.list_df[i] = utils.dynamic_filter(month.list_df[i], 30, '*BHP_AVG', 10)
        month.list_df[i] = utils.dynamic_filter(month.list_df[i], 10, '*BHT_AVG', 50)
        month.list_df[i] = utils.dynamic_filter(month.list_df[i], 10, '*WHP_AVG_P', 50)
        month.list_df[i] = utils.dynamic_filter(month.list_df[i], 10, '*WHT_AVG_P', 50)
        month.list_df[i] = utils.dynamic_filter(month.list_df[i], 10, '*rOIL', 50)
        month.list_df[i] = utils.dynamic_filter(month.list_df[i], 10, '*rGAS', 50)
        month.list_df[i] = utils.dynamic_filter(month.list_df[i], 10, '*WATER', 50)

        day.list_df[i] = utils.dynamic_filter(day.list_df[i], 30, '*BHP_AVG', 10)
        day.list_df[i] = utils.dynamic_filter(day.list_df[i], 10, '*BHT_AVG', 50)
        day.list_df[i] = utils.dynamic_filter(day.list_df[i], 10, '*WHP_AVG_P', 50)
        day.list_df[i] = utils.dynamic_filter(day.list_df[i], 10, '*WHT_AVG_P', 50)
        day.list_df[i] = utils.dynamic_filter(day.list_df[i], 10, '*rOIL', 50)
        day.list_df[i] = utils.dynamic_filter(day.list_df[i], 10, '*rGAS', 50)
        day.list_df[i] = utils.dynamic_filter(day.list_df[i], 10, '*WATER', 50)
    day.df, month.df, test.df = pandas_data.make_stack(day, month, test)
    return day, month, test
  
  def high_freq(df_high, C2_bore):
    '''
    Loads high frequency pressure data into dataframes using excel, usable on local machines but not on databricks.
    
    Outputs:
      high_freq_p: pd.DataFrame
        contains pressure values with other well names empty for plotting
      high_freq_oil: pd.DataFrame
        contains oil rate values with other well names empty for plotting
      df_high: 
        contains all high frequency data
    '''

    # trim excel data 
    df_high[0] = df_high[0][['Date', 'Pressure']]
    df_high[1] = df_high[1][['Date', 'Pressure']]
    df_high[2] = df_high[2][['Date', 'Pressure']]
    df_high[3] = df_high[3][['Date', 'OIL']]
    df_high[4] = df_high[4][['Time @ end', 'Cumulative Volume']]
    df_high[5] = df_high[5][['Time @ end', 'Cumulative Volume']]

    df_high[4] = df_high[4].rename(columns={'Time @ end': '*DATE'})
    df_high[4]['*WELL_BORE_CODE'] = C2_bore[0]
    df_high[5] = df_high[5].rename(columns={'Time @ end': '*DATE'})
    df_high[5]['*WELL_BORE_CODE'] = C2_bore[1]

    for i in range(3):
        df_high[i] = df_high[i].rename(columns={'Date': '*DATE', 'Pressure': '*DHP'})
        df_high[i]['*WELL_BORE_CODE'] = C2_bore[i]
    df_high[3] = df_high[3].rename(columns={'Date': '*DATE'})

    # remove unit cells
    for i in range(6):
        df_high[i].drop(df_high[i].tail(1).index, inplace=True)
        df_high[i].drop(df_high[i].head(1).index, inplace=True)
        df_high[i] = df_high[i].sort_values('*DATE', ascending=True)

    df_high[4].loc[1, '*rOIL'] = df_high[4].loc[1, 'Cumulative Volume']
    df_high[5].loc[1, '*rOIL'] = df_high[5].loc[1, 'Cumulative Volume']

    for i in range(2, len(df_high[4])):
        df_high[4].loc[i, '*rOIL'] = df_high[4].loc[i, 'Cumulative Volume'] - df_high[4].loc[i-1, 'Cumulative Volume']
        df_high[5].loc[i, '*rOIL'] = df_high[5].loc[i, 'Cumulative Volume'] - df_high[5].loc[i-1, 'Cumulative Volume']

    # merge df_high together
    high_freq_p = pd.concat([df_high[0], df_high[1], df_high[2]], ignore_index=True)
    high_freq_oil = pd.concat([df_high[4], df_high[5]], ignore_index=True)

    # set up dataframe to plot with other data
    file_day = '../Data/General/HYME_DAILY_PRODUCTION/NJORD_OFM_HIST3_DAY_20131113_143735.dat' # use your directory
    df_day = make_df(file_day, 'daily').sort_values('*WELL_BORE_CODE')
    day_list, well_day_ids = df_lister(df_day, '*WELL_BORE_CODE', '*DATE')
    t = np.array(well_day_ids)
    tmp = pd.DataFrame()
    tmp['*WELL_BORE_CODE'] = t
    high_freq_p = pd.concat([high_freq_p, tmp], axis=0).sort_values('*WELL_BORE_CODE')
    high_freq_oil = pd.concat([high_freq_oil, tmp], axis=0).sort_values('*WELL_BORE_CODE')
    return high_freq_p, high_freq_oil, df_high



# COMMAND ----------


