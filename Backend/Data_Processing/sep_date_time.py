file = open('sane.csv', 'r')
lines = file.readlines()
file.close()
file = open('final_sane.csv','w')

first_line = lines[0].strip()
file.write(first_line+'\n')

for i in range(1,len(lines)):
	line = lines[i]
	try:
		line = line.strip()
	except:
		continue
	elements = line.split(',')
	for j in range(len(elements)-1):
		file.write(elements[j]+',')
	last_element = elements[len(elements)-1]
	#removing the Z
	last_element = last_element[0:len(last_element)-1]
	last_element  = last_element.replace('T',',')
	file.write(last_element+'\n')

file.close()