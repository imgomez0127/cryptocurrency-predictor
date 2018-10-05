import time
import numpy as np
import random
import matplotlib.pyplot as plt
from LinReg import calculate_price, lin_reg, costFunc,stdErr
import pandas
import sklearn as skl
from sklearn.preprocessing import PolynomialFeatures
import os
import sys
import tensorflow as tf
import tensorflow.keras as keras
if __name__ == "__main__":
	temp = '../MarketCrawler/data/%s.csv'
	path = temp % ('bitcoin')
	print(os.path.exists(path))
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
	print(dates_since_release)
	print(X.shape)
	X = np.hstack((dates_since_release,X))
	p = PolynomialFeatures(X.shape[1])
	X = p.fit_transform(X)
	X = np.delete(X,0,axis=1)
	print(X)
	print(type(X[0][4]))
	mu = np.mean(X,axis=0)[np.newaxis]
	std = np.std(X,axis=0)[np.newaxis]
	mu = np.tile(mu,(X.shape[0],1))
	std = np.tile(std,(X.shape[0],1))
	X = (X-mu)/std
	print(np.mean(X,axis=0,dtype="int64"))
	print(np.std(X,axis=0))
	X = np.hstack((np.ones((X.shape[0],1)),X))
	print(X)
	Xtrain,yTrain = skl.utils.shuffle(X,y)
	print("yeet")
	print(X.shape)
	HL_Nodes = 600
	L = 1
	L /= X.shape[0]
	
	model = keras.Sequential()
	model.add(keras.layers.Dense(HL_Nodes,activation="relu",kernel_regularizer = keras.regularizers.l2(L)))
	model.add(keras.layers.Dense(HL_Nodes,activation="relu",kernel_regularizer = keras.regularizers.l2(L)))
	model.add(keras.layers.Dense(HL_Nodes,activation="relu",kernel_regularizer = keras.regularizers.l2(L)))
	model.add(keras.layers.Dense(1,activation="linear",kernel_regularizer = keras.regularizers.l2(L)))
	model.compile(optimizer=tf.train.AdamOptimizer(.000
		1),loss="mse",metrics=["mae"])
	model.fit(X,y,epochs=5000,batch_size=X.shape[0])
	
	print(X.shape)
	# print(calculate_price(theta,X[0]))
	# print(y[0])
	# print(costFunc(X,y,theta))
	# print(stdErr(X,y,theta))
	plt.plot(range(X.shape[0]),np.flip(y))
	predsList = model.predict(X)
	print(predsList[0])
	print(y[0])
	plt.plot(range(X.shape[0]),list(reversed(predsList)))
	try:
		plt.show()
	except KeyboardInterrupt:
		print()
		print("thanks b")
		sys.exit(0)