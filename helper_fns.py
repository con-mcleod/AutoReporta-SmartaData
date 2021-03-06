#!/usr/bin/python3

import sys, csv, os, sqlite3, re
from constants import *
from flask_login import UserMixin, LoginManager,login_user, current_user, login_required, logout_user
from server import *
from smartadata import *

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

# return the address of the given SMI
def get_SMI_address(SMI):
	print (SMI)
	query = "SELECT address from SMI_details where SMI=?"
	payload = (SMI,)
	address = dbselect(query, payload)
	return address

# return SMI lat/long
def get_SMI_coords(SMI):
	query = "SELECT SMI_latitude, SMI_longitude from SMI_coords where SMI=?"
	payload = (SMI,)
	smi_coords = dbselect(query, payload)
	return smi_coords

# return closest weather station to SMI
def find_closest_stn(SMI, SMI_latitude, SMI_longitude):
	query = """SELECT bom_location, bom_latitude, bom_longitude, 
				((69.1 * (bom_latitude - ?)) * (69.1 * (bom_latitude - ?))) +
				((69.1 * (? - bom_longitude)) * (69.1 * (? - bom_longitude))) AS distance
				FROM BOM_coords
				GROUP BY distance
				ORDER BY distance
				limit 1"""
	payload = (SMI_latitude, SMI_latitude, SMI_longitude, SMI_longitude)
	result = dbselect(query, payload)
	return result

##############################
#                            #
# generator.py helpers       #
#                            #
##############################

# return entire fleet of SMIs
def get_entire_fleet():
	query = "SELECT distinct(SMI) from smi_details"
	payload = None
	result = dbselect(query, payload)
	return result

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

# return weather station (location) of given SMI(s)
def get_SMI_weather_stn(SMI):
	query = "SELECT weather_stn from closest_stn where SMI=?"
	payload = (SMI,)
	result = dbselect(query,payload)
	return result

# return address of given SMI(s)
def get_SMI_address(SMI):
	query = "SELECT address from SMI_details where SMI=?"
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
		if (monthly_forecast[0][i]=="" or monthly_forecast[0][i]==0):
			results.append(0)
			continue
		elif i == JAN:
			result = monthly_forecast[0][i]/days_in_jan
		elif i == FEB: # and not_leap_year
			result = monthly_forecast[0][i]/days_in_feb
		# elif i == FEB and leap_year:
			# result = monthly_forecast[0][i]/days_in_feb_leap
		elif i == MAR:
			result = monthly_forecast[0][i]/days_in_mar
		elif i == APR:
			result = monthly_forecast[0][i]/days_in_apr
		elif i == MAY:
			result = monthly_forecast[0][i]/days_in_may
		elif i == JUN:
			result = monthly_forecast[0][i]/days_in_jun
		elif i == JUL:
			result = monthly_forecast[0][i]/days_in_jul
		elif i == AUG:
			result = monthly_forecast[0][i]/days_in_aug
		elif i == SEP:
			result = monthly_forecast[0][i]/days_in_sep
		elif i == OCT:
			result = monthly_forecast[0][i]/days_in_oct
		elif i == NOV:
			result = monthly_forecast[0][i]/days_in_nov
		elif i == DEC:
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
def get_stn_solar_perf(stn, datatype):
	query = "SELECT obs_value, bom_day, bom_month, bom_year from bom_obs where bom_location=? and datatype=? order by bom_year, bom_month"
	payload = (stn, datatype)
	result = dbselect(query, payload)
	return result

# return the location of the closest weather stn
def get_closest_stn(SMI):
	query = "SELECT weather_stn from closest_stn where SMI=?"
	payload = (SMI)
	result = dbselect(query, payload)
	return result

# return the location of the closest weather stn
def get_closest_stn2(SMI):
	query = "SELECT weather_stn from closest_stn where SMI=?"
	payload = (SMI,)
	result = dbselect(query, payload)
	return result

# return distance between SMI and it's closest weather station
def get_SMI_stn_dist(SMI):
	query = "SELECT distance from closest_stn where SMI=?"
	payload = (SMI)
	result = dbselect(query, payload)
	return result

# return distance between SMI and it's closest weather station
def get_SMI_stn_dist2(SMI):
	query = "SELECT distance from closest_stn where SMI=?"
	payload = (SMI,)
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

# function to translate max temp to a power loss number
def get_temp_effect(temp_values):
	results = []
	for temp in temp_values:
		if temp is not None and temp != "" and temp != 0:
			temp_effect = -(.004 * (temp*.85 - 25))
		else:
			temp_effect = 0
		results.append(temp_effect)
	return results

