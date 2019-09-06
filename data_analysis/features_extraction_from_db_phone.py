#!/usr/bin/python

# This code is a compliment to "Covert lie detection using keyboard dynamics".
# Copyright (C) 2017  Riccardo Spolaor
# See GNU General Public Licence v.3 for more details.
# NO WARRANTY EXPRESSED OR IMPLIED. USE AT YOUR OWN RISK.

import MySQLdb
import sqlite3
import json
import ast
import pandas as pd
import apsw
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
            Q.text_short
FROM 
            sessions_long as S,
            answers_long as A, 
            questions_long as Q
WHERE 
            S.session_id = A.session_id AND  
            Q.question_id= A.question_id AND Q.language="Italian"
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
            print(dict_tmp)
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

def keyrepetition_check(list_keys):
    keys=[]
    for keys_ in list_keys:
        for key_ in keys_:
            character=key_["character"]
            verse=key_["k"]
            if verse=="DOWN":
                keys.append(character)
            #timestamp=key_["tn"]
    consecutive=[]
    repetition_consecutive=0
    num_keys={}
    for III in enumerate(keys):
        if III not in num_keys.keys() :
            num_keys[III]=0
        num_keys[III]+=1
        if len(consecutive)>=1 and consecutive[-1] == III:
            consecutive.append(III)
            if len(consecutive)>repetition_consecutive:
                repetition_consecutive=len(consecutive)    
        else:
            consecutive=[III]
    max_keys=0 ###the most repeated key
    for k in num_keys:
        if num_keys[k]>max_keys:
            max_keys=num_keys[k]
    return {"max_key_repeated":max_keys, "max_consecutive_key":repetition_consecutive}

def first_n_events(list_keys,n):
    used_shift=0
    count=0
    tmp_list_n=[] 
    
    for i,key_ in enumerate(list_keys):
        character=key_["character"]
        verse=key_["k"]
        key_code=key_["cod"]
        timestamp=key_["tn"]
        
        #Icount all the keystrokes
        if character=="u0010" or key_code==16:  #filter shift
            #current_sequence=sequence_interupted(current_sequence)
            if verse=="DOWN":
                used_shift+=1
            continue
        
        elif key_code==8:  #filter del
            continue
        
        #elif key_code==32:  #filter space
            #sequence_interupted() TODO is it interupted?
            #continue

        elif key_code==46:  #filter canc
            continue
        
        elif key_code>=112 and key_code<=122: #filter f1 to f11
            continue
        
        elif key_code>=33 and key_code<=40: #filter arrow and pagup
            continue
        
        elif key_code==13:  #filter ENTER
            continue 
            #End of digits!
        
        elif key_code==9 and key_code==225 and key_code==188 and key_code==18 and key_code==45 and key_code==17:  #filter tab, 
            continue
        
        else:
            tmp_list_n.append(key_)

    #list_n_keys=[None for i in range(n*2)] #N*2 sia up che down
    list_keys_verse=[]
    list_keys_delay=[]
    list_keys_up=[]
    list_keys_down=[]
    list_flight=[]
    list_press=[]
    
    previous=None
    previous_up=None
    previous_down=None
    for i,key_ in enumerate(tmp_list_n[:(n*2 + 1)]):
        if previous is None:
            previous=key_
        else:
            list_keys_verse.append(1.0 if key_["k"]=="UP" else 0.0)
            list_keys_delay.append(float(key_["tn"])-float(previous["tn"]))      
        if key_["k"]=="UP":
            if previous_up is None:
                previous_up=key_
            else:
                list_keys_up.append(float(key_["tn"])-float(previous_up["tn"]))
            
            if previous_down is not None:
                list_flight.append(float(key_["tn"])-float(previous_down["tn"]))                             
        else:
            if previous_down is None:
                previous_down=key_
            else:
                list_keys_down.append(float(key_["tn"])-float(previous_down["tn"]))
            
            if previous_up is not None:
                list_press.append(float(key_["tn"])-float(previous_up["tn"]))
    
    features_n={"firstN_used_shift":used_shift,
                "firstN_both_mean":mean(list_keys_delay), "firstN_both_std":std(list_keys_delay),  
                "firstN_up_mean":mean(list_keys_up), "firstN_up_std":std(list_keys_up), 
                "firstN_down_mean":mean(list_keys_down), "firstN_down_std":std(list_keys_down), 
                "firstN_flight_mean":mean(list_flight), "firstN_flight_std":std(list_flight), 
                "firstN_press_mean":mean(list_press), "firstN_press_std":std(list_press)}
    
    listN_keys_verse=[0.5 for i in range(n*2)]
    listN_keys_delay=[-10000.0 for i in range(n*2)]
    listN_keys_up=[-10000.0 for i in range(n)]
    listN_keys_down=[-10000.0 for i in range(n)]
    listN_flight=[-10000.0 for i in range(n)]
    listN_press=[-10000.0 for i in range(n)]
    
    for i,datum in enumerate(list_keys_verse[:(n*2)]):
        listN_keys_verse[i]=datum
        
    for i,datum in enumerate(list_keys_delay[:(n*2)]):
        listN_keys_delay[i]=datum
        
    for i,datum in enumerate(list_keys_up[:n]):
        listN_keys_up[i]=datum
        
    for i,datum in enumerate(list_keys_down[:n]):
        listN_keys_down[i]=datum
        
    for i,datum in enumerate(list_flight[:n]):
        listN_flight[i]=datum
        
    for i,datum in enumerate(list_press[:n]):
        listN_press[i]=datum
        
    ###################    
    
    for i,datum in enumerate(listN_keys_verse):
        features_n["firstN_verse_%s"%i]=datum
        
    for i,datum in enumerate(listN_keys_delay):
        features_n["firstN_both_%s"%i]=datum
        
    for i,datum in enumerate(listN_keys_up):
        features_n["firstN_up_%s"%i]=datum
        
    for i,datum in enumerate(listN_keys_down):
        features_n["firstN_down_%s"%i]=datum
        
    for i,datum in enumerate(listN_flight):
        features_n["firstN_fligth_%s"%i]=datum
        
    for i,datum in enumerate(listN_press):
        features_n["firstN_press_%s"%i]=datum

    return features_n


