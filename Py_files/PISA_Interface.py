#########################################################
#########################################################
# Basic Description:
#
#
#
#
#########################################################
#########################################################
# Module Imports

import numpy as np 
import sys
import os
import re
import subprocess

from matplotlib import pyplot as plt

#########################################################
#########################################################
# Basic functions

def barPlot(X, width=1, plotlabel='',savelabel='',
             xlabel='', ylabel='NOT PROVIDED', plotColor='#E55334'):
    '''
    Make Histogram plot
    Y:
    X:
    Removed xlow/xhigh variables in function definition

    '''
    plt.rc('axes', linewidth=2)
    plt.rc('lines', markeredgewidth=2)
    plt.rc('font', **{'sans-serif': ['Helvetica']})
    fig = plt.figure(figsize=(15, 12.5))  # set figure dimensions
    ax1 = fig.add_subplot(1, 1, 1)  # allows us to build more complex plots
    for tick in ax1.xaxis.get_major_ticks():
        tick.label1.set_fontsize(20)  # scale for publication needs
        tick.label1.set_fontname('Helvetica')
    for tick in ax1.yaxis.get_major_ticks():
        tick.label1.set_fontsize(20)  # scale for publication needs
        tick.label1.set_fontname('Helvetica')
    plt.ylabel(ylabel, size=22)
    plt.xlabel(xlabel, size=22)
    labels, counts = np.unique(X, return_counts=True)
    plt.bar(labels, counts,align='center',color=plotColor,edgecolor='black',linewidth=1.5,
        width=width,label=plotlabel)
    # plt.bar(X, bins=bins, label=plotlabel,
    #      color=plotColor,edgecolor='black',linewidth=1.5, align='mid')
    # plt.hist(X, bins=bins, range=(xlow,xhigh), label=plotlabel,
    #          color=plotColor)  # best to use HTML color codes: https://htmlcolorcodes.com
    plt.legend(numpoints=1, fontsize=18, loc='best')
    fig.tight_layout()
    plt.savefig(savelabel + '.png', format='png',
                bbox_inches='tight', dpi=300)
    plt.show()

#########################################################
#########################################################

# Input PISA Interfaces as txt file

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
#########################################################
#########################################################

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


# print(g1,g6) # chain label
# print(g2,g7) # residue letter codes
# print(g3,g8) # residue number

# print(g['g1']) # sophisticated method

'''
Clean up chain label for downstream processing
'''
g1_clean=[s.strip(':') for s in g1]
g6_clean=[s.strip(':') for s in g6]

#########################################################
#########################################################

'''
Output general interface information
(1) List of interaction pairs (including duplicates)

'''
pair_array=[]
print('--> List of interacting pairs:')
for i,j,k,w,x,z in zip(g1_clean,g2,g3,g6_clean,g7,g8):
    print('Residue %s-%s from chain %s interacts with Residue %s-%s from chain %s'%(str(j),str(k),str(i),str(x),str(z),str(w)))
    pair_array.append('Residue %s-%s from chain %s interacts with Residue %s-%s from chain %s \n'%(str(j),str(k),str(i),str(x),str(z),str(w)))

