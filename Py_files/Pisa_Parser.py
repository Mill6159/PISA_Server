# Can we parse the interface output?


import numpy as np
import io

filename='PISA_test.txt'

# data=np.loadtxt('PISA_test.txt',
# 	dtype={'names': ('1', '2','3','4','5','6','7','8','9','10','11','12'), 'formats': (str,np.float,np.float,np.float,np.float,np.float,np.float,np.float,np.float,np.float,np.float,np.float)},skiprows=0)
# print(data.head())

# data=[]

# with io.open(filename, mode="r", encoding="utf-8") as f:
#     for line in f:
#         # print(line.split())
#         data.append(line.split())

# print(data)

# n=0

# for i in data:
# 	print(i)
# 	n+=1
# 	if n==2:
# 		break
	# for j in i:
	# 	print(j)
	# 	n+=1
	# 	if n==2:
	# 		break



# data=np.loadtxt('PISA_test.txt', delimiter=' ',
# 	dtype={'names': ('1', '2','3','4','5','6','7','8','9','10','11','12'), 'formats': (str,np.float,str,str,str,np.float,np.float,np.float,np.float,np.float,str,str)})


data=np.genfromtxt(filename,dtype=None)

print(data[1])

n=0
atom_No=[]
for i in data:
	# print(i[0])
	# print(i[1])
	atom_No.append(str(i[0]) + str(i[1]))
	n+=1
	if n==2:
		break
	# for j in i:
	# 	print(j)
	# 	n+=1
	# 	if n==2:
	# 		break


print(atom_No)



