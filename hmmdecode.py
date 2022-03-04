import sys
import os
import itertools
import math
import ast
from itertools import combinations
from collections import Counter

def get_data_model(data_model):
    state1=data_model.get("prob_trans")
    state2=data_model.get("prob_state_em")
    state3=data_model.get("data_occurrences_prob")
    state4=data_model.get("data_in_state_prob")
    state5=data_model.get("data_find_prob")
    state6=data_model.get("state_find_prob")
    state1,state2,state3,state4,state5,state6=ast.literal_eval(state1),ast.literal_eval(state2),ast.literal_eval(state3),ast.literal_eval(state4),ast.literal_eval(state5),ast.literal_eval(state6)
    return(state1,state2,state3,state4,state5,state6)

global prob_initial
prob_initial=-1


def check_limit(data4):
    flag=0
    a,b=4,len(data4)
    if(b==a+1):
        flag=1
    return(flag)

def access_word_set(state3,state4,state5):
    data3,data4,data5=set(),set(),set()
    for i in state3:
        data3.add(i)
    for i in state5:
        data5.add(i)
    for i in state4:
        data4.add(i)
        a=check_limit(data4)
        if(a==1):
            break
    return(data3,data4,data5)

def learn_data_model(learn_file):
    flag=1
    file1=open(learn_file,"r")
    data_access=file1.readlines()
    data_model=dict()
    for i in data_access:
        j,k=i.split("=",flag)
        j=j.strip()
        k=k.strip()
        data_model[j]=k
    return(data_model)

def create_enteries(len_state,len_data,i):
    flag=0
    viterbi_prob_initial=[]
    for a in range(len_state):
        viterbi_prob_initial.append([])
        for b in range(len_data):
            viterbi_prob_initial[a].append(0)
    if(len(i)>prob_initial):
        flag=1
    temp_matrix_index=[]
    for a in range(len_state):
        temp_matrix_index.append([])
        for b in range(len_data):
            temp_matrix_index[a].append(0)
    return(viterbi_prob_initial,flag,temp_matrix_index)

global str_out
str_out=""

def get_state_prob(state_index,l,data5,state2):
    flag=0
    a=check_state_word(data5,state_index)
    if(a==1):
        flag=1
        return(flag)
    else:
        temp=state_index+"/"+l
        b=check_state_word(state2,temp)
        if(b==1):
            return(flag)
        else:
            temp1=state2[temp]
            return(temp1)

def check_state_word(data5,state_index):
    flag=0
    if(state_index not in data5):
        flag=1
    return(flag)

def matrix_viterbi(l,data3,state_prob,state3):
    flag=0
    if(l in data3):
        a=state3[l]
        temp=state_prob*a
        return(temp)
    if(l not in data3):
        return(flag)

def update_matrix(state_prob_trans,state_prob):
    if(state_prob_trans!=0):
        cal_val=state_prob_trans*state_prob
    else:
        cal_val=0
    return(cal_val)

def get_out_final(val_pred,i,str_out):
    data_e=enumerate(i)
    conn="/"
    for ind,data in data_e:
        matrix_val=val_pred[ind]
        temp=data+conn+matrix_val
        str_out=str_out+(temp+" ")
    return(str_out.strip())

def check_pred_prob(initial_prob,val):
    flag=0
    if(initial_prob<val):
        initial_prob=val
        flag=1
    return(initial_prob,flag)


def  get_pred_val(viterbi_prob_initial,i,temp_matrix_index,state6):
    flag=0
    str_out=""
    initial_prob=-1
    f_index=1
    len_state=len(state6)
    len_data=len(i)-f_index
    pred_data=[]
    for j in range(len_state):
        prob_val=viterbi_prob_initial[j][len_data]
        initial_prob,flag=check_pred_prob(initial_prob,prob_val)
        if(flag==1):
            state_val=state6[j]
            index_val=j
    pred_data=[state_val]+pred_data
    while(len_data>0):
        index_val=temp_matrix_index[index_val][len_data]
        pred_data=[state6[index_val]]+pred_data
        len_data=len_data-1
    result_out=get_out_final(pred_data,i,str_out)
    return(result_out)


def main():
    flag=0
    data_file_test=sys.argv[1]
    learn_file="hmmmodel.txt"
    data_model=learn_data_model(learn_file)
    out_file="hmmoutput.txt"
    file1=open(data_file_test)
    data_access=file1.read()
    state1,state2,state3,state4,state5,state6=get_data_model(data_model)
    data3,data4,data5=access_word_set(state3,state4,state5)
    file_out=open(out_file,"w+")
    str_val="->NO_STATE"
    conn="->"
    prob_initial_state=0
    for i in data_access.splitlines():
        len_state=len(state6)
        i=i.split()
        len_data=len(i)
        viterbi_prob_initial,temp_val,temp_matrix_index=create_enteries(len_state,len_data,i)
        temp_val=temp_val*len(i)
        prob_cmp_val=temp_val
        for j in range(len_data):
            state_index=i[j]
            temp1=state6
            word_state=check_state_word(data5,state_index)
            if(prob_cmp_val>prob_initial_state):
                pass
            else:
                prob_initial_state=prob_cmp_val
            if(word_state==1):
                prob_cmp_val=prob_cmp_val*len(state_index)
                temp1=data4
            temp1_en=enumerate(temp1)
            for k,l in temp1_en:
                find_index_data=state6.index(l)
                state_prob=get_state_prob(state_index,l,data5,state2)
                temp_var=state_prob+prob_cmp_val
                if(temp_var>prob_initial_state):
                    pass
                else:
                    prob_initial_state=temp_var
                state_index_data5=check_state_word(data5,state_index)
                if(state_index_data5==1):
                    temp4=find_index_data
                else:
                    temp4=k
                if(j==flag):
                    prob_matrix_flag=check_state_word(data3,l)
                    if(prob_matrix_flag==1):
                        prob_matrix_val=0
                    else:
                        prob_matrix_val=state_prob*state3[l]
                    viterbi_prob_initial[temp4][j]=prob_matrix_val
                else:
                    state_prob_trans,index_state_prob_trans=prob_initial,prob_initial
                    for m,n in enumerate(state6):
                        matrix_viterbi_val=viterbi_prob_initial[m][j-1]
                        state_tran=n+conn+l
                        if(matrix_viterbi_val!=flag):
                            state_tran_check=check_state_word(state1,state_tran)
                            if(state_tran_check==1):
                                state_tran=n+str_val
                            new_prob=state1[state_tran]*matrix_viterbi_val
                        else:
                            new_prob=flag
                        if(new_prob<state_prob_trans):
                            pass
                        if(new_prob>state_prob_trans):
                            state_prob_trans=new_prob
                            index_state_prob_trans=m
                    prob_cmp_val=prob_cmp_val+(state_prob_trans*state_prob)
                    viterbi_prob_initial[temp4][j]=update_matrix(state_prob_trans,state_prob)
                    temp_var=temp_var*index_state_prob_trans
                    temp_matrix_index[temp4][j]=index_state_prob_trans
        val_pred=get_pred_val(viterbi_prob_initial,i,temp_matrix_index,state6)
        file_out.write(val_pred)
        file_out.write("\n")
    file_out.close()


if __name__ == "__main__":
    main()