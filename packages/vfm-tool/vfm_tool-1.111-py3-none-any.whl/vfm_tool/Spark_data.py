# Nicolas Trinephi - acse-nt719
# MAGIC %run /Users/nicolas.trinephi@imperial.ac.uk/VFM_Code/pandas_data

'''Spark DataFrame creator and manipulator

This module allows the user to load data into spark DataFrames.
It requires pyspark, this is readily available on Databricks clusters, as well as the other
dependencies in requirements.txt.

This module accepts space separated value files (.dat).

Contains spark_data class
'''
from vfm_tool.Utils import *
from vfm_tool.Pandas_data import pandas_data

from pyspark.sql.types import *
from pyspark.sql.functions import col

# setup spark environment
from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .appName("VFM Session") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()
# import org.apache.spark as spark

class spark_data(pandas_data):
  '''
  Inherited class of pandas_data for spark data frames
  
  
  Methods:
    df_lister(id_col)
      Creates list of DataFrames, one for each distinct entry in id_col
    make_df()
      Creates PySpark DataFrames from Month, Day and Test Data. 
    high_freq(file_list, well_bore)    Class method
      Creates DataFrames for high frequency pressure data, in spark_data object
  '''
  def df_lister(self, id_col):
    '''
    Creates list of DataFrames, one for each distinct entry in id_col
    Parameters:
      id_col: string
        column with entries to be listed
    '''

    dict_ids = [list(x.asDict().values()) for x in self.df.select(id_col).distinct().collect()] # dict obj
    self.list_ids = []
    for i in range(len(dict_ids)):
      self.list_ids.append(str(dict_ids[i][0])) # keep str values
    # create list of DataFrames
    self.list_df = [self.df.where(self.df[id_col] == x) for x in self.list_ids]

  def make_df(self):
    '''
    Creates PySpark DataFrames from Month, Day and Test Data. 
    
    Creates custom schema for data input, filters unwanted data and returns 
    a list of wells and corresponding DataFrames.
    
    Parameters: 
      file_location: string
    Outputs:
      spark_df.df_lister outputs
    '''

    # create custom schema for specific data sheet types
    if '_DAY.' in self.file_location: # old day data, should not be used much
      print('***********Accepted day data (pre-2012)***********')
      cSchema = StructType([StructField("*WELLID", StringType(), True), 
                               StructField("*DATE", IntegerType(), True),
                               StructField("*BHP", FloatType(), True),
                               StructField("*BHP_TVD", FloatType(), True),
                               StructField("*CHOKE", FloatType(), True),
                               StructField("*DHP", FloatType(), True),
                               StructField("*DHT", FloatType(), True),
                               StructField("*rGAS", FloatType(), True), # change to *GAS if rates are not daily
                               StructField("*GASLIFT", FloatType(), True),
                               StructField("*GI", FloatType(), True),
                               StructField("*rOIL", FloatType(), True), # change to *OIL if rates are not daily
                               StructField("*UCP", FloatType(), True), # P & T to keep
                               StructField("*UCT", FloatType(), True),
                               StructField("*WATER", FloatType(), True),
                               StructField("*WI", FloatType(), True),
                               StructField("*UPTIME", FloatType(), True)])
      # clear unusable values
      utils.re_writer(self.file_location, 'OIL', 'GAS')
      # read data
      self.df = spark.read.format("csv").option("header", "true").option("sep", " ").option("mode", "dropMalformed") \
            .schema(cSchema).load(file_location)
      self.df = self.df.filter(~col('*DATE').isin(['null']))

    elif '_DAY_' in self.file_location:
      print('***********Accepted day data***********')
      cSchema = StructType([StructField("*WELL_BORE_CODE", StringType(), True), 
                                 StructField("*DATE", DateType(), True),
                                 StructField("*ON_STREAM", FloatType(), True),
                                 StructField("*BHP_AVG", FloatType(), True),
                                 StructField("*BHT_AVG", FloatType(), True),
                                 StructField("*DP_TUBING", FloatType(), True),
                                 StructField("*ANNULUS_PRESS_AVG", FloatType(), True),
                                 StructField("*CHOKE_SIZE_AVG_P", FloatType(), True),
                                 StructField("*AVG_CHOKE_UOM", StringType(), True),
                                 StructField("*ALLOC_GASLIFT", FloatType(), True),
                                 StructField("*WHP_AVG_P", FloatType(), True),
                                 StructField("*WHT_AVG_P", FloatType(), True),
                                 StructField("*SAND_RATE", FloatType(), True), 
                                 StructField("*DP_CHOKE_SIZE", FloatType(), True),
                                 StructField("*rOIL", FloatType(), True),
                                 StructField("*COND", FloatType(), True),
                                 StructField("*rGAS", FloatType(), True),
                                 StructField("*WATER", FloatType(), True),
                                 StructField("*GI", FloatType(), True),
                                 StructField("*WI", FloatType(), True),
                                 StructField("*DHP", FloatType(), True),
                                 StructField("*DHT", FloatType(), True),
                                 StructField("*CHOKE_SIZE_AVG_GI", FloatType(), True),
                                 StructField("*CHOKE_SIZE_AVG_WI", FloatType(), True),
                                 StructField("*WHP_AVG_GI", FloatType(), True),
                                 StructField("*WHP_AVG_WI", FloatType(), True),
                                 StructField("*WHT_AVG_GI", FloatType(), True),
                                 StructField("*WHT_AVG_WI", FloatType(), True)])
      # clear unusable values
      utils.re_writer(self.file_location)
      # read data
      self.df = spark.read.format("csv").option("sep", " ").schema(cSchema).load(self.file_location)
      self.df = self.df.filter(~col('*DATE').isin(['null']))
      self.df = self.df.orderBy('*DATE')

    elif 'MONTH' in self.file_location: # month data
      print('***********Accepted month data***********')
      cSchema = StructType([StructField("*WELL_BORE_CODE", StringType(), True), 
                               StructField("*DATE", DateType(), True),
                               StructField("*rGAS", FloatType(), True), # change to *GAS if rates are not daily
                               StructField("*WATER", FloatType(), True),
                               StructField("*GI", FloatType(), True),
                               StructField("*WI", FloatType(), True),
                               StructField("*UPTIME", FloatType(), True),
                               StructField("*BHP_AVG", FloatType(), True), # P & T to keep
                               StructField("*BHT_AVG", FloatType(), True),
                               StructField("*DP_TUBING", FloatType(), True),
                               StructField("*ANNULUS_PRESS_AVG", FloatType(), True),
                               StructField("*ALLOC_GASLIFT", FloatType(), True),
                               StructField("*SAND_RATE", FloatType(), True),
                               StructField("*DP_CHOKE_SIZE", FloatType(), True),
                               StructField("*rOIL", FloatType(), True), # this is probably only oil production # change to *OIL,CHOKE_SIZE_GI if rates are not daily
                               StructField("*CHOKE_SIZE_GI", FloatType(), True),
                               StructField("*CHOKE_SIZE_WI", FloatType(), True),
                               StructField("*CHOKE_SIZE_P", FloatType(), True),
                               StructField("*WHP_GI", FloatType(), True),
                               StructField("*WHP_WI", FloatType(), True),
                               StructField("*WHP_AVG_P", FloatType(), True),
                               StructField("*WHT_GI", FloatType(), True),
                               StructField("*WHT_WI", FloatType(), True),
                               StructField("*WHT_AVG_P", FloatType(), True)])
      # clear unusable values
      utils.re_writer(self.file_location)
      # read data
      self.df = spark.read.format("csv").option("sep", " ").schema(cSchema).load(self.file_location)
      self.df = self.df.filter(~col('*DATE').isin(['null']))
      self.df = self.df.orderBy('*DATE')
    
    elif '_TEST_' in self.file_location: # well test data
      print('***********Accepted test data***********')
      cSchema = StructType([StructField("*WELL_CODE", StringType(), True), 
                               StructField("*DATE", DateType(), True),
                               StructField("*RESULT_NO", StringType(), True),
                               StructField("*END_DATE", StringType(), True), # some -99999
                               StructField("*CHOKE_SIZE", FloatType(), True),
                               StructField("*GOR", FloatType(), True),
                               StructField("*RESERVOIR_PRESS", FloatType(), True),
                               StructField("*rOIL", FloatType(), True),   # rates are daily
                               StructField("*COND_RATE", FloatType(), True),
                               StructField("*rGAS", FloatType(), True),
                               StructField("*PRODUCTIVITY_INDEX", FloatType(), True),
                               StructField("*WATERCUT", FloatType(), True),
                               StructField("*WHP_AVG_P", FloatType(), True),
                               StructField("*WHT_AVG_P", FloatType(), True),
                               StructField("*STRUCTURE", StringType(), True),
                               StructField("*FLUID_PI", FloatType(), True),
                               StructField("*GAS_LIFT", FloatType(), True),
                               StructField("*GAS_LIFT_GKGL", FloatType(), True),
                               StructField("*GAS_LIFT_RGL", FloatType(), True),
                               StructField("*HSV", FloatType(), True),
                               StructField("*QC_M", FloatType(), True),
                               StructField("*QG_M", FloatType(), True),
                               StructField("*QO_M", FloatType(), True),
                               StructField("*QW_M", FloatType(), True),
                               StructField("*SAND_TRAP", FloatType(), True),
                               StructField("*H2S", FloatType(), True),
                               StructField("*TDEV_PRESS", FloatType(), True),
                               StructField("*TDEV_TEMP", FloatType(), True),
                               StructField("*SAND_RATE", FloatType(), True),
                               StructField("*BHP_AVG", FloatType(), True),
                               StructField("*BHT_AVG", FloatType(), True),
                               StructField("*WATER", FloatType(), True)])
      # clear unusable values
      utils.re_writer(self.file_location)
      # read data
      self.df = spark.read.format("csv").option("sep", " ").schema(cSchema).load(self.file_location)
      self.df = self.df.filter(~col('*DATE').isin(['null', 'TEST_WELL', '*DATE']))
      self.df = self.df.orderBy('*DATE')
    else:
      try:
        raise InputError(self.location)
      except:
        print('InputError: Incorrect/No file chosen')
        
  @classmethod
  def high_freq(cls, file_list, well_bore):
    '''
    Creates DataFrames for high frequency pressure data, in spark_data object
    
    With current high frequency data, file_list[3] is the combined oil rate while file_list[:3] 
    contain the pressure values for each tail.
    
    Parameters:
      file_list: list of str
        list of high frequency data file locations
      well_bore: list of str
        well bore names of file contents
    '''
    cls = cls.__new__(cls)  # Does not call pandas_data.__init__()
    
    cls.list_df = []

    for i in range(3):
      cls.df = spark.read.format("csv").option("sep", ",").option("header", 'true')\
                    .schema(StructType([StructField("*DATE", StringType(), True),  # import as str
                                        StructField("*DHP "+well_bore[i], StringType(), True)]))\
                    .load(file_list[i])
      cls.list_df.append(cls.df)               
    cSchema = StructType([StructField("*DATE", StringType(), True), 
                          StructField("*rOIL", StringType(), True)])
    cls.df = spark.read.format("csv").option("sep", ",").option("header", 'true').schema(cSchema).load(file_list[3])
    cls.list_df.append(cls.df)

    cls.list_df = utils.to_pandas(cls.list_df)

    # trim excel data 
    for i in range(3):
      cls.list_df[i] = cls.list_df[i][['*DATE', '*DHP '+well_bore[i]]]
    cls.list_df[3] = cls.list_df[3][['*DATE', '*rOIL']]

    for i in range(3):
        cls.list_df[i]['*WELL_BORE_CODE'] = well_bore[i]

    # remove unit cells
    for i in range(4):
      cls.list_df[i].drop(cls.list_df[i].tail(1).index, inplace=True)
      cls.list_df[i].drop(cls.list_df[i].head(1).index, inplace=True)
      cls.list_df[i]['*DATE']= pd.to_datetime(cls.list_df[i]['*DATE']) # spark importing as string due to null
      cls.list_df[i] = cls.list_df[i].sort_values('*DATE', ascending=True)
    for i in range(3):
      cls.list_df[i]['*DHP '+well_bore[i]] = pd.to_numeric(cls.list_df[i]['*DHP '+well_bore[i]]) # spark importing as string due to 1st line of csv
    cls.list_df[3]['*rOIL'] = pd.to_numeric(cls.list_df[3]['*rOIL'])
    return cls

# COMMAND ----------


