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
	group by obs_day, obs_month, obs_year order by obs_year, obs_month"""
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
# currently ignoring leap year because this program is intended for use from
# 2017 -> eol which wouldn't be more than 3 years, and next leap year is 2020
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

# return list of encompass values for SMI's daily generation
def get_SMI_daily_gen(SMI):
	query = "SELECT value from enc_values where SMI=?"
	payload = (SMI,)
	result = dbselect(query, payload)
	return result

# return list of solar performance for a given state
def get_state_solar_perf(state, datatype):
	
	city = state_to_city(state)

	query = "SELECT obs_value, bom_day, bom_month, bom_year from bom_obs where bom_location=? and datatype=? order by bom_year, bom_month"
	payload = (city, datatype)
	result = dbselect(query, payload)
	return result

# return list of only relevant solar values
def filter_weather(weather_cond, dates):
	relevant = []
	if weather_cond:
		for cond in weather_cond:
			for date in dates:
				if (cond[3]==date[2]) and (cond[2]==date[1]) and (cond[1]==date[0]):
					relevant.append(cond)
	return relevant

# return only the value from the list
def get_weather_vals(relevant_weather_perf, loop_val):
	values = []
	for i in range(0, len(relevant_weather_perf)):
		values.append(relevant_weather_perf[i][0])

	if not values:
		for i in range(0, loop_val):
			values.append(0)
	return values

# return list of all average solar values in each month and year
def get_ave_condition(state, datatype):
	city = state_to_city(state)
	query = "SELECT average_val, bom_month, bom_year, bom_location from bom_ave where bom_location=? and datatype=?"
	payload = (city, datatype)
	result = dbselect(query, payload)
	return result

# return list of only relevant average values
def filter_ave(average_list, dates):
	relevant = []
	for average in average_list:
		for date in dates:
			if (average[1]==date[1] and average[2]==date[2] and average not in relevant):
				relevant.append(average)
	return relevant

# return list of weather condition vs average
def compare_cond_to_ave(cond_vals, dates, state, relevant_ave):
	city = state_to_city(state)
	results = []
	for val, date in zip(cond_vals, dates):
		for ave in relevant_ave:
			if city==ave[3] and date[2]==ave[2] and date[1]==ave[1]:
				if (val is not ""):
					weather_var = val/ave[0]
				else:
					weather_var = 0
				results.append(weather_var)

	if not results:
		for i in range(0, len(dates)):
			results.append(0)

	return results

# return list of performance as actual generation / forecast for each day
def get_daily_perf(SMI, daily_kWh_gen, SMI_daily_forecast, dates):

	perf = []
	for gen, date in zip(daily_kWh_gen, dates):

		if gen[0] == "":
			perf.append(0)
			continue

		if date[1] == 1:
			perf.append(gen[0] / SMI_daily_forecast[0])
		elif date[1] == 2:
			perf.append(gen[0] / SMI_daily_forecast[1])
		elif date[1] == 3:
			perf.append(gen[0] / SMI_daily_forecast[2])
		elif date[1] == 4:
			perf.append(gen[0] / SMI_daily_forecast[3])
		elif date[1] == 5:
			perf.append(gen[0] / SMI_daily_forecast[4])
		elif date[1] == 6:
			perf.append(gen[0] / SMI_daily_forecast[5])
		elif date[1] == 7:
			perf.append(gen[0] / SMI_daily_forecast[6])
		elif date[1] == 8:
			perf.append(gen[0] / SMI_daily_forecast[7])
		elif date[1] == 9:
			perf.append(gen[0] / SMI_daily_forecast[8])
		elif date[1] == 10:
			perf.append(gen[0] / SMI_daily_forecast[9])
		elif date[1] == 11:
			perf.append(gen[0] / SMI_daily_forecast[10])
		elif date[1] == 12:
			perf.append(gen[0] / SMI_daily_forecast[11])

	return perf

# return total performance as average of daily performance
def get_ave_perf(SMI_daily_perf):
	count = 0
	total_perf = 0
	for perf in SMI_daily_perf:
		total_perf += perf
		count += 1

	ave_perf = total_perf/count

	return ave_perf

# return count of number of days with 0 generation
def get_site_off(SMI_daily_gen):
	count = 0
	for gen in SMI_daily_gen:
		if gen[0] == 0 or gen[0] == "":
			count += 1
	return count

# convert state to city
def state_to_city(state):
	if state == "QLD":
		city = "brisbane"
	elif state == "NSW":
		city = "sydney"
	elif state == "SA":
		city = "adelaide"
	elif state == "VIC":
		city = "melbourne"
	else:
		city = None
	return city


# convert performance to an adjusted performance value
def adjust_perf(SMI_daily_perf, solar_cond_vs_ave, slope, intercept, p_value, r_value):
	
	adjusted_result = []
	if (p_value < .05 and r_value*r_value>.5):
		for perf, weather in zip(SMI_daily_perf, solar_cond_vs_ave):
			
			weather_diff = -(weather - 1)
			adjusted_perf = perf + slope*weather_diff
			adjusted_result.append(adjusted_perf)

	if not adjusted_result:
		for i in range(0, len(SMI_daily_perf)):
			adjusted_result.append("")
	return adjusted_result



