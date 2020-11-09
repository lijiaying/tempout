#!/usr/bin/env python3
import os, sys
import json

# filepath = sys.argv[1]
# with open(filepath) as f:
#     contents = f.readlines()

# print(contents[-1])
# resultstr = contents[-1].rstrip('\n').replace('\'', '"')
# print(resultstr)
# veresult = json.loads(resultstr)
results = []

num_outperform_zi = 0
outperform_zi_list = []

zi_list = []
with open('mnist_relu_3_10_zi.txt', 'r') as zif:
    lines = zif.readlines()
    for line in lines:
        line = line.rstrip('\n').replace('\'', '"')
        item = json.loads(line)
        testi = item['test']
        deepz = item['deepzono']
        deepi = item['deepinput']
        zi_list.append([testi, deepz, deepi])
        # print("{'test': ", testi, ", 'deepzono': ", deepz, ", 'deepinput': ", deepi, '}', sep='')
        if deepi>deepz: 
            num_outperform_zi+=1
            outperform_zi_list.append([testi, deepz, deepi])
        

num_outperform_zc = 0
outperform_zc_list = []

zc_list = []
with open('mnist_relu_3_10_zc.txt', 'r') as zcf:
    lines = zcf.readlines()
    for line in lines:
        line = line.rstrip('\n').replace('\'', '"')
        item = json.loads(line)
        testi = item['test']
        deepz = item['deepzono']
        deepc = item['deepcegar']
        zc_list.append([testi, deepz, deepc])
        # print("{'test': ", testi, ", 'deepzono': ", deepz, ", 'deepcegar': ", deepc, '}', sep='')
        if deepc>deepz: 
            num_outperform_zc+=1
            outperform_zc_list.append([testi, deepz, deepc])


print('number of input that deepi outperforms deepz:', num_outperform_zi)
# print('items:', outperform_zi_list)
print('number of input that deepc outperforms deepz:', num_outperform_zc)
# print('items:', outperform_zc_list)

zic_list = []
for zi, zc in zip(zi_list, zc_list):
    assert zi[0] == zc[0]
    testi = zi[0]
    assert zi[1] == zc[1]
    zic_list.append([zi[0], zi[1], zi[2], zc[2]])

num_c_best = 0
num_i_best = 0
num_i_eq_c = 0
num_no_imp = 0
for zic in zic_list:
    deepz, deepi, deepc = zic[1:]
    if deepc>deepz and deepc>deepi: 
        num_c_best+=1
        print('cbest item:', zic)
    if deepi>deepz and deepi>deepc: 
        num_i_best+=1
        print('ibest item:', zic)
    if deepi==deepc and deepi>deepz: 
        num_i_eq_c+=1
        # print('eq:', zic)
    if deepi==deepc and deepi==deepz: 
        num_no_imp+=1

print('Cegar best:', num_c_best)
print('Input best:', num_i_best)
print('Cegar=Input:', num_i_eq_c)
print('No improve:', num_no_imp)
