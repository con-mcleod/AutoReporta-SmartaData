#!/usr/bin/python3

import sys, csv, sqlite3, os, glob, re, shutil, math
from collections import defaultdict
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from helper_fns import *

##############################
#                            #
# PROGRAM EXECUTION          #
#                            #
##############################

if (len(sys.argv) != 4):
	print ("Usage: python3 init.py [encompass_file.csv] [salesforce_file.csv] dataset.db")
	exit(1)

enc_dataset = sys.argv[1]
sf_dataset = sys.argv[2]
DATABASE = sys.argv[3]

##############################
#                            #
# SQL DATABASE CREATION      #
#                            #
##############################

if(os.path.exists(DATABASE)):
	os.remove(DATABASE)

connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()

cursor.execute("""CREATE TABLE enc_values(
	SMI varchar(10),
	datatype varchar(30), 
	obs_day int,
	obs_month int,
	obs_year int,
	value float
	)""")

cursor.execute("""CREATE TABLE SMI_details(
	SMI varchar(10),
	ref_no varchar(40),
	ECS varchar(150),
	installer varchar(60),
	PVsize float,
	panel_brand varchar(100),
	address varchar(150),
	state varchar(10),
	site_status varchar(80),
	install_date date,
	supply_date date,
	export_control int check(export_control in (0,1))
	)""")

cursor.execute("""CREATE table SMI_coords(
	SMI varchar(10),
	SMI_longitude float,
	SMI_latitude float
	)""")

cursor.execute("""CREATE TABLE forecast(
	SMI varchar(10) primary key,
	jan float,
	feb float,
	mar float,
	apr float,
	may float,
	jun float,
	jul float,
	aug float,
	sep float,
	oct float,
	nov float,
	dec float
	)""")

cursor.execute("""CREATE table BOM_ave(
	bom_location varchar(50),
	bom_month int,
	bom_year int,
	datatype varchar(20),
	average_val float
	)""")

cursor.execute("""CREATE table BOM_obs(
	bom_location varchar(50),
	bom_day int,
	bom_month int,
	bom_year int, 
	datatype varchar(10),
	obs_value float
	)""")

cursor.execute("""CREATE table BOM_coords(
	bom_location varchar(50),
	bom_longitude float,
	bom_latitude float
	)""")

cursor.execute("""CREATE table closest_stn(
	SMI varchar(10) primary key,
	weather_stn varchar (15),
	distance float
	)""")

##############################
#                            #
# READ IN ENCOMPASS REPORT   #
#                            #
##############################

row_count = 0
columns = defaultdict(list)
enc_SMIs = []
with open(enc_dataset,'r', encoding='utf-8') as enc_in:
	reader = csv.reader(enc_in)
	for row in reader:
		for (i,v) in enumerate(row):
			columns[i].append(v)
		row_count += 1

for col in columns:
	SMIs = re.findall(r'[a-zA-Z]{1}[0-9]{9}',columns[col][0])
	datatype = columns[col][0].split("- ")[-1]
	enc_dataset = columns[col][1:]
	dates = columns[0][1:]

	for SMI in SMIs:
		if SMI not in enc_SMIs:
			enc_SMIs.append(SMI)
		if (SMI and datatype == "kWh Generation"):
			for i in range(row_count-1):
				day = re.sub(r' .*', '', dates[i])
				month = re.sub(r'[^a-zA-Z]', '', dates[i])
				month_num = month_to_num(month)
				year = re.sub(r'.* ', '', dates[i])
				cursor.execute("""INSERT OR IGNORE INTO enc_values(SMI, datatype, 
					obs_day, obs_month, obs_year, value) VALUES (?,?,?,?,?,?)""", 
					(SMI, datatype, day, month_num, year, enc_dataset[i]))

##############################
#                            #
# READ IN SALESFORCE REPORT  #
#                            #
##############################

