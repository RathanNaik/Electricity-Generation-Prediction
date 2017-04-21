import os
import json
import csv
from collections import Counter
from pprint import pprint

import numpy as np
from plmap import plmapt

from getFile import month_to_num, num_to_month
from get_proba import file_write_json
from get_proba import get_prob


def get_proba(key, value, prob_dic, state_dic):
	"""
	increase = 1, decrease = 2, equal = 3
	"""
	
	prev, increase, decrease, equal, total = 0,0,0,0,0
	state_dic[key] = []
	for i in value:
		
		i = i.replace(",","")
		i = i.replace("N.A.","0.0")
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


def get_rainfall_data(plant, state, district, path1,path2):
	rainfall_data = {}
	num_month = num_to_month()

	with open(path2+state+".csv") as file:
		reader = csv.DictReader(file)
		for row in reader:
			
			if row["District"].strip().lower() == district.lower():
				
				for month_num in range(1,13):
					
					if rainfall_data.get(num_month[month_num]):
						rainfall_data[num_month[month_num]].append(row[num_month[month_num].capitalize()])

					else:
						rainfall_data[num_month[month_num]] = []
						rainfall_data[num_month[month_num]].append(row[num_month[month_num].capitalize()])

	
	with open(path1+district+".csv") as file:
		reader = csv.reader(file)

		for index,row in enumerate(reader):
			
			month_num = index%12
			

			if rainfall_data.get(num_month[month_num+1]):
				rainfall_data[num_month[month_num+1]].append(row[0])
			else:
				rainfall_data[num_month[month_num+1]] = []
				rainfall_data[num_month[month_num+1]].append(row[0])

	
	return rainfall_data



def get_observation_matrix(state_dic,data,plant):

	rain = []
	num_month = num_to_month()
	
	for i in range(1,13):
		
		rain += [i for i in state_dic[num_month[i]]]
	
	plant_state = []
	for i in range(36):
		 plant_state.append(data[plant][i])
	
	
	observation = zip(plant_state,rain[48:84])
	
	return rain,observation


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

	


def rain_fun(path,power_plant_dic,indi_prob_dic,state_dic,transaction_matrix,consolidated_dic,plant_state_dic,plant):
	
	with open(path+"\\plant_district.csv") as f:
		reader = csv.DictReader(f)

		for row in reader:

			if plant_state_dic.get(row["STATION"].replace("  "," ")):
				if row["District"]:
								
					plant_state_dic[row["STATION"].replace("  "," ")].append(str(row["District"].capitalize().replace('\\xa0',' ')).strip())

	plant_state_dic = {key:value for key,value in plant_state_dic.iteritems() if len(value) != 1 }	

	if plant_state_dic.get(plant):
	
		state_path1 = path+"\\d2\\"
		state_path2 = path+"\\monthly-rainfall\\"

		rainfall_data = get_rainfall_data(plant, plant_state_dic[plant][0], plant_state_dic[plant][1], state_path1,state_path2)
		
		indi_prob_dic = {}
		state_dic = {}

		inp = [(key, value, indi_prob_dic, state_dic) for key, value in rainfall_data.iteritems()]
		
		error, output = plmapt(get_proba, inp, [], len(inp))
		#pprint (output[-1])
		indi_prob_dic = output[-1][0]
		state_dic = output[-1][1]
		
		rain,observation = get_observation_matrix(state_dic,consolidated_dic,plant)

		#print state[plant]
		transaction_matrix_dic =  get_observation_prob(observation,plant)
		
		
		dic_list = [
			(rainfall_data,plant+" rainfall"),
			(indi_prob_dic,plant+" indi_rain"),
			(state_dic,plant+" state_rainfall"),
			(transaction_matrix_dic,plant+" observation_matrix"),
			(plant_state_dic,"power_state"),
			]
		inp = [(i[0],path+"\\json_files\\",i[1]) for i in dic_list]
		error, output = plmapt(file_write_json, inp, [], len(inp))
		return (transaction_matrix_dic,indi_prob_dic,state_dic,observation,rain,plant)
	else:
		return ("District not present",0,0,0,0,0)

if __name__=="__main__":
	path = os.getcwd()
	folders = ["monthly-power-generation"]
	plant = "SATPURA TPS"
	category = "THERMAL"
	fuel = "COAL"
	power_plant_dic,indi_prob_dic,state_dic,transaction_matrix,consolidated_dic,plant_state_dic = get_prob(folders,category,fuel)
	rain_fun(path,power_plant_dic,indi_prob_dic,state_dic,transaction_matrix,consolidated_dic,plant_state_dic,plant)
