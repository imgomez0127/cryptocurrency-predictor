"""
	A Python module to make a prediction on cryptocurrencies using Feed Forward Neural Network Regression
	By Ian Gomez
"""
#Python Base Libraries
import os
import time
#Installed Libraries
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas
import sklearn as skl
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras.models import load_model,save_model

def removeNull(dataset,observedVals):
	"""
		Inputs: 
			dataset numpy.array: An array that contains the input data for the cryptocurrency
			observedVals numpy.array: An array that contains the output data for the cryptocurrency
	"""
	i = 0
	for arr in dataset:
		for j in range(len(arr)):
			if(arr[j] == '-'):
				dataset = np.delete(dataset,i,0)
				observedVals = np.delete(observedVals,i,0)
				i -= 1
		i += 1
	return dataset,observedVals
def load_data(CoinName):
	"""
		Inputs: 
			CoinName - name for the cryptocurrency that is being analyzed
		Outputs:
			X - the dataset for the input parameters for the model
			y - the dataset for the output parameters for the model
	"""
	temp = 'data/%s.csv'
	path = temp % (CoinName.lower())
	if(not (os.path.exists(path))):
		raise ValueError("There is no data for that CryptoCurrency")
	df = pandas.read_csv(path)
	X = df.drop(["Date"],axis = 1)
	X = np.asarray(X)
	y = np.asarray(df["Close"].values)
	dates_since_release = list(range(X.shape[0],0,-1))
	dates_since_release = np.asarray(dates_since_release)[np.newaxis].T
	X = np.hstack((dates_since_release,X))
	X,y = removeNull(X,y)
	X = PolynomialFeatures(X.shape[1]).fit_transform(X)
	X = np.delete(X,0,axis=1)
	y = np.delete(y,0,axis=0)
	X = np.delete(X,X.shape[0]-1,axis=0)
	return X,y
def TrainModel(CoinName):
	"""	
		Inputs: CoinName - a string for the name of the crypotcurrency that is being analyzed
		This Function creates a model of the data provided by the Webcrawler and trains it using a Neural Network Regression
	"""
	try:
		X,y = load_data(CoinName)
	except ValueError as e:
		print(e)
		return
	mu = np.mean(X,axis=0)[np.newaxis]
	std = np.std(X,axis=0)[np.newaxis]
	normalizationParams = pandas.DataFrame(np.hstack((mu.T,std.T)),columns=["Mean","Standard Deviation"])
	normsPath = "normalizationParams/" + CoinName.lower() + ".csv" if (os.getcwd().split("/")[-1] == 'LinRegEstimation') else "LinRegEstimation/normalizationParams/" + CoinName.lower() + ".csv"
	normalizationParams.to_csv(normsPath,index=False)
	mu = np.tile(mu,(X.shape[0],1))
	std = np.tile(std,(X.shape[0],1))
	X = (X-mu)/std
	y = np.delete(y,0,axis=0)
	X = np.delete(X,X.shape[0]-1,axis=0)
	Xtrain,yTrain = skl.utils.shuffle(X,y)
	HL_Nodes = int(X.shape[1]*1.6)
	L = 0
	L /= X.shape[0]
	Xtrain,Xtest,yTrain,yTest = train_test_split(X,y,test_size=0.2)
	model = keras.Sequential()
	model.add(keras.layers.Dense(HL_Nodes,activation="relu",kernel_regularizer = keras.regularizers.l2(L),input_shape=(X.shape[1],),use_bias=True))
	model.add(keras.layers.Dense(1,activation="linear",kernel_regularizer = keras.regularizers.l2(L),use_bias=True))
	model.compile(optimizer=keras.optimizers.Adam(lr=.00003),loss="mse",metrics=["mae"])
	model.fit(Xtrain,yTrain,epochs=15000,batch_size=X.shape[0],validation_data=(Xtest,yTest))
	plt.plot(range(X.shape[0]),np.flip(y))
	predsList = model.predict(X)
	modelMetrics = model.evaluate(X,y, batch_size = X.shape[0])
	plt.plot(range(X.shape[0]),list(reversed(predsList)))
	rollingParamsPath = "rollingParamValsFolder/rollingParamVals.txt" if (os.getcwd().split("/")[-1] == 'LinRegEstimation') else "LinRegEstimation/rollingParamValsFolder/rollingParamVals.txt"
	with open(rollingParamsPath,"a") as f:
		f.write("Layers: %d,Node Count %d, Regularization Param: %d \n" % ((len(model.layers)-1),HL_Nodes,L))
		f.write("Training Set MSE: %d, Training Set MAE: %d \n" % (modelMetrics[0],modelMetrics[1]))
	modelPath = 'Models/' + CoinName.lower() + ".h5" if (os.getcwd().split("/")[-1] == 'LinRegEstimation') else 'LinRegEstimation/Models/' + CoinName.lower() + ".h5" 
	save_model(model,modelPath)
	print("Model has been saved in %s" % (modelPath))
	plt.show()
