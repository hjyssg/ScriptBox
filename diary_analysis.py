
# -*- coding: utf-8 -*-
#!/usr/bin/env python

#这个文件用到:
#   unicode IO
#   file iteration
#   sort dict by value
#   regex search
#   iterate by week




import math as m
import datetime 
 

class Diary(object):
  """docstring for Diary"""
  def __init__(self, date, content):
    super(Diary, self).__init__()
    self.date = date
    self.content = content

  def get_length(self):
    return len(self.content)

  def get_emotion_index(self):
    length = len(self.content)
    index = m.log(length, 10)
    return index
 

def get_unwanted_list():
  import string
  unwanted_list = []
  for c in string.ascii_lowercase:
    unwanted_list.append(unicode(c))
  for c in string.digits:
    unwanted_list.append(unicode(c))

  unwanted_list.append(unicode("\r"))
  unwanted_list.append(unicode("\n"))
  unwanted_list.append(unicode(" "))
  unwanted_list.append(unicode("。","utf8"))
  unwanted_list.append(unicode("，","utf8"))
  unwanted_list.append(unicode("、","utf8"))
  return unwanted_list


def plot_by_week(diaries, interested_years = range(2000, 2100), histogram = False):
  """group diray by week,analyze and then plot"""
  import numpy as np
  from collections import OrderedDict
  import itertools

  week_emotion_means = OrderedDict()
  week_emotion_stddevs = OrderedDict()

  def week_number(diary):
    return diary.date.isocalendar()[1]

  def get_date(diary):
    return diary.date

  #year by year
  for year in interested_years:
    #get diaries for each year
    year_diaries = []
    for diary in diaries:
      if diary.date.year == year:
        year_diaries.append(diary)      
    #week by week
    for k, g in itertools.groupby(year_diaries, key=week_number):
      week_diaries = list(g)
      week_emotions = []
      for dd in week_diaries:
        week_emotions.append(dd.get_emotion_index()) 
      # add week diary into week 
      first_date_of_week = week_diaries[0].date
      week_emotion_means[first_date_of_week]  =  np.mean(week_emotions)
      week_emotion_stddevs[first_date_of_week]  =  np.std(week_emotions)

  sorted(week_emotion_means)     
  sorted(week_emotion_stddevs)   

  # for key in week_emotion_means:
  #   print key, week_emotion_means[key]

  import matplotlib.pyplot as plt
  if histogram:
    num_bins = 50
    plt.hist(week_emotion_means.values(), num_bins, normed=1, facecolor='green', alpha=0.5)
    plt.title("Emotion Distribution")
    plt.show()

  average_emotion = np.mean(week_emotion_means.values())

  plt.plot(week_emotion_means.keys(), week_emotion_means.values())
  plt.axhline(y=average_emotion, c="green", hold=None)
  plt.title("Emotion Plot")
  plt.show()

def count_word_usage(diaries, interested_years = range(2000, 2100)):
  #　use 结巴分词 to seperate chinese words
  import jieba
  total_count = 0
  word_frequency_dict = {}
  unwanted_list = get_unwanted_list()

  for diary in diaries:
    if diary.date.year not in interested_years: continue
    seg_list = jieba.cut(diary.content)
    for word in seg_list:
      if word in unwanted_list: continue
      total_count += 1
      if word in word_frequency_dict:
        word_frequency_dict[word] += 1
      else:
        word_frequency_dict[word] = 1  
    

  print "在", interested_years, "年之间"      
  print "一共写了%d个词" % (total_count)
  print "用了%d种词" % (len(word_frequency_dict.keys()))
  ii = 0
  for w in sorted(word_frequency_dict, key=word_frequency_dict.get, reverse=True):
    if ii > 300: break
    ii += 1
    print "[%s] %d" %(w, word_frequency_dict[w]) 

def count_char_usage(diaries, interested_years = range(2000, 2100)):
  total_count = 0
  char_frequency_dict = {}
  unwanted_list = get_unwanted_list()
  for diary in diaries:
    if diary.date.year not in interested_years: continue
    total_count += len(diary.content)
    for cc in diary.content:
      #不需要标点符号
      if cc in unwanted_list: continue
      if cc in char_frequency_dict:
        char_frequency_dict[cc] += 1
      else:
        char_frequency_dict[cc] = 1

  print "在", interested_years, "年之间"      
  print "一共写了%d字" % (total_count)
  print "用了%d种字符" % (len(char_frequency_dict.keys()))
  ii = 0
  for w in sorted(char_frequency_dict, key=char_frequency_dict.get, reverse=True):
    if ii > 100: break
    ii += 1
    print "[%s] %d" %(w, char_frequency_dict[w]) 
    



def read_diaries(support_file_types, interested_years = range(2000, 2100), diary_folder_path = "."):
  """iterate diary location. return a list of diary objects sorted by date"""
  import os
  import re
  import codecs

  diaries = list()

  for dirname, dirnames, filenames in os.walk(diary_folder_path):
    try:
      #日记放在对应年份的文件夹里面 e.g 2010, 2011, 2012
      searchObj = re.search("\d{4}",dirname)
      if searchObj is None: continue   
      year = int(searchObj.group())
      if year not in interested_years: continue
    except Exception, e:
       pass

    for filename in filenames:
      file_extension = os.path.splitext(filename)[1]
      if file_extension not in support_file_types: continue
      #文件用按"月份_日期"命名，比如1月15号是"01_15"
      searchObj = re.search("(\d{2})_(\d{2})",filename)
      if searchObj:
        #convert number and create date object
        month = int(searchObj.group(1))
        day = int(searchObj.group(2))
        tt = datetime.date(year, month, day)
        #get file size
        filePath= os.path.join(dirname, filename)
        #read unicode from file
        f = codecs.open(filePath, mode = "r", encoding='utf-8')
        content = f.read()
        temp_diary = Diary(date = tt, content = content)
        diaries.append(temp_diary)
        f.close()
  sorted(diaries, key = lambda d: d.date)
  # for diary in diaries:
  #   print diary.date
  #   print len(diary.content)
  #   print diary.content
  return diaries


if __name__ == '__main__':
  support_file_types = {".txt"}  
  interested_years = range(2014, 2016)
  diaries =read_diaries(support_file_types, interested_years)
  plot_by_week(diaries, interested_years)
  #count_char_usage(diaries, interested_years)
  #count_word_usage(diaries, interested_years)


