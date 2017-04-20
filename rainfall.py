import os
import json
import csv
from collections import Counter
from pprint import pprint

import numpy as np
from plmap import plmapt

from getFile import month_to_num, num_to_month
from get_proba import file_write_json


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
	
	return prob_dic,state_dic


def get_rainfall_data(plant, state, district, path):
	rainfall_data = {}
	num_month = num_to_month()
	
	with open(path+state+".csv") as file:
		reader = csv.DictReader(file)

		for row in reader:
			#print row["District"].lower(), district.lower()
			if row["District"].strip().lower() == district.lower():
				#print "dadfsd"
				year = int(float(row["Year"]))
				
				
				#print row["January"]
				for month_num in range(1,13):
					#print num_month
					#print num_month[month_num].capitalize()
					if rainfall_data.get(num_month[month_num]):
						rainfall_data[num_month[month_num]].append(row[num_month[month_num].capitalize()])

					else:
						rainfall_data[num_month[month_num]] = []
						rainfall_data[num_month[month_num]].append(row[num_month[month_num].capitalize()])

	return rainfall_data



def get_observation_matrix(state_dic,data,plant):

	rain = []
	num_month = num_to_month()
	
	for i in range(1,12):
		rain += [i for i in state_dic[num_month[i]]]
		
	
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
	#os.chdir(path)
	#print path
	json_path = path+"\\json_files\\"
	with open(json_path+"power_state.json") as data_file:
		power_state = json.load(data_file)

	with open(json_path+"indi_prob.json") as data_file:
		indi_prob = json.load(data_file)

	with open(json_path+"transaction_matrix.json") as data_file:
		transaction_matrix = json.load(data_file)
		
	with open(json_path+'state.json') as data_file:    
	    state = json.load(data_file)

	with open(json_path+'consolidated_state.json') as data_file:    
	    consolidated_state = json.load(data_file)

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
	
	indi_prob_dic = {}
	state_dic = {}

	inp = [(key, value, indi_prob_dic, state_dic) for key, value in rainfall_data.iteritems()]
	
	error, output = plmapt(get_proba, inp, [], len(inp))
	#pprint (output[-1])
	indi_prob_dic = output[-1][0]
	state_dic = output[-1][1]
	
	observation = get_observation_matrix(state_dic,consolidated_state,plant)

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
