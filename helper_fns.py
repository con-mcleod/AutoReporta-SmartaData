#!/usr/bin/python3

import sys, csv, os, sqlite3, re
from constants import *

##############################
#                            #
# Database handling          #
#                            #
##############################

# prepare sql query execution
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

# execute sql query
def dbexecute(query, payload):
	connection = sqlite3.connect(DATABASE)
	cursor = connection.cursor()
	if not payload:
		cursor.execute(query)
	else:
		cursor.execute(query, payload)
	connection.commit()
	connection.close()

##############################
#                            #
# init.py helpers            #
#                            #
##############################

# convert month from string to int
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

##############################
#                            #
# generator.py helpers       #
#                            #
##############################

# return all SMIs from encompass report
def get_all_SMIs():
	query = "SELECT distinct(SMI) from enc_values"
	payload = None
	all_SMIs = dbselect(query, payload)
	return all_SMIs

# return the range of dates from encompass report
def get_all_dates():
	query = """SELECT obs_day, obs_month, obs_year from enc_values 
	group by obs_day, obs_month, obs_year order by obs_year"""
	payload = None
	all_dates = dbselect(query, payload)
	return all_dates

# return details of each SMI in given SMI(s)
def get_SMI_details(SMI):
	query = "SELECT * from SMI_details where SMI=?"
	payload = (SMI,)
	result = dbselect(query,payload)
	return result

# return state (location) of given SMI(s)
def get_SMI_state(SMI):
	query = "SELECT state from SMI_details where SMI=?"
	payload = (SMI,)
	result = dbselect(query,payload)
	return result

# return monthly forecast for given SMI(s)
def get_SMI_forecast(SMI):
	query = "SELECT * from forecast where SMI=?"
	payload = (SMI,)
	result = dbselect(query, payload)
	return result

# convert monthly forecast value to daily forecast value
def monthly_to_daily(monthly_forecast):
	results = []
	for i in range(1, len(monthly_forecast[0])):
		if not int(monthly_forecast[0][i]):
			return 0
		if i == JAN:
			result = monthly_forecast[0][i]/days_in_jan
		if i == FEB: # and not_leap_year
			result = monthly_forecast[0][i]/days_in_feb
		# if i == FEB and leap_year:
			# result = monthly_forecast[0][i]/days_in_feb_leap
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

def get_SMI_daily_gen(SMI):
	query = "SELECT value from enc_values where SMI=?"
	payload = (SMI,)
	result = dbselect(query, payload)
	return result

























##############################
#                            #
# unused                     #
#                            #
##############################

# return all days from encompass report
def get_all_days():
	query = "SELECT distinct(obs_day) from enc_values"
	payload = None
	all_days = dbselect(query, payload)
	return all_days

# return all months from encompass report
def get_all_months():
	query = "SELECT distinct(obs_month) from enc_values"
	payload = None
	all_months = dbselect(query, payload)
	return all_months

# return all years from encompass report
def get_all_years():
	query = "SELECT distinct(obs_year) from enc_values"
	payload = None
	all_years = dbselect(query, payload)
	return all_years