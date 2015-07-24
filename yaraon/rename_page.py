"""
  attach title to each page file
"""

import subprocess
import sys
import codecs
import re
from random import shuffle

output = subprocess.check_output("find yaraon.blog109.fc2.com -type f -mindepth 1 -name *blog-entry-* ",shell = True)
files = output.split("\n")

#use embed db by python
import anydbm
DLs = anydbm.open("DLP","c")

shuffle(files)

for fn in files:
  print "begin==========[%s]"%fn
  try:
    f = codecs.open("%s"%fn, mode= "r", encoding = "utf8")
    content = f.read()
    f.close()
    head = content[0:1000]
    head = re.sub("\n", "", head)
    head = re.sub("\r", "", head)

    #. do not include new line
    p1=re.compile(r"<title>(.*?)</title>")
    match=p1.search(head)
    title =  match.group(1).strip()
    print title

    basename = fn.split("/")[-1]
    basename = basename.split(".")[0]
    newName = "yaraon.blog109.fc2.com/"+basename+"-"+title+".html"

    # print "going to make [%s]"%(newName)
    # raw_input()
    newFile = codecs.open(newName, "w","utf8")
    newFile.write(content)
    newFile.close()
  except Exception, e:
    print "======== FAIL===", fn
    print e
  finally:
    print "========end===", fn
    print  "\n\n\n"
    