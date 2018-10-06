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
from tensorflow.keras import load_model
def TrainModel(CoinName)
	"""	
		Inputs: CoinName - a string for the name of the crypotcurrency that is being analyzed
		This Function creates a model of the data provided by the Webcrawler and trains it using a Neural Network Regression
	"""
	temp = 'MarketCrawler/data/%s.csv'
	path = temp % (coinname.lower())
	if()
	df = pandas.read_csv(path)
	X = df.drop(["Date","Close"],axis = 1)
	X = np.asarray(X)
	y = np.asarray(df["Close"].values)
	i = 0
	for arr in X:
		if(arr[3] == '-'):
			X = np.delete(X,i,0)
			y = np.delete(y,i,0)
			i -= 1
		if(arr[4] == '-'):
			X = np.delete(X,i,0)
			y = np.delete(y,i,0)
			i -= 1
		i += 1
	dates_since_release = list(range(X.shape[0],0,-1))
	dates_since_release = np.asarray(dates_since_release)[np.newaxis].T

	X = np.hstack((dates_since_release,X))
	p = PolynomialFeatures(X.shape[1])
	X = p.fit_transform(X)
	X = np.delete(X,0,axis=1)

	mu = np.mean(X,axis=0)[np.newaxis]
	std = np.std(X,axis=0)[np.newaxis]
	mu = np.tile(mu,(X.shape[0],1))
	std = np.tile(std,(X.shape[0],1))
	X = (X-mu)/std

	X = np.hstack((np.ones((X.shape[0],1)),X))

	Xtrain,yTrain = skl.utils.shuffle(X,y)
	HL_Nodes = 1000
	L = 1
	L /= X.shape[0]
	Xtrain,Xtest,yTrain,yTest = train_test_split(X,y,test_size=0.2)
	model = keras.Sequential()
	model.add(keras.layers.Dense(HL_Nodes,activation="relu",kernel_regularizer = keras.regularizers.l2(L)))
	model.add(keras.layers.Dense(HL_Nodes,activation="relu",kernel_regularizer = keras.regularizers.l2(L)))
	model.add(keras.layers.Dense(HL_Nodes,activation="relu",kernel_regularizer = keras.regularizers.l2(L)))
	model.add(keras.layers.Dense(HL_Nodes,activation="relu",kernel_regularizer = keras.regularizers.l2(L)))
	model.add(keras.layers.Dense(1,activation="linear",kernel_regularizer = keras.regularizers.l2(L)))
	model.compile(optimizer=tf.train.AdamOptimizer(.0001),loss="mse",metrics=["mae"])
	model.fit(Xtrain,yTrain,epochs=5000,batch_size=X.shape[0],validation_data=(Xtest,yTest))
	# print(calculate_price(theta,X[0]))
	# print(y[0])
	# print(costFunc(X,y,theta))
	# print(stdErr(X,y,theta))
	plt.plot(range(X.shape[0]),np.flip(y))
	predsList = model.predict(X)
	modelMetrics = model.evaluate(X,y, batch_size = X.shape[0])
	plt.plot(range(X.shape[0]),list(reversed(predsList)))
	with open("rollingParamVals.txt","a") as f:
		f.write("Layers: %d,Node Count %d, Regularization Param: %d \n" % ((len(model.layers)-1),HL_Nodes,L))
		f.write("Training Set MSE: %d, Training Set MAE: %d \n" % (modelMetrics[0],modelMetrics[1]))
	plt.show()
	model.save(CoinName.lower() + ".h5")
	print("Mode has been saved in %s" % (CoinName.lower() + ".h5"))
def predict(CoinName,X):
	"""
		Inputs:
				CoinName: the name of the CryptoCurrency that is going to be evaluated
				X: A numpy array with the values for Days Since Release, Open, High, Volume, and Market Cap
	"""
	if(not os.path.exists(CoinName.lower() + ".h5")):
		model = load_model(CoinName.lower() + ".h5")
		prediction = model.predict(X)
		return prediction
	else:
		print("There is no model for that CryptoCurrency")
		return None