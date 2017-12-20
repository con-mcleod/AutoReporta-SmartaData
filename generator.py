#!/usr/bin/python

import sys, csv, os, sqlite3, re
from helper_fns import *

if (len(sys.argv) != 3):
	print ("Usage: python3 generator.py [hourly/daily/weekly/fortnightly/monthly] [output.csv]")
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
if (report_frequency == "daily"):
	output_row = daily_top_row()
elif (report_frequency == "weekly"):
	output_row = weekly_top_row()
elif (report_frequency == "fortnightly"):
	output_row = fortnightly_top_row()
elif (report_frequency == "monthly"):
	output_row = monthly_top_row()
else:
	exit(1)
write_to_csv(output_file, 'a', output_row)

# For each SMI, begin the data writing process
for SMI in SMIs:

	output_row = []

	SMI_details = get_SMI_details(SMI[0])
	maxlen = len(SMI_details[0])
	for i in range(0, maxlen):
		output_row.append(SMI_details[0][i])

	SMI_monthly_forecast = get_SMI_forecast(SMI[0])
	SMI_daily_forecast = monthly_to_daily(SMI_monthly_forecast)
	SMI_weekly_forecast = monthly_to_weekly(SMI_monthly_forecast)
	
# Print out each monthly forecast
	# maxlen = len(SMI_monthly_forecast[0])
	# for i in range(1, maxlen-1):
	# 	output_row.append(SMI_monthly_forecast[0][i])

# Print out each daily forecast
	maxlen = len(SMI_monthly_forecast[0])
	for i in range(0, maxlen-1):
		output_row.append(SMI_daily_forecast[i])
	
	for day in days:

		daily_kWh_gen = get_SMI_daily_data(SMI[0], datatype, day[0])[0][0]

		month = re.sub(r'[^a-zA-Z]', '', day[0])
		daily_perf = get_daily_performance(daily_kWh_gen, month, SMI_daily_forecast)

		if daily_kWh_gen is None:
			daily_kWh_gen = 0
		if daily_perf is None:
			daily_perf = 0

		output_row.append(daily_kWh_gen)
		output_row.append(daily_perf)

	with open(output_file,'a') as csv_out:
		writer = csv.writer(csv_out)
		writer.writerow(output_row)
