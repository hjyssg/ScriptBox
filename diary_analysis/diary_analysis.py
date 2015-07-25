
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
import os 
import re
import codecs
 


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
  res = []
  for c in string.ascii_lowercase:
    res.append(c)
  for c in string.digits:
    res.append(c)

  res.append("\r")
  res.append("\n")
  res.append(" ")
  res = [unicode(c) for c in res]
  res.append(unicode("。","utf8"))
  res.append(unicode("，","utf8"))
  res.append(unicode("、","utf8"))
  return res

UNWANTED_LIST = get_unwanted_list()

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

  for diary in diaries:
    if diary.date.year not in interested_years: continue
    seg_list = jieba.cut(diary.content)
    for word in seg_list:
      if word in UNWANTED_LIST: continue
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
  UNWANTED_LIST = get_UNWANTED_LIST()
  for diary in diaries:
    if diary.date.year not in interested_years: continue
    total_count += len(diary.content)
    for cc in diary.content:
      #不需要标点符号
      if cc in UNWANTED_LIST: continue
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
  # print diary_folder_path

  diaries = []

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

def read_files(folder_path = "."):
  result = []
  for dirname, dirnames, filenames in os.walk(folder_path):
    for filename in filenames:
      result.append(os.path.join(dirname, filename))
  return result

def read_emotion_training_set():
  folder = "ChnSentiCorp_htl_ba_6000"
  categories = ["neg", "pos"]
  totalData = {}

  trainingData = {}
  validData = {}

  for cc in categories:
    files = read_files(folder_path = os.path.join(".", folder , cc))
    totalData[cc] = []
    trainingData[cc] = []
    validData[cc] = []

    size = len(files)
    trainingSize = int(0.8 * size)
    for ii in range(0, size):
      try:
        fn = files[ii]
        f = codecs.open(fn, mode="r", encoding="utf8", errors = "ignore")
        content = f.read()
        # print cc,content
        totalData[cc].append(content)
        f.close()

        if ii < trainingSize:
          trainingData[cc].append(content)
        else:
          validData[cc].append(content)

      except Exception, e:
        raise
  return totalData, trainingData, validData

def getTags(sentence):
  # import jieba.analyse
  # result =  jieba.analyse.extract_tags(sentence)
  import jieba
  result = jieba.cut(sentence)
  result = [word for word in result if word not in UNWANTED_LIST and  1 <= len(word) <=5 ]
  return result

class HJYBayesianClassifier(object):
  def __init__(self, trainingSet):
    self.trainingSet = trainingSet
    self.wordCount = {}
    self.categories = trainingSet.keys()
    self.cateCount = {}
    self.total_count = 0

    for cc in self.categories:
      self.cateCount[cc] = 0
      samples = self.trainingSet[cc]
      #each sample text
      for sample in samples:
        self.trainSingleText(sample, cc) 
         
    # for word in self.wordCount.keys():
    #   print word, self.wordCount[word]

  def trainSingleText(self, text, cc):
    seg_list = getTags(text)
    #each word
    for word in seg_list:
      try:
        if word in self.wordCount:
          self.wordCount[word][cc] +=  1
        else:
          self.wordCount[word] = {}
          for temp in self.categories:
            self.wordCount[word][temp] = 0 
          self.wordCount[word][cc] = 1 
        
        self.total_count += 1
        self.cateCount[cc] += 1
      except Exception, e:
        # print "|%s|"%word
        # print wordCount
        # raise
        pass



  def predict(self, text):
    seg_list = getTags(text)
    maxP = 0
    maxC = None
    ##assume training data is balanced
    for cc in self.categories:
      # print cc
      p = 0
      for word in seg_list:
        if word not in self.wordCount: 
          wc = 0
        else:
          wc = self.wordCount[word][cc]

        p += wc/float(self.cateCount[cc])
      if p > maxP:
        maxP = p
        maxC = cc
    return cc



if __name__ == '__main__':
  support_file_types = {".txt"}  
  interested_years = range(2014, 2016)
  diaries = read_diaries(support_file_types, interested_years,
                         diary_folder_path = os.path.join("..", "..","..", "Dropbox", "_Diary"))
  # plot_by_week(diaries, interested_years)
  #count_char_usage(diaries, interested_years)
  #count_word_usage(diaries, interested_years)

  totalData, trainingData, validData = read_emotion_training_set()

  clf = HJYBayesianClassifier(trainingData)

  total = 0
  hit = 0
  for cc in  validData.keys():
    for sample in validData[cc]:
      predict = clf.predict(sample)

      print cc," ->", predict

      # if total > 1:
      #   break


      total += 1
      if predict == cc:
        hit += 1
  print "accuracy is %d/%d = "%(hit, total), float(hit)/total

