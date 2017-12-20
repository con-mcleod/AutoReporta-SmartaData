#!/usr/bin/python

import sys, csv, os, sqlite3, re
from helper_fns import *

if (len(sys.argv) != 2):
	print ("Usage: python3 generator.py [output.csv]")
	exit(1)

output_file = sys.argv[1]

if(os.path.exists(output_file)):
	os.remove(output_file)

SMIs = get_all_SMIs()
datatypes = get_all_datatypes()
dates = get_all_dates()
times = get_all_times()
datatype = "kWh Generation"
