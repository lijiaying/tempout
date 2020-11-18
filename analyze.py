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


def analyze_zc(netname):
    zcs = load_network_result(netname, 'cegar')
    no_imp = 0
    num = 0
    scr = 0
    bss = 0
    if zcs is None:
        return False
    for zc in zcs:
        testi, deepz, deepc = zc
        if deepc>deepz:
            num += 1
            scr += deepc-deepz
            bss += deepz
        if deepz==deepc: 
            no_imp+=1

    if num!=0:
        avg = scr/bss*100
    return num, round(avg, 1)


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
                print(netname, 'zi:', zi, 'zc:', zc)
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
    num={'i>z':0, 'c>z':0, 'i>c':0, 'c>i':0}
    scr={'i>z':0, 'c>z':0, 'i>c':0, 'c>i':0}
    bss={'i>z':0, 'c>z':0, 'i>c':0, 'c>i':0}
    avg={'i>z':0, 'c>z':0, 'i>c':0, 'c>i':0}
    for record in records:
        testi, deepz, deepi, deepc = record
        if deepi>deepz:
            num['i>z'] += 1
            scr['i>z'] += deepi-deepz
            bss['i>z'] += deepz
        if deepc>deepz:
            num['c>z'] += 1
            scr['c>z'] += deepc-deepz
            bss['c>z'] += deepz
        if deepi>deepc:
            num['i>c'] += 1
            scr['i>c'] += deepi-deepc
            bss['i>c'] += deepc
        if deepc>deepi:
            num['c>i'] += 1
            scr['c>i'] += deepc-deepi
            bss['c>i'] += deepi
        if deepi==deepc and deepi==deepz: 
            no_imp+=1

    for key in num:
        if num[key]!=0:
            avg[key] = (scr[key])/bss[key] * 100
    # print('-'*20, 'summary', '-'*20)
    # print('network name:', netname+'.tf')
    # # print('input tested:', len(zic_list))
    # print('  Input>Zono  :', num['i>z'], scr['i>z'], avg['i>z'], '%')
    # print('  Cegar>Zono  :', num['c>z'], scr['c>z'], avg['c>z'], '%')
    # print('  Input>Cegar :', num['i>c'], scr['i>c'], avg['i>c'], '%')
    # print('  Cegar>Input :', num['c>i'], scr['c>i'], avg['c>i'], '%')
    # # print('No improve  :', no_imp)
    # # assert (c_best == c_gt_i)
    # # assert (i_best == i_gt_c)
    # print()
    # print(num['c>i'], num['i>c'], avg['c>i'])
    return num['c>i'], num['i>c'], round(avg['c>i'], 1)
    return (num['i>z'], num['c>z'], num['i>c'], num['c>i'])


def deepcegar_on_deepz():
    K = [3, 4, 5, 6]
    N = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200]
    excludes = [(3,10), (4,50), (5,50), (5,100), (6,100), (6, 200)]
    
    results = []
    for k in K:
        k_result = []
        for n in N:
            # if (k,n) in excludes:
            #     continue
            netname = 'mnist_relu_' + str(k) + '_' + str(n)
            number, percent = analyze_zc(netname)
            k_result.append(number)
            k_result.append(percent)
        results.append(k_result)
        print('k=', k, ' & ', ' & '.join([str(v) for v in k_result]), ' \\\\', sep='')
    print(results)




def deepall():
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
            (c, i, inum) = result
            results.append([k, n, c, i, inum])
            print(results[-1])
            # (ibet, cbet, ibst, cbst) = result
            # results.append([k, n, ibet, cbet, ibst, cbst])
    
    # with open('./sum.csv', 'w') as f:
    #     for result in results:
    #         f.write(','.join(str(v) for v in result)+'\n')




if __name__ == '__main__':
    # deepcegar_on_deepz()
    deepall()