import sys
import os
import glob
import re


#################the main part################

sortFlag=False;
if sys.argv[2] == '-s':
  sortFlag=True;
  sys.remove('-s')

if len(sys.argv)<2:
  print "Please type the docx or text file that you want "
  sys.exit()


##sort output
arr=sys.argv[1:len(sys.argv)]
arr.sort()
##print arr
for arg in arr:
  
  ##support wildcard
  files=glob.glob(arg)
  files.sort()
 
  for file in files:
      
      ##replace & with \&
      file=re.sub('&', '\\&',file)
      
      fileName, fileExtension = os.path.splitext(file)
      os.system('echo '+fileName)
      if  fileExtension=='.docx':
      #http://www.commandlinefu.com/commands/view/4311/extract-plain-text-from-ms-word-docx-files
        command=' unzip -p '+file+' word/document.xml | sed -e \'s/<[^>]\{1,\}>//g; s/[^[:print:]]\{1,\}//g\''
        os.system(command) 
      else:
        command='cat '+file
        os.system(command)
  os.system('echo \n\n')  




