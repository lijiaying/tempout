#!/usr/bin/env python3
import os, sys
import json

contents = [{'test': 0, 'deepzono': 0.016, 'deepinput': [('to240.0', 0.016)]}, {'test': 1, 'deepzono': 0.013, 'deepinput': [('to240.0', 0.013)]}, {'test': 2, 'deepzono': 0.009, 'deepinput': [('to240.0', 0.009)]}, {'test': 3, 'deepzono': 0.013, 'deepinput': [('to240.0', 0.014)]}, {'test': 4, 'deepzono': 0.011, 'deepinput': [('to240.0', 0.011)]}, {'test': 5, 'deepzono': 0.012, 'deepinput': [('to240.0', 0.012)]}, {'test': 6, 'deepzono': 0.013, 'deepinput': [('to240.0', 0.013)]}, {'test': 7, 'deepzono': 0.01, 'deepinput': [('to240.0', 0.01)]}, {'test': 8, 'deepzono': 0.007, 'deepinput': [('to240.0', 0.008)]}, {'test': 9, 'deepzono': 0.014, 'deepinput': [('to240.0', 0.014)]}, {'test': 10, 'deepzono': 0.022, 'deepinput': [('to240.0', 0.022)]}, {'test': 11, 'deepzono': 0.012, 'deepinput': [('to240.0', 0.012)]}, {'test': 12, 'deepzono': 0.01, 'deepinput': [('to240.0', 0.01)]}, {'test': 13, 'deepzono': 0.02, 'deepinput': [('to240.0', 0.021)]}, {'test': 14, 'deepzono': 0.011, 'deepinput': [('to240.0', 0.012)]}, {'test': 15, 'deepzono': 0.016, 'deepinput': [('to240.0', 0.016)]}, {'test': 16, 'deepzono': 0.013, 'deepinput': [('to240.0', 0.013)]}, {'test': 17, 'deepzono': 0.019, 'deepinput': [('to240.0', 0.019)]}, {'test': 18, 'deepzono': 0.01, 'deepinput': [('to240.0', 0.01)]}, {'test': 19, 'deepzono': 0.014, 'deepinput': [('to240.0', 0.014)]}, {'test': 20, 'deepzono': 0.004, 'deepinput': [('to240.0', 0.004)]}, {'test': 21, 'deepzono': 0.011, 'deepinput': [('to240.0', 0.011)]}, {'test': 22, 'deepzono': 0.011, 'deepinput': [('to240.0', 0.011)]}, {'test': 23, 'deepzono': 0.017, 'deepinput': [('to240.0', 0.017)]}, {'test': 24, 'deepzono': 0.009, 'deepinput': [('to240.0', 0.009)]}, {'test': 25, 'deepzono': 0.025, 'deepinput': [('to240.0', 0.025)]}, {'test': 26, 'deepzono': 0.012, 'deepinput': [('to240.0', 0.013)]}, {'test': 27, 'deepzono': 0.015, 'deepinput': [('to240.0', 0.015)]}, {'test': 28, 'deepzono': 0.021, 'deepinput': [('to240.0', 0.021)]}, {'test': 29, 'deepzono': 0.01, 'deepinput': [('to240.0', 0.01)]}]

zi_list = []
for item in contents:
    testi = item['test']
    deepz = item['deepzono']
    deepi = item['deepinput']
    zi_list.append([testi, deepz, deepi])
    temp_dict = {'test': testi, 'deepzono': deepz, 'deepinput': deepi[0][1]}
    print(temp_dict)

# for zi in zi_list:
#     zi_dict = {'test': zi[0]}

