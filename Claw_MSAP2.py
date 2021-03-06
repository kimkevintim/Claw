# Python script
# This script used to "CLAW" MSAP binary data from file [*_d_B.out] which generated by tinyFLP.
#	Frist make mean size from "Polymorphic peaks" as loci name to creat header of list. 
#	Separate data from MspI and HpaII in "Allelic matrix" according to custom character at 
#	sample name, and form two list respectively.
#	And generate a matrix to show new type of MSAP data which can assign M+/H+, M+/H-, M-/H+
#	and	M-/H- to the character defined by yourself.
#
#
# Histroy
#	2017/10/11	Ver.1
#	2017/10/12	Ver.1.2	add threshold setting for minor allele frequency from new MSAP dataset
#	2017/11/23	Ver.2	remove MAF threshold and add methylation sensitive threshold (M/H error rate)
#	2017/11/24 	Ver.2.1 reinclud MAF threshold for non methylation sensitive loci (like AFLP)


import sys


input_file_name = sys.argv[1]
out_file_name = sys.argv[2]
out_file_type = "txt" # csv as , and txt as tab
Pname = "P05" # primer name
Ptype = "B" # primer name at "F"ront or "B"ack of sample name
c_MspI = "M" # character at sample name which represent sample digested by MspI
c_HpaII = "H" # by HpaII
threshold_er = 0.183 # threshold for methylation sensitive (M/H error rate)
threshold_nMS_MAF = 0.05

#	methylation sensitive locus
MpHp = "0" # character represent M+/H+
MpHn = "1" # M+/H-
MnHp = "1" # M-/H+
MnHn = "0" # M-/H-

#	non methylation sensitive locus
nMpHp = "1" # character represent M+/H+
nMpHn = "1" # M+/H-
nMnHp = "1" # M-/H+
nMnHn = "0" # M-/H-



#================================== Main: "claw" the binary data ==========================================
def select_data(x):
	if len(x) > 1:
		if "Polymorphic" in x[0] and "peaks" in x[1]: return 1 # get header also "mean width"
		if "Allelic" in x[0] and "matrix" in x[1]: return 2 # get data also "0101"
		if "Sample" in x[0] and "peak" in x[1] and "statistics" in x[2]: return 3 # time to break

data_range = 0
data_header = ["Ind"]
data_MspI = []
data_HpaII = []

inf = open( input_file_name, "r")
for line in inf:
	line = line.split()
	
	if select_data(line) != None:
		data_range = select_data(line)
		
	if data_range == 1 and len(line) > 3 and "cnt" not in line[0] and "." not in line[0]:
		o_loci_name = line[3]
		loci_name = Pname + "_" + o_loci_name[:5].replace(".","")
		data_header.append(loci_name)
	
	if data_range == 2 and len(line) == 2 and "matrix" not in line:
		sample_name = line[0] # get sample names
		if Ptype == "B": data_ind = [sample_name[4:-(len(Pname)+2)]] # remove coordinate of well 
		if Ptype == "F": data_ind = [sample_name[4+(len(Pname)+2):]]
		for locus in list(line[1]): data_ind.append(locus) # turn locus from string to list
		if c_MspI in sample_name[4:]: data_MspI.append(data_ind)	# indenitfy MspI 
		if c_HpaII in sample_name[4:]: data_HpaII.append(data_ind)	# indenitfy HpaII 

	if data_range == 3: break
inf.close()

import operator
data_MspI = sorted(data_MspI, key=operator.itemgetter(0))
data_HpaII = sorted(data_HpaII, key=operator.itemgetter(0))
data_MspI.insert(0, data_header)
data_HpaII.insert(0, data_header)
#_______________________________________________________________________________________________________




#===== cheak both dataset content same sample and equal numbers of loci ======
if len(data_MspI) == len(data_HpaII):
	for i in range(len(data_HpaII)-1):
		if data_MspI[i+1][0] != data_HpaII[i+1][0]:
			print("Samples are different between MspI and HpaII")
			print("MspI: "+data_MspI[i+1][0], "HpaII: "+data_HpaII[i+1][0])
else:
	print("Number of samples are not equal between MspI and HpaII")
	sys.exit()
	
for j in [data_MspI, data_HpaII]:
	for i in j:
		if len(i) != len(data_header):
			print("Number of loci are not equal between samples!!!!!")
			sys.exit()
#______________________________________________________________________________




#======== show numbers and names of locus and samples ========
print("\nFound " + str(len(data_HpaII)-1) + " samples:")
for i in range(len(data_HpaII)-1):
	print(data_HpaII[i+1][0] + "\t", end="")
print()

print("\nFound " + str(len(data_header)-1) + " loci:")
for i in range(len(data_header)-1):
	print(data_header[i+1] + "\t", end="")
print()
#_____________________________________________________________

	

	
	
#============== make lists of methylation sensitive and non sensitive locus position ==============
MspI_count_locus1 = ["M1N"]
for j in range(len(data_header)-1):
	count_1 = 0
	for i in range(len(data_MspI)-1):
		if data_MspI[i+1][j+1] == "1": count_1 += 1
	MspI_count_locus1.append(count_1)
	