def predict(CoinName,X):
	"""
		Inputs:
				CoinName: the name of the CryptoCurrency that is going to be evaluated
				X: A numpy array with the previous day's values for the Days Since Release, Open, High, Volume, and Market Cap, and Close
	"""
	modelPath = 'Models/' + CoinName.lower() + ".h5" if (os.getcwd().split("/")[-1] == 'LinRegEstimation') else 'LinRegEstimation/Models/' + CoinName.lower() + ".h5" 
	if(not os.path.exists(modelPath)):
		return "\nThere is no model for that CryptoCurrency"
	inputParams = PolynomialFeatures(len(X)).fit_transform(np.asarray(X).reshape((1,-1)))[0].T
	inputParams = np.delete(inputParams,0)
	model = load_model(modelPath)
	normsPath = "normalizationParams/" + CoinName.lower() + ".csv" if (os.getcwd().split("/") == 'LinRegEstimation') else 'LinRegEstimation/normalizationParams/' + CoinName.lower() + ".csv"
	normalizationParams = pandas.read_csv(normsPath)
	mu = np.asarray(normalizationParams["Mean"].values)[np.newaxis].T
	std = np.asarray(normalizationParams["Standard Deviation"].values)[np.newaxis].T
	params = (params[np.newaxis].T-mu)/std
	inputParams = np.delete(inputParams,inputParams.shape[0]-1,axis=0)
	prediction = model.predict(params.T)
	return prediction[0][0]
def graphModel(CoinName):
	try:
		inputParams,y = load_data(CoinName)
	except ValueError as e:
		return str(e)
	modelPath = 'Models/' + CoinName.lower() + ".h5" if (os.getcwd().split("/")[-1] == 'LinRegEstimation') else 'LinRegEstimation/Models/' + CoinName.lower() + ".h5" 
	if(not os.path.exists(modelPath)):
		return "\nThere is no model for that CryptoCurrency"
	model = load_model(modelPath)
	normsPath = "normalizationParams/" + CoinName.lower() + ".csv" if (os.getcwd().split("/")[-1] == 'LinRegEstimation') else "LinRegEstimation/normalizationParams/" + CoinName.lower() + ".csv"
	normalizationParams = pandas.read_csv(normsPath)
	mu = np.asarray(normalizationParams["Mean"].values)[np.newaxis]
	std = np.asarray(normalizationParams["Standard Deviation"].values)[np.newaxis]
	mu = np.tile(mu,(inputParams.shape[0],1))
	std = np.tile(std,(inputParams.shape[0],1))
	inputParams = (inputParams-mu)/std
	y = np.delete(y,0,axis=0)
	inputParams = np.delete(inputParams,inputParams.shape[0]-1,axis=0)
	print(y.shape)
	print(inputParams.shape)
	predsList = model.predict(inputParams)
	plt.plot(range(inputParams.shape[0]),np.flip(y))
	plt.plot(range(inputParams.shape[0]),list(reversed(predsList)))
	plt.show()
def modelMAE(CoinName):
	try:
		inputParams,y = load_data(CoinName)
	except ValueError as e:
		return str(e)
	modelPath = 'Models/' + CoinName.lower() + ".h5" if (os.getcwd().split("/")[-1] == 'LinRegEstimation') else 'LinRegEstimation/Models/' + CoinName.lower() + ".h5" 
	if(not os.path.exists(modelPath)):
		return "\nThere is no model for that CryptoCurrency"
	normsPath = "normalizationParams/" + CoinName.lower() + ".csv" if (os.getcwd().split("/")[-1] == 'LinRegEstimation') else "LinRegEstimation/normalizationParams/" + CoinName.lower() + ".csv"
	normalizationParams = pandas.read_csv(normsPath)
	mu = np.asarray(normalizationParams["Mean"].values)[np.newaxis]
	std = np.asarray(normalizationParams["Standard Deviation"].values)[np.newaxis]
	mu = np.tile(mu,(inputParams.shape[0],1))
	std = np.tile(std,(inputParams.shape[0],1))
	inputParams = (inputParams-mu)/std
	return model.evaluate(inputParams,y)
