# !/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime as DT
import codecs 
import re

def readCSV(fn, beginDate):
    p = re.compile("(\d+)")
    dates = []
    difs = []

    minDif = 0
    maxDif = 200

    lines = codecs.open(fn, mode = "r", encoding = "utf8", errors="ignore").readlines()
    for ii in range(1, len(lines)):
        line = lines[ii]
        # print line
        cols  = line.split(",")
        ss = cols[-1].strip()

        m = p.findall(ss)
        if m is not None and len(m) > 3:
            year = int(m[0])
            month = int(m[1])
            day = int(m[2])
            dd = DT.date(year, month, day)
        
            dif = dd - beginDate
            dif = dif.days

            if dif < minDif or dif > maxDif:
                continue

            difs.append(dif)
            dates.append(dd)

            # print dd, " ---", dif

    print fn
    print "total ",len(dates)," doujins"
 

    result = {}

    for ii in xrange(minDif, maxDif+1):
        result[ii] = 0

    for dif in difs:
        result[dif] = result[dif] + 1
        

    # print result
    for key in result.keys():
        print key, "--", result[key]
    print "\n-----------"




if __name__ == '__main__':
    readCSV("c84.csv", DT.date(2013, 8, 10))
    readCSV("c85.csv", DT.date(2013, 12, 30))
    readCSV("c86.csv", DT.date(2014, 8, 15))
    readCSV("c87.csv", DT.date(2014, 12, 30))





