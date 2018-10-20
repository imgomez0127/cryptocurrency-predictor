"""
	A Python module to make a prediction on cryptocurrencies using Feed Forward Neural Network Regression
	By Ian Gomez
"""
#Python Base Libraries
import os
import time
#Installed Libraries
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
		Inputs: dataset - 
	"""
	i = 0
	for arr in dataset:
		if(arr[3] == '-' or arr[4] == '-'):
			dataset = np.delete(dataset,i,0)
			observedVals = np.delete(observedVals,i,0)
			i -= 1
		i += 1
	return dataset,observedVals
def TrainModel(CoinName):
	"""	
		Inputs: CoinName - a string for the name of the crypotcurrency that is being analyzed
		This Function creates a model of the data provided by the Webcrawler and trains it using a Neural Network Regression
	"""
	temp = 'data/%s.csv'
	path = temp % (CoinName.lower())
	if(not (os.path.exists(path))):
		print("There is no data for that CryptoCurrency")
		return None
	df = pandas.read_csv(path)
	X = df.drop(["Date","Close"],axis = 1)
	X = np.asarray(X)
	y = np.asarray(df["Close"].values)
	X,y = removeNull(X,y)
	dates_since_release = list(range(X.shape[0],0,-1))
	dates_since_release = np.asarray(dates_since_release)[np.newaxis].T
	X = np.hstack((dates_since_release,X))
	p = PolynomialFeatures(X.shape[1])
	X = p.fit_transform(X)
	X = np.delete(X,0,axis=1)
	mu = np.mean(X,axis=0)[np.newaxis]
	std = np.std(X,axis=0)[np.newaxis]
	normalizationParams = pandas.DataFrame(np.hstack((mu.T,std.T)),columns=["Mean","Standard Deviation"])
	normsPath = "normalizationParams/" + CoinName.lower() + ".csv" if (os.getcwd() == '/home/imgomez/coding/market-searcher/LinRegEstimation') else "LinRegEstimation/normalizationParams/" + CoinName.lower() + ".csv"
	normalizationParams.to_csv(normsPath,index=False)
	mu = np.tile(mu,(X.shape[0],1))
	std = np.tile(std,(X.shape[0],1))
	X = (X-mu)/std
	Xtrain,yTrain = skl.utils.shuffle(X,y)
	HL_Nodes = 1000
	L = 1
	L /= X.shape[0]
	Xtrain,Xtest,yTrain,yTest = train_test_split(X,y,test_size=0.2)
	model = keras.Sequential()
	model.add(keras.layers.Dense(HL_Nodes,activation="relu",kernel_regularizer = keras.regularizers.l2(L),input_shape=(X.shape[1],)))
	model.add(keras.layers.Dense(HL_Nodes,activation="relu",kernel_regularizer = keras.regularizers.l2(L)))
	model.add(keras.layers.Dense(HL_Nodes,activation="relu",kernel_regularizer = keras.regularizers.l2(L)))
	model.add(keras.layers.Dense(HL_Nodes,activation="relu",kernel_regularizer = keras.regularizers.l2(L)))
	model.add(keras.layers.Dense(1,activation="linear",kernel_regularizer = keras.regularizers.l2(L)))
	model.compile(optimizer=keras.optimizers.Adam(lr=.0001),loss="mse",metrics=["mae"])
	model.fit(Xtrain,yTrain,epochs=15,batch_size=X.shape[0],validation_data=(Xtest,yTest))
	plt.plot(range(X.shape[0]),np.flip(y))
	predsList = model.predict(X)
	modelMetrics = model.evaluate(X,y, batch_size = X.shape[0])
	plt.plot(range(X.shape[0]),list(reversed(predsList)))
	rollingParamsPath = "rollingParamValsFolder/rollingParamVals.txt" if (os.getcwd() == '/home/imgomez/coding/market-searcher/LinRegEstimation') else "LinRegEstimation/rollingParamValsFolder/rollingParamVals.txt"
	with open(rollingParamsPath,"a") as f:
		f.write("Layers: %d,Node Count %d, Regularization Param: %d \n" % ((len(model.layers)-1),HL_Nodes,L))
		f.write("Training Set MSE: %d, Training Set MAE: %d \n" % (modelMetrics[0],modelMetrics[1]))
	plt.show()
	modelPath = 'Models/' + CoinName.lower() + ".h5" if (os.getcwd() == '/home/imgomez/coding/market-searcher/LinRegEstimation') else 'LinRegEstimation/Models/' + CoinName.lower() + ".h5" 
	save_model(model,modelPath)
	print("Mode has been saved in %s" % (modelPath))
def predict(CoinName,X):
	"""
		Inputs:
				CoinName: the name of the CryptoCurrency that is going to be evaluated
				X: A numpy array with the values for Days Since Release, Open, High, Volume, and Market Cap
	"""
	modelPath = 'Models/' + CoinName.lower() + ".h5" if (os.getcwd() == '/home/imgomez/coding/market-searcher/LinRegEstimation') else 'LinRegEstimation/Models/' + CoinName.lower() + ".h5" 
	if(not os.path.exists(modelPath)):
		return "\nThere is no model for that CryptoCurrency"
	inputParams = PolynomialFeatures(len(X)).fit_transform(np.asarray(X).reshape((1,-1)))[0].T
	inputParams = np.delete(inputParams,0)
	model = load_model(modelPath)
	normsPath = "normalizationParams/" + CoinName.lower() + ".csv" if (os.getcwd() == '/home/imgomez/coding/market-searcher/LinRegEstimation') else 'LinRegEstimation/normalizationParams/' + CoinName.lower() + ".csv"
	normalizationParams = pandas.read_csv(normsPath)
	mu = np.asarray(normalizationParams["Mean"].values)[np.newaxis].T
	std = np.asarray(normalizationParams["Standard Deviation"].values)[np.newaxis].T
	params = (inputParams[np.newaxis].T-mu)/std
	prediction = model.predict(params.T)
	return prediction[0][0]
def graphModel(CoinName):
	print("YEEE")
	temp = 'data/%s.csv'
	path = temp % (CoinName.lower())
	if(not (os.path.exists(path))):
		return "There is no data for that CryptoCurrency"
	modelPath = 'Models/' + CoinName.lower() + ".h5" if (os.getcwd() == '/home/imgomez/coding/market-searcher/LinRegEstimation') else 'LinRegEstimation/Models/' + CoinName.lower() + ".h5" 
	if(not os.path.exists(modelPath)):
		return "\nThere is no model for that CryptoCurrency"
	df = pandas.read_csv(path)
	X = df.drop(["Date","Close"],axis = 1)
	print(X.shape)
	X = np.asarray(X)
	y = np.asarray(df["Close"].values)
	X,y = removeNull(X,y)

	dates_since_release = list(range(X.shape[0],0,-1))
	dates_since_release = np.asarray(dates_since_release)[np.newaxis].T
	X = np.hstack((dates_since_release,X))
	print(X.shape)
	print("yeet")
	inputParams = PolynomialFeatures(X.shape[1]).fit_transform(X)
	inputParams = np.delete(inputParams,0,axis=1)
	print(inputParams.shape)
	model = load_model(modelPath)
	normsPath = "normalizationParams/" + CoinName.lower() + ".csv" if (os.getcwd() == '/home/imgomez/coding/market-searcher/LinRegEstimation') else "LinRegEstimation/normalizationParams/" + CoinName.lower() + ".csv"
	normalizationParams = pandas.read_csv(normsPath)
	mu = np.asarray(normalizationParams["Mean"].values)[np.newaxis].T
	std = np.asarray(normalizationParams["Standard Deviation"].values)[np.newaxis].T
	print(std.shape)
	
	mu = np.tile(mu,(inputParams.shape[0],1))
	std = np.tile(std,(inputParams.shape[0],1))
	inputParams = (inputParams-mu)/std
	predsList = model.predict(inputParams)
	
	plt.plot(range(X.shape[0]),list(reversed(predsList)))
	plt.show()
