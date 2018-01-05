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

def get_all_days():
	query = "SELECT distinct(obs_day) from observation"
	payload = None
	all_days = dbselect(query, payload)
	return all_days

def get_all_months():
	query = "SELECT distinct(obs_month) from observation"
	payload = None
	all_months = dbselect(query, payload)
	return all_months

def get_all_years():
	query = "SELECT distinct(obs_year) from observation"
	payload = None
	all_years = dbselect(query, payload)
	return all_years

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
		if not int(monthly_forecast[0][i]):
			return 0
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

def get_SMI_hourly_data(SMI, datatype, obs_time):
	query = "SELECT value from observation where SMI=? and obs_time=? and datatype=?"
	payload = (SMI, obs_time, datatype)
	result = dbselect(query, payload)
	return result

def get_SMI_daily_data(SMI, datatype, obs_day):
	query = "SELECT sum(value) from observation where SMI=? and obs_day=? and datatype=?"
	payload = (SMI, obs_day, datatype)
	result = dbselect(query, payload)
	return result

def get_month(SMI, datatype, obs_day):
	query = "SELECT obs_month from observation where SMI=? and obs_day=? and datatype=?"
	payload = (SMI, obs_day, datatype)
	result = dbselect(query, payload)
	return result

def get_SMI_weekly_data(SMI, datatype, obs_week):
	pass

def get_SMI_monthly_data(SMI, datatype, obs_month):
	query = "SELECT sum(value) from observation where SMI=? and obs_month=? and datatype=?"
	payload = (SMI, obs_month, datatype)
	result = dbselect(query, payload)
	return result

def get_daily_performance(daily_kWh_gen, month, SMI_daily_forecast):
	if month == 1:
		result = daily_kWh_gen / SMI_daily_forecast[0]
	elif month == 2:
		result = daily_kWh_gen / SMI_daily_forecast[1]
	elif month == 3:
		result = daily_kWh_gen / SMI_daily_forecast[2]
	elif month == 4:
		result = daily_kWh_gen / SMI_daily_forecast[3]
	elif month == 5:
		result = daily_kWh_gen / SMI_daily_forecast[4]
	elif month == 6:
		result = daily_kWh_gen / SMI_daily_forecast[5]
	elif month == 7:
		result = daily_kWh_gen / SMI_daily_forecast[6]
	elif month == 8:
		result = daily_kWh_gen / SMI_daily_forecast[7]
	elif month == 9:
		result = daily_kWh_gen / SMI_daily_forecast[8]
	elif month == 10:
		result = daily_kWh_gen / SMI_daily_forecast[9]
	elif month == 11:
		result = daily_kWh_gen / SMI_daily_forecast[10]
	elif month == 12:
		result = daily_kWh_gen / SMI_daily_forecast[11]
	return result