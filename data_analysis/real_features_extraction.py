import MySQLdb
import sqlite3
import json
import ast
import pandas as pd
import apsw
import math
import sys
from numpy import mean, std
from copy import deepcopy

mobile_=0
N=5 #keystrokes

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     port=8889, 
                     user="phpmyadminuser", # your username
                      passwd="password", # your password
                      db="truth_or_lie") #name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor() 

id="A.session_id"
if sys.argv[1]!="all":
    id=sys.argv[1]
queryNOmobile="""
SELECT
            A.question_id,
            A.text_answer, 
            A.keystroke,
            A.accellerometer_typing,
            A.gyroscope_typing,
            A.timestamp_prompted,
            A.timestamp_first_digit,
            A.timestamp_enter,
            A.gyroscope_before,
            A.accellerometer_before, 
            A.timestamp_tap,
            S.session_id,
            S.mind_condition,
            S.device_info,
            Q.gulpease
FROM 
            sessions_long as S,
            answers_long as A, 
            questions_long as Q
WHERE 
            S.session_id = """ + id + """ AND 
            Q.question_id= A.question_id AND 
            Q.language="Italian"
ORDER BY S.session_id, A.question_id;
"""
                
# Use all the SQL you like
print("query executing...", cur.execute(queryNOmobile))
print("End")

def string_to_list_of_dict(st):
    if len(st) > 2: 
        st=st.replace("},{","}|{")
        st=st.replace("[","")
        st=st.replace("]","")
        st=st.replace(":\",\"",":\"comma\"")
        st=st.replace(":\":\"",":\"colon\"")
        st=st.replace(":\";\"",":\"period\"")
        st=st.replace(":\"\r\"",":\"ENTER\"")
        
        st=st.replace(":\',\'",":\'comma\'")
        st=st.replace(":\':\'",":\'colon\'")
        st=st.replace(":\';\'",":\'period\'")
        st=st.replace(":\'\r\'",":\'ENTER\'")
        
        #list of dictionaries
        st_l = st.split("|")
        st_list_dict=[]
        for elem in st_l:
            elem=elem.replace("{","")
            elem=elem.replace("}","")
            #just in case
            tmp=elem.split(",")
            tmp=[t.replace("\"","") for t in tmp]
            dict_tmp={}
            for t in tmp:
                k=t.split(":")
                #print k
                k1=k[1]
                if k[0] == "tn": # or k[0] == "t": #timestamp
                    k1=float(k1)
                elif k[0]== "cod": #key code
                    k1=int(k1)
                else:
                    k1="%s"%k1  #character or UP/DOWN
                dict_tmp["%s"%k[0]]=k1
            st_list_dict.append(dict_tmp)
        st_final=sorted(st_list_dict, key=lambda k: k['tn']) 
        return st_final

def string_to_list_of_dict_sensors(st):
    if len(st) > 2: 
        st=st.replace("},{","}|{")
        st=st.replace("[","")
        st=st.replace("]","")
        st=st.replace(":\",\"",":\"comma\"")
        st=st.replace(":\":\"",":\"colon\"")
        st=st.replace(":\";\"",":\"period\"")
        st=st.replace(":\"\r\"",":\"ENTER\"")
        
        st=st.replace(":\',\'",":\'comma\'")
        st=st.replace(":\':\'",":\'colon\'")
        st=st.replace(":\';\'",":\'period\'")
        st=st.replace(":\'\r\'",":\'ENTER\'")
        
        #list of dictionaries
        st_l = st.split("|")
        st_list_dict=[]
        for elem in st_l:
            elem=elem.replace("{","")
            elem=elem.replace("}","")
            #just in case
            tmp=elem.split(",")
            tmp=[t.replace("\"","") for t in tmp]
            dict_tmp={}
            for t in tmp:
                k=t.split(":")
                #print k
                k1=k[1]
                k1=float(k1)  #character or UP/DOWN
                dict_tmp["%s"%k[0]]=k1
            st_list_dict.append(dict_tmp)
        st_final=sorted(st_list_dict, key=lambda k: k['t']) 
        return st_final

