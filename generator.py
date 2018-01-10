#!/usr/bin/python3

import sys, csv, os, sqlite3, re
from openpyxl import Workbook
from helper_fns import *

##############################
#                            #
# PROGRAM EXECUTION          #
#                            #
##############################

if (len(sys.argv) != 2):
	print ("Usage: python3 generator.py [output_file]")
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

wb = Workbook()
ws = wb.active
ws.title = "Daily Report"

row_count = 0
for SMI in SMIs:

	col_count = 0

	SMI_details = get_SMI_details(SMI[0])
	SMI_monthly_forecast = get_SMI_forecast(SMI[0])
	SMI_daily_forecast = monthly_to_daily(SMI_monthly_forecast)
	SMI_state = get_SMI_state(SMI[0])[0][0]

	SMI_daily_gen = get_SMI_daily_gen(SMI[0])

	for x in range(0, len(SMI_details)):
		for detail in SMI_details[x]:
			ws.cell(row=row_count+1, column=col_count+1).value = detail
			col_count += 1

	for df in SMI_daily_forecast:
		ws.cell(row=row_count+1, column=col_count+1).value = df
		col_count += 1

	for y in range(0, len(SMI_daily_gen)):
		for value in SMI_daily_gen[y]:
			ws.cell(row=row_count+1, column=col_count+1).value = value
			ws.cell(row=row_count+1, column=col_count+2).value = "Measured performance"
			ws.cell(row=row_count+1, column=col_count+3).value = "Solar adjusted"
			ws.cell(row=row_count+1, column=col_count+4).value = "Temp adjusted"
			ws.cell(row=row_count+1, column=col_count+5).value = "Rain adjusted"
			ws.cell(row=row_count+1, column=col_count+6).value = "Actual performance"
			col_count += 6

	row_count += 1

# Save the file
wb.save(output_file)




	# for each date in encompass report
		# fetch the daily generation
		# store daily generation/forecast

		# fetch BOM data for date matching SMI_state to appropriate city
