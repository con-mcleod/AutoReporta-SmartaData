#!/usr/bin/python

import sys, csv, os, sqlite3, re
from constants import *
from helper_fns import *

datatype = "kWh Generation"

def daily_top_row():
	days = get_all_days()

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

	for day in days:
		output_row.append(day[0])
		output_row.append("% Perf")

	return output_row

def write_daily_data(output_file, SMIs, days):

	# For each SMI, begin the data writing process
	for SMI in SMIs:

		output_row = []

		SMI_details = get_SMI_details(SMI[0])
		maxlen = len(SMI_details[0])
		for i in range(0, maxlen):
			output_row.append(SMI_details[0][i])

		SMI_monthly_forecast = get_SMI_forecast(SMI[0])
		SMI_daily_forecast = monthly_to_daily(SMI_monthly_forecast)
	
	# Print out each daily forecast
		maxlen = len(SMI_monthly_forecast[0])
		for i in range(0, maxlen-1):
			output_row.append(SMI_daily_forecast[i])
		
		for day in days:

			daily_kWh_gen = get_SMI_daily_data(SMI[0], datatype, day[0])[0][0]
			month = int(get_month(SMI[0], datatype, day[0])[0][0])

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
	return