def first_n_events_labels(n):     
    features_n_labels=["firstN_used_shift","firstN_both_mean","firstN_both_std",  
                "firstN_up_mean", "firstN_up_std", 
                "firstN_down_mean", "firstN_down_std", 
                "firstN_flight_mean", "firstN_flight_std", 
                "firstN_press_mean", "firstN_press_std"]
    
    listN_keys_verse=[0.5 for i in range(n*2)]
    listN_keys_delay=[-10000.0 for i in range(n*2)]
    listN_keys_up=[-10000.0 for i in range(n)]
    listN_keys_down=[-10000.0 for i in range(n)]
    listN_flight=[-10000.0 for i in range(n)]
    listN_press=[-10000.0 for i in range(n)]    
        
    ###################    
    
    for i,datum in enumerate(listN_keys_verse):
        features_n_labels.append("firstN_verse_%s"%i)
        
    for i,datum in enumerate(listN_keys_delay):
        features_n_labels.append("firstN_both_%s"%i)
        
    for i,datum in enumerate(listN_keys_up):
        features_n_labels.append("firstN_up_%s"%i)
        
    for i,datum in enumerate(listN_keys_down):
        features_n_labels.append("firstN_down_%s"%i)
        
    for i,datum in enumerate(listN_flight):
        features_n_labels.append("firstN_fligth_%s"%i)
        
    for i,datum in enumerate(listN_press):
        features_n_labels.append("firstN_press_%s"%i)

    return features_n_labels


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
    
    for key_ in list_keys:
        character=key_["character"]
        verse=key_["k"]
        key_code=key_["cod"]
        timestamp=float(key_["tn"])
        
        if character=="u0010" or key_code==16:  #filter shift
            #current_sequence=sequence_interupted(current_sequence)
            if verse=="DOWN":
                number_shift+=1
            continue
        
        elif key_code==8:  #filter del
            current_sequence=sequence_interupted(current_sequence)
            if verse=="DOWN":
                number_del+=1
            continue
        
        elif key_code==32:  #filter space
            #sequence_interupted() TODO is it interupted?
            if verse=="DOWN":
                number_space+=1
            #continue #now I consider the spaces too
        
        elif key_code==46:  #filter canc
            current_sequence=sequence_interupted(current_sequence)
            if verse=="DOWN":
                number_canc+=1
            continue
        
        elif key_code>=112 and key_code<=122:  #filter f1 to f11
            current_sequence=sequence_interupted(current_sequence)
            continue
        
        elif key_code>=33 and key_code<=40: #filter arrow and pagup
            current_sequence=sequence_interupted(current_sequence)
            if verse=="DOWN":
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
    
    return {"number_shift":number_shift,
            "number_del":number_del,
            "number_canc":number_canc,
            "number_arrow":number_arrow,
            "number_space":number_space,
            "consecutive_press":consecutive_press,
            "consecutive_raw":[tmp_list],
            "time_key_before_enter_down":time_key_before_enter_down,
            "time_key_before_enter_up":time_key_before_enter_up,
            "time_key_before_enter_flight":time_key_before_enter_flight,
            "time_key_before_enter_down_raw":time_key_before_enter_down_raw,
            "time_key_before_enter_up_raw":time_key_before_enter_up_raw,
            "time_key_before_enter_flight_raw":time_key_before_enter_flight_raw,
            }

