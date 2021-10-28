from math import *

import numpy as np
import pandas as pd

def cal_score(test_type, age, time, wrong):
	''' Description:
	This is the core function to calcuate the VR scores to evaluation the VR performance.
	'''
    
	XX = np.array([1, age])
	YY = np.array([time, wrong])

	if test_type == 'Supermarket':
		Sigma = np.array([[171.43212258, 4.5813051537],[4.5813051537, 1.43038077996]])
		Beta = np.array([[9.754721871846625, -0.234485368314833],[0.724371957915356, 0.018527037454740]])
		scale = 8.33333333334
		threshold = 78.7115178454

	elif test_type == 'City Navigation - Night':
		Sigma = np.array([[1.27532796087, 0.000256718],[0.000256718538, 0.00071714777]]) * 1000
		Beta = np.array([[42.879298963, 0.8786125205],[1.79591036367, -0.004724489]])
		scale = 4.34782608695
		threshold = 88.688195418969627

	elif test_type == 'Stair Navigation - Night':
		Sigma = np.array([[4.5193834875, -0.00670999751],[-0.006709997515, 0.004349299174]]) * 1000
		Beta = np.array([[52.929274142, 1.288877122],[3.5054645900, 0.01019351506]])
		scale = 6.6666666667
		threshold = 82.818293342591190

	elif test_type == 'City Navigation - Day':
		Sigma = np.array([[2.012679334093086, 0.011670698898637],[0.011670698898637, 0.000786950520701]]) * 1000
		Beta = np.array([[41.353683031547511, 0.153495002290970],[1.687292514467054, 0.005247170227570]])
		scale = 16.6666666667
		threshold = 56.638082439383545

	elif test_type == 'Stair Navigation - Day':
		Sigma = np.array([[4.663066808803745, -0.001770684754166],[-0.001770684754166, 0.001192329634867]]) * 1000
		Beta = np.array([[14.975185882824167, -1.053466347483571],[3.782319720365088, 0.035435999656656]])
		scale = 12.5
		threshold = 67.865716040140683

	VR_MahDist = sqrt(np.dot(np.dot((YY-np.dot(XX,Beta)), np.linalg.inv(Sigma)), ((YY-np.dot(XX,Beta)).T)))
	VR_ScMDist = VR_MahDist * scale
	score = 100 - VR_ScMDist
 
	return score, Beta, threshold