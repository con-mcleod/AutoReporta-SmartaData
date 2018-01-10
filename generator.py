#!/usr/bin/python3

import sys, csv, os, sqlite3, re
from openpyxl import Workbook
from openpyxl.formatting import Rule
from openpyxl.styles import Color, Font, PatternFill, Border, Alignment
from openpyxl.formatting.rule import ColorScaleRule, CellIsRule, FormulaRule
from openpyxl.utils import get_column_letter
from helper_fns import *


##############################
#                            #
# PROGRAM EXECUTION          #
#                            #
##############################

if (len(sys.argv) != 2):
	print ("Usage: python3 generator.py [output_file]")
	exit(1)

output_file = sys.argv[1]

if(os.path.exists(output_file)):
	os.remove(output_file)

##############################
#                            #
# store data in lists        #
#                            #
##############################

SMIs = get_all_SMIs()
dates = get_all_dates()

##############################
#                            #
# populate xlsx file         #
#                            #
##############################

wb = Workbook()
ws = wb.active
ws.title = "Daily Report"


# apply conditional format to % cells to flag under/overperforming
redFill = PatternFill(start_color='EE1111', end_color='EE1111', fill_type='solid')
greenFill = PatternFill(start_color='00FF00', end_color='00FF00', fill_type='solid')
for i in range(0,69*6, 6):
	to_format = get_column_letter(26+i)
	to_format = str(to_format) + "3:" + str(to_format) + "68"
	ws.conditional_formatting.add(to_format,CellIsRule(operator='lessThan', formula=['.8'], fill=redFill))
	ws.conditional_formatting.add(to_format,CellIsRule(operator='greaterThan', formula=['1.2'], fill=greenFill))

# bold the top row
bolded_font = Font(bold=True)
for i in range(1,439):
	ws.cell(row=1, column=i).font = bolded_font
	ws.cell(row=2, column=i).font = bolded_font

# merging top row and centering for clearer reading
ws.merge_cells('A1:L1')
ws.merge_cells('M1:X1')
for i in range(0,69*6, 6):
	merge_lhs = get_column_letter(25+i)
	merge_rhs = get_column_letter(25+i+5)
	to_merge = str(merge_lhs) + "1:" + str(merge_rhs) + "1"
	ws.merge_cells(to_merge)

for cell in ws['1:1']:
	cell.alignment = Alignment(horizontal='center')


# populate sheet
dates = get_all_dates()

row_count = 0
for SMI in SMIs:

	col_count = 0

	if (row_count == 0):
		ws.cell(row=row_count+1, column=col_count+1).value = "Salesforce Details"
		ws.cell(row=row_count+1, column=col_count+13).value = "Daily Forecast"

		ws.cell(row=row_count+2, column=col_count+1).value = "SMI"
		ws.cell(row=row_count+2, column=col_count+2).value = "Ref No"
		ws.cell(row=row_count+2, column=col_count+3).value = "ECS"
		ws.cell(row=row_count+2, column=col_count+4).value = "Installer"
		ws.cell(row=row_count+2, column=col_count+5).value = "PVsize"
		ws.cell(row=row_count+2, column=col_count+6).value = "Panel Brand"
		ws.cell(row=row_count+2, column=col_count+7).value = "Address"
		ws.cell(row=row_count+2, column=col_count+8).value = "State"
		ws.cell(row=row_count+2, column=col_count+9).value = "Site Status"
		ws.cell(row=row_count+2, column=col_count+10).value = "Install Date"
		ws.cell(row=row_count+2, column=col_count+11).value = "Supply Date"
		ws.cell(row=row_count+2, column=col_count+12).value = "Export Control"
		ws.cell(row=row_count+2, column=col_count+13).value = "Jan"
		ws.cell(row=row_count+2, column=col_count+14).value = "Feb"
		ws.cell(row=row_count+2, column=col_count+15).value = "Mar"
		ws.cell(row=row_count+2, column=col_count+16).value = "Apr"
		ws.cell(row=row_count+2, column=col_count+17).value = "May"
		ws.cell(row=row_count+2, column=col_count+18).value = "Jun"
		ws.cell(row=row_count+2, column=col_count+19).value = "Jul"
		ws.cell(row=row_count+2, column=col_count+20).value = "Aug"
		ws.cell(row=row_count+2, column=col_count+21).value = "Sep"
		ws.cell(row=row_count+2, column=col_count+22).value = "Oct"
		ws.cell(row=row_count+2, column=col_count+23).value = "Nov"
		ws.cell(row=row_count+2, column=col_count+24).value = "Dec"

		for date in dates:
			date = str(date)
			date = re.sub(r'(\(|\))', '', date)
			ws.cell(row=row_count+1, column=col_count+25).value = date
			ws.cell(row=row_count+2, column=col_count+25).value = "Actual Gen"
			ws.cell(row=row_count+2, column=col_count+26).value = "Curr Perf"
			ws.cell(row=row_count+2, column=col_count+27).value = "Solar Perf"
			ws.cell(row=row_count+2, column=col_count+28).value = "Temp Perf"
			ws.cell(row=row_count+2, column=col_count+29).value = "Rain Perf"
			ws.cell(row=row_count+2, column=col_count+30).value = "Adjusted Perf"
			col_count += 6

		row_count += 1

	else:

		SMI_details = get_SMI_details(SMI[0])
		SMI_monthly_forecast = get_SMI_forecast(SMI[0])
		SMI_daily_forecast = monthly_to_daily(SMI_monthly_forecast)
		SMI_state = get_SMI_state(SMI[0])[0][0]

		SMI_daily_gen = get_SMI_daily_gen(SMI[0])

		SMI_daily_perf = get_daily_perf(SMI, SMI_daily_gen, SMI_daily_forecast, dates)

		for x in range(0, len(SMI_details)):
			for detail in SMI_details[x]:
				ws.cell(row=row_count+1, column=col_count+1).value = detail
				col_count += 1

		for df in SMI_daily_forecast:
			ws.cell(row=row_count+1, column=col_count+1).value = df
			col_count += 1

		for y in range(0, len(SMI_daily_gen)):
			for gen in SMI_daily_gen[y]:
				ws.cell(row=row_count+1, column=col_count+1).value = gen

				ws.cell(row=row_count+1, column=col_count+2).number_format = '0.00%'
				ws.cell(row=row_count+1, column=col_count+2).value = SMI_daily_perf[y]

				ws.cell(row=row_count+1, column=col_count+3).value = None
				ws.cell(row=row_count+1, column=col_count+4).value = None
				ws.cell(row=row_count+1, column=col_count+5).value = None
				ws.cell(row=row_count+1, column=col_count+6).value = None

				col_count += 6


	row_count += 1

# Save the file
wb.save(output_file)