proc = subprocess.Popen(['pwd'], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
current_dir=str(out,'utf-8')

List_Interacting_Pairs='List_Interacting_Pairs.txt'
List_Interacting_Pairs_Name=current_dir.rstrip()+'/'+List_Interacting_Pairs

List_Interacting_Pairs_File=open(List_Interacting_Pairs_Name,"w")
List_Interacting_Pairs_File.writelines(pair_array)
List_Interacting_Pairs_File.close()

'''
Distribution of interacting pairs
In this case AB=BA
i.e ARG-GLU==GLU-ARG and is converted accordingly..
'''
dist_data=[]
for i,j in zip(g2,g7):
    dist_data.append('%s-%s'%(str(i),str(j)))

dist_data_mod = [sub.replace('ARG-GLU','GLU-ARG') for sub in dist_data] 
dist_data_mod = [sub.replace('ARG-ASP','ASP-ARG') for sub in dist_data_mod] 
dist_data_mod = [sub.replace('LYS-GLU','GLU-LYS') for sub in dist_data_mod] 
dist_data_mod = [sub.replace('TYR-GLU','TYR-ARG') for sub in dist_data_mod] 
dist_set = set(dist_data_mod) # number of unique occurences


# histPlot(X=dist_data,bins=len(dist_set),plotlabel='Interface Residues Distribution',
#     savelabel='PISA_Int_Residue_Distribution',xlabel='Interacting Pairs',ylabel='Frequency (counts)')

barPlot(X=dist_data_mod, width=1, plotlabel='Interface Residue Distribution',
    savelabel='PISA_Int_Residue_Distribution',xlabel='Interacting Pairs',ylabel='Frequency (counts)')

#########################################################
#########################################################

'''

Generating useful dataframes for import into PyMol Scripts


(1) Highlight interacting pairs indiscriminatingly 
'''

# Build line by line
# First import comic style..
cmd=[]

# This command shows each residue in stick form
# kind of an ugly approach..

for i,j,w,z in zip(g1_clean,g3,g6_clean,g8):
	cmd.append('show sticks, chain %s and resi %s; show sticks, chain %s and resi %s;'%(str(i),str(j),str(w),str(z)))


# Generate a selection for each interface (d1/d2) to work with

seend1 = set()
resultd1 = []
for item in g3:
    if item not in seend1:
        seend1.add(item)
        resultd1.append(item)

resi_list1="+".join(resultd1)

cmd1=['select int_residues_%s, chain %s and resi %s'%(str(g1_clean[0]),str(g1_clean[0]),str(resi_list1))]

## Other interface

seend2 = set()
resultd2 = []
for item in g8:
    if item not in seend2:
        seend2.add(item)
        resultd2.append(item)


resi_list2="+".join(resultd2)

cmd2=['select int_residues_%s, chain %s and resi %s'%(str(g6_clean[0]),str(g6_clean[0]),str(resi_list2))]

'''
Dump PyMol script into current working directory
(1) Generate full path to current directory with input text file is located
(2) Generate a .txt file at that location that contains:
(3a) Script for select both interfaces individually and as a group
(3b) '' + shows the interface at orange sticks!
(3c) '' + '' + shows each unit at a surface with transparency = 0.5
(3d) ..... + calculates hydrogen bonds between interfaces
'''

## General Pymol formatting

cmd_comic_p1 = ['set antialias = 1 ; set ambient=0.3 ; set direct=1.0 ; set ribbon_radius =0.2 ; set cartoon_highlight_color =grey50 ; set ray_trace_mode=1 ; set stick_radius = 0.2 ; set mesh_radius = 0.02 ; hide lines ; set cartoon_tube_radius, 0.2 ; set cartoon_fancy_helices=1 ; set cartoon_cylindrical_helices=0 ; set cartoon_flat_sheets = 1.0 ; set cartoon_smooth_loops = 0']
cmd_comic_p2 =['set_color maarine=  [0.3, 0.8, 1.0] ; set_color graay=[0.8,0.8,0.8] ; set_color greeen=[0.0,0.5,0.0] ; set_color cyaan=[0.19,1.0,1.0] ; set_color oraange=[1.0,0.5043103448,0.03448275862] ; set_color piink=[1.0,0.2594339623,0.4622641509] ; set_color darkbluue=[0.2923976608,0.4444444444,1.0] ; set_color Lgreeen=[0,1.0,0.09130434783] ; set_color reed=[1.0,0.2130434783,0.0] ;']
cmd_comic = ";".join(cmd_comic_p1 + cmd_comic_p2)

## Step (1)

proc = subprocess.Popen(['pwd'], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
current_dir=str(out,'utf-8')

outfileName2='Interface_Selection.txt'
file2Name=current_dir.rstrip()+'/'+outfileName2
cmd3 = [";".join(cmd1+cmd2)]
# print(cmd3)
cmd4=['select allInt_residues, int_residues_%s + int_residues_%s ; '%(str(g1_clean[0]),str(g6_clean[0]))]
select_cmd = ";".join(cmd3+cmd4)
# print(select_cmd)

## Step (2/3)

file2=open(file2Name,"w")
file2.writelines(cmd_comic)
file2.writelines(select_cmd) 
file2.close()

## (3b)

outfileName3='Interface_Sticks_and_Surface.txt'
file3Name=current_dir.rstrip()+'/'+outfileName3

sticksSurface_cmd = 'color cyaan, chain %s ; color maarine, chain %s ; flag ignore, allInt_residues, set ; show sticks, allInt_residues ;util.cbao allInt_residues ; show surface'%(str(g1_clean[0]),str(g6_clean[0]))

file3=open(file3Name,"w")
file3.writelines(cmd_comic)
file3.writelines(select_cmd) 
file3.writelines(sticksSurface_cmd)
file3.close()

## (3c)

## (3d)

h_cmd = 'h_add int_residues_%s ; h_add int_residues_%s ; '%(str(g1_clean[0]),str(g6_clean[0]))
h_cmd = h_cmd + 'select don, allInt_residues and (elem n,o) ; '
h_cmd = h_cmd + 'select acc, allInt_residues and (elem o or (elem n and not (neighbor hydro))) ; '
h_cmd = h_cmd + 'dist HBA, (int_residues_%s and acc),(int_residues_%s and don), 3.2 ; '%(str(g1_clean[0]),str(g6_clean[0]))
h_cmd = [h_cmd]
h_cmd = ";".join([sticksSurface_cmd] + h_cmd)


outfileName4='Interface_SticksSurfaceHbonds.txt'
file4Name=current_dir.rstrip()+'/'+outfileName4

file4=open(file4Name,"w")
file4.writelines(cmd_comic)
file4.writelines(select_cmd) 
file4.writelines(h_cmd)
file4.close()


#########################################################
#########################################################
#########################################################
#########################################################