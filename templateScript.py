#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs 
import re
import subprocess


# output = subprocess.check_output(["ls", "-R", "pixiv"])
output = subprocess.check_output(["ls -R pixiv"], shell = True)

lines = output.split("\n")

# lines = f.readlines()
# f= codecs.open("p1.txt", mode = "r", encoding = "utf8")

p = re.compile("(\d{3,})")

for line in lines:
  # print line

  r1 = p.search(line)
  if r1:
    pass

