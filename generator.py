#!/usr/bin/python

import sys, csv, os, sqlite3, re
from helper_fns import *
#from 1min_fns import *
#from 10min_fns import *
#from hourly_fns import *
from daily_fns import *
#from weekly_fns import *
#from monthly_fns import *

if (len(sys.argv) != 3):
	print ("Usage: python3 generator.py [1min/10min/hourly/daily/weekly/monthly] [output.csv]")
	exit(1)

report_frequency = sys.argv[1]
output_file = sys.argv[2]

if(os.path.exists(output_file)):
	os.remove(output_file)

SMIs = get_all_SMIs()
datatypes = get_all_datatypes()
times = get_all_times()
days = get_all_days()
months = get_all_months()
years = get_all_years()
datatype = "kWh Generation"

# FUNCTION TO SET UP CSV HEADINGS
# if (report_frequency == "1min"):
# 	output_row = 1min_top_row()
# elif (report_frequency == "10min"):
# 	output_row = 10min_top_row()
# elif (report_frequency == "hourly"):
# 	output_row = hourly_top_row()
if (report_frequency == "daily"):
	output_row = daily_top_row()
# elif (report_frequency == "weekly"):
# 	output_row = weekly_top_row()
# elif (report_frequency == "monthly"):
# 	output_row = monthly_top_row()
else:
	print ("Incorrect report time interval!")
	exit(1)
write_to_csv(output_file, 'a', output_row)


# FUNCTION TO FILL IN REPORT DATA
if (report_frequency == "daily"):
	output_row = write_daily_data(output_file, SMIs, days)
else:
	exit(1)