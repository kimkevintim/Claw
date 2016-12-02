print "This simple program can extract AFLP data from \
the output file of Peak Scanner Software and remove \
coordinate of tank which in front of the sample name. \n"

'''
infile = raw_input('Enter input file name: \n')
print
tem_outfile = raw_input('Enter output file name which including file \
extension : <or press Enter to use defualt name "out_file.txt"> \n')
'''
import math
import xlwt
wb = xlwt.Workbook()
ws = wb.add_sheet('Polymorphic peaks')
i = 0
j = 0

inf = open('p5_d_G.out', 'r')
#inf = open(infile, 'r')
'''
if tem_outfile == '':
	outf = open('out_file.txt', 'w')
else:
	outf = open(outfile, 'w')
'''

data_range = 0

while True:
	line = inf.readline()
	
	# select the area of AFLP data 
	if line.count('Polymorphic peaks') == 1:
		data_range = 1
	elif line.count('Allelic matrix') == 1:
		data_range = 2
	
	# block blank line, maybe can let user to input numbers of marker as len(pick)
	if data_range == 1:
		pick = line
		#print pick.find('-') == -1
		if len(pick) > 20 and pick.find('-') == -1:
		
			cnt = line[:5].strip()
			#print cnt
			if cnt == '.': continue
			print cnt
			ws.write(i, 0, cnt)
			
			cnt = line[6:15].strip()
			print '\t' + cnt,
			if j == 0: ws.write(i, 1, cnt)
			elif j > 0: ws.write(i, 1, round(float(cnt), 1))
			
			cnt = line[16:27].strip()
			print '\t' + cnt,
			ws.write(i, 2, cnt)
			
			cnt = line[28:39].strip()
			print '\t' + cnt,
			ws.write(i, 3, cnt[:5].replace('.',''))
			
			cnt = line[40:51].strip()
			print '\t' + cnt,
			ws.write(i, 4, cnt)
			
			cnt = line[52:63].strip()
			print '\t' + cnt,
			ws.write(i, 5, cnt)
			
			cnt = line[64:75].strip()
			print '\t' + cnt,
			ws.write(i, 6, cnt)
			
			cnt = line[76:87].strip()
			print '\t' + cnt,
			ws.write(i, 7, cnt)
			
			cnt = line[88:99].strip()
			print '\t' + cnt,
			ws.write(i, 8, cnt)
			
			cnt = line[100:111].strip()
			print '\t' + cnt,
			ws.write(i, 9, cnt)
			
			cnt = line[112:].strip()
			print '\t' + cnt
			ws.write(i, 10, cnt)
	
	
			i += 1
			j += 1
			
	elif data_range == 2: break
	
wb.save('peak_xlwt.xls')
	
inf.close()

