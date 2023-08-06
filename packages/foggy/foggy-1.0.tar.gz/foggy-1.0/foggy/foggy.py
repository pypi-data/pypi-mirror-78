import cfgrib
import sys
import os
import os.path
import glob
import pandas as pd
import numpy as np
from numpy.random import seed
import re
import random
from collections import Counter
import shutil

import matplotlib.pyplot as plt
import matplotlib.colors
import cartopy.crs as ccrs

from scipy import interpolate
from imblearn.over_sampling import RandomOverSampler

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import backend as K
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import EarlyStopping



from sklearn.metrics import confusion_matrix
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve
from sklearn.metrics import auc
from sklearn.metrics import roc_auc_score



seed_value = 1
os.environ['PYTHONHASHSEED']=str(seed_value)
random.seed(seed_value)
np.random.seed(seed_value)
tf.random.set_seed(seed_value)
session_conf = tf.compat.v1.ConfigProto(intra_op_parallelism_threads=1, inter_op_parallelism_threads=1)
sess = tf.compat.v1.Session(graph= tf.compat.v1.get_default_graph(), config=session_conf)
tf.compat.v1.keras.backend.set_session(sess)

### Preprocessing------------------------------------------------------------

def DataframeCreator(filedir, fogdates_csv, airport = 'AAA', utc = '18'):

    """
    Creates dataframe with dates in column 1 and fog or nofog in column 2

    Args:

    filedir (str, path): directory of all data files # file name example: nz4kmN-ECMWF-SIGMA_02_18_110912_030.00.grb
    fogdates_csv (str, path): csv file with all of the dates of fog occurence at AAA, HNA, CHA and DNA
    airport (str): 3 letter airport being investigated (eg. AAA is Auckland Airport)
    utc (str): model forecast time in zulu

    Returns:

    df: dataframe of all dates and whether fog or nofog

    """

    fogdates = pd.read_csv(fogdates_csv) 
    fogdates = np.array(fogdates.loc[:, airport + ' ' + utc + 'Z'])
    fogdates = fogdates[np.logical_not(np.isnan(fogdates))] #gets rid of NaN values

    df = {}
    for subdir, dirs, files in os.walk(filedir):
        for file in files:
            if file.endswith('_0' + utc + '.00.grb'): # might need to be changed depending on file names
                date = '20' + file.split('_')[2] #amends the file name to be the date of model data
                df[file] = 0 # 0 means nofog
                for fogdate in fogdates:
                    fogdate = str(fogdate).split('.')[0] # specific condition for the filename

                    if fogdate in date:
                        df[file] += 1 # 1 means fog
                df[file] = [df[file]]
                df[file].append(date) #add a column with the date

    #to print and verify fog dates
    # for key, value in df.items():  
    #     if value ==1:
    #         print (key, value)

    df = pd.DataFrame([(k, *v) for k, v in df.items()])
    df.columns = ['filename'] + ['fg'] + ['date']

    return df

def DFtoCSVSaver(df, savefolder, airport = 'AAA', utc = '15'):

        df.to_csv(savefolder + airport + utc + 'DataFrame.csv')

def ReDirecter(filedir, savefolder, airport = 'AAA', utc = '18', f = 1.0, nf = 0.1):

    """
    ReDirect is a function that creates a balanced subset of data ands moves it into a TrainData directory. 
    This is done to balance the data since the number of nofog events massively outweighs the number of fog events
    at all airports.

    Args:

    filedir (str, path): directory of all data files
    savefolder (str, path): root directory
    airport (str): 3 letter airport code (eg. AAA is Auckland Airport)
    utc (str): model forecast time in zulu
    f (float): decimal of fog cases to move 
    nf (float): decimal of nofog cases to move

    Returns:

    none

    """

    fogdates_csv = savefolder + airport + utc + 'DataFrame.csv'
    df = pd.read_csv(fogdates_csv)
    subsetdir = savefolder + 'TrainData' + airport + utc
    os.mkdir(subsetdir) 

    fog = df[ df['fg'] == 1 ].sample(frac=f)
    nofog = df[ df['fg'] == 0 ].sample(frac=nf)
    if len(os.listdir(subsetdir)) == 0:
        for filename in fog['filename']:
            for subdir, dirs, files in os.walk(filedir):
                for file in files:
                    if file.endswith(filename):
                        shutil.copy(subdir +'/' + file, subsetdir)
        for filename in nofog['filename']:
            for subdir, dirs, files in os.walk(filedir):
                for file in files:
                    if file.endswith(filename):
                        shutil.copy(subdir +'/' + file, subsetdir)
    else: 
        print("Directory is not empty")

