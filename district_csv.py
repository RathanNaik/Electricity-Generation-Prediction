import os
import csv
from pprint import pprint
path = os.getcwd()
old_path = path +"\\monthly-rainfall\\"

new_path = path +"\\distrct-rainfall\\"

if not os.path.exists(new_path):
	os.makedirs(new_path)

for sub,dir,files in os.walk(old_path):

	for file in files:
		print file
		#reader = csv.DictReader(open(old_path+file,"rb"))
		with open(old_path+file) as file:
			reader = csv.reader(file)
			district_dic = {}
			district_list = []

			
			for row in list(reader)[1:]:
				
				if district_dic.get(row[1]):
					district_dic[row[1]].append(row[2:])
				else:
					district_dic[row[1]] = []
					district_dic[row[1]].append(row[2:])

			for key,value in district_dic.iteritems():
				with open(new_path+key+".csv","wb") as f:
					writer = csv.writer(f)
					writer.writerows(value)
		
