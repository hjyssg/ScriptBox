# -*- coding: utf-8 -*- 
import requests
import os

def download_tag_page(tag, page):
    url = " angumi.tv/anime/tag/%s?page=%d" % (tag, page)
    print "loading", url, " ..."
    response = requests.get(url)
    response.encoding = "utf8"  #修正encoding，真他吗的坑
    if response.status_code != 200:
        print r
        raise Exception("NOT 200")

    from bs4 import BeautifulSoup as BS
    soup = BS(response.text)
    anime_list = soup.find(id = "browserItemList")


    if anime_list == None or len(anime_list.contents) == 0:
        print "reach the end of %d " % (year)
        return "END_OF_YEAR"

    for anime in anime_list.find_all("li"):
      subject_id =  string.replace(anime["id"], "item_", "")
      subject_id =  int(subject_id)

      try:
        jp_title =  anime.find(class_ = "inner").h3.small
        print jp_title.text.strip(), "  ", subject_id
      except Exception, e:
        pass


def download_year_page(year, page):
    url = "http://bangumi.tv/anime/browser/airtime/%d?page=%d" % (year, page)
    print "loading", url, " ..."
    response = requests.get(url)
    response.encoding = "utf8"  #修正encoding，真他吗的坑
    if response.status_code != 200:
        print r
        raise Exception("NOT 200")

    from bs4 import BeautifulSoup as BS
    soup = BS(response.text)
    anime_list = soup.find(id = "browserItemList")


    if anime_list == None or len(anime_list.contents) == 0:
        print "reach the end of %d " % (year)
        return "END_OF_YEAR"
    text =  anime_list.prettify()


    import codecs
    fn = "%d_%02d.txt" % (year, page)
    fn = os.path.join(".","index",fn)
    with codecs.open(fn, 'w', encoding = "utf8") as out_file:
        out_file.write(text)
    print "write [%s] into [%s]" % (url, fn)
    del response

def download_the_year_animes():
    for year in reversed(range(2000, 2016)):
        for page in xrange(1,40):
            try:
                if download_year_page(year, page) == "END_OF_YEAR":
                    break
                pass
            except Exception, e:
                import traceback
                traceback.print_exc()

            import time, random
            time.sleep(random.random())



def read_files(supported_file_types = {".txt"} , file_folder_path = "index"):
  import re
  import codecs
  import string

  for dirname, dirnames, filenames in os.walk(file_folder_path):
    for filename in filenames:
      
      #only allow supported file
      file_extension = os.path.splitext(filename)[1]
      if file_extension not in supported_file_types: continue
      filePath= os.path.join(dirname, filename)
      content = open(filePath).read()
      from bs4 import BeautifulSoup as BS
      soup = BS(content)

      ll = list()
      for anime in soup.find_all("li"):
        subject_id =string.replace(anime["id"], "item_","")
        subject_id =  int(subject_id)
        ll.append(subject_id)

        # try:
        #   jp_title =  anime.find(class_ = "inner").h3.small
        #   print jp_title.text.strip()
        # except Exception, e:
        #   pass
        
        #find(class_ = "grey").text
        chn = anime.find(class_ = "inner").find("a").text
        #print jp_title, chn
      for e in sorted(ll):
        print e


if __name__ == '__main__':
  try:
    os.mkdir("index")
  except Exception, e:
  pass