def filter_unwanted_and_count(list_keys):
    tmp_list=[]
    
    #full_sequence=[]
    consecutive_press=[] #list of list
    current_sequence=[]
    
    def sequence_interupted(current_sequence):
        consecutive_press.append(current_sequence)
        return []
    #down only
    
    number_shift=0
    number_del=0
    number_canc=0
    number_arrow=0
    number_space=0
    number_break=0
    
    time_key_before_enter_down=0.
    time_key_before_enter_up=0.
    time_key_before_enter_flight=0.
    
    previous_key_down=None
    previous_key_up=None
    
    time_key_before_enter_down_raw=0.
    time_key_before_enter_up_raw=0.
    time_key_before_enter_flight_raw=0.
    
    previous_key_down_raw=None
    previous_key_up_raw=None
    
    time_key_array = []

    for key_ in list_keys:
        character=key_["character"]
        verse=key_["k"]
        key_code=key_["cod"]
        timestamp=float(key_["tn"])
        
        if verse=="UP" and previous_key_up is not None:
            time_key_array.append(timestamp - float(previous_key_up["tn"]))
            
        if character=="u0010" or key_code==16:  #filter shift
            #current_sequence=sequence_interupted(current_sequence)
            if verse=="UP":
                number_shift+=1
            continue
        
        elif key_code==8:  #filter del
            current_sequence=sequence_interupted(current_sequence)
            if verse=="UP":
                number_del+=1
            continue
        
        elif key_code==32:  #filter space
            #sequence_interupted() TODO is it interupted?
            if verse=="UP":
                number_space+=1
            #continue #now I consider the spaces too
        
        elif key_code==46:  #filter canc
            current_sequence=sequence_interupted(current_sequence)
            if verse=="UP":
                number_canc+=1
            continue
        
        elif key_code>=112 and key_code<=122:  #filter f1 to f11
            current_sequence=sequence_interupted(current_sequence)
            continue
        
        elif key_code>=33 and key_code<=40: #filter arrow and pagup
            current_sequence=sequence_interupted(current_sequence)
            if verse=="UP":
                number_arrow+=1
            continue
        
        elif key_code==13: #filter ENTER
            current_sequence=sequence_interupted(current_sequence)
            #filtered
            if previous_key_down is not None and verse=="DOWN":
                time_key_before_enter_down=timestamp - float(previous_key_down["tn"])                
            if previous_key_up is not None and verse=="UP":
                time_key_before_enter_up=timestamp - float(previous_key_up["tn"])
            if previous_key_up is not None and verse=="DOWN":
                time_key_before_enter_flight= timestamp - float(previous_key_up["tn"])
            
            #raw
            if previous_key_down_raw is not None and verse=="DOWN":
                time_key_before_enter_down_raw =timestamp - float(previous_key_down_raw["tn"])                
            if previous_key_up is not None and verse=="UP":
                time_key_before_enter_up_raw = timestamp - float(previous_key_up_raw["tn"])
            if previous_key_up is not None and verse=="DOWN":
                time_key_before_enter_flight_raw = timestamp - float(previous_key_up_raw["tn"])
            continue 
            #End of digits!
        
        elif key_code==9 and key_code==225 and key_code==188 and key_code==18 and key_code==45 and key_code==17:  #filter tab, 
            current_sequence=sequence_interupted(current_sequence)
            continue
        
        else:
            if verse=="DOWN":
                previous_key_down=key_
            elif verse=="UP":
                previous_key_up=key_
            current_sequence.append(key_)
        
        if verse=="DOWN":
            previous_key_down_raw=key_
        elif verse=="UP":
            previous_key_up_raw=key_
            
        #I count all the keystrokes
        tmp_list.append(key_)
            
    #sequence_interupted()
    sum_mean=0
    length=len(time_key_array)
    if length > 0:
        for i in range(length):
            sum_mean+=time_key_array[i]
        
        mean=sum_mean/length
        sum_variance=0

        for i in range(length):
            sum_variance+=(time_key_array[i] - mean)**2

        variance = sum_variance/length
        for i in range(length):
            if time_key_array[i] > mean+math.sqrt(variance):
                number_break+=1

    return {"number_shift":number_shift,
            "number_del":number_del,
            "number_canc":number_canc,
            "number_arrow":number_arrow,
            "number_space":number_space,
            "number_break":number_break,
            "consecutive_press":consecutive_press,
            "consecutive_raw":[tmp_list],
            "time_key_before_enter_down":time_key_before_enter_down,
            "time_key_before_enter_up":time_key_before_enter_up,
            "time_key_before_enter_flight":time_key_before_enter_flight,
            "time_key_before_enter_down_raw":time_key_before_enter_down_raw,
            "time_key_before_enter_up_raw":time_key_before_enter_up_raw,
            "time_key_before_enter_flight_raw":time_key_before_enter_flight_raw,
            }

