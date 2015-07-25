import os
import codecs

def output_files(folder_path = "."):
  print folder_path
  for dirname, dirnames, filenames in os.walk(folder_path):
    for filename in filenames:
      fn = os.path.join(dirname, filename)
      f = codecs.open(fn, mode="r", encoding="gbk", errors = "ignore")
      content = f.read()
      f2 = codecs.open(os.path.join(dirname, "utf_"+filename), mode="w", encoding="utf8", errors = "ignore")
      f2.write(content)
      f2.close()
      f.close()

if __name__ == '__main__':
  folder = "ChnSentiCorp_htl_ba_6000"
  types = ["neg", "pos"]
  result = {}

  for tt in types:
    output_files(folder_path = os.path.join(".", "diary_analysis", folder , tt))
   