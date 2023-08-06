import foggy

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



def CNNActivator(filedirectory, fogcsvdirectory, savedirectory,
			 airportcode = 'AAA', modeltime = '15', fog = 1.0, nofog = 0.02,
			 modelfields = ['msl', 'r'], levels = [0, 0], resolution = [64, 64],
			 randomseed = 1, Nx = 423, Ny = 519, testratio = 0.4, numFog = 100, 
			 numNofog= 100, numEpochs = 30, valsplit = 0.2, modelname = None):

	"""

	Example function (mainloop) that runs through the whole process of creating the dataframe, creating X and Y arrays, 
	balancing data, splitting test and train, building a CNN, fitting and evaluating it and 
	using a ROC curve metric.

	Args:

	filedirectory (str): directory with data (grib) files
	fogcsvdirectory (str): directory of csv file with fog event dates 
	savedirectory (str): directory to save csv and data subsets
	airport code (str): 3 letter code eg. 'AAA' for Auckland Airport
	modeltime (str): UTC model forecast time eg. '15' for 15Z
	fog (float) : percentage of fog events to use to balance dataset (usually 1.0 )
	nofog (float) : percentage of fog events to use to balance dataset (as many as there are fog events)
	modelfields (list): shortnames (str) from grib
	levels (list): list of different heights (int) for data in grib, if not use 0 for each element of modelfields
	resolution (list, 2 elements): drop resolution to help CNN generalize
	randomseed (int): to keep track of models and keep independent and random
	Nx and Ny (int): number of gridpoints in grib for x and y respectively
	testratio (float): ratio of data to put aside for testing (rest is for training)
	numFog and numNofog (int): oversampling to create more data
	valsplit (float): ratio separated for validation 
	modelname (str): to call on previous model (h5), if not use None

	Returns:

	none

	"""

	#checks if df exists
	try:
		df = pd.read_csv(savedirectory + airportcode + modeltime + 'DataFrame.csv')
	except:
		foggy.DataframeCreator(filedir = filedirectory, fogdates_csv = fogcsvdirectory, 
									airport = airportcode, utc = modeltime)

		foggy.DFtoCSVSaver(df, savefolder = savedirectory, airport = airportcode, utc = modeltime)
	
	#checks if training subset exists

	if not os.path.exists(savedirectory + airportcode + modeltime + 'ZTrainData'): 
		foggy.ReDirecter(filedir = filedirectory, savefolder = savedirectory,
					airport = airportcode, utc = modeltime, f = fog, nf = nofog)

	if not os.path.exists(savedirectory + airportcode + modeltime + 'X' + str(randomseed) + '.npy'):  
		X, Y, File_list = foggy.DataDealer(savefolder = savedirectory, var_names = modelfields,
											level = levels, res = resolution,
											airport = airportcode, utc = modeltime,
											random = randomseed, N_x = Nx, N_y = Ny)
		X = np.load(savedirectory + airportcode + modeltime + 'X' + str(randomseed) + '.npy')
		Y = np.load(savedirectory + airportcode + modeltime + 'Y' + str(randomseed) + '.npy')
		F = np.load(savedirectory + airportcode + modeltime + 'File_list' + str(randomseed) + '.npy')

	else:

		X = np.load(savedirectory + airportcode + modeltime + 'X' + str(randomseed) + '.npy')
		Y = np.load(savedirectory + airportcode + modeltime + 'Y' + str(randomseed) + '.npy')
		F = np.load(savedirectory + airportcode + modeltime + 'File_list' + str(randomseed) + '.npy')
		
	X, Xmin, Xmax = foggy.Normalizer(X)

	X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = testratio, random_state = randomseed)

	X_train, Y_train = foggy.RandomSampler(X_train,Y_train, n_fog = numFog, n_nofog = numNofog, random_state = randomseed)

	if modelname == None:
		model = foggy.Base5kBuilder(X_train)
		model.summary()
		
		history = model.fit(X_train, Y_train, epochs = numEpochs,
	                     	validation_split = valsplit)

		plt.plot(history.history['loss'], label='loss')
		plt.plot(history.history['val_loss'], label = 'val loss')
		plt.title('Comparing Loss and Validation Loss Curves')
		plt.ylabel('loss')
		plt.xlabel('epoch')
		plt.legend(loc='best')
		plt.show()

		#test the model:

		ProbPred = model.predict(X_test)
		#print(f'Ycorrect = {Y_test}')
		#print(f'ProbPred = {ProbPred}')
		Y_pred = np.argmax(ProbPred, axis=1)
		#print(f'Y_pred = {Y_pred}')
		cm = confusion_matrix(Y_test, Y_pred)
		print(f'confusion matrix = {cm}')

		TN = cm[0][0] # true negative: number of nofog events correctly pred by machine
		FN = cm[1][0] # false negative: number of fog events incorrectly pred 
		TP = cm[1][1] # true positive: number of fog events correctly pred
		FP = cm[0][1] # false positive: number of nofog events incorrectly pred

		#evaluate model:

		scores = model.evaluate(X_test, Y_test, verbose=0)
		print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
		print('fogaccuracy:', str(round((TP/(FN + TP))*100)) + '%')
		
		#save model:
		foggy.ModelSaver(model, airport = airportcode, utc = modeltime, epochs = str(numEpochs), 
								accuracy = str(round(scores[1]*100,2)), fogaccuracy = str(round((TP/(FN + TP))*100)))
		print("Saved model to disk")
	
	else:
		model = foggy.ModelLoader(modelname)

	#ROC metric:
	X_test = np.array(X_test)
	Y_test = np.array(Y_test)
	foggy.ROCScorer(model = model, X = X_test, Y = Y_test, plot = True)