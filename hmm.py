import os
import json
import operator
from pprint import pprint
import itertools as ite
import json
from get_proba import get_prob
from tester import rain_fun
from plmap import plmapt
from get_proba import file_write_json

def state_dic():
	return {"i":1,"d":2,"e":3}

def hmm_way(state_sequence_dic,sequence,t):
	
	output = []

	for i in range(t):
		total = 0
		for key,value in state_sequence_dic.iteritems():
			
			if key[i] == sequence:
				total += value
			
		output.append(total)
	
	return output



def dp_way(perms,pi,plant_state_matrix,observation_matrix,t,sequence_observation):
	state_convert = state_dic()
	state_sequence_dic = {}
	
	for string in perms:
		i = 0
		p = 1
		#print string
		for sub_index in range(len(string)-1):
			value = state_convert[string[sub_index]] - 1
			#print value
			
			if i == 0:
				#print observation_matrix[value][sequence_observation[i]-1]
				x = pi[value]*observation_matrix[value][sequence_observation[i]-1]
				#print x
				p *= x
			else:
				value_1 = state_convert[string[sub_index+1]]-1
				#print plant_state_matrix
				x = plant_state_matrix[value][value_1] * observation_matrix[value_1][sequence_observation[i]-1]
				#print x
				p *=  x
			i+=1

		state_sequence_dic[string] = p
	
	#pprint(state_sequence_dic)
	return max(state_sequence_dic.iteritems(), key = operator.itemgetter(1))[0], state_sequence_dic


def error(actual, calcul):
	return 100 - round((abs(actual-calcul)/float(actual))*100,2)



if __name__=="__main__":
	path = os.getcwd()
	plant_states_dic, plant_indi_prob, plant_state_matrix = get_prob(["monthly-power-generation"],"THERMAL")
	observation_matrix, rain_indi_prob, rain_state, plant = rain_fun(path)
	t = 3
	#print observation_matrix[plant]
	#print observation_matrix[plant][0][0]
	#sequence_observation = [3,2,1 ] #chanrapur
	#sequence_observation = [3,3,3] #dn tata
	sequence_observation = [3,3,1]
	state_sequence = ["i","d","e"]
	perms = []
	
	perms =  ["".join(p) for p in ite.product(state_sequence,repeat=t)]

	#perms = sorted(set(perms))

	pi = plant_indi_prob[plant]
	#print pi
	dp, state_sequence_dic = dp_way(perms, pi, plant_state_matrix[plant], observation_matrix[plant], t,sequence_observation)
	print dp
	hmm_dic = {}
	#print hmm_way(state_sequence_dic,"i",t,hmm_dic)
	for i in state_sequence:
		hmm_dic[i] = hmm_way(state_sequence_dic,i,t)

	print  state_sequence_dic["idi"], state_sequence_dic[dp]
	print error(state_sequence_dic["idi"],state_sequence_dic[dp])
	pprint (hmm_dic)
	file_write_json(state_sequence_dic,path,plant+" state sequence")
	#print plant_state_matrix[plant]