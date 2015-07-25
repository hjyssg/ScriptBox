# -*- coding: utf-8 -*-
import os
import re
import sys
import time
import codecs
import string
import datetime as DT
from bs4 import BeautifulSoup as BS
import codecs

def read_files(folder_path = "."):
  result = []
  for dirname, dirnames, filenames in os.walk(folder_path):
    for filename in filenames:
      result.append(os.path.join(dirname, filename))
  return result



if __name__ == '__main__':
  files = read_files(folder_path = os.path.join(".", "raw_output"))
  ii = 0
  for fn in files:
    try:
      f = codecs.open(fn, mode="r", encoding="utf8", errors = "ignore")
      soup = BS(f)
      f.close()

      comment_rows = soup.find_all(class_ = "comment-item")
      
      for comment_row in comment_rows:
        rating = comment_row.find(class_ = "rating")
        comment = comment_row.find("p")
        if rating is None or comment is None: continue
        print rating["title"],  comment.text
      
    except Exception, e:
      pass



