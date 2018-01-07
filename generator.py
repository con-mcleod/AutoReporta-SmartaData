#!/usr/bin/python3

import sys, csv, os, sqlite3, re
import pandas as pd
import numpy as np

from helper_fns import *
from constants import *


if(len(sys.argv) != 2):
	print ("Usage: python3 generator.py output.xlsx")
	exit (1)

output_file = sys.argv[1]

if(os.path.exists(output_file)):
	os.remove(output_file)

conn = sqlite3.connect(DATABASE)

days = get_all_days()
months = get_all_months()
report_period = get_all_daymonths()


sql_daily_query = """
SELECT distinct(o.smi), d.ref_no, d.ECS, d.installer, d.PVsize, d.panel_brand, d.address, d.state, d.site_status, d.install_date, d.supply_date, d.export_control, f.jan/31, f.feb/28, f.mar/31, f.apr/30, f.may/31, f.jun/30, f.jul/31, f.aug/31, f.sep/30, f.oct/31, f.nov/30, f.dec/31, o.obs_day, o.obs_month, sum(o.value)
from observation as o 
	join SMI_details as d
		on o.smi=d.smi
	join forecast as f
		on o.smi=f.smi
where o.datatype="kWh Generation" and o.obs_day=%s
group by o.smi, o.obs_day, o.obs_month
""" % days[0]

SMIs = pd.read_sql(sql_daily_query, conn)

SMIs.to_excel('output.xlsx', sheet_name='Sheet1')