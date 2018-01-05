#!/usr/bin/python3

import sys, csv, os, sqlite3, re
import pandas as pd
import numpy as np

from helper_fns import *


if(len(sys.argv) != 2):
	print ("Usage: python3 generator.py output.xlsx")
	exit (1)

output_file = sys.argv[1]

if(os.path.exists(output_file)):
	os.remove(output_file)

df = pd.read_sql("SELECT * from SMI_details", sqlite3.connect(DATABASE))

df.to_excel(output_file, sheet_name="DailyReport")