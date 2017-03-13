import os
import csv
import json
from collections import Counter

from plmap import plmapt
from pprint import pprint
import numpy as np


def get_transtition_matrix(key, value, transaction_matrix_dic):
	total = len(value)
	matrix = np.zeros((3,3))
	for (x,y),c in Counter(zip(value, value[1:])).iteritems():
		matrix[x-1,y-1] = c
		
	matrix1 = matrix.tolist()
	
	for i in matrix1:
		su = sum(i)
		
		for j in i:
			i[i.index(j)] = round(j/float(su),2)
	transaction_matrix_dic[key] = matrix1
	
	return transaction_matrix_dic


def get_proba(key, value, prob_dic, state_dic):
	"""
	increase = 1, decrease = 2, equal = 3
	"""
	
	prev, increase, decrease, equal, total = 0,0,0,0,0
	state_dic[key] = []
	for i in value:
		
		i = i.replace(",","")
		i = int(round(float(i),2))
		if int(prev)<int(i):
			state_dic[key].append(1)
			increase +=1
		elif int(prev)>int(i):
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



def file_write_json(dic, path, file_name):
	f_json = json.dumps(dic)
	#print path+"\\"+file_name
	with open(path+"\\"+file_name+".json","w") as file:
		file.write(f_json)



def get_prob(folders, category):
	path = os.getcwd()
	#print path
	total = 0
	power_plant_dic = {}
	plant_state_dic = {}
	for i in folders:
		file_path = path+"/"+i+"/"
		total = 0
		os.chdir(file_path)
		increase, decrease, equal, total = 0,0,0,0
		for subdir, dire, files in os.walk("."):
			
			for file in files:
				total +=1
				with open(subdir+"/"+file) as fr:
					reader = csv.DictReader(fr)
					prev = 0
					for row in reader:
						if row["CATEGORY"] == "THERMAL" and row["FUEL"] == "COAL":
							if power_plant_dic.get(row["STATION"]):
								power_plant_dic[row["STATION"]].append(row["ACTUAL GENERATION"])
							else:
								#print power_plant_dic["CHANDRAPUR(MAHARASHTRA) STPS"]
								time = total-2
								power_plant_dic[row["STATION"]] = ['0']*time
								power_plant_dic[row["STATION"]].append(row["ACTUAL GENERATION"])
								plant_state_dic[row["STATION"]] = row["STATE"]

				
		
		
		for key,value in power_plant_dic.iteritems():
			if len(value) != total:
				#print value
				
				length = len(value)
				#print length
				rem = total - len(value)
				for i in range(rem):
					value.append('0')
				power_plant_dic[key] = value
				


		indi_prob_dic = {}
		state_dic = {}
		#for key, value in power_plant_dic.iteritems():
		#	pprint(get_proba(key,value, indi_prob_dic, state_dic))
		#	break
		
		inp = [(key,value,indi_prob_dic,state_dic) for key,value in power_plant_dic.iteritems()]
		error, output = plmapt(get_proba, inp, [], len(power_plant_dic.keys())/2)
		
		output_dic = output[-1]
		#print output_dic
		indi_prob_dic,state_dic = output_dic

		
		transaction_matrix = {}

		inp = [(key,value,transaction_matrix) for key, value in state_dic.iteritems()]
		error, output = plmapt(get_transtition_matrix, inp, [], len(state_dic.keys())/2)
		transaction_matrix = output[-1]

		dic_list = [
				(power_plant_dic,"power_plant"),
				(indi_prob_dic,"indi_prob"),
				(state_dic,"state"), 
				(transaction_matrix,"transaction_matrix"),
				(plant_state_dic,"power_state")
				]
		inp = [(i[0],path,i[1]) for i in dic_list]
		error, output = plmapt(file_write_json, inp, [], len(inp))
	return (state_dic,indi_prob_dic,transaction_matrix)
		
		
if __name__=="__main__":
	folders = ["monthly-power-generation"]
	
	category = "THERMAL"
	
	get_prob(folders, category)