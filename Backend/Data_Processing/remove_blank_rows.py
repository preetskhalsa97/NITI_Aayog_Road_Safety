file = open('bangalore-cas-alerts.csv' ,'r')
lines = file.readlines()
file.close()
file = open('without_blank_rows.csv','w')

for line in lines:
	try:
		line = line.strip()
		file.write(line+'\n')
	except:
		continue

file.close()