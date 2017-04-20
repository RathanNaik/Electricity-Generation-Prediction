import urllib as url
import os, calendar

from plmap import plmapt
from csv_from_excel import csv_to_excel
from collections import OrderedDict as odict

def month_to_num():


    d = {"january":1, "february":2,"march":3, "april":4,"may":5,"june":6,"july": 7, "august":8, "september": 9, "october" :10, "november" :11, "december": 12}
    
    return d

def num_to_month():
    rev_dic = {v:k for k, v in month_to_num().iteritems()}
    return rev_dic

def download_url(url_str, cal_dic, rev_dic):

    
    month, year = url_str.split("resources/")[1].split("/")[0].split("-")[-2:]
    data_set = '-'.join(url_str.split("resources/")[1].split("/")[0].split("-")[:-2])
    new_url = url_str.split(month)[0]
    i_year = eval(year)
    month_num = cal_dic[month]
    if not os.path.exists("./"+data_set):
        os.makedirs(data_set)
    while i_year<=2015:
        
        directory = os.path.join("./"+data_set, str(i_year))
        #directory = "./"+str(i_year)
        if not os.path.exists(directory):
            os.makedirs(directory)
        while month_num <= 12:
            file_name = rev_dic[month_num]+"-"+str(i_year)
            extension = ".csv"
            #print month_num
            if not os.path.exists(directory + file_name+extension):
                url_to_download = new_url + file_name +"/download"
                fullname = os.path.join(directory, file_name+extension)
                read_url = url.urlopen(url_to_download).read()
                if read_url.__contains__("window.location.href =") :
                    actual_url = eval(url.urlopen(url_to_download).read().split("window.location.href =")[1].split("\n")[0].strip())
                    #print actual_url
                    url.urlretrieve(actual_url,fullname)
            month_num +=1
            
            if month_num == 13:
                month_num = 1
                break
            
        i_year += 1
                
            
        

if __name__=="__main__":
    #print type(monthToNum())
    path = "./monthly-rainfall/"
    if not os.path.exists(path):
        os.makedirs(path)
        
    csv_to_excel(path,".\Datasets\Rainfall\District-wise Rainfall data_2004-2010.xls")
    cal_dic = month_to_num()
    #download_url(f, cal_dic, numToMonth())
    with open("url.txt","r") as f:
        inp = [(i.strip(),cal_dic, num_to_month()) for i in f.readlines()]
        error, output = plmapt(download_url, inp, [], len(inp))
        print error
    
    #f.close()
   