def DataDealer(savefolder, var_names = ['msl', 'r'], level = [0, 0], res = [64, 64],
                airport = 'AAA', utc = '18', random = 1, N_x = 423, N_y = 519):

    """
    Reads grib files and saves data as n-dim nparray.

    Args:
    
    savefolder (str, path): root directory
    var_names (list): shortnames (str) from grib
    level (list): list of different heights (int) for data in grib, if not use 0 for each element of modelfields
    res (list, 2 elements): drop resolution to help CNN generalize
    airport (str): 3 letter airport code (eg. AAA is Auckland Airport)
    utc (str): model forecast time in zulu
    random (int): to keep track of models and keep independent and random
    N_x and N_y (int): number of gridpoints in grib for x and y respectively

    Returns:

    X (list): model field data for each file
    Y (list): classifier encoded 0 for no fog and 1 for fog events
    File_list (list): contains filenames in the same order as X and Y


    """
    
    subsetdir = savefolder + airport + utc + 'ZTrainData'
    fogdates_csv = savefolder + airport + utc + 'DataFrame.csv'

    File_list = [] 
    X = [] 
    Y = [] 

    xax = np.linspace(0., 1., N_x) # scale down resolution 
    yax = np.linspace(0., 1., N_y) 
    xax2 = np.linspace(0., 1., res[1])
    yax2 = np.linspace(0., 1., res[0])


    df = pd.read_csv(fogdates_csv) 

    for file in glob.glob(subsetdir+'/*.grb'):
        basename = os.path.basename(file)
        File_list.append(basename)
        y = df[df['filename']==basename]['fg'].values[0]
        Y.append(y)
        imgMatrix = np.zeros((N_y, N_x, len(var_names))) 
        imgMatrix2 = np.zeros((res[0], res[1], len(var_names)))
        ds = cfgrib.open_dataset(file)
        count = 0
        for var in var_names:
            #fill the imgMatrix[x, :, :] for each x is the model field
            try:
                imgMatrix[:, :, count] = ds[var].data
            except:
                try:
                    imgMatrix[ :, :, count] = ds[var].data[level[count], ...]
                    print(f'reading at level = {level}')
                except:
                    print('?no comprende?')
            finterp = interpolate.interp2d(x=xax, y=yax, z = imgMatrix[:, :, count], kind = 'linear')
            imgMatrix2[:, :, count] = finterp(x=xax2, y=yax2)
            count += 1
        X.append(imgMatrix2)
        
        ds.close()

    np.save(savefolder + airport + utc + 'X'+ str(random) + '.npy', X)  
    np.save(savefolder + airport + utc + 'Y' + str(random) + '.npy', Y) 
    np.save(savefolder + airport + utc + 'File_list' + str(random) + '.npy', File_list) 

    return X, Y, File_list

def Normalizer(X):
    """
    Normalizes values in X. 

    Args:

    X (list): Model field data from each file

    Returns:

    X (list): Normalized model field data from each file
    Xmin, Xmax (list): Normalized min and max of data

    """
    nsamples = len(X)
    nvars = X[0].shape[-1]
    # global min/max
    Xmin = + float('inf') * np.ones((nvars,), np.float64)
    Xmax = - float('inf') * np.ones((nvars,), np.float64)
    for i in range(nsamples):
        # min/max values for this sample
        xmin = np.array([X[i][..., j].min() for j in range(nvars)])
        xmax = np.array([X[i][..., j].max() for j in range(nvars)])
        # adjust the global min/max
        Xmin = np.minimum(Xmin, xmin)
        Xmax = np.maximum(Xmax, xmax)

    for i in range(nsamples):
        for j in range(nvars):
            X[i][..., j] = (X[i][..., j] - Xmin[j])/(Xmax[j] - Xmin[j])

    return X, Xmin, Xmax

def RandomSampler(X, Y, n_fog = None, n_nofog = None, random_state = 40):
    """
    Randomly oversamples the data and classifier with respect to fog and nofog events 
    seperately in order to create more (and balanced) data.

    Args:

    X, Y (list): Model field data (X) and the corresponding classification (Y) from each file
    n_fog and n_nofog (int): amount to oversample with respect to fog and nofog data.
    randomstate (int): to keep track of models and keep independent and random


    Returns:
    X_res, Y_res (array): randomly oversampled input, output and file names

    """

    print('Original dataset shape %s' % Counter(Y))

    if n_fog and n_nofog:
        ros = RandomOverSampler(sampling_strategy={0: n_nofog, 1: n_fog},
                                random_state=random_state)
    else:
        ros = RandomOverSampler(random_state=random_state)

    nrows = len(X)
    inds = np.array([i for i in range(nrows)], np.int).reshape((nrows, 1))
    inds_res, Y_res = ros.fit_resample(inds, Y)
    X_res = [X[i[0]] for i in inds_res]
    print('Resampled dataset shape %s' % Counter(Y_res))

    X_res = np.array(X_res)

    return X_res, Y_res 