# print all the first cell of all the rows
data={}
session_id_list = []
fetchall = cur.fetchall()
for row in fetchall :
    """
    0    A.question_id,
    1    A.text_answer, 
    2    A.keystroke,
    3    A.accellerometer_typing,
    4    A.gyroscope_typing,
    5    A.timestamp_prompted,
    6    A.timestamp_first_digit,
    7    A.timestamp_enter, 
    8    A.gyroscope_before,
    9    A.accellerometer_before,
    10   A.timestamp_tap,
    11   S.session_id,
    12   S.mind_condition,
    13   S.device_info,
    14   Q.gulpease
    """    
    question_id = row[0]
    answer = row[1]
    json_keystroke = row[2]
    accellerometer_typing = row[3]
    gyroscope_typing = row[4]
    gyroscope_before = row[8]
    accellerometer_before = row[9]
    session_id=row[11]
    mind_condition=row[12]
    mobile=row[13]
    gulpease=row[14]

    if session_id not in session_id_list:
        session_id_list.append(session_id)
        data[session_id] = []

    #tmp={"question_id":question_id, "session_id":session_id, "answer":answer}
    
    #tmp["prompted-firstdigit"]=float(row[6])-float(row[5])
    tmp={}
    tmp["firstdigit-enter"]=float(row[7])-float(row[6])
    #tmp["prompted-enter"]=float(row[7])-float(row[5])
    
    #tmp["answer_length"]=len(answer.strip())

    tmp["writing_time"] = tmp["firstdigit-enter"]
    tmp["writing_speed"] = len(answer.strip())/tmp["firstdigit-enter"]
    #tmp["question_text"]=text_short
    tmp["mind_condition"]=mind_condition
    tmp["gulpease"]=gulpease
    
    if (json_keystroke == "[]"):
        continue

    obj=string_to_list_of_dict(json_keystroke)
    features = filter_unwanted_and_count(obj)
    tmp["time_key_before_enter_down"]=features["time_key_before_enter_down"]
    tmp["number_del"]=features["number_del"]
    tmp["number_break"]=features["number_break"]
    data[session_id].append(tmp)

labels_data=["firstdigit-enter", "writing_time", "writing_speed", "mind_condition", "gulpease", "time_key_before_enter_down", "number_del", "number_break"]

file_o=open("features.txt","w")
for i,lab in enumerate(labels_data):
    file_o.write("\"%s\",\n"%(lab))
    print(lab)  

import csv,gzip

if sys.argv[1]!="all":
    file="features_one_session.csv"
else:
    print("Creation of features")
    file="features.csv"

print(sys.argv[1])
with open(file, 'w') as f:  # Just use 'w' mode in 3.x
    w = csv.DictWriter(f, labels_data)
    w.writeheader()
    for part in sorted(data):
        for row in data[part]:
            w.writerow(row)
            
