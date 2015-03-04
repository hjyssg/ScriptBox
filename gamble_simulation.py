# -*- coding: utf-8 -*-
#!/usr/bin/env python

from random import randint

# 我想测试的是这样的：
# 进行1000局50%胜负，其中每赢一次就加倍投注，连赢X（x赋值2～10进行试验）次就立即结束游戏。
# 连赢被中断则投注回归1.玩家初始值为零，求500000个玩家在游戏结束时的值的分布。 
def one_sample(total_times = 1000, time_to_quit = 10):
    histoty = list()
    grade = 0
    bet = 1
    
    for x in xrange(0,total_times):
        outcome = randint(0,1)  #50% chance to win
        histoty.append(outcome)
        if outcome == 1: #win
            grade += bet  
            bet *= 2
            if hasSeqWinInLastTimes(histoty, time_to_quit):
                return grade
        else: #when lose
            grade -= bet
            bet = 1
    return grade
    
# arr. 1 for win, 0 for lost
# n: the number of sequent win
def hasSeqWinInLastTimes(arr, n):
    if len(arr) < n: #at least play n times
        return False
    for x in xrange(len(arr)-n,len(arr)):
        if arr[x] == 0: return False
    return True


def unit_test():
   #print  hasSeqWinInLastTimes([0,0,0,1,1,1,1], 5)
   #print  hasSeqWinInLastTimes([0,0,1,1,1,1,1], 1)
   #print one_sample(total_times = 1000, time_to_quit = 10)
   pass
#unit_test()

def calculate_total_distribution(total = 5000):
    distribution = list()


    #Text Progress Bar in the Console
    #http://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    import sys
    one_percent = total/100

    print "calculating..."
    for x in xrange(0,total):
        distribution.append(one_sample())

        if x%one_percent == 0:
            #print x
            percent = x/one_percent
            ss = "\r%d%%" % (percent)
            sys.stdout.write(ss)
            sys.stdout.flush()


    print "result"
    print distribution

    import matplotlib.pyplot as plt
    num_bins = 400
    plt.hist(distribution, num_bins, normed=1, facecolor='green', alpha=0.5)
    plt.title("grade Distribution")
    plt.show()


calculate_total_distribution(total = 10000)