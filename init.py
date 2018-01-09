#!/usr/bin/python

import sys, csv, sqlite3, os, glob, re, shutil
from collections import defaultdict
from helper_fns import *

if (len(sys.argv) != 4):
	print ("Usage: python3 init.py [encompass_file.csv] [salesforce_file.csv] dataset.db")
	exit(1)

enc_dataset = sys.argv[1]
sf_dataset = sys.argv[2]
DATABASE = sys.argv[3]

if(os.path.exists(DATABASE)):
	os.remove(DATABASE)

connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()
