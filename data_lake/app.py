#%%
from flask import Flask, request, jsonify
from get_data import *
from send_xml2db import *
from tqdm import tqdm
import time
import json
import pymongo
import numpy as np
import itertools
app = Flask(__name__) 


mongoclient=pymongo.MongoClient('mongodb://localhost:27017')
db = mongoclient["datalake"]
key_collection=db['keys']
state_collection=db['state']

# 'folder_list':glob.glob('Data/*/'),'count':len(glob.glob('Data/*/')),
# global folder_state


temp_location='/home/temp_location'

#required_labels={'GMR':['PER','AIRCRAFT','PBS','GPU'],'Adani':['person','truck'],'Tatapower':['person']}
@app.route('/ping',methods=['GET']) 
# ‘/’ URL is bound with hello_world() function. 
def ping(): 
    return jsonify({'ping': 'pong'})

#@app.route('/download_format',methods=['POST'])
#def download_format():
#	req_format=json.loads(request.data)['form']
#	if req_format=='pascalvoc':


@app.route('/query_Annotations',methods=['POST'])
def query_Annotations():
    print(type(request.data))
    required_labels=json.loads(request.data)

    print(required_labels)
    try:
        create_temp_location(temp_location)
        #Annots=list(map(lambda x: list(key_collection.find({
        #                            f"data.class.{x}":{'$exists':1}
         #                       })
          #                      ),required_labels))
        #df=pd.DataFrame(Annots)
        combined_annots=[]
        a=[]
        for client in required_labels.keys():
            #print(client)
            Annots=list(map(lambda x: list(key_collection.find({'$and':[
                                        {f"data.class.{x}":{'$exists':1}},{'location_map':{'$regex':client}
                                    }]})
                                    ),required_labels[client]))
            ann=list(itertools.chain.from_iterable(Annots))
            #print(ann)
            # Remove dulpicates
            #for i in tqdm(range(int(9e6))): 
                #pass
            ann=[i for n, i in enumerate(ann) if i not in ann[n + 1:]]
            combined_annots.extend(ann)
            print(len(ann))
            a.append(len(ann))

            #for i in tqdm(range(0,100)):
            #time.sleep(0.1)
            
            #print(ann[0])
        # Annots=list(key_collection.find())
        #print(combined_annots)
        print('converting to CSV')
        for i in a:
            #print(a[i])
            
            for j in tqdm(range(i)):
                time.sleep(0.1)

        # csv=convert_Pascal_VOC_format(combined_annots,temp_location,required_labels)
        csv=convert2yolo(combined_annots,temp_location,required_labels)
        
        get_imagesandCSV(temp_location)
        
        remove_temp_location(temp_location)

                
        return jsonify({'status': 1})
        
    except Exception as e:
        print(e)
        jsonify({'status': 0})

@app.route('/query_Annotations',methods=['POST'])
def query_Annotations():
    print(type(request.data))
    required_labels=json.loads(request.data)
    #annotation_type=json.loads(request.data)[1]
    #print(annotation_type['form'])

    #print(required_labels)
    try:
        create_temp_location(temp_location)
        #Annots=list(map(lambda x: list(key_collection.find({
        #                            f"data.class.{x}":{'$exists':1}
         #                       })
          #                      ),required_labels))
        #df=pd.DataFrame(Annots)
        combined_annots=[]
        a=[]
        for client in required_labels.keys():
            #print(client)
            Annots=list(map(lambda x: list(key_collection.find({'$and':[
                                        {f"data.class.{x}":{'$exists':1}},{'location_map':{'$regex':client}
                                    }]})
                                    ),required_labels[client]))
            ann=list(itertools.chain.from_iterable(Annots))
            #print(ann)
            # Remove dulpicates
            #for i in tqdm(range(int(9e6))): 
                #pass
            ann=[i for n, i in enumerate(ann) if i not in ann[n + 1:]]
            combined_annots.extend(ann)
            print(len(ann))
            a.append(len(ann))

            #for i in tqdm(range(0,100)):
            #time.sleep(0.1)
            
            #print(ann[0])
        # Annots=list(key_collection.find())
        #print(combined_annots)
        print('converting to CSV')
        for i in a:
            #print(a[i])
            
            for j in tqdm(range(i)):
                time.sleep(0.1)

        csv=convert_Pascal_VOC_format(combined_annots,temp_location,required_labels)
        #csv=convert2yolo(combined_annots,temp_location,required_labels)
        
        get_imagesandCSV(temp_location)
        
        remove_temp_location(temp_location)

                
        return jsonify({'status': 1})
        
    except Exception as e:
        print(e)
        jsonify({'status': 0})

