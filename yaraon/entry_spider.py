import subprocess
import sys
import codecs
import re
from random import shuffle

output = subprocess.check_output("find yaraon.blog109.fc2.com -type f -mindepth 1 -name *html |egrep .*page-[\d]*",shell = True)
files = output.split("\n")

#use embed db by python
import anydbm
DLs = anydbm.open("DLP","c")

shuffle(files)

for f in files:
  print "begin==========[%s]"%f
  try:
    f = codecs.open("%s"%f, "r")
    content = f.read()
    p1=re.compile("http://yaraon.blog109.fc2.com/blog-entry-(\d{4,}).html")
    matches=p1.findall(content)

    # shuffle(matches)
    for m1 in matches:
      page_number = int(m1)

      # print page_number
      #save record into python
      key = "%d"%(page_number)
      # print type(key)
      if key in DLs: 
        print "SKIPED ACCORDING TO DB"
        continue
      DLs[key] = "1"

      # print page_number
      url = "http://yaraon.blog109.fc2.com/blog-entry-%d.html"%(page_number)
      print "LALLALALALLALALALLALALALLALALLA",url
      output=subprocess.check_output("wget -e robots=off --exclude-domains www.facebook.com -nc -T 6 -E -H -k -p %s"%url, shell = True)
  except Exception, e:
    print "FAILED ============ ", f
    print e
  else:
    print "SUCCESSED ============ ", f
 

