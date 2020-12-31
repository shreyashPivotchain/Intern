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

    copy_command=[]
    for annot in annotations:
        #print(annot)
        try:
            newname=annot['filename']

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
                    for i in range(len(cords)):
                        
                        f_name=annot['filename']
                        w=annot['data']['width']
                        h=annot['data']['height']
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
    df.to_csv(osp.join(temp_location,'csv_file'),index=False)
    return df


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
