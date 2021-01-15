#%%
import os
import os.path as osp
import glob
import shutil
import pymongo
import pandas as pd
import itertools
from zipfile import ZipFile
import datetime
import subprocess
import traceback
from itertools import chain
#%%

def remove_temp_location(temp_location):
    shutil.rmtree(temp_location)

def create_temp_location(temp_location):
    if osp.exists(temp_location):
        shutil.rmtree(temp_location)
        os.mkdir(temp_location)
    else:
        os.mkdir(temp_location)


def get_imagesandCSV(temp_location):
    
    zipname='task_{}.tar.gz'.format(datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S"))
    Command = f"tar -czvf {zipname} {temp_location}"
    process = subprocess.Popen(Command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

#%%
def convert_Pascal_VOC_format(annotations,temp_location,required_labels):
    l=[]
    
    required_labels=set(list(chain.from_iterable(required_labels.values())))
    #a=list(required_labels)
    #print(a[0])

    copy_command=[]
    for annot in annotations:
        #print(annot)
        try:
            newname=annot['filename']
            #print(newname)

            ##########*************REPLACE WITH cp or rsync command**************############
            #source=annot['location_map']
            #des=(osp.join(temp_location,newname))
            #print(annot['location_map'])
            #print(osp.join(temp_location,newname))
            shutil.copy2(annot['location_map'],osp.join(temp_location,newname))
            #subprocess.run(['rsync', annot['location_map'] (osp.join(temp_location,newname))],shell=True)
            #subprocess.call(['cp', source des],shell=True)

            # os.rename(annot['location_map'],newname)
            
            # classes=list(annot['data']['class'].keys())
            # classes=required_labels
            for lab in required_labels:
                try:
                    cords=annot['data']['class'][lab]
                    print(len(cords))
                    for i in range(len(cords)):
                        
                        f_name=annot['filename']
                        w=annot['data']['width']
                        h=annot['data']['height']
                        print(w,h)
                        clas=lab
                       # c=annot['data']['client']
                        xmin,ymin,xmax,ymax=annot['data']['class'][lab][i].values()
                        l.append([f_name,w,h,clas,xmin,ymin,xmax,ymax])
                except Exception as e:
                    #print(e)
                    pass
                    #traceback.print_exc()

        except Exception as e:
            pass
            #print(e)
            #traceback.print_exc()s
            pass
                

    df=pd.DataFrame(l,columns=['filename','width','height','class','xmin','ymin','xmax','ymax'])
    df.to_csv(osp.join(temp_location,'csv_file.csv'),index=False)
    return df


def convert2yolo(annotations,temp_location,required_labels):
      

    required_labels=set(list(chain.from_iterable(required_labels.values())))
    
    labelmap={}
    for i,lab in enumerate(required_labels):
        #print(lab)
        labelmap[lab]=i
    #print(labelmap)

    for annot in annotations:
        
        try:
            newname=annot['filename']
            #print(newname)
            shutil.copy2(annot['location_map'],osp.join(temp_location,newname))

            

            l=[]
            for lab in required_labels:
                #print(lab)
                
                try:
                    cords=annot['data']['class'][lab]
                    #print(cords)
                    for i in range(len(cords)):
                        #print(annot)
                        


                           # for idx,d in annot[annot['filename']==fname].iterrows():
                                #print(idx)
                            #class_id=n
                        
                        w=annot['data']['width']
                        h=annot['data']['height']
                        #print('!!!!!!!!!!!!!!!',annot['data']['class'][lab][0]['xmin'])

                        wb=annot['data']['class'][lab][0]['xmax']-annot['data']['class'][lab][0]['xmin']
                        hb=annot['data']['class'][lab][0]['ymax']-annot['data']['class'][lab][0]['ymin']
                        
                        xc=annot['data']['class'][lab][0]['xmin']+wb/2
                        yc=annot['data']['class'][lab][0]['ymin']+hb/2


                        #print(w,h)
                        l.append([labelmap[lab],round(xc/w,6), round(yc/h,6),round(wb/annot['data']['width'],6),round(hb/annot['data']['height'],6)])
                    df=pd.DataFrame(l)
                        # df.to_csv(newname[:-3]+'txt',index=False,sep=' ',header=False)
                    df.to_csv(osp.join(temp_location,'{}.txt'.format(newname[:-4])),header=None,index=False)

                        #print(l)
         

                except Exception as e:
                    #traceback.print_exc()
                    pass


        except Exception as e:
            traceback.print_exc()
        #print(e)
            #traceback.print_exc()s
         
        # shutil.copy(annot['location_map'],osp.join(temp_location,newname))
    #df=pd.DataFrame(l)
    #print(df)
    #df.to_csv('/'+newname[:-3]+'txt',index=False,sep=' ',header=False)


                        
                    
    
    

                
                


        

                          



                  





    """for fname in data['filename'].unique():
        l=[]
        for idx,d in data[data['filename']==fname].iterrows():
            w=d['xmax']-d['xmin']
            h=d['ymax']-d['ymin']
            xc=d['xmin']+w/2
            yc=d['ymin']+h/2


            l.append([cls_id, round(xc/d['width'],6), round(yc/d['height'],6),round(w/d['width'],6),round(h/d['height'],6)])
        df=pd.DataFrame(l)
        shutil.copy('/data_lake/kotak_data_23dec/'+fname,'yolo/')
        df.to_csv('yolo/'+fname[:-3]+'txt',index=False,sep=' ',header=False)

if __name__==__main:
    data=pd.read_csv('file.csv')
    # all_imgs=data[data['class'].isin(['Explosion','Arson'])]"""


#%%
#query all the files which have these classes
if __name__=='__main__':
    mongoclient=pymongo.MongoClient('mongodb://localhost:27017')
    db = mongoclient["datalake"]
    key_collection=db['keys']

    required_labels=['person','PER']
    temp_location='temp_location'

    create_temp_location(temp_location)
    Annots=list(map(lambda x: list(key_collection.find({
                                f"data.class.{x}":{'$exists':1}
                            })
                            ),required_labels))
    ann=list(itertools.chain.from_iterable(Annots))
    ann=[i for n, i in enumerate(ann) if i not in ann[n + 1:]]
    # Annots=list(key_collection.find())
    print('converting to CSV')
    csv=convert_Pascal_VOC_format(ann,temp_location,required_labels)
    get_imagesandCSV(temp_location)
    remove_temp_location(temp_location)
