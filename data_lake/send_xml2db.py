#%%
import pymongo
import glob
import os
import shutil
import re
import xml.etree.ElementTree as ET


def xml_to_csv(xml_file):
    
    classes_names = []
    xml_list = []

    tree = ET.parse(xml_file)
    root = tree.getroot()
    width = int(root.find("size")[0].text)
    height = int(root.find("size")[1].text)
    d={'width':int(root.find("size")[0].text),
        'height':int(root.find("size")[1].text),
        'class':{}}
    #print(root.findall("object"))
    for member in root.iter("object"):
        classes_names.append(member.find('name').text)
        #print(member[1].text)
        for box in member.findall('bndbox'):
            
            if not member.find('name').text in d['class']:
                d['class'][member.find('name').text]=[]
            
            cords={'xmin':int(int(float(box.find("xmin").text))),
                'ymin':int(int(float(box.find("ymin").text))),
                'xmax':int(int(float(box.find("xmax").text))),
                'ymax':int(int(float(box.find("ymax").text)))}

            d['class'][member.find('name').text].append(cords)

    return d
#%%
def check_new_entry(state_collection):
    folders=set(glob.glob('Data/*/'))
    try:
        query=list(state_collection.find())[0]
        
        if 'folder_list' in query:
            folder_list=set(query['folder_list'])
        else:
            folder_list=set([])
        new_folders=folders.difference(folder_list)
        return list(new_folders)
    except:
        return []

#%%
# check last filename in keys collection
def get_next_number(key_collection):
    try:
        last_entry=list(key_collection.find())[-1]
        print(last_entry)
        # last_number=last_entry['filename']
        last_number=int(re.findall(r'\d+', last_entry['filename'])[0])
        print(last_number)
        next_number=last_number+1
    except:
        next_number=0
    return next_number

######Find all the new images and XMLs in the specified local directory 
#%%
# if __name__=='__main__':

#     mongoclient=pymongo.MongoClient('mongodb://localhost:27017')
#     db = mongoclient["datalake"]
#     key_collection=db['keys']
#     state_collection=db['state']

#     # 'folder_list':glob.glob('Data/*/'),'count':len(glob.glob('Data/*/')),
#     folder_state={'state':'current'}
#     state_collection.insert_one(folder_state)


#     new_img_folders=check_new_entry(state_collection)
#     next_number=get_next_number(key_collection)
#     for folder in new_img_folders:

#         # img_files=sorted(glob.glob(f'./Data/{folder}/*.jpg', recursive = True))
#         #img_files=sorted(glob.glob(os.path.join(folder,'**/*.jpg'), recursive = True))
#         xml_files=sorted(glob.glob(os.path.join(folder,'**/*.xml'), recursive = True))


#         # Make keys for xml files#####
#         img_dict=[]
#         img_keys={}
#         for xml in xml_files:
#             #print(xml)
#             #print(os.path.dirname(xml))
#             data=xml_to_csv(xml)
#             if len(data['class']) ==0:
#                 print(xml)
#             if len(data['class']) !=0 :
#                 # print(data)
#                 img_keys[f'frame_{next_number}.jpg']={}
#                 img_keys[f'frame_{next_number}.jpg']={'filename':f'frame_{next_number}.jpg'}
#                 img_keys[f'frame_{next_number}.jpg']['location_map']=xml.replace('xml','jpg')
#                 img_keys[f'frame_{next_number}.jpg']['data']=data
#                 #print(img_keys)
#                 # shutil.copy(os.path.basename(xml))
#                 img_dict.append(img_keys[f'frame_{next_number}.jpg'])
#                 # key_collection.insert_one(img_keys[f'frame_{next_number}.jpg'])    
#                 next_number+=1
#             # break

#         key_collection.insert_many(img_dict)

#     # Update Data Folder state in DB

#     # folder_list=glob.glob('Data/*/')
#     #%%
#     folder_state={'folder_list':glob.glob('Data/*/'),'count':len(glob.glob('Data/*/'))}
#     state_collection.update_one({'state':'current'},{"$set":folder_state})

