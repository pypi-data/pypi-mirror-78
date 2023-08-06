'''Nicolas Trinephi - acse-nt719

Module Containing visualization functions.

Requires plotly, hvplot, holoviews and panel installed. Requires notebook widgets for holoviews
visualizations. Jupyter Notebook is known to work best.

Functions:
  data_plot(df_day, df_month, df_test, x_val ,y_val, title, day='Day', month='Month', test='Test')
    Plots day, month and test data together on the same axis
  holo_plot(df_day, df_month, df_test)
    Interactive plotting of the historic data, parameters against date
  hf_plot(df_high)
    high frequency pressure and oil rate plot using plotly
  scatter_plot(df_day, df_month, df_test)
    Plots parameters against parameter and oil rate against parameter to check for outliers.
  scatter_plot
    Creates scatter plots of pressure vs temperature and oil rate against pressures and temperatures
  
'''

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as pyo
import panel as pn
import hvplot
import hvplot.pandas
import holoviews as hv
import panel as pn

# parameter names
oil_rate = '*rOIL'
gas_rate = '*rGAS'
water_rate = '*WATER'
BHP = '*BHP_AVG'
BHT = '*BHT_AVG'
WHP = '*WHP_AVG_P'
WHT = '*WHT_AVG_P'
code = '*WELL_BORE_CODE'
date = '*DATE'

#global plotting functions
def data_plot(df_day, df_month, df_test, x_val ,y_val, title, day='Day', month='Month', test='Test'):
  '''
  Plots day, month and test data together on the same axis

  Parameters:
    df_day: pd.DataFrame
      dataframes containing day data
    df_month: pd.DataFrame
      dataframes containing month data
    df_test: pd.DataFrame
      dataframes containing test data
    x_val: str
      column to be used as x values
    y_val: str
      column to be used as y values
    title: str
      title of plot
    day: str default: 'Day'
      label of day line
    month: str default: 'Month'
      label of month line
    test: str default: 'Test'
      label of test line

  Output:
    plot: hvplot
      interactive plot with day, month and test lines on the same axis
  '''

  day_plot = df_day.hvplot.scatter(x=x_val, y=y_val, groupby=code, height=600, width=1000, label=day, title=title)
  month_plot = df_month.hvplot.scatter(x=x_val, y=y_val, groupby=code, label=month)
  test_plot = df_test.hvplot.scatter(x=x_val, y=y_val, groupby=code, label=test)
  plot = day_plot * month_plot * test_plot
  return plot

def holo_plot(df_day, df_month, df_test):
  '''
  Interactive plotting of the historic data, parameters against date

  Parameters:
    df_day: pd.DataFrame
      dataframes containing day data
    df_month: pd.DataFrame
      dataframes containing month data
    df_test: pd.DataFrame
      dataframes containing test data

  Output:
    plot: hvpot
      interactive plot of historic data, parameters against date in two columns  
  '''

  # oil graph
  oil = data_plot(df_day, df_month, df_test, date, oil_rate, 'OIL').opts(ylabel='Oil Rate (m\u00b3/day)')

  # gas graph
  gas = data_plot(df_day, df_month, df_test, date, gas_rate, 'GAS').opts(ylabel='Gas Rate (m\u00b3/day)')

  # water graph
  water = data_plot(df_day, df_month, df_test, date, water_rate, 'WATER').opts(ylabel='Water Rate (m\u00b3/day)')

  # pressure
  back_pressure = data_plot(df_day, df_month, df_test, date, BHP, 'Pressure', day='Day BHP', month='Month BHP', test='Test BHP')
  work_pressure = data_plot(df_day, df_month, df_test, date, WHP, 'Pressure', day='Day WHP', month='Month WHP', test='Test WHP')
  pressure = back_pressure * work_pressure
  pressure = pressure.opts(ylabel='Pressure (bar)')

  # temperature
  back_temp = data_plot(df_day, df_month, df_test, date, BHT, 'Temperature', day='Day BHT', month='Month BHT', test='Test BHT')
  work_temp = data_plot(df_day, df_month, df_test, date, WHT, 'Temperature', day='Day WHT', month='Month WHT', test='Test WHT')
  temp = back_temp * work_temp
  temp = temp.opts(ylabel='Temperature (\N{DEGREE SIGN}C)')
  plot = (oil + gas + water + pressure + temp).cols(2)
  return plot
  
def hf_plot(df_high, bore):
  '''
  high frequency pressure and oil rate plot using plotly

  Parameters:
    df_high: list of pd.DataFrames
      list of high frequency data frames, [3] is expected to be oil rate
    bore: list of str
      bore names
  ''' 

  fig = make_subplots(specs=[[{"secondary_y": True}]])
  fig.update_layout(
      autosize=True,
      height=800)
  for i in range(3):
    fig.add_trace(go.Scattergl(x=df_high[i]['*DATE'], y=df_high[i]['*DHP '+bore[i]], name=bore[i], mode='markers'))
  fig.add_trace(go.Scattergl(x=df_high[3]['*DATE'], y=df_high[3]['*rOIL'], name='Oil Rate', mode='lines+markers',\
                               marker_color='black'), secondary_y=True)
  
  fig.update_layout(
    title="LSTM forecast and actual",
    xaxis_title="Date",
    yaxis_title='Pressure (bar)',
    yaxis2_title="Rate (m\u00b3)",
    font=dict(
      family="Courier New, monospace",
      size=26,
      color="#7f7f7f"))
  fig.show()
  
def scatter_plot(df_day, df_month, df_test):
  '''
  Plots parameters against parameter and oil rate against parameter to check for outliers.

  Parameters:
    df_day: pd.DataFrame
      dataframe of day data
    df_month: pd.DataFrame
      dataframe of month data
    df_test: pd.DataFrame
      dataframe of test data

  Output:
    plot: hvplot
      scatter plots in two columns
  '''

  wpt = data_plot(df_day, df_month, df_test, WHT, WHP, 'Pressure-Temperature', day='Day BHP', month='Month BHP', test='Test BHP')
  bpt = data_plot(df_day, df_month, df_test, BHT, BHP, 'Pressure-Temperature', day='Day BHP', month='Month BHP', test='Test BHP')
  owp = data_plot(df_day, df_month, df_test, oil_rate, WHP, 'oil WHP', day='Day WHP', month='Month WHP', test='Test WHP')
  obp = data_plot(df_day, df_month, df_test, oil_rate, BHP, 'oil BHP', day='Day BHP', month='Month BHP', test='Test BHP')
  owt = data_plot(df_day, df_month, df_test, oil_rate, WHT, 'oil WHT', day='Day WHT', month='Month WHT', test='Test WHT')
  obt = data_plot(df_day, df_month, df_test, oil_rate, BHT, 'oil BHT', day='Day BHT', month='Month BHT', test='Test BHT')
  plot = (wpt + bpt + owp + obp + owt + obt).cols(2)
  return plot

# COMMAND ----------