### Plotting ------------------------------------------------------------

def QuickPlotter(grb): 
    
    """
    
    Plots data using imshow from matplotlib

    Args:
    grb (str, path): grib file path
    
    """
    
    ds = cfgrib.open_dataset(grb)
    var = ds.variables['t2m']

    data = var.values

    lons = ds.msl.longitude 
    lats = ds.msl.latitude
    plt.imshow(data)
    plt.show()

def RightSideUpPlotter(grb):

    """
    
    Plots data right side up 
    
    """
    
    ds = cfgrib.open_dataset(grb)
    var = ds.variables['t2m']

    data = var.values

    lons = ds.msl.longitude 
    lats = ds.msl.latitude
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree(central_longitude = 180.0))
    ac = ax.contourf(lons, lats, data, transform=ccrs.PlateCarree()) #remove f after ax.contour to get lines 
    ax.coastlines()
    plt.title(var.attrs['long_name'])
    #make a colorbar
    #c_bar = fig.colorbar(ac, shrink = 0.8)
    plt.show()

### CNN Architecture ------------------------------------------------------------


def Base5kBuilder(X_train):
    # k is the kernel size
    model = keras.Sequential()

    model.add(keras.layers.Conv2D(filters=16, kernel_size=(5,5), 
                                strides=(1,1), 
                                padding='same', 
                                data_format='channels_last', 
                                activation='relu', 
                                input_shape=X_train.shape[1:]))
    model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))  # which filter most successful in identifying certain feature

    # second layer 
    model.add(keras.layers.Conv2D(filters=8, kernel_size=(5,5), 
                                strides=(1,1), 
                                padding='same', 
                                data_format='channels_last', 
                                activation='relu'))
    model.add(keras.layers.MaxPooling2D(pool_size=(2, 2))) # pool size
    #third layer
    model.add(keras.layers.Conv2D(filters=8, kernel_size=(5,5), 
                                strides=(1,1), 
                                padding='same', 
                                data_format='channels_last', 
                                activation='relu'))
    model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dropout(0.2))
    model.add(keras.layers.Dense(2, activation='softmax')) 
    # configure the model for training
    model.compile(optimizer='adam', 
                loss='sparse_categorical_crossentropy', 
                metrics=['accuracy'])

    return model



def Base3kBuilder(X_train):

    # k is the kernel size

    model = keras.Sequential()

    model.add(keras.layers.Conv2D(filters=32, kernel_size=(3,3), 
                                strides=(1,1), 
                                padding='same', 
                                data_format='channels_last', 
                                activation='relu', 
                                input_shape=X_train.shape[1:]))
    model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))  # which filter most successful in identifying certain feature

    # second layer 
    model.add(keras.layers.Conv2D(filters=32, kernel_size=(3,3), 
                                strides=(1,1), 
                                padding='same', 
                                data_format='channels_last', 
                                activation='relu'))
    model.add(keras.layers.MaxPooling2D(pool_size=(2, 2))) # pool size
    #third layer
    model.add(keras.layers.Conv2D(filters=32, kernel_size=(3,3), 
                                strides=(1,1), 
                                padding='same', 
                                data_format='channels_last', 
                                activation='relu'))
    model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(keras.layers.Conv2D(filters=32, kernel_size=(3,3), 
                                strides=(1,1), 
                                padding='same', 
                                data_format='channels_last', 
                                activation='relu'))
    model.add(keras.layers.MaxPooling2D(pool_size=(2, 2))) 

    model.add(keras.layers.Conv2D(filters=32, kernel_size=(3,3), 
                                strides=(1,1), 
                                padding='same', 
                                data_format='channels_last', 
                                activation='relu'))
    model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))  

    #model.add(keras.layers.Dropout(0.2))
    model.add(keras.layers.Flatten())
    #model.add(keras.layers.Dropout(0.2))
    model.add(keras.layers.Dense(2, activation='softmax'))  

    model.compile(optimizer='adam', 
                loss='sparse_categorical_crossentropy', 
                metrics=['accuracy'])
    
    return model

