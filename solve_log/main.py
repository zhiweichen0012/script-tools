# encoding: utf-8
'''
@author: zhiwei

@contact: zhiweichen95@126.com
@software: PyCharm
@file: main.py
@time: 2018/10/28 10:24 AM
'''

# from solve_log.solveLog import SolveLog
from solveLog import SolveLog
if __name__ == '__main__':
    a = SolveLog("./log/vgg16-c5_1x_3.1.log")
    a.read_txt()
