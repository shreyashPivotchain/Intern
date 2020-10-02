#!/usr/bin/env python3

import os
import re
import subprocess
import pandas as pd

df1 = pd.read_csv('gas_cylinder_sheet.csv')

for i in range(0,df1.shape[0]):

    obj=df1.iloc[i].to_dict()
    try:
        f=obj['video_name'].split('.')
        fn=os.mkdir(f[0])
    except Exception as e:
        pass
    for j in range(1,5):
        try:
            if obj['t'+str(j)+'_start']:                
                start=obj['t'+str(j)+'_start']                                                               
                duration=obj['t'+str(j)+'_cut_duration']                                                                                          
                print('ffmpeg -y -ss {} -i {} -to {} -r 2 {}/{}_%06d.jpg'.format(start,i,duration,f[0],f[0]))                                     
                subprocess.call('ffmpeg -y -ss {} -i {} -to {} -r 2 {}/{}_%06d.jpg'.format(start,obj['video_name'],duration,f[0],f[0]),shell=True)
            
        except Exception as e:
        	print(e)



		
	
