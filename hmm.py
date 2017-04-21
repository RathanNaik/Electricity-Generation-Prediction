import os
import json
import operator
from pprint import pprint
import itertools as ite
import json
import csv

from plmap import plmapt

from get_proba import get_prob
from rainfall import rain_fun
from get_proba import file_write_json


def state_dictionary():
	return {"i":1,"d":2,"e":3}



def rev_state_dictionary():
	rev_dic = {v:k for k, v in state_dictionary().iteritems()}

	return rev_dic

def normalize(lis):

	while lis.__contains__(0.0):
	
		index = lis.index(0.0)
		for i,val in enumerate(lis):
			if i != index and val != 0.0:
				lis[i] = lis[i] - 0.01
				lis[index] += 0.01

def forward(pi,plant_state_matrix,observation_matrix,t,sequence_observation):
	
	f_prev = {}
	fwd = []

	normalize(pi)
	for i in plant_state_matrix:
		normalize(i)

	for i in observation_matrix:
		normalize(i)

	for i, observation_i in enumerate(sequence_observation):
		f_curr = {}

		for j in range(3):
			if i == 0:
				prev_f_sum = pi[j]

			else:
				prev_f_sum = sum(f_prev[k]*plant_state_matrix[k][j] for k in range(3))
			
			f_curr[j] = observation_matrix[j][observation_i-1]*prev_f_sum
			
		fwd.append(f_curr)
		f_prev = f_curr
	
	p_fwd = sum(f_curr[k]*plant_state_matrix[k][2] for k in range(3))
	

	bkw = []
	b_prev = {}

	for i,observation_i_plus in enumerate(reversed(sequence_observation[1:]+[None])):
		b_curr = {}

		for j in range(3):

			if i == 0:
				b_curr[j] = plant_state_matrix[j][1]
			else:
				b_curr[j] = sum(plant_state_matrix[j][l]*observation_matrix[l][observation_i_plus-1]*b_prev[l] for l in range(3))

		bkw.insert(0,b_curr)
		b_prev = b_curr
	#print observation_matrix
	p_bkw = sum(pi[l]*observation_matrix[l][sequence_observation[0]-1]*b_curr[l] for l in range(3))

	posterior = []

	for i in range(len(sequence_observation)):
		posterior.append([fwd[i][j] * bkw[i][j] / p_fwd for j in range(3)])

	
	return fwd, bkw,posterior



def dp_way(perms,pi,plant_state_matrix,observation_matrix,t,sequence_observation):
	state_convert = state_dictionary()
	state_sequence_dic = {}
	
	for string in perms:
		i = 0
		p = 1
		
		for sub_index in range(len(string)-1):
			value = state_convert[string[sub_index]] - 1
			#print value
			
			if i == 0:
				
				x = pi[value]*observation_matrix[value][sequence_observation[i]-1]
				
				p *= x
				
			else:
				value_1 = state_convert[string[sub_index+1]]-1
				
				x = plant_state_matrix[value][value_1] * observation_matrix[value_1][sequence_observation[i]-1]
				

				p *=  x
			i +=1
		
		state_sequence_dic[string] = p
	state_sequence_dic = {k:v for k,v in state_sequence_dic.iteritems() if v!=0.0}
	
	return max(state_sequence_dic.iteritems(), key = operator.itemgetter(1))[0], state_sequence_dic



def hmm_way(state_sequence_dic,sequence,t):
	
	output = []

	for i in range(t):
		total = 0
		for key,value in state_sequence_dic.iteritems():
			
			if key[i] == sequence:
				total += value
			
		output.append(total)
	
	return output


if __name__=="__main__":
	

	path = os.getcwd()
	path += "\\"
	json_path = path +"prediction_files\\"
	plant = "CHANDRAPUR(MAHARASHTRA) STPS"
	power_plant_dic,indi_prob_dic,state_dic,transaction_matrix,consolidated_dic,plant_state_dic = get_prob(["monthly-power-generation"],"THERMAL","COAL")

	month_value = indi_prob_dic[plant]
	max_value = 1
	for key,value in month_value.iteritems():
		inc,dec,eq = value[0],value[1],value[2]	

		if (inc+dec) < eq/2:
			max_value += 1
		else:
			max_value += -1

	if max_value <= 4:

		observation_matrix, rain_indi_prob, rain_state,observation,rain_list, plant = rain_fun(path,power_plant_dic,indi_prob_dic,state_dic,transaction_matrix,consolidated_dic,plant_state_dic,plant)
		
		if type(observation_matrix) != str:
			state_sequence = ["i","d","e"]
			t = 3
			
			actual_list = consolidated_dic[plant][84:84+t]
			actual_list = [rev_state_dictionary()[i] for i in actual_list]
			actual_string = "".join(actual_list)
			
			
			sequence_observation = rain_list[132:132+t]
			
			perms = []
			
			perms =  ["".join(p) for p in ite.product(state_sequence,repeat=t)]

			
			
			pi = indi_prob_dic[plant]["december"]
			
			
			
			a,b,c = forward(pi,transaction_matrix[plant],observation_matrix[plant],t,sequence_observation)
			#pprint(a)
			
			
			pi = c[2]
			pi = [round(i,2) for i in pi]
			
			dp, state_sequence_dic = dp_way(perms, pi, transaction_matrix[plant], observation_matrix[plant], t,sequence_observation)
			with open("output.txt","w") as file:

				file.write(" ".join([rev_state_dictionary()[i] for i in sequence_observation])+"\t rainfall sequence \n")
				file.write(dp+" predicted "+actual_string+" actual result")
			hmm_dic = {}
			

		else:
			with open("output.txt","w") as file:
				file.write(observation_matrix)
			

	else:
		with open("output.txt","w") as file:
			file.write(plant+" has been closed")
	#print plant_state_matrix[plant]