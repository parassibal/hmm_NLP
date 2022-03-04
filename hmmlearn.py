import sys
import os
import itertools
import math
from itertools import combinations
from collections import Counter


def get_data1(temp,temp1):
    temp,temp1=Counter(temp),Counter(temp1)
    data_model=dict()
    for i in temp:
        temp2=data_split(i,"c")
        cal_val=temp[i]/temp1[temp2]
        data_model[i]=cal_val
    return(data_model)

def get_data2(temp2,len_data,temp,temp1):
    data_model=dict()
    temp2,temp=Counter(temp2),Counter(temp)
    split_conn="/"
    next_state_conn="->"
    no_next_state="->NO_STATE"
    for i in temp:
        temp4=i.split(next_state_conn)[0]
        cal_val=(temp[i]+1)/(temp2[temp4]+len_data)
        data_model[i]=cal_val
    for i in temp1:
        cal_val=temp2[i]+len(temp1)
        j=i+no_next_state
        data_model[j]=1/cal_val
    return(data_model)

def get_data3(temp,len_data):
    temp=Counter(temp)
    data_model=dict()
    for i in temp:
        cal_val=temp[i]/len_data
        data_model[i]=cal_val
    return(data_model)

def check_trans(temp5,temp6,i,j,temp):
    len_data=i-1
    if(len_data>j):
        a=i[j+1]
        a=data_split(a,"c")
        temp5.append(temp)
        temp6.append(temp+"->"+a)
    return(temp5,temp6)

def not_in_check(data1,data2):
    flag=0
    if(data1 not in data2):
        flag=1
    return(flag)


def data_check(temp,temp7,temp1):
    a=not_in_check(temp,temp7)
    if(a==1):
        temp7[temp]=set()
    else:
        b=not_in_check(temp1,temp7[temp])
        if(b==0):
            pass
        else:
            temp2=temp7[temp]
            temp2.add(temp1)
            temp7[temp]=temp2
    return(temp7)


def data_split(a,b):
    split_conn="/"
    next_state_conn="->"
    if(b=="c" or b=="sc"):
        a=a.rsplit(split_conn,1)
        if(b=="sc"):
            return(a)
        else:
            return(a[1])
    else:
        a=a.split(next_state_conn)
        return(a[0])

def state_cal(i,temp1,split_conn):
    a=i.split(split_conn)
    temp1.append(a[-1])
    return(temp1)

def check_len_data(data1,data2):
    flag=0
    if(data1<data2):
        flag=1
    return(flag)


def main():
    learn_out="hmmmodel.txt"
    split_conn="/"
    f_index=1
    temp=[]
    temp7=dict()
    data_file=sys.argv[1]
    temp5,temp6=[],[]
    file1=open(data_file)
    data_access=file1.read()
    next_state_conn="->"
    temp3,temp4,temp1=[],[],[]
    d_a1=data_access.splitlines()
    len_data=len(d_a1)
    for  i in data_access.splitlines():
        i=i.split()
        temp=temp+i
        temp1=state_cal(i[0],temp1,split_conn)
        len_data_enum=len(i)-f_index
        data_e=enumerate(i)
        for j,k in data_e:
            temp2= k.rsplit(split_conn,1)
            s=temp2[1]
            temp4.append(s)
            temp3.append(temp2[0])
            data_check_len=check_len_data(j,len_data_enum)
            if(data_check_len==1):
                temp_data_val=i[j+1]
                temp5.append(s)
                new_data=data_split(temp_data_val,"c")
                temp6.append(s+next_state_conn+new_data)
            temp7=data_check(s,temp7,temp2[0])
    for i in temp7:
        len_per_state=len(temp7[i])
        temp7[i]=len_per_state
    flag=dict()
    file2=open(learn_out,"w+")
    for i,j in sorted(temp7.items(),key=lambda r:-r[1]):
        flag[i]=j
    data5=set(temp3)
    state1=get_data1(temp,temp4)
    state1=dict(state1)
    ab=list(set(temp4))
    data2=set(temp4)
    state2=get_data2(temp5,len(ab),temp6,ab)
    state2=dict(state2)
    file2.write("prob_trans="+str(state2))
    file2.write("\n")
    file2.write("prob_state_em="+str(state1))
    file2.write("\n")
    state3=get_data3(temp1,len_data)
    state3=dict(state3)
    file2.write("data_occurrences_prob="+str(state3))
    file2.write("\n")
    flag=dict(flag)
    file2.write("data_in_state_prob="+str(flag))
    file2.write("\n")
    data5=set(temp3)
    file2.write("data_find_prob="+str(list(data5)))
    file2.write("\n")
    file2.write("state_find_prob="+str(list(data2)))
    file2.write("\n")
    file2.close()

if __name__ == "__main__":
    main()