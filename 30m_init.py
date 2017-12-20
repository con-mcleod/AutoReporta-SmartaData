#!/usr/bin/python

import sys, csv, sqlite3, os, glob, re, shutil, codecs
from collections import defaultdict

if (len(sys.argv) != 4):
	print ("Usage: python3 init.py [encompass_file.csv] [salesforce_file.csv] dataset.db")
	exit(1)

enc_dataset = sys.argv[1]
sf_dataset = sys.argv[2]
DATABASE = sys.argv[3]

if(os.path.exists(DATABASE)):
	os.remove(DATABASE)

connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()



cursor.execute("""CREATE TABLE observation(
	SMI TEXT,
	datatype TEXT, 
	obs_time TEXT,
	obs_day INT,
	obs_month TEXT,
	obs_year INT,
	value FLOAT
	)""")

cursor.execute("""CREATE TABLE SMI_details(
	SMI TEXT,
	ref_no TEXT,
	ECS TEXT,
	installer TEXT,
	PVsize FLOAT,
	panel_brand TEXT,
	address TEXT,
	state TEXT,
	site_status TEXT,
	install_date DATE,
	supply_date DATE,
	export_control INTEGER
	)""")

cursor.execute("""CREATE TABLE forecast(
	SMI TEXT,
	jan FLOAT,
	feb FLOAT,
	mar FLOAT,
	apr FLOAT,
	may FLOAT,
	jun FLOAT,
	jul FLOAT,
	aug FLOAT,
	sep FLOAT,
	octo FLOAT,
	nov FLOAT,
	dec FLOAT
	)""")

SMIs = []
row_count = 0

# READ IN ENCOMPASS REPORT
# Note: this is hardcoded to fit a report using 60 minute intervals
# Todo: rewrite so that it can handle multiple report formats
columns = defaultdict(list)
with codecs.open(enc_dataset,'r', encoding='utf-8', errors='ignore') as enc_in:
	reader = csv.reader(enc_in)
	for row in reader:
		for (i,v) in enumerate(row):
			columns[i].append(v)
		row_count += 1

count = 0
for col in columns:

	SMIs = re.findall(r'[a-zA-Z]{1}[0-9]{9}',columns[col][0])
	data_type = columns[col][0].split("- ")[-1]
	enc_dataset = columns[col][1:]
	dates = columns[0][1:]
	times = columns[1][1:]

	for SMI in SMIs:
		if SMI:
			for i in range(row_count-1):
				day = re.sub(r'-.*', '', dates[i])
				month = re.sub(r'[^a-zA-Z]', '', dates[i])
				month_num = month_to_num(month)
				year = re.sub(r'.*-', '', dates[i])
				cursor.execute("""INSERT INTO observation(SMI, datatype, obs_time, obs_day, obs_month, obs_year, value)
					VALUES (?,?,?,?,?,?,?)""", (SMI, data_type, times[i], day, month_num, year, enc_dataset[i]))
	count += 1

sf_rowCount = 0


# READ IN "MONTHLY REPORT" SALESFORCE REPORT
# Note: this is hardcoded because the report structure does not change
# Todo: rewrite so that it can handle multiple report formats
with codecs.open(sf_dataset,'r', encoding='utf-8', errors='ignore') as sf_in:
	rows = sf_in.readlines()
	rows = rows[:-7]

	for row in rows:
		row = row.split(',')
		for i in range(0,24):
			result = re.sub(r'\"', '', row[i])

			if i == 0:
				SMI = result
				if SMI is None:
					SMI = ""
			elif i == 1:
				ref_no = result
				if ref_no is None:
					ref_no = ""
			elif i == 2:
				ECS = result
				if ECS is None:
					ECS = ""
			elif i == 3:
				installer = result
				if installer is None:
					installer = ""
			elif i == 4:
				PVsize = result
				if PVsize is None:
					PVsize = ""
			elif i == 5:
				panel_brand = result
				if panel_brand is None:
					panel_brand = ""
			elif i == 6:
				address = result
				if address is None:
					address = ""
			elif i == 7:
				state = result
				if state is None:
					state = ""
			elif i == 8:
				jan = result
				if jan is None:
					jan = ""
			elif i == 9:
				feb = result
				if feb is None:
					feb = ""
			elif i == 10:
				mar = result
				if mar is None:
					mar = ""
			elif i == 11:
				apr = result
				if apr is None:
					apr = ""
			elif i == 12:
				may = result
				if may is None:
					may = ""
			elif i == 13:
				jun = result
				if jun is None:
					jun = ""
			elif i == 14:
				jul = result
				if jul is None:
					jul = ""
			elif i == 15:
				aug = result
				if aug is None:
					aug = ""
			elif i == 16:
				sep = result
				if sep is None:
					sep = ""
			elif i == 17:
				octo = result
				if octo is None:
					octo = ""
			elif i == 18:
				nov = result
				if nov is None:
					nov = ""
			elif i == 19:
				dec = result
				if dec is None:
					dec = ""
			elif i == 20:
				site_status = result
				if site_status is None:
					site_status = ""
			elif i == 21:
				install_date = result
				if install_date is None:
					install_date = ""
			elif i == 22:
				supply_date = result
				if supply_date is None:
					supply_date = ""
			elif i == 23:
				export_control = result.rstrip()
				if export_control is None:
					export_control = ""

		cursor.execute("""INSERT OR IGNORE INTO SMI_details(SMI, ref_no, ECS, installer, 
			PVsize, panel_brand, address, state, site_status, install_date, 
			supply_date, export_control) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""", (SMI, ref_no, ECS, installer, PVsize, panel_brand, address, state, site_status, install_date, supply_date, export_control))

		cursor.execute("""INSERT OR IGNORE INTO forecast(SMI, jan, feb, mar, apr, 
			may, jun, jul, aug, sep, octo, nov, dec) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
			(SMI, jan, feb, mar, apr, may, jun, jul, aug, sep, octo, nov, dec))

		sf_rowCount += 1

connection.commit()
connection.close()
