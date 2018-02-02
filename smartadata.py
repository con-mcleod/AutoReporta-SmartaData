#!/usr/bin/python3

from flask import Flask, render_template, session, redirect, request, url_for, send_file
from flask_login import current_user, login_required, logout_user, LoginManager
from helper_fns import *
from server import app
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn import linear_model
import io
import base64



########################
#      LOGIN PAGE      #
########################
@app.route('/', methods=['GET','POST'])
def login():
	error = None
	notLogged = True
	if request.method == "POST":
		uid = request.form["uid"]
		pw = request.form["pw"]
		if "login" in request.form:
			if check_uid(uid):
				if check_pw(uid,pw):
					return redirect(url_for('dashboard'))
				else:
					error = "Invalid password!"
			else:
				error = "Invalid User ID!"
	return render_template('login.html', error=error, notLogged=notLogged)

########################
#    DASHBOARD PAGE    #
########################
@app.route('/dashboard', methods=['GET', 'POST'])
# @login_required
def dashboard():
	# uid = current_user.user_id
	if request.method == "POST":
		if "bom_grab" in request.form:
			return redirect(url_for('bom_grabber'))
		elif "run_reports" in request.form:
			return redirect(url_for('reports_dash'))
		elif "fleet_manager" in request.form:
			return redirect(url_for('fleet_manager'))

	return render_template('dashboard.html')

########################
#   BOM GRABBER PAGE   #
########################
@app.route('/bom_grabber', methods=['GET', 'POST'])
# @login_required
def bom_grabber():
	# uid = current_user.user_id
	if request.method == "POST":
		if "bom_script" in request.form:
			return redirect(url_for('bom_grabber'))
		elif "dashboard" in request.form:
			return redirect(url_for('dashboard'))

	return render_template('bom_grabber.html')

########################
#    FLEET MANAGER     #
########################
@app.route('/fleet_manager', methods=['GET', 'POST'])
# @login_required
def fleet_manager():

	fleet = get_entire_fleet()

	if request.method == "POST":
		if "dashboard" in request.form:
			return redirect(url_for('dashboard'))
		for SMI in fleet:
			if SMI[0] in request.form:
				return redirect(url_for('SMI_dash', SMI=SMI[0]))
			elif (SMI[0] + "_cases") in request.form:
				return redirect(url_for('SMI_cases', SMI=SMI[0]))

	return render_template('fleet_manager.html', fleet=fleet)


########################
#     REPORT DASH      #
########################
@app.route('/reports_dash', methods=['GET', 'POST'])
# @login_required
def reports_dash():
	# uid = current_user.user_id
	SMIs = get_all_SMIs()
	dates = get_all_dates()
	SMIs_unadjusted = []
	SMIs_adjusted = []
	SMIs_off_days = []
	SMIs_perf_var = []
	SMIs_closest_stn = []
	SMIs_stn_distance = []

	for SMI in SMIs:
		SMI_monthly_forecast = get_SMI_forecast(SMI[0])
		SMI_daily_forecast = monthly_to_daily(SMI_monthly_forecast)
		SMI_daily_gen = get_SMI_daily_gen(SMI[0])
		SMI_daily_perf = get_daily_perf(SMI, SMI_daily_gen, SMI_daily_forecast, dates)
		average_perf = '{:.2%}'.format(get_ave_perf(SMI_daily_perf))
		site_off_count = get_site_off(SMI_daily_gen)
		perf_variance = '{:.2%}'.format(np.var(SMI_daily_perf))
		
		stn_checker = get_SMI_weather_stn(SMI[0])

		if (stn_checker):

			SMI_weather_stn = get_SMI_weather_stn(SMI[0])[0][0]

			stn_solar_perf = get_stn_solar_perf(SMI_weather_stn, "solar")
			stn_temp_perf = get_stn_solar_perf(SMI_weather_stn, "temp")
			relevant_solar_perf = filter_weather(stn_solar_perf, dates)
			relevant_temp_perf = filter_weather(stn_temp_perf, dates)

			solar_vals = get_weather_vals(relevant_solar_perf, len(dates))
			temp_vals = get_weather_vals(relevant_temp_perf, len(dates))

			average_solar = get_ave_condition(SMI_weather_stn, "solar")
			relevant_ave_solar = filter_ave(average_solar, dates)
			solar_cond_vs_ave = compare_cond_to_ave(solar_vals, dates, SMI_weather_stn, relevant_ave_solar)
			solar_correlation = np.corrcoef(SMI_daily_perf, solar_cond_vs_ave)
			closest_weather_stn = get_closest_stn(SMI)[0][0]
			# 1.60934 is converting mile to km
			SMI_stn_distance = int(1.60934*get_SMI_stn_dist(SMI)[0][0])

			temp_effect = get_temp_effect(temp_vals)

			temp_adjusted = temp_adjust(SMI_daily_perf, temp_effect)

			perf_x = np.array(temp_adjusted)
			solar_y = np.array(solar_cond_vs_ave)

			if not all(val==0 for val in perf_x):
				sol_slope, sol_intercept, sol_r_value, sol_p_value, sol_std_err = stats.linregress(perf_x, solar_y)
				sol_adjusted_perf = adjust_perf(temp_adjusted, solar_cond_vs_ave, sol_slope, sol_intercept, sol_p_value, sol_r_value)
				ave_adjusted = get_ave_perf(sol_adjusted_perf)
				if ave_adjusted is not None:
					ave_adjusted = '{:.2%}'.format(ave_adjusted)
				elif ave_adjusted is None:
					ave_adjusted = ""
		else:
			ave_adjusted = ""
			solar_correlation = [["",""]]
			sol_adjusted_perf = create_list_of_blanks(len(dates))
			solar_cond_vs_ave = create_list_of_blanks(len(dates))
			temp_effect = create_list_of_blanks(len(dates))

		SMIs_unadjusted.append(average_perf)
		SMIs_adjusted.append(ave_adjusted)
		SMIs_off_days.append(site_off_count)
		SMIs_perf_var.append(perf_variance)
		SMIs_closest_stn.append(closest_weather_stn)
		SMIs_stn_distance.append(SMI_stn_distance)


	SMIs_stats = zip(SMIs, SMIs_unadjusted, SMIs_adjusted, SMIs_off_days, SMIs_perf_var, SMIs_closest_stn, SMIs_stn_distance)

	if request.method == "POST":
		if "dashboard" in request.form:
			return redirect(url_for('dashboard'))
		for SMI in SMIs:
			if SMI[0] in request.form:
				return redirect(url_for('SMI_dash', SMI=SMI[0]))

	return render_template('reports_dash.html', SMIs_stats=SMIs_stats)

