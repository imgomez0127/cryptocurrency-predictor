import matplotlib.pyplot as mpl
import numpy as np
import pandas
import time
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
import tensorflow as tf
from tensorflow import keras
import os
from NN import removeNull
def ValidationCurve(X,y,layers,input_layer_size=1300,iterations = 5000,L = 0):
	testErrorSet = []
	CVErrorSet = []
	testAcc=[]
	cvAcc=[]
	X,X_test,y,y_test = train_test_split(X,y,test_size = .2)
	print(X.shape)
	LayersCount = np.arange(1,11,1)
	#time.sleep(5)
	for i in range(len(LayersCount)):
		reg_param = float(L/(X.shape[0]))
		print(LayersCount)
		model = keras.Sequential()
		for _ in range(LayersCount[i]):
			model.add(keras.layers.Dense(input_layer_size,activation="relu",kernel_regularizer = keras.regularizers.l2(L),input_shape=(X.shape[1],)))
			model.add(keras.layers.Dropout(.5))
		model.add(keras.layers.Dense(input_layer_size,activation="relu",kernel_regularizer=keras.regularizers.l2(reg_param),use_bias = True,input_shape=(input_layer_size,)))
		model.add(keras.layers.Dense(1,kernel_regularizer = keras.regularizers.l2(reg_param),activation="linear", use_bias = True))
		model.compile(optimizer=keras.optimizers.Adam(.00000001),loss="mse",metrics=["mae"])
		model.fit(X,y,epochs=iterations,batch_size=X.shape[0],validation_data=(X_test,y_test))
		testEval= model.evaluate(X,y,batch_size=X.shape[0])
		cvEval = model.evaluate(X_test,y_test,batch_size=X_test.shape[0])
		testErrorSet.append(testEval[0])
		CVErrorSet.append(cvEval[0])
		testAcc.append(testEval[1])
		cvAcc.append(cvEval[1])
	print(model.evaluate(X,y,batch_size=X.shape[0]))
	print("L values: " + str(L))
	print("Test Errors for respective L:" + str(testErrorSet))
	print("CV Errors for respective L: " + str(CVErrorSet))
	mpl.plot(LayersCount,testErrorSet)
	mpl.plot(LayersCount,CVErrorSet)
	mpl.show()
if __name__ == '__main__':
	temp = '../data/%s.csv' 
	path = temp % ("loki")
	if(not (os.path.exists(path))):
		print("There is no data for that CryptoCurrency")
	modelPath = 'Models/' + "bitcoin" + ".h5" if (os.getcwd() == '/home/imgomez/coding/market-searcher/LinRegEstimation') else 'LinRegEstimation/Models/' + "bitcoin" + ".h5" 
	if(not os.path.exists(modelPath)):
		print("\nThere is no model for that CryptoCurrency")
	df = pandas.read_csv(path)
	X = df.drop(["Date","Close"],axis = 1)
	X = np.asarray(X)
	y = np.asarray(df["Close"].values)
	X,y = removeNull(X,y)
	dates_since_release = list(range(X.shape[0],0,-1))
	dates_since_release = np.asarray(dates_since_release)[np.newaxis].T
	X = np.hstack((dates_since_release,X))
	X = PolynomialFeatures(X.shape[1]).fit_transform(X)
	X = np.delete(X,0,axis=1)
	mu = np.mean(X,axis=0)[np.newaxis]
	std = np.std(X,axis=0)[np.newaxis]
	mu = np.tile(mu,(X.shape[0],1))
	std = np.tile(std,(X.shape[0],1))
	X = (X-mu)/std
	LayersCount = 923
	classification_nodes = 10
	print(X.shape)
	ValidationCurve( X, y, X.shape[1])
	"""50/50= 1.506 2.605 100/100 1,0499 2.2086"""
