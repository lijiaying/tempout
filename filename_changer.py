#!/usr/bin/env python3
import os, sys
import json


dir = './smu'
for f in os.listdir(dir):
    if f.endswith('.all.test0_100.txt'):
        f_path = os.path.join(dir, f)
        os.rename(f_path, f_path[:-18]+'.txt')