def series_statistics_extraction(label,series_):
    serie = pd.Series(series_)
    stats={}
    methods=["max","min","median","mad","std","kurt","var","mean","skew"]
    def get_value(pkts, method, params=None):   
            #print('get value %s on obj count %s ' % (method, pkts.count())
            try:
                res = getattr(pkts, method)() if params is None else getattr(pkts, method)(params) 
            except ZeroDivisionError:
                return 0.0
            is_nul=not pd.notnull(res)
            if res is None or is_nul:
                return 0.0
            else:
                return res 
    for method in methods:
        tmp=get_value(serie, method)
        stats[label+"_"+method]= tmp
    
        #quantile
    
    for i in range(1,10,1):
        stats[label+"_quantile%s"%(i*10)]=get_value(serie, "quantile",i/10.0)
                
    #number of packets
    stats[label+"_length"]=len(serie)

    """
    for w in range(int(max_length/(window_size/2))):
        for serie in [pkt_total_sizes, pkt_in_sizes,  pkt_out_sizes]:
            serie_w=serie[w*(window_size/2):w*(window_size/2)+window_size]
            for method in methods:
                stats.append(get_value(serie_w, method)) 
                
            #quantile
              
                for i in range(1,10,1):
                    stats.append(get_value(serie_w, "quantile",i/10.0))
                    
                #number of packets
                stats.append(len(serie_w))
    """    
    return stats

def series_statistics_labels(label=None):
    labels=["max","min","median","mad","std","kurt","var","mean","skew"]
        #quantile
    for i in range(1,10,1):
        labels.append("quantile%s"%(i*10))
            
        #number of packets
    labels.append("length")

    """
    for w in range(int(max_length/(window_size/2))):
        for serie in [pkt_total_sizes, pkt_in_sizes,  pkt_out_sizes]:
            serie_w=serie[w*(window_size/2):w*(window_size/2)+window_size]
            for method in methods:
                stats.append(get_value(serie_w, method)) 
                
            #quantile
              
                for i in range(1,10,1):
                    stats.append(get_value(serie_w, "quantile",i/10.0))
                    
                #number of packets
                stats.append(len(serie_w))
    """    
    return labels


