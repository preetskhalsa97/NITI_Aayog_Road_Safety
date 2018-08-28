file = open('without_blank_rows.csv','r')
lines = file.readlines()
file.close()
file = open('sane.csv','w')

for i in range(len(lines)):
	line = lines[i]
	try:
		line = line.strip()
	except:
		print (i)
		continue
	if (i==0):
		file.write(line+'\n')
		continue
	if (line == lines[i-1].strip()):
		continue
	file.write(line+'\n')

file.close()