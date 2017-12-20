#!/usr/bin/python

import sys, csv, os, sqlite3, re
from constants import *

#######################
# CSV Handling
#######################

def write_to_csv(filename, flag, output_row):

	with open(filename,flag) as csv_out:
		writer = csv.writer(csv_out)
		writer.writerow(output_row)

def month_to_num(month):
	if month == "Jan": 
		return 1
	elif month == "Feb":
		return 2
	elif month == "Mar":
		return 3
	elif month == "Apr":
		return 4
	elif month == "May":
		return 5
	elif month == "Jun":
		return 6
	elif month == "Jul":
		return 7
	elif month == "Aug":
		return 8
	elif month == "Sep":
		return 9
	elif month == "Oct":
		return 10
	elif month == "Nov":
		return 11
	elif month == "Dec":
		return 12
	else:
		return 0

#######################
# Database Handling
#######################

DATABASE = "dataset.db"

def dbselect(query, payload):
	connection = sqlite3.connect(DATABASE)
	cursorObj = connection.cursor()
	if not payload:
		rows = cursorObj.execute(query)
	else:
		rows = cursorObj.execute(query,payload)
	results = []
	for row in rows:
		results.append(row)
	cursorObj.close()
	return results

def dbexecute(query, payload):
	connection = sqlite3.connect(DATABASE)
	cursor = connection.cursor()
	if not payload:
		cursor.execute(query)
	else:
		cursor.execute(query, payload)
	connection.commit()
	connection.close()

#######################
# SQL Functions
#######################

def get_all_SMIs():
	query = "SELECT distinct(SMI) from observation"
	payload = None
	all_SMIs = dbselect(query, payload)
	return all_SMIs

def get_all_datatypes():
	query = "SELECT distinct(datatype) from observation"
	payload = None
	all_datatypes = dbselect(query, payload)
	return all_datatypes

def get_all_dates():
	query = "SELECT distinct(obs_date) from observation"
	payload = None
	all_dates = dbselect(query, payload)
	return all_dates

def get_all_times():
	query = "SELECT distinct(obs_time) from observation"
	payload = None
	all_times = dbselect(query, payload)
	return all_times

#######################
# Salesforce Modelling
#######################

def get_SMI_details(SMI):
	query = "SELECT * from SMI_details where SMI=?"
	payload = (SMI,)
	result = dbselect(query,payload)
	return result

def get_SMI_forecast(SMI):
	query = "SELECT * from forecast where SMI=?"
	payload = (SMI,)
	result = dbselect(query, payload)
	return result

# function to convert monthly forecast to daily forecast
def monthly_to_daily(monthly_forecast):
	results = []
	for i in range(1, len(monthly_forecast[0])):
		if i == JAN:
			result = monthly_forecast[0][i]/days_in_jan
		if i == FEB:
			result = monthly_forecast[0][i]/days_in_feb
		if i == MAR:
			result = monthly_forecast[0][i]/days_in_mar
		if i == APR:
			result = monthly_forecast[0][i]/days_in_apr
		if i == MAY:
			result = monthly_forecast[0][i]/days_in_may
		if i == JUN:
			result = monthly_forecast[0][i]/days_in_jun
		if i == JUL:
			result = monthly_forecast[0][i]/days_in_jul
		if i == AUG:
			result = monthly_forecast[0][i]/days_in_aug
		if i == SEP:
			result = monthly_forecast[0][i]/days_in_sep
		if i == OCT:
			result = monthly_forecast[0][i]/days_in_oct
		if i == NOV:
			result = monthly_forecast[0][i]/days_in_nov
		if i == DEC:
			result = monthly_forecast[0][i]/days_in_dec
		results.append(result)
	return results

def monthly_to_weekly(monthly_forecast):
	weekly_forecast = []
	daily_forecast = monthly_to_daily(monthly_forecast)
	for i in range(0, len(daily_forecast)):
		weekly_forecast.append(daily_forecast[i]*7)
	return weekly_forecast

#######################
# Encompass Modelling
#######################

def get_SMI_daily_data(SMI, datatype, day):
	query = "SELECT sum(value) from observation where SMI=? and obs_date=? and datatype=?"
	payload = (SMI, day, datatype)
	result = dbselect(query, payload)
	return result

def get_SMI_hourly_data(SMI, datatype, obs_time):
	query = "SELECT value from observation where SMI=? and obs_time=? and datatype=?"
	payload = (SMI, time, datatype)
	result = dbselect(query, payload)
	return result

def get_daily_performance(daily_kWh_gen, month, SMI_daily_forecast):
	if month == "Jan":
		result = daily_kWh_gen / SMI_daily_forecast[0]
	elif month == "Feb":
		result = daily_kWh_gen / SMI_daily_forecast[1]
	elif month == "Mar":
		result = daily_kWh_gen / SMI_daily_forecast[2]
	elif month == "Apr":
		result = daily_kWh_gen / SMI_daily_forecast[3]
	elif month == "May":
		result = daily_kWh_gen / SMI_daily_forecast[4]
	elif month == "Jun":
		result = daily_kWh_gen / SMI_daily_forecast[5]
	elif month == "Jul":
		result = daily_kWh_gen / SMI_daily_forecast[6]
	elif month == "Aug":
		result = daily_kWh_gen / SMI_daily_forecast[7]
	elif month == "Sep":
		result = daily_kWh_gen / SMI_daily_forecast[8]
	elif month == "Oct":
		result = daily_kWh_gen / SMI_daily_forecast[9]
	elif month == "Nov":
		result = daily_kWh_gen / SMI_daily_forecast[10]
	elif month == "Dec":
		result = daily_kWh_gen / SMI_daily_forecast[11]
	return result