def series_keystrokes_consecutive(list_dict_consecutive):
    series2_up=[]
    series2_down=[]
    series2_flight=[]
    series2_press=[]
    series2_both=[]
    
    series3_up=[]
    series3_down=[]
    series3_both=[]
    
    breakers=0 #down before up
    
    #list of consecutive keystrokes
    for keystrokes_ in list_dict_consecutive:
        #consecutive keystrokes
        previous_up=None
        previous_down=None
        previous_key=None
    
        #for TRIGRAPH
        previous2_up=None
        previous2_down=None
        
        previous2_key=None
    
        #I ignore the sequence of only 1 element
        if len(keystrokes_)<=1:
            continue
        
        for key_ in keystrokes_:
            character=key_["character"]
            verse=key_["k"]
            key_code=key_["cod"]
            timestamp=key_["tn"]
            
            #there are 2 consecutive down or 2 up
            if previous_key is not None and previous_key["k"]==verse:
                breakers+=1 
                #print previous_key["character"], key_["character"] #
            
            if verse=="UP":
                #DIGRAPH
                if previous_up is not None:
                    series2_up.append( timestamp - previous_up["tn"] )
                
                if previous_down is not None and previous_down["cod"]==key_code:
                    series2_press.append(timestamp - previous_down["tn"])
                
                #TRIGRAPH
                if previous2_up is not None:
                    series3_up.append( timestamp - previous2_up["tn"] )
                
                if previous2_down is not None:
                    series3_both.append( timestamp - previous2_down["tn"] )
                
                previous2_up=previous_up
                previous_up=key_
                
            elif verse=="DOWN":
                #DIGRAPH
                if previous_down is not None:
                    series2_down.append( timestamp - previous_down["tn"])
                if previous_up is not None: 
                    series2_flight.append(timestamp - previous_up["tn"])
                
                #TRIGRAPH
                if previous2_down is not None:
                    series3_down.append( timestamp - previous2_down["tn"])
                
                previous2_down=previous_down
                previous_down=key_
                
            #both
            if previous_key is not None:
                series2_both.append(timestamp - previous_key["tn"])
                    
            previous2_key=previous_key
            previous_key=key_
#     
#     if breakers>6:
#         for elem in list_dict_consecutive:
#             for i in elem :
#                 print i
#             print "-----------------------"
#             
#         print "############################"
#

    return {"series_di_both":series2_both,
            "series_di_up":series2_up,
            "series_di_down":series2_down,
            "series_di_flight":series2_flight,
            "series_di_press":series2_press,
            "series_tri_up":series3_up,
            "series_tri_down":series3_down,
            "series_tri_both":series3_both,
            "breakers":breakers #significant only on UP and DOWN   
            } 


###################################################################
####################### main ######################################
###################################################################
only_down_sessions=[]
all_sessions=[]

DATA_only_down={}
DATA_UPandDOWN={}
data={}
session_id_list = []

