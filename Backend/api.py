from flask import Flask, jsonify
import pandas
from flask_cors import CORS

app=Flask(__name__) #app is a Flask object
CORS(app)

df = pandas.read_csv('final_sane.csv')

# @app.route('/driver_behaviour/<string:name>',methods=['GET'])
def driver_behaviour(name):
	"""
	name: name of the driver
	
	returns:
	avg_freq -- arr
	month -- arr
	"""

	df_driver = df.loc[df['deviceCode_deviceCode'] == int(name)]
	month2driving_days = dict()
	month2avg_freq = dict()
	month2days = dict()

	overall_driving_days = 0

	avg_freq = []
	months = []

	for i in range(0, len(df_driver)):
		row = df_driver.iloc[i]
		date = row['date']
		# print (type(date)) # string
		month = date.split('-')[1]
		day = date.split('-')[2]
		if (month not in month2driving_days):
			# we encounter a new month
			month2driving_days[month] = 0
			month2avg_freq[month] = 0
			month2days[month] = set()
		if (day not in month2days[month]):
			# we encounter a new day
			month2days[month].add(day)
			month2driving_days[month]+=1
		month2avg_freq[month]+=1

	for month in month2avg_freq:
		month2avg_freq[month] /= month2driving_days[month]
		overall_driving_days+=month2driving_days[month]
		months.append(month)
		avg_freq.append(month2avg_freq[month])

	months, avg_freq = zip(*sorted(zip(months, avg_freq)))
	data = {'months':months, 'avg_freq':avg_freq, 'overall_driving_days':overall_driving_days}
	# response = jsonify(data)
	# return response
	return data

@app.route('/driver',methods=['GET'])
def function_driver():
	"""
	var: kind of accidents

	returns:
	names_arr -- arr
	--> everything else: arr only
	overall
	FCW
	HMW
	Overspeed
	LDWL
	LDWR
	PCW
	UFCW
	"""
	names = dict()
	overall = []
	FCW = []
	HMW = []
	Overspeed = []
	LDWL = []
	LDWR = []
	PCW = []
	UFCW = []
	names_arr = []

	for i in range(len(df)):
		row = df.iloc[i]
		this_name = row['deviceCode_deviceCode']
		this_type = row['deviceCode_pyld_alarmType']

		if (this_name not in names):
			names[this_name] = dict()
			names[this_name]['FCW'] = 0
			names[this_name]['HMW'] = 0
			names[this_name]['Overspeed'] = 0
			names[this_name]['LDWL'] = 0
			names[this_name]['LDWR'] = 0
			names[this_name]['PCW'] = 0
			names[this_name]['UFCW'] = 0
			names[this_name]['overall'] = 0

		names[this_name]['overall']+=1
		names[this_name][this_type]+=1

	for name in names:
		names_arr.append(name)
		overall.append(names[name]['overall'])

	overall, names_arr = zip(*sorted(zip(overall, names_arr), reverse=True)) # descending order of overall
	overall = list(overall)
	names_arr = list(names_arr)
	for name in names_arr:
		FCW.append(names[name]['FCW'])
		HMW.append(names[name]['HMW'])
		Overspeed.append(names[name]['Overspeed'])
		LDWL.append(names[name]['LDWL'])
		LDWR.append(names[name]['LDWR'])
		PCW.append(names[name]['PCW'])
		UFCW.append(names[name]['UFCW'])

	driver_month = []
	driver_month_freq = []
	for i in range(len(names_arr)):
		name = names_arr[i]
		behaviour = driver_behaviour(name)
		driver_month.append(behaviour['months'])
		driver_month_freq.append(behaviour['avg_freq'])
		num_days = behaviour['overall_driving_days']
		# print (type(overall))
		# print (type(FCW))
		# print (type(overall[i]))
		# print (type(num_days))
		overall[i]/=num_days
		FCW[i]/=num_days
		HMW[i]/=num_days
		Overspeed[i]/=num_days
		LDWL[i]/=num_days
		LDWR[i]/=num_days
		PCW[i]/=num_days
		UFCW[i]/=num_days

	rank = []

	for i in range(1, len(names_arr)+1):
		rank.append(i)

	data = {'rank':rank,'driver_month':driver_month, 'driver_month_freq':driver_month_freq, 'names_arr':names_arr, 'overall':overall, 'FCW':FCW, 'HMW':HMW, 'Overspeed':Overspeed, 'LDWL':LDWL, 'LDWR':LDWR, 'PCW':PCW, 'UFCW':UFCW}
	response = jsonify(data)
	return response


@app.route('/area/<string:var>',methods=['GET'])
def function_area(var):
	"""
	var: "location#type_of_collision"
	type & location- either a name in the CSV or "all"

	returns:
	lati
	longi
	freq  -- arr
	areas -- arr
	index  -- 1,2,3,4...
	"""
	elements = var.split('[]')
	location = elements[0]
	type_of_collision = elements[1]

	lati = []
	longi = []
	freq = []
	area = []
	index = []

	final_df = None

	if (location == "all" and type_of_collision == "all"):
		final_df = df

	elif (location == "all"):
		final_df = df.loc[df['deviceCode_pyld_alarmType'] == type_of_collision]

	elif (type_of_collision == "all"):
		final_df = df.loc[df['deviceCode_location_wardName'] == location]

	else:
		final_df = df.loc[df['deviceCode_location_wardName'] == location]
		final_df = final_df.loc[final_df['deviceCode_pyld_alarmType'] == type_of_collision]

	area_dict = dict() # area->freq
	# now we have final_df
	for i in range(len(final_df)):

		row = final_df.iloc[i]
		this_lati = row['deviceCode_location_latitude']
		this_longi = row['deviceCode_location_longitude']
		lati.append(this_lati)
		longi.append(this_longi)
		this_area = row['deviceCode_location_wardName']
		if (this_area not in area_dict):
			area_dict[this_area] = 0
		area_dict[this_area]+=1

	for unique_area in area_dict:
		area.append(unique_area)
		freq.append(area_dict[unique_area])

	for i in range(1, len(area)+1):
		index.append(i)

	freq, area = zip(*sorted(zip(freq,area), reverse=True))

	data = {'lati':lati, 'longi':longi, 'area':area, 'freq':freq, 'index':index}
	response = jsonify(data)

	return response

if __name__=='__main__':
	app.run(debug=True)