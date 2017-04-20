import os
import csv
import json
import operator
from collections import Counter
from collections import defaultdict

from plmap import plmapt
from pprint import pprint
import numpy as np

from getFile import month_to_num
from getFile import num_to_month

def default_to_regular(d):
    if isinstance(d, defaultdict):
        d = {k: default_to_regular(v) for k, v in d.iteritems()}
    return d


def month_count():

	month_to_num_dic = month_to_num()
	key_list = sorted(month_to_num_dic.keys(),key=month_to_num_dic.get)
	
	
	ret_dic = defaultdict(list)
	return ret_dic



def get_transtition_matrix(key, value, transaction_matrix_dic,consolidated_dic):

	num_month_dic = num_to_month()
	matrix = np.zeros((3,3))
	
	consolidated_values = []
	times = 1
	while times <= 8:
		consolidated_values += [value[num_month_dic[i]][times-1] for i in range(1,13)]
		times += 1
	
	for (x,y),c in Counter(zip(consolidated_values, consolidated_values[1:])).iteritems():
		matrix[x-1,y-1] = c
		
	matrix1 = matrix.tolist()
	
	for i in matrix1:
		su = sum(i)
		
		for j in i:
			i[i.index(j)] = round(j/float(su),2)

	transaction_matrix_dic[key] = matrix1
	consolidated_dic[key] = consolidated_values

	return transaction_matrix_dic,consolidated_dic


def get_proba(key, value, prob_dic, state_dic):
	"""
	increase = 1, decrease = 2, equal = 3
	"""
	prob_dic[key] = defaultdict(list)
	esti_list = []
	state_dic[key] = defaultdict(list)
	for month,value_list in value.iteritems():
		
		value_list =[i.replace(",","") for i in value_list]
		prev, increase, decrease, equal, total = 0,0,0,0,0
		for actual in value_list:
			
			actual = int(round(float(actual),2))
			
			
			diff = abs(int(actual)-int(prev))

			esti = int(round(float(50.0*int(diff)/100),2))
			esti_list.append(esti)
			if int(prev)<int(actual) and diff > esti:
				state_dic[key][month].append(1) 
				increase +=1
			elif int(prev)>int(actual) and diff >esti:
				state_dic[key][month].append(2)
				decrease +=1
			else:
				state_dic[key][month].append(3)
				equal +=1
			prev = actual
			total +=1
		
	
		prob_dic[key][month] = [round(increase/float(total),2), round(decrease/float(total),2), round(equal/float(total),2)] 
	#print prob_dic
	# print(esti_list)
	return prob_dic,state_dic



def file_write_json(dic, path, file_name):
	f_json = json.dumps(dic)
	#print path+"\\"+file_name
	path = path+"/json_files/"
	if not os.path.exists(path):
		os.makedirs(path)
	with open(path+file_name+".json","w") as file:
		file.write(f_json)



def get_prob(folders, category):
	
	path = os.getcwd()
	
	total = 0
	power_plant_dic = {}
	plant_state_dic = {}
	month_not_present = defaultdict(list)
	power_plant_dic = defaultdict(dict)
	for i in folders:

		file_path = path+"/"+i+"/"
		total = 0
		
		for subdir, dire, files in os.walk(file_path):
			tmp_str =  subdir
			
			tmp_str = subdir.split("/")[-1].strip()
			
			if tmp_str and type(eval(tmp_str)) == int:
				
				num_month_dic = num_to_month()

				for i in range(1,13):
					month = num_month_dic[i]
					csv_path = subdir+"/"+num_month_dic[i]+"-"+tmp_str+".csv"
					if os.path.exists(csv_path):

						with open(csv_path) as fr:
							reader = csv.DictReader(fr)

							station_list = []
							for row in reader:

								if row["CATEGORY"] == category and row["FUEL"] == "COAL":
									if power_plant_dic.get(row["STATION"]):
										if not row["STATION"] in station_list:
											power_plant_dic[row["STATION"]][month].append(row["ACTUAL GENERATION"])
											station_list.append(row["STATION"])
										


									else:
										station_list.append([row["STATION"]])
										power_plant_dic[row["STATION"]] = month_count()

										if len(month_not_present.keys())!=0:
											for key,value in month_not_present.iteritems():
												power_plant_dic[row["STATION"]][key] += value

										power_plant_dic[row["STATION"]][month].append(row["ACTUAL GENERATION"])
										plant_state_dic[row["STATION"]] = row["STATE"]
										
						

					else:
						
						month_not_present[month].append('0')
						
		for key,value in power_plant_dic.iteritems():
			for i in month_to_num().keys():
				if len(value[i]) < 8:
					value[i] += ['0']*(8-len(value[i]))
		
				
		
		power_plant_dic = default_to_regular(power_plant_dic)
					


		indi_prob_dic = defaultdict(dict)
		state_dic = defaultdict(dict)
		# for key, value in power_plant_dic.iteritems():

		# 	if key.__contains__("CHANDRAPUR(MAHARASHTRA)"):
				
				
		# 		x,y = get_proba(key,value, indi_prob_dic, state_dic)

		# 		x = default_to_regular(x)
		# 		y = default_to_regular(y)

		# 		pprint(x)
		# 		pprint(y)
		# 		break
		# exit()
		inp = [(key,value,indi_prob_dic,state_dic) for key,value in power_plant_dic.iteritems()]
		error, output = plmapt(get_proba, inp, [], len(power_plant_dic.keys())/2)
		
		output_dic = output[-1]
		#print output_dic
		indi_prob_dic,state_dic = output_dic
		indi_prob_dic = default_to_regular(indi_prob_dic)
		state_dic = default_to_regular(state_dic)
		
		transaction_matrix = {}
		consolidated_dic = {}
		# for key, value in state_dic.iteritems():

		# 	if key.__contains__("AKALTARA"):
		# 		for x,v in value.iteritems():
		# 			v = [str(i) for i in v]
		# 			pprint(x+" : "+" ".join(v))
				
		# 		x,y = get_transtition_matrix(key,value,transaction_matrix,consolidated_dic)

		# 		x = default_to_regular(x)
		# 		# y = default_to_regular(y)

		# 		pprint(x)
		# 		print y
		# 		break
		# exit()

		inp = [(key,value,transaction_matrix,consolidated_dic) for key, value in state_dic.iteritems()]
		error, output = plmapt(get_transtition_matrix, inp, [], len(state_dic.keys())/2)
		transaction_matrix,consolidated_dic = output[-1]

		dic_list = [
				(power_plant_dic,"power_plant"),
				(indi_prob_dic,"indi_prob"),
				(state_dic,"state"), 
				(transaction_matrix,"transaction_matrix"),
				(consolidated_dic,"consolidated_state"),
				(plant_state_dic,"power_state")
				]
		inp = [(i[0],path,i[1]) for i in dic_list]
		error, output = plmapt(file_write_json, inp, [], len(inp))
	return (state_dic,indi_prob_dic,transaction_matrix,consolidated_dic)
		
		
if __name__=="__main__":
	folders = ["monthly-power-generation"]
	
	category = "THERMAL"
	
	get_prob(folders, category)