sf_rowCount = 0
with open(sf_dataset,'r', encoding='utf-8', errors='ignore') as sf_in:
	for row in csv.reader(sf_in, delimiter=','):
		if row[0] == '':
			break
		if row[0] ==  "SMI (No Check Sum)":
			continue
		for i in range(0,24):

			result = re.sub(r'\"', '', row[i])
			if i == 0:
				SMI = result
			elif i == 1:
				ref_no = result
			elif i == 2:
				ECS = result
			elif i == 3:
				installer = result
			elif i == 4:
				PVsize = result
			elif i == 5:
				panel_brand = result
			elif i == 6:
				address = result
			elif i == 7:
				state = result
			elif i == 8:
				jan = result
			elif i == 9:
				feb = result
			elif i == 10:
				mar = result
			elif i == 11:
				apr = result
			elif i == 12:
				may = result
			elif i == 13:
				jun = result
			elif i == 14:
				jul = result
			elif i == 15:
				aug = result
			elif i == 16:
				sep = result
			elif i == 17:
				octo = result
			elif i == 18:
				nov = result
			elif i == 19:
				dec = result
			elif i == 20:
				site_status = result
			elif i == 21:
				install_date = result
			elif i == 22:
				supply_date = result
			elif i == 23:
				export_control = result.rstrip()
				if export_control == "Yes":
					export_control = 1
				else:
					export_control = 0

		cursor.execute("""INSERT OR IGNORE INTO SMI_details(SMI, ref_no, ECS, installer, 
			PVsize, panel_brand, address, state, site_status, install_date, 
			supply_date, export_control) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""", 
			(SMI, ref_no, ECS, installer, PVsize, panel_brand, address, state, site_status, 
				install_date, supply_date, export_control))

		cursor.execute("""INSERT OR IGNORE INTO forecast(SMI, jan, feb, mar, apr, 
			may, jun, jul, aug, sep, oct, nov, dec) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
			(SMI, jan, feb, mar, apr, may, jun, jul, aug, sep, octo, nov, dec))

		sf_rowCount += 1

##############################
#                            #
# READ IN BOM DATA           #
#                            #
##############################

bom_folder = os.path.join("weather_data","*")
all_locations = []

for file in glob.glob(bom_folder):
	
	bom_location = re.sub(r'[0-9]+.*$','',file)
	bom_location = re.sub(r'^.*/','',bom_location)
	bom_datatype = re.sub(r'^.*[0-9]+','',file)
	bom_datatype = re.sub(r'\..*$','',bom_datatype)

	if bom_location not in all_locations:
		all_locations.append(bom_location)

	day = 0
	with open(file) as f:
		for row in f:
			row = re.sub(r'\s{2}', ',',row).rstrip()
			if (day == 0):
				year = int(re.sub(r'[^0-9]','',row))
			else:
				values = row.split(",")
				if (day <= 31):
					for i in range(1,13):
						cursor.execute("""INSERT OR IGNORE INTO bom_obs(bom_location, bom_day, bom_month, bom_year, datatype, obs_value)
							values (?,?,?,?,?,?)""", (bom_location, day, i, year, bom_datatype, values[i]))
			day += 1
			if (row[0:4] == 'Mean'):
				values = row.split(",")
				for i in range(1,13):
					cursor.execute("""INSERT OR IGNORE INTO bom_ave(bom_location, bom_month, bom_year, datatype, average_val)
							values (?,?,?,?,?)""", (bom_location, i, year, bom_datatype, values[i]))

##############################
#                            #
# COMMIT FILES TO DATABASE   #
#                            #
##############################

connection.commit()
connection.close()

##############################
#                            #
# GEOPY                      #
#                            #
##############################

connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()

for station in all_locations:
	geolocator = Nominatim()
	try:
		location = geolocator.geocode(station + ", Australia", timeout = 6)
		if location is not None:
			print (station, location.latitude, location.longitude)
			cursor.execute("""INSERT OR IGNORE INTO bom_coords(bom_location, bom_longitude, bom_latitude)
				values (?,?,?)""", (station, location.longitude, location.latitude))
	except GeocoderTimedOut as e:
		print ("Error: geocode failed on %s" % station)

for SMI in enc_SMIs:
	address = get_SMI_address(SMI)[0][0]
	geolocator = Nominatim()
	try:
		location = geolocator.geocode(address, timeout = 6)
		if location is not None:
			print (SMI, location.latitude, location.longitude)
			cursor.execute("""INSERT OR IGNORE INTO SMI_coords(SMI, SMI_longitude, SMI_latitude) 
				VALUES (?,?,?)""", (SMI, location.longitude, location.latitude))
	except GeocoderTimedOut as e:
		print ("Error: geocode failed on %s" % SMI)

##############################
#                            #
# COMMIT GEOPY TO DATABASE   #
#                            #
##############################

connection.commit()
connection.close()

##############################
#                            #
# NEAREST NEIGHBOUR          #
#                            #
##############################

connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()

for SMI in enc_SMIs:
	SMI_coords = get_SMI_coords(SMI)
	
	if SMI_coords:
		SMI_latitude = SMI_coords[0][0]
		SMI_longitude = SMI_coords[0][1]
		weather_stn = find_closest_stn(SMI, SMI_latitude, SMI_longitude)
		location = weather_stn[0][0]
		distance = math.sqrt(weather_stn[0][3])
		print (SMI, location, distance)
		cursor.execute("""INSERT OR IGNORE INTO closest_stn(SMI, weather_stn, distance) 
				VALUES (?,?,?)""", (SMI, location, distance))

##############################
#                            #
# COMMIT NEIGHBOUR TO DB     #
#                            #
##############################

connection.commit()
connection.close()
