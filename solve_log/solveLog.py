# encoding: utf-8
'''
@author: zhiwei

@contact: zhiweichen95@126.com
@software: PyCharm
@file: solveLog.py
@time: 2018-12-01 14:18
'''

import re


class SolveLog():
    def __init__(self, path_txt):
        self.path_txt = path_txt

    def read_txt(self):
        f = open(self.path_txt)
        lines = f.readlines()
        result_ap = ""
        result_corLoc = ""
        pattern_ap = "(^reprint snapshot name for the result.+[^/]/)|(^INFO voc_dataset_evaluator.py: 13[6|7]:) "
        pattern_corLoc = "(^reprint snapshot name for the result.+[^/]/)|(^INFO voc_dataset_evaluator.py: 18[1|2]:) "
        for line in lines:
            linec = line
            if re.match(pattern_ap, line) is not None:
                line = re.sub(re.compile(pattern_ap), '', line)
                if re.match("^[0-9.]+$", line):
                    line = line.replace("\n", " ")
                result_ap += line
            if re.match(pattern_corLoc, linec) is not None:
                linec = re.sub(re.compile(pattern_corLoc), '', linec)
                if re.match("^[0-9.]+$", linec):
                    linec = linec.replace("\n", " ")
                result_corLoc += linec
        print "result_ap:\n" + result_ap
        print "result_corLoc:\n" + result_corLoc
