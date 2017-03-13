import os
import json
import csv
from pprint import pprint

from plmap import plmapt
from getFile import monthToNum, numToMonth
from get_proba import get_proba
from get_proba import file_write_json#(dic, path, file_name)

def get_rainfall_data(plant, state, district, path):
	rainfall_data = {}
	num_month = numToMonth()
	month_to_num = monthToNum()
	with open(path+state+".csv") as file:
		reader = csv.DictReader(file)

		for row in reader:
			#print row["District"].lower(), district.lower()
			if row["District"].strip() == district:
				#print "dadfsd"
				year = int(float(row["Year"]))
				
				rainfall_data[year] = []
				#print row["January"]
				for month_num in range(1,13):
					#print num_month
					#print num_month[month_num].capitalize()
					rainfall_data[year].append(row[num_month[month_num].capitalize()])

	return rainfall_data


if __name__=="__main__":
	path = os.getcwd()
	with open("power_state.json") as data_file:
		power_state = json.load(data_file)

	with open('state.json') as data_file:    
	    data = json.load(data_file)

	plant = "CHANDRAPUR(MAHARASHTRA) STPS"
	distrcit = "Chandrapur"
	state_path = path+"/monthly-rainfall/"

	rainfall_data = get_rainfall_data(plant, power_state[plant], distrcit, state_path)

	indi_prob_dic = {}
	state_dic = {}
	
	inp = [(key, value, indi_prob_dic, state_dic) for key, value in rainfall_data.iteritems()]
	
	error, output = plmapt(get_proba, inp, [], len(inp))
	#pprint (output[-1])
	indi_prob_dic = output[-1][0]
	state_dic = output[-1][1]

	dic_list = [(rainfall_data,"rainfall"),(indi_prob_dic,"indi_rain"),(state_dic,"state_rainfall")]
	inp = [(i[0],path,i[1]) for i in dic_list]
	error, output = plmapt(file_write_json, inp, [], len(inp))
