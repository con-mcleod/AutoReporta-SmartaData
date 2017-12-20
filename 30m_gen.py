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

#### TO SET UP TOP ROW ####
output_row = []
output_row.append("SMI")
output_row.append("Ref No")
output_row.append("ECS")
output_row.append("Installer")
output_row.append("PV size")
output_row.append("Panel make")
output_row.append("Address")
output_row.append("State")
output_row.append("Site status")
output_row.append("Install date")
output_row.append("Supply date")
output_row.append("Export control")