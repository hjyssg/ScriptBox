# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import re
import sys
import math as m
import datetime 
import itertools 
import numpy as np
from collections import OrderedDict
from scipy import stats

def week_number(date):
  return date.isocalendar()[1]

## 用日记字数估计情绪变化
## 我心情好，活动丰富的时候，日记写很长。
## 心情不好无聊寂寞的时候，日记写很短。


supported_file_types = {".txt"}  
interested_years = range(2012, 2015)
# print interested_years


total_day_emotion_table = OrderedDict()

for dirname, dirnames, filenames in os.walk("."):
  try:
    #日记放在对应年份的文件夹里面 e.g 2010, 2011, 2012
    searchObj = re.search("\d{4}",dirname)
    if searchObj is None: continue   
    year = int(searchObj.group())
    if year not in interested_years: continue
  except Exception, e:
     pass

  for filename in filenames:
    fileExtension=os.path.splitext(filename)[1]
    if fileExtension in supported_file_types:
        searchObj = re.search("(\d{2})_(\d{2})",filename)
        if searchObj:
          #convert number and create date object
          month = int(searchObj.group(1))
          day = int(searchObj.group(2))
          tt = datetime.date(year, month, day)
          #get file size
          filePath= os.path.join(dirname, filename)
          statinfo = os.stat(filePath)
          ss = statinfo.st_size
          #"dump" the value to avoid extreme value
          emotion_index = m.log(ss, 1.2) 
          #emotion_index = ss
          total_day_emotion_table[tt] = emotion_index


total_week_emotion_mean_table = OrderedDict()
total_week_emotion_stdev_table = OrderedDict()

#year by year
for year in interested_years:
  #get dates for each year
  dates_in_this_year = []
  for date in total_day_emotion_table:
    if date.year == year:
      dates_in_this_year.append(date)
  #week by week
  for k, g in itertools.groupby(dates_in_this_year, key=week_number):
    week_days = list(g)
    week_emotions = []
    for dd in week_days:
      week_emotions.append(total_day_emotion_table[dd])
    ss = week_days[0]
    total_week_emotion_mean_table[ss]=  np.mean(week_emotions)
    total_week_emotion_stdev_table[ss]=  np.std(week_emotions)

average_emotion = np.mean(total_week_emotion_mean_table.values())
print "average_emotion ",average_emotion


import matplotlib.pyplot as plt
num_bins = 50
plt.hist(total_week_emotion_mean_table.values(), num_bins, normed=1, facecolor='green', alpha=0.5)
plt.title("Emotion Distribution")
plt.show()


plt.plot(total_week_emotion_mean_table.keys(), total_week_emotion_mean_table.values())
plt.axhline(y=average_emotion, c="green", hold=None)
plt.title("Emotion Plot")
plt.show()