def CropBuilder(X_train, NZ = False, SouthIsland = False, Airport = 'AAA'):

    # build the neural network for a cropped domain around NZ or South Island, North Island

    model = keras.Sequential()
    if NZ == True:
        model.add(keras.layers.Cropping2D(cropping=((40, 40), (40, 40)), input_shape=(193, 241, 2)))
    else:
        if SouthIsland == True:
            model.add(keras.layers.Cropping2D(cropping=((10, 70), (50, 30)), input_shape=(193, 241, 2)))
        else:
            print('yes')
            model.add(keras.layers.Cropping2D(cropping=((70, 10), (20, 60)), input_shape=(193, 241, 2)))

    model.add(keras.layers.Conv2D(filters=32, kernel_size=(3,3), 
                                strides=(1,1), 
                                padding='same', 
                                data_format='channels_last', 
                                activation='relu', 
                                input_shape=X_train.shape[1:]))
    model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))  # which filter most successful in identifying certain feature

    # second layer 
    model.add(keras.layers.Conv2D(filters=32, kernel_size=(3,3), 
                                strides=(1,1), 
                                padding='same', 
                                data_format='channels_last', 
                                activation='relu'))
    model.add(keras.layers.MaxPooling2D(pool_size=(2, 2))) # pool size
    #third layer
    model.add(keras.layers.Conv2D(filters=32, kernel_size=(3,3), 
                                strides=(1,1), 
                                padding='same', 
                                data_format='channels_last', 
                                activation='relu'))
    model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(keras.layers.Conv2D(filters=32, kernel_size=(3,3), 
                                strides=(1,1), 
                                padding='same', 
                                data_format='channels_last', 
                                activation='relu'))
    model.add(keras.layers.MaxPooling2D(pool_size=(2, 2))) 

    model.add(keras.layers.Conv2D(filters=32, kernel_size=(3,3), 
                                strides=(1,1), 
                                padding='same', 
                                data_format='channels_last', 
                                activation='relu'))
    model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))  

    model.add(keras.layers.Dropout(0.2))
    model.add(keras.layers.Flatten())
    #model.add(keras.layers.Dropout(0.2))
    model.add(keras.layers.Dense(2, activation='softmax'))  

    model.compile(optimizer='adam', 
                loss='sparse_categorical_crossentropy', 
                metrics=['accuracy'])
    return model

### Saving and loading models in h5 ------------------------------------------------------------

def ModelSaver(model, airport, utc, epochs, accuracy, fogaccuracy):
    """
    Save the keras model for later evaluation
    
    Args:
    model: the trained CNN model
    airport (str): 3 letter airport code (eg. AAA is Auckland Airport)
    utc (str): model forecast time in zulu
    epochs (int): number of epochs model used
    accuracy (str): accuracy of the model ( I used str(round(scores[1]*100,2)) from model.evaluate)
    fogaccuracy (str): true positives/(false negatives + true positives) number of 
                        fog events correctly predicted by the machine
    
    Returns:
    none
    """
    model.save(airport + utc + 'e' + epochs + '_' + accuracy + '_' + fogaccuracy + '.h5')
    print("Model Saved Successfully.")


def ModelLoader(name):
    """
    Load the keras model from file and prints summary, accuracy and fog accuracy

    Args:
    name (str): the trained CNN model airport + utc + '_' + accuracy + '_' + fogaccuracy + '.h5'
    
    Returns:
    model: pre-trained model 
    """
    model = load_model(name)
    print('Model Successfully Loaded from {}.h5.'.format(name))
    model.summary()
    print('accuracy = ' + name[9:13] + '%')
    print('fog accuracy = ' + name[15:19] + '%')

    return model

### Evaluating the model ------------------------------------------------------------

def ROCScorer(model, X, Y, plot = True):

    """
    Args:
    X, Y: Testing X (e.g. rh and mslp) and Y (fog vs nofog coded as 0, 1)
                     np.arrays
    plot: if true plots ROC curve with AUC 

    Returns:

    auc(float): area under the curve 

    """

    Y_pred_keras = model.predict(X)[:,1]

    fpr_keras, tpr_keras, thresholds_keras = roc_curve(Y, Y_pred_keras)

    from sklearn.metrics import auc

    auc_keras = auc(fpr_keras, tpr_keras)

    auc = roc_auc_score(Y, Y_pred_keras)
    print('AUC: %.3f' % auc)

    if plot == True:
        plt.figure(1)
        plt.plot([0, 1], [0, 1], 'k--')
        plt.plot(fpr_keras, tpr_keras, label='F (area = {:.3f})'.format(auc_keras))
        plt.xlabel('False positive rate')
        plt.ylabel('True positive rate')
        plt.title('ROC curve')
        plt.legend(loc='best')
        plt.show()

    return auc


