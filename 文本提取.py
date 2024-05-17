import json
import os
import re

scnpath='scn_json\\'
filenames=os.listdir(scnpath)
for i in filenames:
    if 'resx' in i:
        filenames.remove(i)


out=[]
id=1
for file in filenames:
    json_file=open(scnpath+file,'r',encoding='utf8')
    json_file=json.load(json_file)

    if "scenes" not in json_file:
        continue
    scenes=json_file["scenes"]

    for scene in scenes:
        if 'texts' in scene:
            for text in scene['texts']:
                dic={}
                if text[0]!=None:
                    dic['name']=text[0]
                if text[1]!=None:
                    dic['message']=text[1][0][1]
                out.append(dic)

        if 'selects' in scene:
            for select in scene['selects']:
                dic={}
                dic['id']=id
                dic['message']=select['text']
                out.append(dic)
                id+=1

outfile=open('texts.json','w',encoding='utf8')
json.dump(out,outfile,ensure_ascii=False,indent=4)


namelist=[]
for i in out:
    #if 'name' in i:
    #    if i['name'] not in namelist:
    #        namelist.append(i['name'])
    if 'name' in i:
        if i['name'] not in namelist:
            namelist.append(i['name'])

json.dump(namelist,open('namelist.json','w',encoding='utf8'),ensure_ascii=False,indent=4)  