@app.route('/update_data2db',methods=['POST'])
def update_data2db():
    folder_state={'state':'current'}
    state_collection.insert_one(folder_state)
    new_img_folders=check_new_entry(state_collection)
    next_number=get_next_number(key_collection)
    try:
        for folder in new_img_folders:

            # img_files=sorted(glob.glob(f'./Data/{folder}/*.jpg', recursive = True))
            #img_files=sorted(glob.glob(os.path.join(folder,'**/*.jpg'), recursive = True))
            xml_files=sorted(glob.glob(os.path.join(folder,'**/*.xml'), recursive = True))


            # Make keys for xml files#####
            img_dict=[]
            img_keys={}
            for xml in xml_files:
                #print(xml)
                #print(os.path.dirname(xml))
                data=xml_to_csv(xml)
                if len(data['class']) !=0 :
                    # print(data)
                    img_keys[f'frame_{next_number}.jpg']={}
                    img_keys[f'frame_{next_number}.jpg']={'filename':f'frame_{next_number}.jpg'}
                    img_keys[f'frame_{next_number}.jpg']['location_map']=xml.replace('xml','jpg')
                    img_keys[f'frame_{next_number}.jpg']['data']=data
                    #print(img_keys)
                    # shutil.copy(os.path.basename(xml))
                    img_dict.append(img_keys[f'frame_{next_number}.jpg'])
                    # key_collection.insert_one(img_keys[f'frame_{next_number}.jpg'])    
                    next_number+=1
                # break
            key_collection.insert_many(img_dict)
        #%%
        folder_state={'folder_list':glob.glob('Data/*/'),'count':len(glob.glob('Data/*/'))}
        state_collection.update_one({'state':'current'},{"$set":folder_state})
        
    except Exception as e:
        print(e)
        jsonify({'status': 0})
    return jsonify({'status': 1})

@app.route('/updated_clients',methods=['POST'])
def updated_clients():
    d=list(db.state.find({}))
    ab=pd.DataFrame(d)
    l=ab.iloc[0]['folder_list']
    clients=[]
    label_count=[]
    

    for i in l:
        a=i.split('/')
        clients.append(a[1].split('_')[0])
    #print(clients)
    for j in clients:
    	print(j)
    	d1=key_collection.find({'location_map':{'$regex':j}})

    	l=list(map(lambda x:list(x.keys()),d1.distinct('data.class')))

    	unique_labs=set(chain.from_iterable(l))
    	label_count.append(len(unique_labs))
    client_label_map=dict(zip(clients,label_count))
    client_label_list=[]
    for i in client_label_map.items():
    	client_label_list.append(i)
    print(client_label_list)
    new=[]
    for i in range(0,len(client_label_list)):
    	new.append({"Name":client_label_list[i][0],"label_count":client_label_list[i][1]})
    print(new)
    	
    	#clijsonify({"client_labels":[{"Name":i[0],"label_count":i[1]}]})
    


    #print(client_label_map.values())
    #print(client_label_map)
    
    	#new.append(json({"client_labels":[{"Name":i[0],"label_count":i[1]}]}))
    

    return jsonify({"client_labels":new})

    




#%%
@app.route('/unique_labels',methods=['POST'])
def unique_labels():
    client_labels=json.loads(request.data)['data']
    print(client_labels)
    # AA=key_collection.distinct('data.class')
    #d1=key_collection.find({'location_map':{'$regex':'GMR'}})
    d1=key_collection.find({'location_map':{'$regex':client_labels}})

    l=list(map(lambda x:list(x.keys()),d1.distinct('data.class')))
    unique_labs=set(list(chain.from_iterable(l)))
    # df=pd.DataFrame(l)
    # print(l)
    # unique_labs=pd.unique(df[np.arange(df.shape[1])].values.ravel('K'))
    print(unique_labs)
    return jsonify({'client_labels': list(unique_labs)})
    
    # Annots=list(map(lambda x: list(key_collection.find({
    #                                 f"data.class.{x}":{'$exists':1}
    #                             })
    #                             ),required_labels))

#%%
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True) 