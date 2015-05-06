# -*- coding: utf-8 -*- 
import requests
import string
import shutil
import requests
import  codecs
import threading
import os


    


def analysis(soup): 
  
    title = soup.find(class_ = "nameSingle")
    #...

    # cv_infos = soup.find(id = "browserItemList").find_all("span",class_= "tip_j")
    # for cv_info in cv_infos:
    #     print cv_info.small.span.text
    #     print cv_info.find(class_="tip").text
    #     print cv_info.a.text
    #     print "---"

    # comment_infos = soup.find_all(class_ = "item clearit")

    # infos = soup.find(id = "infobox").find_all("li")
    # for info in infos:
    #     key = info.span.text
    #     value = string.replace(info.text, key, "")
    #     key = key.split(": ")[0]
    #     print "(%s) (%s)" % (key, value)


class download_single_page_thread(threading.Thread):  
    def __init__(self, subject_id, proxies = None, lock = None):  
        threading.Thread.__init__(self, name = str(subject_id))
        self.lock = lock 
        self.subject_id = subject_id
        self.proxies = proxies 
      
    def run(self): 
        try:
            self.load_single_anime() 
        except Exception, e:
            #import traceback
            #traceback.print_exc()
            print "----FAIL AT", self.subject_id
            #print self.proxies, " -- ", self.proxies["http"]
            # self.lock.acquire()
            # try:
            #     global fail_count, proxy_ips
            #     proxy_ips.remove(self.proxies["http"])
            #     fail_count += 1
            #     if fail_count > 100:
            #         quit()
            # except Exception, e:
            #     pass
            # self.lock.release()
        else:
            print "--FINISHED", line

    def download_img(self, url):
        rs = requests.get(url,timeout = 10, stream=True, proxies=self.proxies)

        try:
          os.mkdir("anime_pages")
        except Exception, e:
          pass
        fn = url.split("/")[-1]
        fn = os.path.join(".", "anime_pages", fn)
        with open(fn, 'wb') as out_file:
            shutil.copyfileobj(rs.raw, out_file)
        # print "save [%s]" % (fn)
        del rs

    def load_single_anime(self):
        url = "http://bangumi.tv/subject/%d" % self.subject_id
        #print "loading [", url, "]..."
        rs = requests.get(url, timeout = 5, proxies=self.proxies)
        rs.encoding = "utf8"  #修正encoding，真他吗的坑
        if rs.status_code != 200:
            print r
            raise Exception("NOT 200")

        from bs4 import BeautifulSoup as BS
        soup = BS(rs.text)

        fn = "%d.html"%(self.subject_id)
        fn = os.path.join(".", "anime_pages", fn)
        with codecs.open(fn, 'w', encoding = "utf8") as out_file:
            out_file.write(soup.prettify())
        #print "write [%s] into [%s]" % (url, fn)

        cover_img = soup.find(class_=  "thickbox cover")
        self.download_img("http:"+cover_img["href"])


if __name__ == '__main__':
    fail_count = 0
    temp_proxy_ips = open("proxies.txt").readlines()
    proxy_ips = list()
    for pp in temp_proxy_ips:
        proxy_ips.append("http://"+pp.strip())


    
    lines=open("subject_ids.txt").readlines()
    proxy_index = 0
    lock = threading.Lock()
    for line in lines:
        #a limited number of threads
        thr_num = 15
        while threading.activeCount() >= thr_num:
            import time, random
            time.sleep(0.2)

        if proxy_index < thr_num:
            proxies = {}
            proxy_index += 1
        else:
            proxy_index = 0
            proxies = {}

        #print type(proxies),proxies
        thread = download_single_page_thread(subject_id = int(line), lock = lock,proxies= proxies)
        thread.start()

       


 

        