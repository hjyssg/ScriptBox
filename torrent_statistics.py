# -*- coding: utf-8 -*-
#!/usr/bin/env python

import datetime  as DT
import torrentparse   #https://github.com/mohanraj-r/torrentparse
from sqlobject import *

class Torrent(SQLObject):
  name = StringCol(length=300, default=None)
  dtype = StringCol()
  date = DateTimeCol()
  size = FloatCol()

def get_total_size(info):
      """
         get total size in by MB
      """
      total = 0.0
      for f in info:
          total += f[1]
      return total/1024.0/1024.0/1024.0

def read_torrents(supported_file_types = {".torrent"} , torrent_folder_path = "."):
  """iterate torrent location. return a dict:  date->torrent_number"""
  import os
  import re
  import codecs

  for dirname, dirnames, filenames in os.walk(torrent_folder_path):
    for filename in filenames:
      

      #only allow supported file
      file_extension = os.path.splitext(filename)[1]
      if file_extension not in supported_file_types: continue
      #get modified time

      filePath= os.path.join(dirname, filename)
      tt = DT.datetime.fromtimestamp(os.path.getmtime(filePath))
      #date_str = "%d_%02d_%02d"%(t.year, t.month, t.day)

      try:
        from torrentparse import TorrentParser
        tp = TorrentParser(filePath)
        #print tp.get_creation_date()," ",tp.get_total_size()

        info = tp.get_files_details()
        if len(info) == 1:
          dtype = os.path.splitext(info[0][0])[1]
          name = info[0][0]
        else:
          dtype = "folder"
          name = filename

        #date = DT.datetime.utcfromtimestamp(tp.get_creation_date())
        #if date == None: date = tt
        date = tt

        # print Torrent.select(Torrent.q.date == date).count()


        tor = Torrent(name = name, 
                      date = date,
                      dtype = dtype,
                      size = get_total_size(info)
                      )
        #print tor

      except Exception, e:
        #print type(filename)
        #print e
        pass

def calMean(ll):
  total = 0.0
  for e in ll:
    total += e
  return total/len(ll)
    
if __name__ == '__main__':
  sqlhub.processConnection = connectionForURI('sqlite:/:memory:')
  Torrent.createTable()
  read_torrents()

  print "total %d torrent files" % (Torrent.select().count())
  torrents =  list(Torrent.select().orderBy('date'))
  
  typeCount = dict()
  typeSizes = dict()
  size_list = list()
  folder_sizes = list()


  for tor in torrents:
    size_list.append(tor.size)
    if tor.dtype in typeCount:
      typeCount[tor.dtype] += 1
      typeSizes[tor.dtype] += tor.size
    else:
      typeCount[tor.dtype] = 1
      typeSizes[tor.dtype] = tor.size


  import matplotlib.pyplot as plt
  from matplotlib.ticker import MultipleLocator, FormatStrFormatter  

  plt.title("torrent statistics")
  
  ax = plt.subplot(121)
  ax.yaxis.set_major_locator(MultipleLocator(100) )  
  plt.bar(range(len(typeCount)), typeCount.values(), align='center')
  plt.xticks(range(len(typeCount)), typeCount.keys())
  plt.grid(True)
  plt.title("type versus number")
  


  ax2 = plt.subplot(122) 
  ax2.yaxis.set_major_locator(MultipleLocator(10) )  
  plt.bar(range(len(typeSizes)), typeSizes.values(), align='center')
  plt.xticks(range(len(typeSizes)), typeSizes.keys())
  plt.title("type versus GB")
  plt.grid(True)
  plt.show()

  
  oldestDate = torrents[0].date.date()
  nearestDate = torrents[0].date.date()
  for tor in torrents:
    dd = tor.date.date()
    if dd < oldestDate:
      oldestDate = dd
    if dd > nearestDate:
      nearestDate = dd
  print "from %s to %s"%(oldestDate, nearestDate)

 

  #init the dict
  date2num = dict()
  date2size = dict()
  it = oldestDate
  while it <= nearestDate:
     date2num[it] = 0
     date2size[it] = 0
     it += DT.timedelta(1)

  #iterate day by day
  #put into by date. year-month-day   
  for tor in torrents:
    dd = tor.date.date()

    #elimiate extreme value
    if date2num[dd] > 50: 
      date2num[dd] = 0
      date2size[dd] = 0

    date2size[dd] += tor.size
    date2num[dd] += 1

  print "mean number %d" % (calMean(date2num.values()))  
  print "mean size %f GB " % (calMean(date2size.values())  )


  ##plot torrent number distribution 
  # ax2 = plt.subplot(111) 
  # num_bins = 100
  # plt.hist(date2num.values(), num_bins, facecolor='green', alpha=0.5)
  # plt.title("Num Distribution")
  # plt.show()  

  
  #group by the day of the month  
  day2size = [0]*32 
  day2num = [0]*32
  day2count = [0]*32
  for dd in date2size.keys():
    day2size[dd.day] += date2size[dd]
    day2num[dd.day] += date2num[dd]
    day2count[dd.day] += 1



  avg_size_by_day = []
  avg_num_by_day = []
  for xx in xrange(1,32):
    avg = day2size[xx]/float(day2count[xx])
    avg_size_by_day.append(avg)

    avg2 = day2num[xx]/float(day2count[xx])
    avg_num_by_day.append(avg2)
    
    #print "day:%02d size:%2.01f num:%d m_num:%d" %( xx,day2size[xx], day2num[xx],day2count[xx])


  ax3 = plt.subplot(211) 
  plt.plot(range(1,32), avg_num_by_day, '-')
  plt.plot(range(1,32), avg_num_by_day, 'ro')
  plt.axis([1, 31, 0, 30])
  plt.grid(True)
  plt.title("day versus number")
  ax3.xaxis.set_major_locator(MultipleLocator(1))  
  ax3.yaxis.set_major_locator(MultipleLocator(5))  



  ax4 = plt.subplot(212) 
  plt.plot(range(1,32), avg_size_by_day, '-')
  plt.plot(range(1,32), avg_size_by_day, 'ro')
  plt.axis([1, 31, 0, 15])
  plt.grid(True)
  plt.title("day versus GB")
  ax4.xaxis.set_major_locator(MultipleLocator(1))  
  ax4.yaxis.set_major_locator(MultipleLocator(1))  

  plt.show()
