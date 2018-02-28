import time
import numpy as np
import random
import matplotlib.pyplot as plt
def lin_reg(X,y,theta = [],epoch=1000,alpha=.001,L=0):
	#alpha is the learning rate and u need to change this based on what ur analyzing
	# the main tradeoff is that if u have it too low it will take 4ever to converge and if it is too high
	# it can fail to converge and u will get a bunch of infinte numbers
	# epoch is the amount of training ur algorithm will do and there is something to be said about overtraining dont know how to determine this yet
	# newThetaJ = thetaJ - alpha * d/d(thetaJ) cost
	# cost = 1/m * Sum((mx+b - y)^2)
	# d/d theta0 = 2/m * Sum(mx+b-y)
	# d/d theta 1 = 2/m * Sum(x *(mx+b-y))
	if theta == []:
		theta = np.zeros(X.shape[1])[np.newaxis].T
	m = X.shape[0]
	for i in range(0,epoch):
		therta = np.copy(theta)
		therta[0] = 0
		theta -= alpha * (1/m) * X.T.dot(((X.dot(theta))-y[np.newaxis].T)) + ((L/m)*therta)
	return theta
def calculate_price(Theta,x):
	return Theta.T.dot(x[np.newaxis].T)
def costFunc(X,y,theta,L=0):
	therta = np.copy(theta)
	therta[0] = 0
	return (1/X.shape[0]) * sum((X.dot(theta) - y[np.newaxis].T)**2) + (L/X.shape[0]) * sum(therta * therta)
def stdErr(X,y,theta):
	return np.sqrt((1/X.shape[0]) * sum( ((y[np.newaxis].T - X.dot(theta)) ** 2) ))