s = 'document.getElementById("0").onclick = function() {myFunction()};function myFunction(){popUp(driver_month[0],driver_month_freq[0]);}'
file = open('jugaad_file.txt','w')

for i in range(1, 27):
	s = 'document.getElementById("'+str(i)+'").onclick = function() {myFunction'+str(i)+'()};function myFunction'+str(i)+'(){popUp(driver_month['+str(i-1)+'],driver_month_freq['+str(i-1)+']);}'
	file.write(s+'\n')
file.close()