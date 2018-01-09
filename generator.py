#!/usr/bin/python3

import sys, csv, os, sqlite3, re
from helper_fns import *

##############################
#                            #
# PROGRAM EXECUTION          #
#                            #
##############################

if (len(sys.argv) != 2):
	print ("Usage: python3 generator.py [output.csv]")
	exit(1)

output_file = sys.argv[1]

if(os.path.exists(output_file)):
	os.remove(output_file)

##############################
#                            #
# store data in lists        #
#                            #
##############################

SMIs = get_all_SMIs()
dates = get_all_dates()

##############################
#                            #
# populate xlsx file         #
#                            #
##############################

for SMI in SMIs:

	SMI_details = get_SMI_details(SMI[0])
	SMI_monthly_forecast = get_SMI_forecast(SMI[0])
	SMI_daily_forecast = monthly_to_daily(SMI_monthly_forecast)
	SMI_state = get_SMI_state(SMI[0])[0][0]

	# for each date in encompass report
		# fetch the daily generation
		# store daily generation/forecast

		# fetch BOM data for date matching SMI_state to appropriate city
