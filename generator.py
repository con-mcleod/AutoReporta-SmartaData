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

output_row.append("Jan Daily")
output_row.append("Feb Daily")
output_row.append("Mar Daily")
output_row.append("Apr Daily")
output_row.append("May Daily")
output_row.append("Jun Daily")
output_row.append("Jul Daily")
output_row.append("Aug Daily")
output_row.append("Sep Daily")
output_row.append("Oct Daily")
output_row.append("Nov Daily")
output_row.append("Dec Daily")


for date in dates:
	output_row.append(date[0])
	output_row.append("% Perf")

write_to_csv(output_file, 'a', output_row)

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

# Print out each monthly forecast
	maxlen = len(SMI_monthly_forecast[0])
	for i in range(0, maxlen-1):
		output_row.append(SMI_daily_forecast[i])
	
	for date in dates:

		daily_kWh_gen = get_SMI_daily_data(SMI[0], datatype, date[0])[0][0]

		month = re.sub(r'[^a-zA-Z]', '', date[0])
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
