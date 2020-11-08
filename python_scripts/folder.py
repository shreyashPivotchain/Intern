 


import os 
import shutil 

 
path = '/home/sai/docs'

l = os.listdir(path) 


for i in l: 
	name, ext = os.path.splitext(i) #used to split pathname 
	print(name)

	print(ext)
	ext = ext[1:] 

	print(ext)
 
	if ext == '': 
		continue

	 
	if os.path.exists(path+'/'+ext): 
		shutil.move(path+'/'+i, path+'/'+ext+'/'+i) 

	 
	else: 
		os.makedirs(path+'/'+ext) 
		shutil.move(path+'/'+i, path+'/'+ext+'/'+i) 
