import glob
import os
folders=os.listdir('/home/sai/Aish/Pivotchain/Data_Collection/garbage_data/')
for fold in folders:
	print(fold)
	imgs=glob.iglob(fold+'/*.jpg')
	xmls=glob.iglob(fold+'/*.xml')
	for img in imgs:
		if img.replace('jpg','xml') not in xmls:
			os.remove(img)#image


