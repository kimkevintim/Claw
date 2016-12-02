print "This simple program can extract AFLP data from \
the output file of Peak Scanner Software and remove \
coordinate of tank which in front of the sample name. \n"

'''
infile = raw_input('Enter input file name: \n')
print
tem_outfile = raw_input('Enter output file name which including file \
extension : <or press Enter to use defualt name "out_file.txt"> \n')
'''

inf = open('p5_d_G.out', 'r')
outf = open('out_file.txt', 'w')
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
	if line.count('Allelic matrix') == 1:
		data_range = 1
	elif line.count('Sample peak statistics') == 1:
		data_range = 2
	
	# block blank line, maybe can let user to input numbers of marker as len(pick)
	if data_range == 1:
		pick = line
		if len(pick) > 20:
		
			# get sample names
			sample = line[:21].strip()
			
			# remove coordinate of well 
			cut = 0
			for baseline in sample:
				cut += 1
				if baseline == '_': break
			sample = sample[cut:]
			# output sample name
			print sample,
			outf.write(sample)
			
			# get AFLP markers
			marker = line[22:]
			for loci in marker:
			
				# avoid \n in the end
				if loci == '1':
					print '\t' + loci,
					outf.write('\t' + loci)
				elif loci == '0':
					print '\t' + loci,
					outf.write('\t' + loci)
					
			# output AFLP markers
			print
			outf.write('\n')
			
	
	elif data_range == 2: break
	
		
inf.close()
outf.close()
