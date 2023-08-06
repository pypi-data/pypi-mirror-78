'''Nicolas Trinephi - acse-nt719

Keras LSTM trainer

This module allows the user to input a dataset, prepare it for insertion into keras LSTM algorithm, train an LSTM network 
and predict from a test set.

Inputs should be pd.DataFrames.

This script requires all libraries from requirements.txt to be installed on the cluster/machine.

Contains VFM_LSTM class.
'''

from vfm_tool.Utils import *

# import machine learning libraries
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import tensorflow as tf
from keras.optimizers import Adam
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Bidirectional, Dense, LSTM, Dropout
from tensorflow.python.keras.layers.advanced_activations import LeakyReLU
from tensorflow.keras.callbacks import Callback, ModelCheckpoint, EarlyStopping
from matplotlib import pyplot
import numpy as np
import mlflow
import mlflow.keras
  
class VFM_LSTM():
  '''
  Normalizes and trains an LSTM model to predict a test set.
  
  Attributes:
    RANDOM_SEED: int
      set random seed for wieght initialization
    input: pd.DataFrame
      dataframe of the problem
    name: str
      name of model
    train_size: int or float (usually int)
      percentage of the samples to be used as training set
    train: pd.DataFrame
      train set
    test: pd.DataFrame
      test set
    num_labels: int
      number of labels in the input
    list_labels: list of str
      label names
    f_transformer: sklearn.preprocessing.StandardScaler()
      normalization of training features
    l_transformer: sklearn.preprocessing.StandardScaler()
      normalization of training labels
    f_cols: int
      number of feature columns
    l_cols: int
      number of label columns
    X_train: np.array
      training set features
    X_test: np.array
      test set features
    y_train: np.array
      training set labels
    y_test: np.array
      test set labels
    model: Sequential()
      keras model
    history: model.fit()
      training the model
    y_pred_inv: np.array
      unscaled prediction array
    rates: str
      name of labels
    metrics: float
      calculated metrics of the prediction
      
  Methods
    split_data(split_prcnt)
      splits the input data into training and test set
    normalize()
      rescales the data with sklearn.preprocessing.StandScaler()
    to_supervised(lbck)
      wrapper for c_dataset, adds lookback
    c_dataset(X, y lbck=1)  static method
      creates supervised learning data set with lookback 
    train_model(units, epochs, batch_size, lr, drop, mode)
      trains keras LSTM model
    loss_model()
      plots the training loss and validation loss
    predict_y()
      predict the test set and calculate metrics
    eval_metrics(actual, pred)   static method
      calculate rmse, mae and r2 score
    predict_plot(combined=True)
      plot prediction
    log_mlflow(log_dir)
      save model parameters and metrics in log_dir
  '''
  
  RANDOM_SEED = 42
  np.random.seed(RANDOM_SEED)
  tf.random.set_seed(RANDOM_SEED)
  tf.keras.backend.set_floatx('float64')

  def __init__(self, input, name):
    '''
    Parameters:
      input: pd.Dataframe
        dataframe of the problem
      name: str
        name of model
    '''
    
    self.input = input
    self.dataset = input.copy() # we copy the data so that the original data is not changed
    self.name = name
    self.train_size = None
    self.train = None
    self.test = None
    self.num_labels = None
    self.list_labels = None
    self.f_transformer = None
    self.l_transformer = None
    self.f_cols = None
    self.l_cols = None
    self.X_train = None
    self.X_test = None
    self.y_train = None
    self.y_test = None
    self.model = None
    self.history = None
    self.y_pred_inv = None
    self.rates = None
    self.metrics = None
    self.mode = None
    self.lr = None
    self.units = None
    self.num_epoch = None
    self.batch_size = None
    self.drop = None
    
    print('Data loaded and copied.')
    
  def split_data(self, split_prcnt):
    '''
    splits the input data into training and test set
    
    Parameter:
      split_prcnt: int or float (usually int)
        percentage of data to make training set
    '''

    if split_prcnt >= 100:
      raise Exception('Pick a number between 0 and 100 exclusive')
    if split_prcnt <= 0:
      raise Exception('Pick a number between 0 and 100 exclusive')

    train_split = split_prcnt/100 
    self.train_size = int(len(self.dataset) * train_split)
    test_size = len(self.dataset) - self.train_size
    self.train, self.test = self.dataset.iloc[0:self.train_size], self.dataset.iloc[self.train_size:len(self.dataset)] 
    print('Data split:')
    print(' ', split_prcnt, '% training : ', len(self.train))
    print(' ', 100 - split_prcnt, '% test : ', len(self.test))
    print('\n')
    
  def normalize(self):
    '''
    Rescales data and finds labels
    '''
    # check how many labels we have
    self.num_labels = 0
    self.list_labels = []
    
    if '*rOIL' in self.input.columns:
      self.num_labels += 1
      self.list_labels.append('*rOIL')
    if '*rGAS' in self.input.columns:
      self.num_labels += 1
      self.list_labels.append('*rGAS')
    if '*WATER' in self.input.columns:
      self.num_labels += 1
      self.list_labels.append('*WATER')
    if self.num_labels == 0:
      raise TypeError('There are no labels in the input dataset.')
      
    self.rate = []
    for label in self.list_labels:
      # replace labels for nice plotting
      if label == '*rGAS':
        self.rate.append('Gas Rate')
      elif label == '*rOIL':
        self.rate.append('Oil Rate')
      elif label == '*WATER':
        self.rate.append('Water Rate')
      else:
        try:
          raise InputError(label)
        except:
          print('InputError: ', label, ' is not a label from the dataset.')
          
    cols = self.dataset.columns.tolist()
    
    # feature and labels
    self.f_cols = cols[:-self.num_labels] # right of dataframe is features
    self.l_cols = cols[-self.num_labels:] # left of dataframe is labels
    
    # normalization
    self.f_transformer = StandardScaler()
    self.l_transformer = StandardScaler()

    # apply scalers to features and labels l
    self.f_transformer = self.f_transformer.fit(self.train[self.f_cols].to_numpy())
    self.l_transformer = self.l_transformer.fit(self.train[self.l_cols].to_numpy())

    self.train.loc[:, self.f_cols] = self.f_transformer.transform(self.train[self.f_cols].to_numpy())
    self.train[self.l_cols] = self.l_transformer.transform(self.train[self.l_cols].to_numpy())
    self.test.loc[:, self.f_cols] = self.f_transformer.transform(self.test[self.f_cols].to_numpy())
    self.test[self.l_cols] = self.l_transformer.transform(self.test[self.l_cols].to_numpy())    
    
  def to_supervised(self, lbck):
    '''
    Creates supervised data sets
    Parameter:
      lbck: int
        amount of past data to add as features
    '''
    
    self.lbck = lbck
    self.X_train, self.y_train = self.c_dataset(self.train, self.train[self.l_cols], self.lbck)
    self.X_test, self.y_test = self.c_dataset(self.test, self.test[self.l_cols], self.lbck)
    
  
  @staticmethod
  def c_dataset(X, y, lbck=1): # writen by Alexis
    '''
    Reshapes datasets to sequences with lookback for supervised learning
    
    Parameters:
      X: pd.DataFrame
        Training dataset
      y: pd.DataFrame
        Test dataset
      lbck: int
        amount of past data to add as features
      
    Outputs:
      Xs: np.array
        features
      ys: np.array
        labels
    '''

    Xs, ys = [], []
    for i in range(len(X) - lbck):
        v = X.iloc[i:(i + lbck)].values
        Xs.append(v)        
        ys.append(y.iloc[i + lbck])
    return np.array(Xs), np.array(ys)

  def train_model(self, units, epochs, batch_size, lr, drop, mode):
    '''
    Trains LSTM model
    
    Parameters:
      units: int
        number of LSTM neurons
      epochs: int
        number of iterations
      batch_size: int
        section of data to input
      lr: float
        learning rate
      drop: float
        drop rate
      mode: str
        LSTM model to use
    ''' 

    self.mode = mode
    self.lr = lr
    self.units = units
    self.num_epoch = epochs
    self.batch_size = batch_size
    self.drop = drop

    self.model = Sequential()
    
    if self.mode == 'classic':
      self.model.add(LSTM(units, input_shape=(self.X_train.shape[1], self.X_train.shape[2])))
      print(self.mode, 'LSTM')
    elif self.mode == 'bidirectional':
      self.model.add(Bidirectional(LSTM(units),input_shape=(self.X_train.shape[1], self.X_train.shape[2])))
      print(mode, 'LSTM')      
    elif self.mode == 'stacked': # two layers, any more is not useful for the extended training time required
      self.model.add(LSTM(units, input_shape=(self.X_train.shape[1], self.X_train.shape[2]), return_sequences=True))
      self.model.add(LSTM(units, input_shape=(self.X_train.shape[1], self.X_train.shape[2])))          
      print(self.mode, 'LSTM')
    elif self.mode == 'stacked-bi':
      self.model.add(Bidirectional(LSTM(units, return_sequences=True),input_shape=(self.X_train.shape[1], self.X_train.shape[2])))
      self.model.add(Bidirectional(LSTM(units),input_shape=(self.X_train.shape[1], self.X_train.shape[2])))
      print(self.mode, 'LSTM')
    elif self.mode == 'bi+classic':
      self.model.add(Bidirectional(LSTM(units, return_sequences=True),input_shape=(self.X_train.shape[1], self.X_train.shape[2])))
      self.model.add(LSTM(units, input_shape=(self.X_train.shape[1], self.X_train.shape[2])))
      print(self.mode, 'LSTM')
    else: 
      try:
        raise InputError(self.mode)
      except:
        print('InputError: ', self.mode, ' is not a valid LSTM mode.')
    
    self.model.add(Dropout(self.drop))
    self.model.add(Dense(self.num_labels)) 
    
    adam = Adam(lr=lr)
    # Stop training when a monitored quantity has stopped improving.
    earlystop = [EarlyStopping(monitor="loss", min_delta = 0.00001, patience = 35, mode = 'auto', restore_best_weights=True)] 
    checkpointer = ModelCheckpoint(filepath=self.name + "_weights.hdf5", verbose=1, save_best_only=True, monitor='val_mean_squared_error')

    # Using regression loss function 'Mean Standard Error' and validation metric 'Mean Absolute Error'
    self.model.compile(loss='mse', optimizer='adam', metrics=['mae','MeanSquaredError'])
    
    # fit the model
    self.history = self.model.fit(self.X_train, self.y_train, \
                            epochs=self.num_epoch, \
                            validation_split=0.1, \
                            callbacks = [checkpointer, earlystop], \
                            verbose=2, \
                            shuffle=False, \
                            initial_epoch=0, \
                            batch_size=self.batch_size)
    
  def loss_plot(self): # written by Alexis
    '''
    Plot the training and validation loss.
    '''
    
    # Calculate the train loss and train metric, in this case mean absolute error
    train_loss = np.mean(self.history.history['loss'])
    train_mae = np.mean(self.history.history['mae'])

    #title = 'Train Loss: {0:.3f} Test Loss: {1:.3f}\n  Train MAE: {2:.3f}, Val MAE: {3:.3f}'.format(train_loss, score[0], train_mae, score[1])
    title = 'Model Loss'

    # Plot loss function
    fig = pyplot.figure()
    pyplot.style.use('seaborn')
    
    pyplot.rcParams.update({'font.size': 30})
    pyplot.plot(self.history.history['loss'], 'c-', label='train')
    pyplot.plot(self.history.history['val_loss'], 'm:', label='validation')
    pyplot.xlabel('Epochs')
    pyplot.ylabel('Loss')
    pyplot.title(title)
    pyplot.legend()
    pyplot.grid(True)
    fig.set_size_inches(w=7,h=7)
    pyplot.show()

  def predict_y(self):
    '''
    Predict the unseen test set and calculate metrics.
    
    Output:
      self.metrics: instance dictionary
        dictionary containing metrtics of the model's prediction
    '''
    
    self.model.load_weights(self.name + '_weights.hdf5')
    y_pred = self.model.predict(self.X_test)
    #Performing Inverse Scaling, to revert the normalization scale
    
    y_train_inv = self.l_transformer.inverse_transform(self.y_train)
    y_test_inv = self.l_transformer.inverse_transform(self.y_test)
    self.y_pred_inv = self.l_transformer.inverse_transform(y_pred)
    
    self.metrics = {} # save metrics in a nested dictionary.
    for i in range(len(self.list_labels)):
      rmse, mae, r2 = self.eval_metrics(y_test_inv[:,i].flatten(), self.y_pred_inv[:,i].flatten())
      self.metrics[self.rate[i]] = {'rmse' : rmse, 
                                     'mae' : mae, 
                                      'r2' : r2}
    return self.metrics
  
  @staticmethod
  def eval_metrics(actual, pred):
    '''
    Calculate rmse, mae and r2 score.
    
    Parameters:
      actual: np.array
        actual test set
      pred: np.array
        prediction of test set
    '''
    
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2

  def predict_plot(self, DATE, combined=True):
    '''
    Plot the prediction.
    
    Parameters:
      DATE: pd.DataFrame
        date indexes
      combined: bool default True
        If true combines the lines of the predicted rates.
    '''
    
    data_H = self.input[self.l_cols]
    train_data_H = data_H[:self.train_size]
    valid_data_H = data_H[self.train_size:]
    # re-attach the dates
    # df train
    df_train = pd.DataFrame(train_data_H)
    df_train = pd.concat([DATE, df_train], axis=1, join='inner')

    # df actual
    df_actual = pd.DataFrame(valid_data_H)
    df_actual = pd.concat([DATE, df_actual], axis=1, join='inner')

    # df prediction, get the index of the predictions and attach corresponding dates
    pred_idx = np.arange(len(train_data_H) + self.lbck, len(train_data_H)+ self.lbck + len(self.y_test))
    df_predict = pd.DataFrame(self.y_pred_inv, columns=['predicted '+ lb for lb in self.list_labels])
    df_predict = pd.concat([df_predict, pd.DataFrame(pred_idx, columns=['index'])], axis=1)
    df_predict = df_predict.set_index('index')
    df_predict = pd.concat([DATE, df_predict], axis=1, join='inner')
    
    if combined: # all lines on the same plot
      if '*rGAS' in self.list_labels and len(self.list_labels) > 1: # gas requires second y axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])        # oil and water rate can share one y axis
        for i, label in enumerate(self.list_labels):
          if label =='*rGAS': # setup secondary axis for gas
            fig.add_trace(go.Scattergl(x=df_train['*DATE'], y=df_train[label], name='Train ' + self.rate[i], mode='markers'), secondary_y=True)
            fig.add_trace(go.Scattergl(x=df_actual['*DATE'], y=df_actual[label], name='Actual test ' + self.rate[i], mode='markers'), secondary_y=True)
            fig.add_trace(go.Scattergl(x=df_predict['*DATE'], y=df_predict['predicted ' + label], name='Prediction ' + self.rate[i], mode='markers'), secondary_y=True)
            continue
          # water and oil lines
          fig.add_trace(go.Scattergl(x=df_train['*DATE'], y=df_train[label], name='Train ' + self.rate[i], mode='markers'))
          fig.add_trace(go.Scattergl(x=df_actual['*DATE'], y=df_actual[label], name='Actual test ' + self.rate[i], mode='markers'))
          fig.add_trace(go.Scattergl(x=df_predict['*DATE'], y=df_predict['predicted ' + label], name='Prediction ' + self.rate[i], mode='markers'))
          fig.update_layout(autosize=True,
                            height=800,
                            title="LSTM forecast and actual ",
                            xaxis_title="Date",
                            yaxis_title="Rate (m\u00b3)",
                            yaxis2_title='Rate (m\u00b3)',
                            font=dict(family="Courier New, monospace",
                                      size=26,
                                      color="#7f7f7f"))
        fig.show()
      else: # if gas by itself or no gas
        fig = go.Figure()
        for i, label in enumerate(self.list_labels):
          fig.add_trace(go.Scattergl(x=df_train['*DATE'], y=df_train[label], name='Train ' + self.rate[i], mode='markers'))
          fig.add_trace(go.Scattergl(x=df_actual['*DATE'], y=df_actual[label], name='Actual test ' + self.rate[i], mode='markers'))
          fig.add_trace(go.Scattergl(x=df_predict['*DATE'], y=df_predict['predicted ' + label], name='Prediction ' + self.rate[i], mode='markers'))
          fig.update_layout(autosize=True,
                            height=800,
                            title="LSTM forecast and actual",
                            xaxis_title="Date",
                            yaxis_title="Rate (m\u00b3)",
                            font=dict(family="Courier New, monospace",
                                      size=26,
                                      color="#7f7f7f"))
        fig.show()
    else: # sub plots
      if len(self.rate) == 3:
        fig = make_subplots(rows=len(self.rate), cols=1, subplot_titles=(self.rate[0], self.rate[1], self.rate[2]))
        fig.update_layout(height=1500, width=1800)
      elif len(self.rate) == 2:
        fig = make_subplots(rows=len(self.rate), cols=1, subplot_titles=(self.rate[0], self.rate[1]))      
        fig.update_layout(height=1200, width=1800)
      elif len(self.rate) == 1:
        raise Exception('Too few labels for subplot, use default combined=True.')

      for i, label in enumerate(self.list_labels):
        fig.add_trace(go.Scattergl(x=df_train['*DATE'], y=df_train[label], name='Train ' + self.rate[i], mode='markers', marker_color='blue'), row=i+1, col=1)
        fig.add_trace(go.Scattergl(x=df_actual['*DATE'], y=df_actual[label], name='Actual test ' + self.rate[i], mode='markers', marker_color='green'), row=i+1, col=1)
        fig.add_trace(go.Scattergl(x=df_predict['*DATE'], y=df_predict['predicted ' + label], name='Prediction ' + self.rate[i], mode='markers', marker_color='orange'), row=i+1, col=1)       
        fig.update_xaxes(title_text="Date", row=i+1, col=1)
        fig.update_yaxes(title_text='Rate (m\u00b3)', row=i+1, col=1)
        fig.update_layout(title="LSTM forecast and actual",
                          font=dict(family="Courier New, monospace",
                                    size=26,
                                    color="#7f7f7f"),
                          title_text="LSTM Predictions")
        
      for i in fig['layout']['annotations']:
            i['font'] = dict(size=26,color='#ff0000')
      fig.show()
    
  def log_mlflow(self, log_dir):
    '''
    Save model parameters and metrics in log_dir
    
    Parameter:
      log_dir: str
        location of mlflow experiment file
    '''
    
    mlflow.set_experiment(log_dir)
    mlflow.keras.autolog()
    mlflow.start_run()
    mlflow.log_param('run_name', self.mode + '_' + self.name)
    mlflow.log_param("learning_rate", self.lr)
    mlflow.log_param('units', self.units)
    mlflow.log_param('epochs', self.num_epoch)
    mlflow.log_param('lookback', self.lbck)
    mlflow.log_param('batch_size', self.batch_size)
    mlflow.log_param('dropout', self.drop)

    for i, label in enumerate(self.rate):
      mlflow.log_metric("test_rmse_"+self.rate[i], self.metrics[label]['rmse'])
      mlflow.log_metric("test_r2_"+self.rate[i], self.metrics[label]['r2'])
      mlflow.log_metric("test_mae_"+self.rate[i], self.metrics[label]['mae'])
    mlflow.end_run()    


# COMMAND ----------