def temp_adjust(SMI_daily_perf, temp_effect):
	results = []
	for perf, effect in zip(SMI_daily_perf, temp_effect):
		results.append(perf*(1+effect))
	return results

# return list of all average solar values in each month and year
def get_ave_condition(stn, datatype):
	query = "SELECT average_val, bom_month, bom_year, bom_location from bom_ave where bom_location=? and datatype=?"
	payload = (stn, datatype)
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
def compare_cond_to_ave(cond_vals, dates, stn, relevant_ave):
	results = []
	for val, date in zip(cond_vals, dates):
		for ave in relevant_ave:
			if stn==ave[3] and date[2]==ave[2] and date[1]==ave[1]:
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
		if date[1] == 1 and SMI_daily_forecast[0]!=0:
			perf.append(gen[0] / SMI_daily_forecast[0])
		elif date[1] == 2 and SMI_daily_forecast[1]!=0:
			perf.append(gen[0] / SMI_daily_forecast[1])
		elif date[1] == 3 and SMI_daily_forecast[2]!=0:
			perf.append(gen[0] / SMI_daily_forecast[2])
		elif date[1] == 4 and SMI_daily_forecast[3]!=0:
			perf.append(gen[0] / SMI_daily_forecast[3])
		elif date[1] == 5 and SMI_daily_forecast[4]!=0:
			perf.append(gen[0] / SMI_daily_forecast[4])
		elif date[1] == 6 and SMI_daily_forecast[5]!=0:
			perf.append(gen[0] / SMI_daily_forecast[5])
		elif date[1] == 7 and SMI_daily_forecast[6]!=0:
			perf.append(gen[0] / SMI_daily_forecast[6])
		elif date[1] == 8 and SMI_daily_forecast[7]!=0:
			perf.append(gen[0] / SMI_daily_forecast[7])
		elif date[1] == 9 and SMI_daily_forecast[8]!=0:
			perf.append(gen[0] / SMI_daily_forecast[8])
		elif date[1] == 10 and SMI_daily_forecast[9]!=0:
			perf.append(gen[0] / SMI_daily_forecast[9])
		elif date[1] == 11 and SMI_daily_forecast[10]!=0:
			perf.append(gen[0] / SMI_daily_forecast[10])
		elif date[1] == 12 and SMI_daily_forecast[11]!=0:
			perf.append(gen[0] / SMI_daily_forecast[11])
		else:
			perf.append(0)
	return perf

# return total performance as average of daily performance
def get_ave_perf(daily_perf):
	count = 0
	total_perf = 0
	for perf in daily_perf:
		if perf == "":
			break
		else:
			total_perf += perf
			count += 1
	if count != 0:
		ave_perf = total_perf/count
		return ave_perf
	else:
		return None

# return count of number of days with 0 generation
def get_site_off(SMI_daily_gen):
	count = 0
	for gen in SMI_daily_gen:
		if gen[0] == 0 or gen[0] == "":
			count += 1
	return count

# convert performance to an adjusted performance value
def adjust_perf(SMI_daily_perf, solar_cond_vs_ave, slope, intercept, p_value, r_value):
	adjusted_result = []
	if (p_value < .1 and r_value*r_value>.5):
		for perf, weather in zip(SMI_daily_perf, solar_cond_vs_ave):
			if perf == 0:
				adjusted_result.append(0)
			elif (weather == 0):
				adjusted_result.append("")
			else:
				weather_diff = -(weather - 1)
				adjusted_perf = perf + slope*weather_diff
				adjusted_result.append(adjusted_perf)				

	if not adjusted_result:
		for i in range(0, len(SMI_daily_perf)):
			adjusted_result.append("")
	return adjusted_result

# create a list of blanks
def create_list_of_blanks(length):
	i = 0
	zero_list = []
	while i < length:
		zero_list.append("")
		i += 1
	return zero_list

def numbered_list(length):
	i = 1
	numbered_list = []
	while i < length+1:
		numbered_list.append(i)
		i+=1
	return numbered_list


##############################
#                            #
# USER INTERFACE HELPERS     #
#                            #
##############################

#######################
# User Class
#######################
class User(UserMixin):
	def __init__(self, id):
		self.id = id

	@property
	def user_id(self):
		return self.id

def get_user(user_id):
	return User(user_id)

@login_manager.user_loader
def load_user(user_id):
	user = get_user(user_id)
	return user	

def check_uid(uid):
	if uid == "origin":
		return True
	else:
		return False

def check_pw(uid,pw):
	if uid == "origin" and pw == ";":
		user = get_user(uid)
		login_user(user)
		return True
	else:
		return False
