import subprocess
import sys

print sys.argv
if len(sys.argv) == 3:
  try:
    beg = int(sys.argv[1])
    end = int(sys.argv[2])
  except Exception, e:
    raise
else:
  beg = 1
  end = 450



#download index page
for ii in range(beg, end):
  print "========begin===", ii
  try:
    url = "http://yaraon.blog109.fc2.com/page-%d.html"%(ii)
    
    #output=subprocess.check_output("wget -nc -e use_proxy=yes -e http_proxy=173.214.168.55:8080 -e robots=off -T 6 -E -H -k -p  %s"%url, shell = True)

    output=subprocess.check_output("wget -nc -e robots=off -T 6 -E -H -k -p  %s"%url, shell = True)
  except Exception, e:
    print "======== FAIL===", ii
  finally:
    print "========end===", ii
    print  "\n\n\n"
