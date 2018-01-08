#!/usr/bin/python3

import sys, csv, os, sqlite3, re
import pandas as pd
import numpy as np
import xlsxwriter

from helper_fns import *
from constants import *

if(len(sys.argv) != 2):
	print ("Usage: python generator.py output.xlsx")
	exit (1)

output_file = sys.argv[1]

if(os.path.exists(output_file)):
	os.remove(output_file)

conn = sqlite3.connect(DATABASE)

days = get_all_days()
months = get_all_months()
report_period = get_all_daymonths()


sql_daily_query = """
SELECT distinct(o.smi), d.ref_no, d.ECS, d.installer, d.PVsize, d.panel_brand, d.address, d.state, d.site_status, d.install_date, d.supply_date, d.export_control,
		f.jan/31 as jan_daily, f.feb/28 as feb_daily, f.mar/31 as mar_daily, f.apr/30 as apr_daily, f.may/31 as may_daily, f.jun/30 as jun_daily, f.jul/31 as jul_daily, f.aug/31 as aug_daily, f.sep/30 as sep_daily, f.oct/31 as oct_daily, f.nov/30 as nov_daily, f.dec/31 as dec_daily, 
		o.obs_day, o.obs_month, sum(o.value) as kWh_Generated, sum(o.value)/(f.nov/30) as day_performance
from observation as o 
	join SMI_details as d
		on o.smi=d.smi
	join forecast as f
		on o.smi=f.smi
where o.datatype="kWh Generation"
group by o.smi, o.obs_day, o.obs_month
order by o.smi, o.obs_month
"""

SMIs = pd.read_sql(sql_daily_query, conn)

writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')
SMIs.to_excel(writer, sheet_name='AutoReporta')

workbook = writer.book
worksheet = writer.sheets['AutoReporta']

percent_fmt = workbook.add_format({'num_format': '0.0%'})
worksheet.set_column('AC:AC', 12, percent_fmt)

#underperforming
format1 = workbook.add_format({'bg_color': '#FFC7CE','font_color': '#9C0006'})
worksheet.conditional_format('AC2:AC2157', {'type': 'cell', 'criteria': '<=', 'value': .80, 'format': format1})
#overperforming
format2 = workbook.add_format({'bg_color': '#C6EFCE','font_color': '#006100'})
worksheet.conditional_format('AC2:AC2157', {'type': 'cell', 'criteria': '>=', 'value': 1.20, 'format': format2})

writer.save()