HpaII_count_locus1 = ["H1N"]
for j in range(len(data_header)-1):
	count_1 = 0
	for i in range(len(data_HpaII)-1):
		if data_HpaII[i+1][j+1] == "1": count_1 += 1
	HpaII_count_locus1.append(count_1)

MS = ["MS"]	#methylation sensitive rate
for i in range(len(MspI_count_locus1)-1):
	MS.append(abs(MspI_count_locus1[i+1] + HpaII_count_locus1[i+1])/(len(data_MspI)-1))

#for i in range(len(MS)-1): print(data_header[i+1], round(MS[i+1], 4))
#print(MspI_count_locus1)
#print(HpaII_count_locus1)

MS_locus_position = [0]
nMS_locus_position = [0]
for i in range(len(MS)-1):
	if MS[i+1] > threshold_er: MS_locus_position.append(i+1)
	else: nMS_locus_position.append(i+1)
#print(MS_locus_position, len(MS_locus_position))
#print(nMS_locus_position, len(nMS_locus_position))
#__________________________________________________________________________________________________





#================== separate methylation sensitive and non sensitive loci into two lists =================
data_MS = []
for j in range(len(data_MspI)):
	data_MH_ind = []
	for i in MS_locus_position:
		if data_MspI[j][i] == "1" and data_HpaII[j][i] == "1": data_MH_ind.append(MpHp)
		elif data_MspI[j][i] == "1" and data_HpaII[j][i] == "0": data_MH_ind.append(MpHn)
		elif data_MspI[j][i] == "0" and data_HpaII[j][i] == "1": data_MH_ind.append(MnHp)
		elif data_MspI[j][i] == "0" and data_HpaII[j][i] == "0": data_MH_ind.append(MnHn)
		else: data_MH_ind.append(data_MspI[j][i])
	data_MS.append(data_MH_ind)

data_nMS = []
for j in range(len(data_MspI)):
	data_MH_ind = []
	for i in MS_locus_position:
		if data_MspI[j][i] == "1" and data_HpaII[j][i] == "1": data_MH_ind.append(nMpHp)
		elif data_MspI[j][i] == "1" and data_HpaII[j][i] == "0": data_MH_ind.append(nMpHn)
		elif data_MspI[j][i] == "0" and data_HpaII[j][i] == "1": data_MH_ind.append(nMnHp)
		elif data_MspI[j][i] == "0" and data_HpaII[j][i] == "0": data_MH_ind.append(nMnHn)
		else: data_MH_ind.append(data_HpaII[j][i])
	data_nMS.append(data_MH_ind)
#print(len(data_MS), data_MS[0])
#for i in range(len(data_MS)): print(len(data_MS[i]))
#print(data_MS[0])
#print(data_MS[1], len(data_MS[1]))
for j in [data_MS, data_nMS]:
	for i in j:
		if len(i) != len(j[0]):
			print("Number of loci are not equal between samples in stage 2!!!!!")
			sys.exit()
#_______________________________________________________________________________________________________
			




#=========================================== MAF threshold for nMS dataset ========================================
if threshold_nMS_MAF > 0:
	locus_out_AF = []
	AF_out_AF = []
	for j in range(len(data_nMS[0])-1):
		count_1 = 0
		for i in range(len(data_nMS)-1):
			if data_nMS[i+1][j+1] == "1" : count_1 += 1
		#print("0: " + str(count_0))
		#print("1: " + str(count_1))
		if count_1/(len(data_nMS)-1) <= threshold_nMS_MAF or count_1/(len(data_nMS)-1) >= 1-threshold_nMS_MAF: 
			locus_out_AF.append(data_nMS[0][j+1])
			AF_out_AF.append(count_1 / (len(data_nMS)-1))
			#print(data_MH[0][j+1], end="")
			#print(": " + str(count_0 / (len(data_MH)-1)))
	#print(locus_out_AF)

print("\nRemove " + str(len(locus_out_AF)) + \
" locus which allele frequency out of threshold " + str(threshold_nMS_MAF) + " from nMS daset:")
for i in range(len(locus_out_AF)):
	print("  " + locus_out_AF[i] + ": " + str(round(AF_out_AF[i], 3)))

for i in locus_out_AF:
	index_below_MAF = data_nMS[0].index(i)
	for j in range(len(data_nMS)): del data_nMS[j][index_below_MAF]
		#print (str(j+1) + " : " + str(index_below_MAF))

print("\nNew nMS dataset have formed by " + str(len(data_nMS[0])-1) + " locus")

for i in data_nMS:
	if len(i) != len(data_nMS[0]):
		print("Number of loci are not equal between samples in nMS after MAF threshold!!!!!")
		sys.exit()
#__________________________________________________________________________________________________________________




if out_file_type == "txt": out_type = "\t"
if out_file_type == "csv": out_type = ","

outf = open(out_file_name + '_MS.' + out_file_type, 'w')
for i in data_MS:
	j = out_type.join(i)
	outf.write(j + '\n')
outf.close()
print("\nOutputing... " + str(out_file_name) + "_MS." + out_file_type + "       DONE !!!")

outf = open(out_file_name + '_nMS.' + out_file_type, 'w')
for i in data_nMS:
	j = out_type.join(i)
	outf.write(j + '\n')
outf.close()
print("\nOutputing... " + str(out_file_name) + "_nMS." + out_file_type + "       DONE !!!")


