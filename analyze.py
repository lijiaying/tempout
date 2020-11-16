#!/usr/bin/env python3
import os, sys
import json





def analyze(netname):
    zifile = './zi/' + netname+'.txt'
    zcfile = './zc/' + netname+'.txt'
    zicfile = './zic/' + netname+'.txt'
    if not os.path.exists(zifile) or not os.path.exists(zcfile):
        return
    # print('---', netname)

    num_outperform_zi = 0
    outperform_zi_list = []

    zi_list = []
    with open(zifile, 'r') as zif:
        lines = zif.readlines()
        for line in lines:
            if line.startswith('#'):
                continue
            line = line.rstrip('\n').replace('\'', '"')
            # print('>>', line)
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
    with open(zcfile, 'r') as zcf:
        lines = zcf.readlines()
        for line in lines:
            if line.startswith('#'):
                continue
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

    # print('number of input that deepinput outperforms deepzono:', num_outperform_zi)
    # print('items:', outperform_zi_list)
    # print('number of input that deepcegar outperforms deepzono:', num_outperform_zc)
    # print('items:', outperform_zc_list)

    zic_list = []
    with open(zicfile, 'w') as zicf:
        for zi, zc in zip(zi_list, zc_list):
            assert zi[0] == zc[0]
            testi = zi[0]
            if zi[1] != zc[1]:
                print('zi:', zi, 'zc:', zc)
                continue
            zic_list.append([zi[0], zi[1], zi[2], zc[2]])
            item = {'test': zi[0], 'deepzono': zi[1], 'deepinput': zi[2], 'deepcegar': zc[2]}
            zicf.write(str(item) + '\n')

    num_c_best = 0
    num_i_best = 0
    num_i_eq_c = 0
    num_i_gt_z = 0
    num_c_gt_z = 0
    num_no_imp = 0
    for zic in zic_list:
        deepz, deepi, deepc = zic[1:]
        if deepc>deepz and deepc>deepi: 
            num_c_best+=1
            # print('cbest item:', zic)
        if deepi>deepz and deepi>deepc: 
            num_i_best+=1
            # print('ibest item:', zic)
        if deepi==deepc and deepi>deepz: 
            num_i_eq_c+=1
            # print('eq:', zic)
        if deepi>deepz:
            num_i_gt_z += 1
        if deepc>deepz:
            num_c_gt_z += 1
        if deepi==deepc and deepi==deepz: 
            num_no_imp+=1

    print('-'*20, 'summary', '-'*20)
    print('network name:', netname+'.tf')
    # print('input tested:', len(zic_list))
    print('Cegar best  :', num_c_best)
    print('Input best  :', num_i_best)
    print('Cegar=Input :', num_i_eq_c)
    print('Input>Zono  :', num_i_gt_z)
    print('Cegar>Zono  :', num_c_gt_z)
    # print('No improve  :', num_no_imp)
    print()


if __name__ == '__main__':
    K = [3, 4, 5, 6]
    N = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200]
    excludes = [(3,10), (4,50), (5,50), (5,100), (6,100), (6, 200)]
    
    for k in K:
        for n in N:
            # if (k,n) in excludes:
            #     continue
            netname = 'mnist_relu_' + str(k) + '_' + str(n)
            analyze(netname)