# print all the first cell of all the rows
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
    14   Q.text_short
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
    text_short=row[14]

    if session_id not in session_id_list:
        session_id_list.append(session_id)
        data[session_id] = []
    
    tmp={"question_id":question_id, "session_id":session_id, "answer":answer}
    
    tmp["prompted-firstdigit"]=float(row[6])-float(row[5])
    tmp["firstdigit-enter"]=float(row[7])-float(row[6])
    tmp["prompted-enter"]=float(row[7])-float(row[5])
    
    tmp["answer_length"]=len(answer.strip())

    """tmp["accelerometer_typing"]=string_to_list_of_dict_sensors(accellerometer_typing)"""
    
    tmp["question_text"]=text_short
    
    if (json_keystroke == "[]"):
        continue

    obj=string_to_list_of_dict(json_keystroke)
    features_N=first_n_events(obj,N)
    features = filter_unwanted_and_count(obj)
    series = series_keystrokes_consecutive(features["consecutive_press"])
    series_raw = series_keystrokes_consecutive(features["consecutive_raw"])
    
    repetitions=keyrepetition_check(features["consecutive_press"])
    tmp["max_key_repetition"]=repetitions["max_key_repeated"]
    tmp["max_key_consecutive"]=repetitions["max_consecutive_key"]
        
    tmp["number_shift"]=features["number_shift"]
    tmp["number_del"]=features["number_del"]
    tmp["number_canc"]=features["number_canc"]
    tmp["number_arrow"]=features["number_arrow"]
    tmp["number_shift"]=features["number_shift"]
    tmp["number_space"]=features["number_space"]
    tmp["number_delcanc"]=features["number_del"]+features["number_canc"]
        
    tmp["time_key_before_enter_down"]=features["time_key_before_enter_down"]
    tmp["time_key_before_enter_up"]=features["time_key_before_enter_up"]
    tmp["time_key_before_enter_flight"]=features["time_key_before_enter_flight"]
    tmp["time_key_before_enter_down_raw"]=features["time_key_before_enter_down_raw"]
    tmp["time_key_before_enter_up_raw"]=features["time_key_before_enter_up_raw"]
    tmp["time_key_before_enter_flight_raw"]=features["time_key_before_enter_flight_raw"]
        
    tmp["breakers"]=series["breakers"]
    
    for lab in first_n_events_labels(N):
        tmp["%s"%lab]=features_N[lab]
    
    series_stats={}
    
    for mode in ["filtered","raw"]:
        serie = series if mode=="filtered" else series_raw
        for label in serie:
            if label =="breakers":
                continue
            series_stats[label]=series_statistics_extraction("%s_"%mode+label, serie[label])
            for label_1 in series_stats:
                for label_2 in series_stats[label_1]:
                    tmp[label_2]=series_stats[label_1][label_2]
            
    #print tmp
    #print "-------------------------------------------"
    
    #for i,label in enumerate(tmp):
    #    print i,label
    #answer_true,features_true
    
    #print json_keystroke_true
    #print json.load(json_keystroke_true)
    #data[participant_id]["keystroke_true"]=json.load(json_keystroke_true)
    #data[participant_id]["keystroke_false"]=json.load(json_keystroke_false)

    if tmp["session_id"] not in all_sessions:
        all_sessions.append(tmp["session_id"])

    data[session_id].append(tmp)
    
#creazione labels
labels_data_base=["question_id","question_text","session_id","answer"]
labels_data=deepcopy(labels_data_base)

#data_distinct=[]

labels_data.append("answer_length")
labels_data.append("breakers")
    
times=["prompted-firstdigit","firstdigit-enter","prompted-enter"]
for time_ in times:
    labels_data.append("%s"%time_)
    
labels_data.append("max_key_repetition")
labels_data.append("max_key_consecutive")
        
series_=["series_di_both", "series_di_up","series_di_down","series_di_flight","series_di_press","series_tri_both", "series_tri_up","series_tri_down"]
stats_labels=series_statistics_labels()#label
    
for mode in ["filtered","raw"]:
    for serie_type in series_:
        for stat in stats_labels:
            labels_data.append("%s_%s_%s"%(mode,serie_type,stat))
    
number_=["shift", "del","canc","shift","space","delcanc","arrow"]
    
for num in number_:
    labels_data.append("number_%s"%num)
    
time_=["time_key_before_enter_down","time_key_before_enter_up","time_key_before_enter_flight","time_key_before_enter_down_raw","time_key_before_enter_up_raw","time_key_before_enter_flight_raw"]
for time in time_:
    labels_data.append("%s"%time)
        
for lab in first_n_events_labels(N):
    labels_data.append("%s"%lab)
        
file_o=open("list_features.txt","w")
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
for i,lab in enumerate(labels_data):
    file_o.write("\"%s\",\n"%(lab))
    print(lab)  

import csv,gzip

file_="data_NOMobile_" if mobile=="smartphone" else "data_Mobile_"
marker_= "_filter7"

with open(file_+"all_test"+marker_+".csv", 'w') as f:  # Just use 'w' mode in 3.x
    w = csv.DictWriter(f, labels_data)
    w.writeheader()
    for part in sorted(data):
        for row in data[part]:
            w.writerow(row)
            
with open(file_+"UPandDOWN"+marker_+".csv", 'w') as f:  # Just use 'w' mode in 3.x
    w = csv.DictWriter(f, labels_data)
    w.writeheader()
    for part in sorted(DATA_UPandDOWN):
        for row in DATA_UPandDOWN[part]:
            w.writerow(row)