########################
#       SMI DASH       #
########################
@app.route('/SMI_dash_<SMI>', methods=['GET', 'POST'])
# @login_required
def SMI_dash(SMI):

	
	dates = get_all_dates()
	SMI_monthly_forecast = get_SMI_forecast(SMI)
	SMI_daily_forecast = monthly_to_daily(SMI_monthly_forecast)
	SMI_daily_forecast_ints = []
	for fc in SMI_daily_forecast:
		fc = '{0:.2f}'.format(fc)
		SMI_daily_forecast_ints.append(fc)
	SMI_daily_gen = get_SMI_daily_gen(SMI)
	if (SMI_daily_gen):
		SMI_daily_perf = get_daily_perf(SMI, SMI_daily_gen, SMI_daily_forecast, dates)
		average_perf = '{:.2%}'.format(get_ave_perf(SMI_daily_perf))
		site_off_count = get_site_off(SMI_daily_gen)
		perf_variance = '{:.2%}'.format(np.var(SMI_daily_perf))
		
		stn_checker = get_SMI_weather_stn(SMI)

		if (stn_checker):

			SMI_weather_stn = get_SMI_weather_stn(SMI)[0][0]
			stn_solar_perf = get_stn_solar_perf(SMI_weather_stn, "solar")
			stn_temp_perf = get_stn_solar_perf(SMI_weather_stn, "temp")
			relevant_solar_perf = filter_weather(stn_solar_perf, dates)
			relevant_temp_perf = filter_weather(stn_temp_perf, dates)

			solar_vals = get_weather_vals(relevant_solar_perf, len(dates))
			temp_vals = get_weather_vals(relevant_temp_perf, len(dates))

			average_solar = get_ave_condition(SMI_weather_stn, "solar")
			relevant_ave_solar = filter_ave(average_solar, dates)
			solar_cond_vs_ave = compare_cond_to_ave(solar_vals, dates, SMI_weather_stn, relevant_ave_solar)
			solar_correlation = np.corrcoef(SMI_daily_perf, solar_cond_vs_ave)
			closest_weather_stn = get_closest_stn2(SMI)[0][0]

			# 1.60934 is converting mile to km
			SMI_stn_distance = int(1.60934*get_SMI_stn_dist2(SMI)[0][0])

			temp_effect = get_temp_effect(temp_vals)

			temp_adjusted = temp_adjust(SMI_daily_perf, temp_effect)

			perf_x = np.array(temp_adjusted)
			solar_y = np.array(solar_cond_vs_ave)

			if not all(val==0 for val in perf_x):
				sol_slope, sol_intercept, sol_r_value, sol_p_value, sol_std_err = stats.linregress(perf_x, solar_y)
				sol_adjusted_perf = adjust_perf(temp_adjusted, solar_cond_vs_ave, sol_slope, sol_intercept, sol_p_value, sol_r_value)
				ave_adjusted = get_ave_perf(sol_adjusted_perf)
		else:
			ave_adjusted = ""
			solar_correlation = [["",""]]
			sol_adjusted_perf = create_list_of_blanks(len(dates))
			solar_cond_vs_ave = create_list_of_blanks(len(dates))
			temp_effect = create_list_of_blanks(len(dates))

		img = io.BytesIO()

		y = sol_adjusted_perf
		x = numbered_list(len(sol_adjusted_perf))
		plt.plot(x,y)
		plt.savefig(img, format='png')
		img.seek(0)

		plot_url = base64.b64encode(img.getvalue()).decode()

	else:
		plot_url = None
	img2 = io.BytesIO()
	y2 = SMI_daily_forecast_ints
	x2 = numbered_list(len(SMI_daily_forecast_ints))
	plt.plot(x2,y2)
	# plt.
	plt.savefig(img2, format='png')
	img2.seek(0)

	plot_url2 = base64.b64encode(img2.getvalue()).decode()

	if request.method == "POST":
		if "dashboard" in request.form:
			return redirect(url_for('dashboard'))

	return render_template('smi_dash.html', df=SMI_daily_forecast_ints, plot_url=plot_url, plot_url2=plot_url2)

########################
#    SMI CASES DASH    #
########################
@app.route('/<SMI>_cases', methods=['GET', 'POST'])
# @login_required
def SMI_cases(SMI):

	if request.method == "POST":
		if "dashboard" in request.form:
			return redirect(url_for('dashboard'))
	return render_template('smi_cases.html')