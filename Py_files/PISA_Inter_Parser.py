import numpy as np 
import sys
import os
import re
import subprocess

filename='pseudoDimer.txt'

N=5
# Method 1:
out=[]
with open(filename, "r") as f: # important to use with command when dealing with files
    counter = 0
    # print('File: %s' % filename)
    for line in f:
    	counter += 1
    	out.append(line)


'''
##########################################################################################
##########################################################################################

Remember entries are paired..
i.e. entry 1 goes with entry 2
3 with 4 and so on... but I built this into the design

Build a regular expression to extract "columns" from the PISA output
Group1=
Group2=
Group3=
Group4=
Group5=
Group6=
Group7=

Empties arrays to drop new "columns" into

(1) Sophisticated way

'''
g={}
for i in range(1,8):
	g['g{0}'.format(i)]=[]
# print(g['g1'])

'''
(2) Brute-force
'''

g1=[]
g2=[]
g3=[]
g4=[]
g5=[]
g6=[]
g7=[]
g8=[]
g9=[]

### Defining the regular expression
pattern_PISA = re.compile(r'([A-Z]{1}:)([A-Z]{3})\s([0-9]+)(\[[0-9A-Z\s]+\])\s*([A-Z0-9]*\.[0-9]*)\s*([A-Z]{1}:)([A-Z]{3})\s([0-9]+)(\[[0-9A-Z\s]+\])')

match_PISA = pattern_PISA.finditer(str(out))


for match in match_PISA:
    il,ij=match.span()[0],match.span()[1]
    PISA_entry=str(out)[il:ij]
    # print(PISA_entry) # return Chi^2 value from fit
    # group0=match.group(0)
    # print(group0)
    group1=match.group(1)
    g1.append(group1)
    g['g1'].append(group1)
    # print(group1)
    group2=match.group(2)
    g2.append(group2)
    # print(group2)
    group3=match.group(3)
    g3.append(group3)
    # print(group3)
    group4=match.group(4)
    g4.append(group4)
    # print(group4)
    group5=match.group(5)
    g5.append(group5)
    # print(group4)
    group6=match.group(6)
    g6.append(group6)
    # print(group4)
    group7=match.group(7)
    g7.append(group7)
    # print(group4)
    group8=match.group(8)
    g8.append(group8)
    # print(group4)
    group9=match.group(9)
    g9.append(group9)
    # print(group4)

# print('Length Group1 vs Group2: ', len(g1), len(g4))

# print(g1,g6)
# print(g3,g8)
# print(g['g1']) # sophisticated method

'''

Generating useful dataframes for import into PyMol Scripts


(1) Highlight interacting pairs indiscriminatingly 
'''

# intPairs=[]
# for i,j in zip(g3,g8):
# 	intPairs.append(i,j) # can't do this..

# print(intPairs)

g1_clean=[s.strip(':') for s in g1]
g6_clean=[s.strip(':') for s in g6]

# Build line by line
# First import comic style..
cmd=[]

# This command shows each residue in stick form
# kind of an ugly approach..

for i,j,w,z in zip(g1_clean,g3,g6_clean,g8):
	cmd.append('show sticks, chain %s and resi %s; show sticks, chain %s and resi %s;'%(str(i),str(j),str(w),str(z)))


# Generate a selection for each interface (d1/d2) to work with
# print(g3)
# print(" + ".join(g3))
seend1 = set()
resultd1 = []
for item in g3:
    if item not in seend1:
        seend1.add(item)
        resultd1.append(item)

# print(resultd1)

resi_list1="+".join(resultd1)
# resi_list1.replace(" ","")
# print(resi_list1)

cmd1=['select int_residues_%s, chain %s and resi %s'%(str(g1_clean[0]),str(g1_clean[0]),str(resi_list1))]
# print(cmd1)

# Other interface

# print(g8)
# print(" + ".join(g8))
seend2 = set()
resultd2 = []
for item in g8:
    if item not in seend2:
        seend2.add(item)
        resultd2.append(item)

# print(resultd2)

resi_list2="+".join(resultd2)
# resi_list2.replace(" ","")
# print(resi_list2)

cmd2=['select int_residues_%s, chain %s and resi %s'%(str(g6_clean[0]),str(g6_clean[0]),str(resi_list2))]
# print(cmd2)

# resi_list2=[]
# for i,j,w,z in zip(g1_clean,g3,g6_clean,g8):
# 	resi_list1.append('%s +'%j)
	# cmd1.append()
# print(resi_list1)

# print(cmd)

'''
Dump PyMol script into current working directory
'''

proc = subprocess.Popen(['pwd'], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
current_dir=str(out,'utf-8')



# outfileName1='Test.txt'
# file1Name=current_dir.rstrip()+'/'+outfileName1

# file1=open(file1Name,"w")
# file1.writelines(cmd) 
# file1.close()



outfileName2='Interface_Selection.txt'
file2Name=current_dir.rstrip()+'/'+outfileName2
cmd3 = [";".join(cmd1+cmd2)]
# print(cmd3)
cmd4=['select allInt_residues, int_residues_A + int_residues_B']
select_cmd = ";".join(cmd3+cmd4)
print(select_cmd)
file2=open(file2Name,"w")
file2.writelines(select_cmd) 
file2.close()




##########################################################################################
##########################################################################################