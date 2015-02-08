
# -*- coding: utf-8 -*-
#!/usr/bin/env python

#这个文件用到:
#   unicode IO
#   file iteration
#   sort dict by value
#   regex search


import os
import re
import sys
import math as m
import datetime 
import itertools 
import numpy as np
from collections import OrderedDict

import string
unwanted_list = []
for c in string.ascii_lowercase:
  unwanted_list.append(unicode(c))
for c in string.digits:
  unwanted_list.append(unicode(c))

unwanted_list.append(unicode(" "))
unwanted_list.append(unicode("。","utf8"))
unwanted_list.append(unicode("，","utf8"))


def week_number(date):
  return date.isocalendar()[1]

def analysic_by_week():
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


## 用日记字数估计情绪变化
## 我心情好，活动丰富的时候，日记写很长。
## 心情不好无聊寂寞的时候，日记写很短。

chinese_char_frequency_dict = {}
total_chinese_char_count = 0
supported_file_types = {".txt"}  
interested_years = range(2014, 2016)
# print interested_years

count_chinese_char_frequency = True
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
          emotion_index = ss
          total_day_emotion_table[tt] = emotion_index

          
          import codecs
          #read unicode from file
          f = codecs.open(filePath, mode = "r", encoding='utf-8')
          if count_chinese_char_frequency:
            for cc in f.read().replace('\n', ''):
              total_chinese_char_count += 1
              #不需要标点符号
              if cc in unwanted_list: continue
              if cc in chinese_char_frequency_dict:
                chinese_char_frequency_dict[cc] += 1
              else:
                chinese_char_frequency_dict[cc] = 1


if count_chinese_char_frequency:
  #sort the frequncy reversely
  print "一共写了%d字" % (total_chinese_char_count)
  print "用了%d种字符" % (len(chinese_char_frequency_dict.keys()))
  ii = 0
  for w in sorted(chinese_char_frequency_dict, key=chinese_char_frequency_dict.get, reverse=True):
    if ii > 100: break
    ii += 1
    print "%s %d" %(w, chinese_char_frequency_dict[w]) 




# analysic_by_week()



