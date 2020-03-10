# Python script
#	This script used to process output file "*_d_B.out" from tinyFLP.
#	Primary generate binary data from [Allelic matrix] and use mean size from [Polymorphic peaks] as loci name.
#	And estimate error rate when repeat sample included.
#	Also calculate ambiguous loci in each repeats, make it easier to choose which repeat as formal data.
#	If error rate seen too high, we also calculate ambiguous loci cross sample.
#	To reveal whcih loci seen more "ambiguous", and can be remove by Black list. 
#
# Histroy
#	2017/09/20	Ver.4	introduce Black list
#	2017/08/11	Ver.3	


input_file_name = 'P07M_with3rep'	# without "_d_B.out"
#out_file_name = 'P07M'
Pname = "P06H"	# primer name
Ptype = "B" # primer name at 'F'ront or 'B'ack of sample
RepID = '_r'	# replicate identifier, if sample included these characters would be treated as repead
Black = ['2461_P06H', '3758_P06H', '4792_P06H', '2100_P06H']
#Black = []


inf = open( input_file_name + '_d_B.out', 'r')

# ============================= Functions ============================= #
def select_data(line_in):
	if 'Polymorphic peaks' in line_in:  # get header also 'mean width'
		return 1
	if 'Allelic matrix' in line_in:  # get data also '0101'
		return 2
	if 'Sample peak statistics' in line_in:  # time to break
		return 3

def get_header(line):
	header = line[3]
	#print header
	return header[:5].replace('.','') + "_" + Pname  # remove space and append primer name
# _____________________________ Functions _____________________________ #





# ========================== Main founction of Claw =========================== #
#	select 0/1 data, adjusted sample name and position of peaks as loci name	#
data_range = 0
data = []
data_rep = []
data_header = ['Sample']

for line_in in inf:
	line = line_in.split()
	#print line

	# ~~~~ selection different kinds of data ~~~~ #
	if select_data(line_in) != None:
		data_range = select_data(line_in)
		#print data_range

	# ~~~~ build header ~~~~ #
	if data_range == 1 and len(line) > 3 and "cnt" not in line:
		#print line
		data_header.append(get_header(line))
		#print data_header

	# ~~~~ grap sample name and 0101 data ~~~~ #
	if data_range == 2 and len(line) == 2 and "matrix" not in line:
		#print line
		data_ind = []
		sample = line[0] # get sample names
		if Ptype == 'B': data_ind.append(sample[4:-(len(Pname)+1)]) # remove coordinate of well 
		if Ptype == 'F': data_ind.append(sample[4+(len(Pname)+1):])
		#print data_ind
		for locus in list(line[1]): # turn locus from string to list
			data_ind.append(locus)
		#print data_ind
		if "_r" in data_ind[0]: data_rep.append(data_ind)
		else: data.append(data_ind)

	if data_range == 3: break

inf.close()

import operator
data_rank = sorted(data, key=operator.itemgetter(0))
data_rep_rank = sorted(data_rep, key=operator.itemgetter(0))
data_rank.insert(0, data_header)
data_rep_rank.insert(0, data_header)
#print data_header
#print data_rank
#print data_header
#print sample
# __________________________ Main founction of Claw ___________________________ #





# =============  Data visualization for check by eye  ============= #
number_repeat = 3
j = 0
print
print 'Found ' + str(len(data_rank)-1) + ' samples:'
for i in data_rank[1:] : 
	print(i[0]),
	j+=1
	print '\t',
print
print
print 'Found ' + str(len(data_rep_rank)-1) + ' samples for error rate estimation:'
for i in data_rep_rank[1:] : 
	print(i[0]),
	j+=1
	if j % number_repeat == 0: print
	else: print ',',
print

j = 0
print 'Found ' + str(len(data_header)-1) + ' locus:'
print '  ',
for i in data_header[1:]:
	print(i),
	j+=1
	if j == len(data_header)-1: print
	else: print ',',
print
# ______________ Data visualization for check by eye ______________ #





# ======================== Black list ======================== #

if len(Black) > 1:
	print '\n# # # # # # # # # # # # #'
	print '#   Black list in use   #'
	print '# # # # # # # # # # # # #'
	print '\nLocus: ' + ', '.join(Black) + \
			'\n removed from error estimation\n\n'

	for i in Black:
		j = 0
		rem = data_rep_rank[0].index(i)
		while j < len(data_rep_rank): 
			del data_rep_rank[j][rem]
			j += 1

# ======================== Black list ======================== #






# =================== estimation for error rate =================== #
three_repeat = []
temp = []
i = 1
j = 1
l = 0
re_loci_count = [0,0,0]
number_of_er_perloci = []
error_loci = 0
temp_re_loci_count = 0
while j < len(data_rep_rank[i]):
	while i < (len(data_rep_rank)):
		temp.append(data_rep_rank[i][j])
		i += 1
		if (i-1) % 3 == 0:
			if temp.count('1') == 2:
				error_loci += 1
				for k in temp:
					if k == '0': re_loci_count[l] += 1
					l += 1
				l = 0
			if temp.count('0') == 2:
				error_loci += 1
				for k in temp:
					if k == '1': re_loci_count[l] += 1
					l += 1
				l = 0
			temp =[]
			
		if (i-1) % 36 == 0:
			#print temp_re_loci_count 
			#print error_loci
			number_of_er_perloci.append(error_loci - temp_re_loci_count) 
			temp_re_loci_count = error_loci
			
		#print temp
			#print temp
		#print temp
	i = 1
	#three_repeat.append(temp)
	#temp = []
	j += 1

Nsample = float(len(data_rep_rank)-1)
Nloci = (len(data_rep_rank[0])-1)
error_rate = float(error_loci) / (Nsample * Nloci)

print str(error_loci) +' ambiguous loci across repeats from same samples have been found\
 at total '+ str(int(Nsample * Nloci)) + ' peaks'
print '  Error rate =',
print '%.2f%%' % (error_loci / (Nsample * Nloci)*100)
print

# ~~~~~~~~~~~~~~~~~ print Error rate relivet values ~~~~~~~~~~~~~~~~~#
print 'Number of ambiguous loci content at each repeats: '
for i in re_loci_count:
	l += 1
	print '  ' + str(i) + ' in repeat_' + str(l)
#print number_of_er_perloci
print '\n'+'Number of sample content ambiguous loci at each locus:'
m = 0
good_loci = 0
for i in number_of_er_perloci:
	if i > 0:
		print '  Loci_' + str(m+1) + ' ' + str(data_rep_rank[0][m+1]) +': ' \
		+ str(i)
	if i == 0: good_loci += 1
	m += 1
print '\n  ' + str(good_loci) + ' locus without any ambiguous loci'


# ___________________ estimation for error rate ___________________ #



'''
# ==================== data output ==================== #
outf = open(out_file_name + '.tsv', 'w')
for i in data_rank:
	k = '\t'.join([str(j) for j in i])
	outf.write(k+'\n')
outf.close()
print
print 'Output Binary dataset: ' + str(out_filename) + '.tsv'
# ____________________ data output ____________________ #
'''




print '\n\n Done !!'