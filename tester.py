import os
import json
import csv
from collections import Counter
from pprint import pprint

from plmap import plmapt
from getFile import monthToNum, numToMonth
#from get_proba import get_proba
from get_proba import file_write_json#(dic, path, file_name)
import numpy as np

def get_proba(key, value, prob_dic, state_dic):
	"""
	increase = 1, decrease = 2, equal = 3
	"""
	
	prev, increase, decrease, equal, total = 0,0,0,0,0
	state_dic[key] = []
	for i in value:
		
		i = i.replace(",","")
		i = int(round(float(i),2))
		diff = abs(int(i)-int(prev))
		if int(prev)<int(i) and diff > 5:
			state_dic[key].append(1)
			increase +=1
		elif int(prev)>int(i) and diff > 5:
			state_dic[key].append(2)
			decrease +=1
		else:
			state_dic[key].append(3)
			equal +=1
		prev = i
		total +=1
	
		
	prob_dic[key] = [round(increase/float(total),2), round(decrease/float(total),2), round(equal/float(total),2)] 
	#print prob_dic
	
	return prob_dic,state_dic


def get_rainfall_data(plant, state, district, path):
	rainfall_data = {}
	num_month = numToMonth()
	month_to_num = monthToNum()
	with open(path+state+".csv") as file:
		reader = csv.DictReader(file)

		for row in reader:
			#print row["District"].lower(), district.lower()
			if row["District"].strip().lower() == district.lower():
				#print "dadfsd"
				year = int(float(row["Year"]))
				
				rainfall_data[year] = []
				#print row["January"]
				for month_num in range(1,13):
					#print num_month
					#print num_month[month_num].capitalize()
					rainfall_data[year].append(row[num_month[month_num].capitalize()])

	return rainfall_data

def get_observation_matrix(state_dic,data,plant):
	rain = []
	for i in range(2008,2011):
		if i == 2008:
			#print state_dic[i]
			for z in range(3,12):
				#print state_dic[i]
				rain.append(state_dic[i][z])
		else:
			for z in range(0,12):
				rain.append(state_dic[i][z])
	plant_state = []
	for i in range(33):
		 plant_state.append(data[plant][i])
	
	observation = zip(plant_state,rain)
	return observation

def get_observation_prob(observation,key):
	transaction_matrix_dic={}
	count_1,count_2, count_3 = 0,0,0
	matrix = np.zeros((3,3))

	for (x,y),c in Counter(observation).iteritems():
		matrix[x-1,y-1] = c
	#print matrix

	matrix1 = matrix.tolist()
	for i in matrix1:
		su = sum(i)
		if su != 0:
			for j in i:
				i[i.index(j)] = round(j/float(su),2)
	
	transaction_matrix_dic[key] = matrix1
	
	return transaction_matrix_dic

	#for i in observation:


def rain_fun(path):
	os.chdir(path)
	#print path
	with open(path+"/power_state.json") as data_file:
		power_state = json.load(data_file)

	with open(path+"/indi_prob.json") as data_file:
		indi_prob = json.load(data_file)

	with open(path+"/transaction_matrix.json") as data_file:
		transaction_matrix = json.load(data_file)
		
	with open(path+'/state.json') as data_file:    
	    state = json.load(data_file)

	plant = "CHANDRAPUR(MAHARASHTRA) STPS"
	#plant = "DURGAPUR TPS"
	#plant = "Dr. N.TATA RAO TPS"
	#plant = "GH TPS (LEH.MOH.)"
	district = "Chandrapur"
	#district = "BURDWAN"
	#district = "Krishna"
	#district = "Bhatinda"
	state_path = path+"/monthly-rainfall/"

	rainfall_data = get_rainfall_data(plant, power_state[plant], district, state_path)
	#print rainfall_data
	indi_prob_dic = {}
	state_dic = {}

	inp = [(key, value, indi_prob_dic, state_dic) for key, value in rainfall_data.iteritems()]
	
	error, output = plmapt(get_proba, inp, [], len(inp))
	#pprint (output[-1])
	indi_prob_dic = output[-1][0]
	state_dic = output[-1][1]
	#print state_dic
	

	observation = get_observation_matrix(state_dic,state,plant)
	#print observation

	#print state[plant]
	transaction_matrix_dic =  get_observation_prob(observation,plant)

	dic_list = [
		(rainfall_data,plant+" rainfall"),
		(indi_prob_dic,plant+" indi_rain"),
		(state_dic,plant+" state_rainfall"),
		(transaction_matrix_dic,plant+" observation_matrix")
		]
	inp = [(i[0],path,i[1]) for i in dic_list]
	error, output = plmapt(file_write_json, inp, [], len(inp))
	return (transaction_matrix_dic,indi_prob_dic,state_dic,plant)

if __name__=="__main__":
	path = os.getcwd()
	rain_fun(path)
