#!/usr/bin/env python3
import os, sys
import json


def load_network_result(netname, key):
    if key=='input': 
        dir='zi'
        x = 'deepinput'
    elif key=='cegar': 
        dir='zc'
        x = 'deepcegar'
    else: 
        exit(key, ' is not a valid key') 
    file = os.path.join(dir, netname+'.txt')
    if not os.path.exists(file):
        return None
    lst = []
    with open(file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('#'):
                continue
            line = line.rstrip('\n').replace('\'', '"')
            # print('>>', line)
            item = json.loads(line)
            testi = item['test']
            deepz = item['deepzono']
            deepx = item[x]
            lst.append([testi, deepz, deepx])
    return lst



def combine_results(netname):
    zis = load_network_result(netname, 'input')
    zcs = load_network_result(netname, 'cegar')
    if not zis or not zcs:
        return None
    file = os.path.join('zic', netname+'.txt')
    with open(file, 'w') as f:
        for zi, zc in zip(zis, zcs):
            assert zi[0] == zc[0]
            if zi[1] != zc[1]:
                print('zi:', zi, 'zc:', zc)
                continue
            item = {'test': zi[0], 'deepzono': zi[1], 'deepinput': zi[2], 'deepcegar': zc[2]}
            f.write(str(item) + '\n')
    return True
    


def load_combined_result(netname):
    dir='zic'
    file = os.path.join(dir, netname+'.txt')
    if not os.path.exists(file):
        if combine_results(netname) is None:
            return None
    lst = []
    with open(file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('#'):
                continue
            line = line.rstrip('\n').replace('\'', '"')
            # print('>>', line)
            item = json.loads(line)
            testi = item['test']
            deepz = item['deepzono']
            deepi = item['deepinput']
            deepc = item['deepcegar']
            lst.append([testi, deepz, deepi, deepc])
    return lst



def analyze(netname):
    records = load_combined_result(netname)
    if records is None:
        return None
    no_imp = 0
    numbr={'i>z':0, 'c>z':0, 'i>c':0, 'c>i':0}
    score={'i>z':0, 'c>z':0, 'i>c':0, 'c>i':0}
    basis={'i>z':0, 'c>z':0, 'i>c':0, 'c>i':0}
    averg={'i>z':0, 'c>z':0, 'i>c':0, 'c>i':0}
    for record in records:
        testi, deepz, deepi, deepc = record
        if deepi>deepz:
            numbr['i>z'] += 1
            score['i>z'] += deepi-deepz
            basis['i>z'] = deepz
        if deepc>deepz:
            numbr['c>z'] += 1
            score['c>z'] += deepc-deepz
            basis['c>z'] = deepz
        if deepi>deepc:
            numbr['i>c'] += 1
            score['i>c'] += deepi-deepc
            basis['i>c'] = deepc
        if deepc>deepi:
            numbr['c>i'] += 1
            score['c>i'] += deepc-deepi
            basis['c>i'] = deepi
        if deepi==deepc and deepi==deepz: 
            no_imp+=1

    for key in numbr:
        if numbr[key]!=0:
            averg[key] = (score[key])/basis[key]/numbr[key] * 100
    print('-'*20, 'summary', '-'*20)
    print('network name:', netname+'.tf')
    # print('input tested:', len(zic_list))
    print('  Input>Zono  :', numbr['i>z'], score['i>z'], averg['i>z'], '%')
    print('  Cegar>Zono  :', numbr['c>z'], score['c>z'], averg['c>z'], '%')
    print('  Input>Cegar :', numbr['i>c'], score['i>c'], averg['i>c'], '%')
    print('  Cegar>Input :', numbr['c>i'], score['c>i'], averg['c>i'], '%')
    # print('No improve  :', no_imp)
    # assert (c_best == c_gt_i)
    # assert (i_best == i_gt_c)
    print()
    return (numbr['i>z'], numbr['c>z'], numbr['i>c'], numbr['c>i'])




if __name__ == '__main__':
    K = [3, 4, 5, 6]
    N = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200]
    excludes = [(3,10), (4,50), (5,50), (5,100), (6,100), (6, 200)]
    
    results = []
    for k in K:
        for n in N:
            # if (k,n) in excludes:
            #     continue
            netname = 'mnist_relu_' + str(k) + '_' + str(n)
            result = analyze(netname)
            if result is None:
                continue
            (ibet, cbet, ibst, cbst) = result
            results.append([k, n, ibet, cbet, ibst, cbst])
    
    with open('./sum.csv', 'w') as f:
        for result in results:
            f.write(','.join(str(v) for v in result)+'\n')
