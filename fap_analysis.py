# !/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime as DT
import codecs 

def plot_faps(fap_counts, stop_counts):
    import matplotlib.pyplot as plt
    plt.scatter(fap_counts, stop_counts)
    plt.show()

    plt.scatter(fap_totals, stop_counts)
    plt.show()

    plt.scatter(stop_counts, fap_counts)
    plt.show()

    plt.scatter(stop_counts, fap_totals)
    plt.show()

    num_bins = 5
    plt.hist(stop_counts, num_bins,  facecolor='green', alpha=0.5)
    plt.show()


def print_mean_by_days(fap_data, fap_date, days = 3):
    print "print by %d days"%days
    steps = len(fap_data)/days
    for ii in range(0, steps):
        partion = fap_data[ii*days:(ii+1)*days]
        temp = sum(partion)/float(len(partion))
        date = fap_date[ii*days]
        date2 = fap_date[(ii+1)*days-1]
        print "%s to %s: %f"%(date.strftime("%Y-%m-%d"), date2.strftime("%m-%d"), temp)

    #the last partion    
    partion = fap_data[steps*days:]
    temp = sum(partion)/float(len(partion))
    date = fap_date[steps*days]
    date2 = fap_date[-1]
    print "%s to %s: %f"%(date.strftime("%Y-%m-%d"), date2.strftime("%m-%d"), temp)


def print_distribution(ll):
    dist = [0]*10
    for e in ll:
        dist[e] += 1

    for ii in range(1, len(dist)):
        print "%d  %d  %f"%(ii, dist[ii], float(dist[ii])/len(ll)*100)

def calculate_continuity(fapDatas):
    fapCounts = []     #每次坚持的天数
    stopCounts  = []  #每次休息的天数
    fapTotals = []    #每次坚持时的次数

    x = 0
    while x < len(fapDatas):
        if fapDatas[x] == 0:
            count = 0
            while x < len(fapDatas) and fapDatas[x] == 0:
                 count += 1 
                 x += 1
            stopCounts.append(count)
        elif fapDatas[x] > 0:
            count = 0
            total = 0
            while x < len(fapDatas) and  fapDatas[x] > 0:
                count += 1
                total += fapDatas[x]
                x += 1
            fapCounts.append(count)
            fapTotals.append(total)


    #打印连续和休息对应
    # x = 0
    # tt =  min(len(fapCounts), len(stopCounts))
    # print "共 %d 对数据" % (tt)    
    # print "连续天数| 总数 |休息天数"
    # while x < tt:
    #     print "  %d         %d    %d" %(fapCounts[x], fapTotals[x], stopCounts[x])
    #     x += 1

    import numpy as np 
    print "总平均每天次数", np.mean(fapDatas)
    print "平均休息天数", np.mean(stopCounts)
    print "平均坚持天数", np.mean(fapCounts)

    print "休息天数分布"
    print_distribution(stopCounts)

    print "坚持天数分布"
    print_distribution(fapCounts)

def predifct_by_classifier(fapDatas, fapDates, step = 4):
    #use the n fap records before any day as vector
    #use it to train the svm
    #用前n天的数据当作input矢量来训练模型
    X = []
    Y = []
    dates = []
    for ii in xrange(step, len(fapDatas)):
        dd = fapDates[ii]
        beg = ii-step

        day = dd.day
        wd = dd.weekday()

        vector = [wd, day] + fapDatas[beg: ii]
        vector = [float(v) for v in vector]

        # print beg, ii
        # print vector, fapDatas[ii]
        X.append(vector)
        Y.append(fapDatas[ii])
        dates.append(dd)

    from sklearn import preprocessing
    scaler = preprocessing.StandardScaler().fit(X)
    scaledX =  scaler.transform(X)  
    trainSize = int(len(X) * 0.95)
    trainingX = scaledX[0:trainSize]
    trainingY = Y[0:trainSize]

    from sklearn import svm
    clf = svm.SVC()
    clf.fit(trainingX, trainingY)

    hit = 0
    for ii in range(trainSize,len(scaledX)):
        vX = scaledX[ii]
        vY = Y[ii]
        predict = clf.predict(vX)
        print dates[ii],vX," -> %d and the predictiton is %d"%(vY, predict)
        if vY == predict:
            hit += 1
    size2 = (len(scaledX) - trainSize)
    hit = float(hit) /size2
    print "hit rate is %.2f"%hit

    test = [5,28,0,0, 1, 0]
    test = [float(v) for v in test]
    print test, " will predict", clf.predict(scaler.transform(test))

    test = [1,1,0,0, 0, 0]
    test = [float(v) for v in test]
    print test, " will predict", clf.predict(scaler.transform(test))

    test = [1,1, 2, 2, 0, 0]
    test = [float(v) for v in test]
    print test, " will predict", clf.predict(scaler.transform(test))


if __name__ == '__main__':
    FAP_DATAS = []
    FAP_DATES = []
    lines = codecs.open("fap.csv", mode = "r", encoding = "utf8", errors="ignore").readlines()
    for ii in range(1, len(lines)):
        line = lines[ii]
        # print line
        cols  = lines[ii].split(",")
        if cols[1] == "":break #reach the end of record
        date = DT.datetime.strptime(cols[0], "%m/%d/%y")
        num =  int(cols[1])
        # print date, num

        FAP_DATAS.append(num)
        FAP_DATES.append(date)

    # print_mean_by_days(FAP_DATAS, FAP_DATES, days = 15)
    calculate_continuity(FAP_DATAS)

    predifct_by_classifier(FAP_DATAS, FAP_DATES)



