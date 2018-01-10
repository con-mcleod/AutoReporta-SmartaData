#!/usr/bin/python3

import sys, csv, os, sqlite3, re
import numpy as np
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




######### 
#ws2
ws2 = wb.create_sheet()
ws2.title = "Summary Stats"

ws2.merge_cells('A1:G1')
ws2.merge_cells('H1:I1')

for cell in ws2['1:1']:
	cell.alignment = Alignment(horizontal='center')


########

# apply conditional format to % cells to flag under/overperforming
redFill = PatternFill(start_color='EE1111', end_color='EE1111', fill_type='solid')
greenFill = PatternFill(start_color='00FF00', end_color='00FF00', fill_type='solid')
for i in range(0,69*6, 6):
	to_format = get_column_letter(26+i)
	to_format = str(to_format) + "3:" + str(to_format) + "68"
	ws.conditional_formatting.add(to_format,CellIsRule(operator='lessThan', formula=['.7'], fill=redFill))
	ws.conditional_formatting.add(to_format,CellIsRule(operator='greaterThan', formula=['1.3'], fill=greenFill))

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


		#######
		# ws2 set up

		ws2.cell(row=row_count+1, column=col_count+1).value = "Salesforce Details"
		ws2.cell(row=row_count+1, column=col_count+8).value = "Summary Stats"

		for i in range(1,12):
			ws2.cell(row=1, column=i).font = bolded_font
			ws2.cell(row=2, column=i).font = bolded_font

		ws2.cell(row=row_count+2, column=col_count+1).value = "SMI"
		ws2.cell(row=row_count+2, column=col_count+2).value = "ECS"
		ws2.cell(row=row_count+2, column=col_count+3).value = "Address"
		ws2.cell(row=row_count+2, column=col_count+4).value = "State"
		ws2.cell(row=row_count+2, column=col_count+5).value = "Site Status"
		ws2.cell(row=row_count+2, column=col_count+6).value = "PV Size"
		ws2.cell(row=row_count+2, column=col_count+7).value = "Export Control"
		ws2.cell(row=row_count+2, column=col_count+8).value = "Performance for Period"
		ws2.cell(row=row_count+2, column=col_count+9).value = "Perf variance"
		ws2.cell(row=row_count+2, column=col_count+10).value = "Site off #days"

		##########

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

		average_perf = get_ave_perf(SMI_daily_perf)
		site_off_count = get_site_off(SMI_daily_gen)

		perf_variance = np.var(SMI_daily_perf)
		


#########
# populate summary stats page

		for detail in SMI_details:

			ws2.cell(row=row_count+1, column=col_count+1).value = detail[0]
			ws2.cell(row=row_count+1, column=col_count+2).value = detail[2]
			ws2.cell(row=row_count+1, column=col_count+3).value = detail[6]
			ws2.cell(row=row_count+1, column=col_count+4).value = detail[7]
			ws2.cell(row=row_count+1, column=col_count+5).value = detail[8]
			ws2.cell(row=row_count+1, column=col_count+6).value = detail[4]
			ws2.cell(row=row_count+1, column=col_count+7).value = detail[11]

			ws2.conditional_formatting.add('H3:H68',CellIsRule(operator='lessThan', formula=['.7'], fill=redFill))
			ws2.conditional_formatting.add('H3:H68',CellIsRule(operator='greaterThan', formula=['1.3'], fill=greenFill))

			ws2.conditional_formatting.add('I3:I68',CellIsRule(operator='greaterThan', formula=['.2'], fill=redFill))

			ws2.conditional_formatting.add('J3:J68',CellIsRule(operator='greaterThan', formula=['5'], fill=redFill))

			ws2.cell(row=row_count+1, column=col_count+8).number_format = '0.00%'
			ws2.cell(row=row_count+1, column=col_count+8).value = average_perf
			ws2.cell(row=row_count+1, column=col_count+9).number_format = '0.00%'
			ws2.cell(row=row_count+1, column=col_count+9).value = perf_variance
			ws2.cell(row=row_count+1, column=col_count+10).value = site_off_count
			
#########

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
