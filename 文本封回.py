import json
import os
import re
import sys

scnpath='scn_json\\'
outpath='scn_json_out\\'

filenames=os.listdir(scnpath)
for i in filenames:
    if 'resx' in i:
        filenames.remove(i)

def chuli(text):
    if text=='' or text=='　':
        return ''
    if text[0]=='「':
        text=text[1:]
    if text[-1]=='」':
        text=text[:-1]
    return text

yiwen=open('yiwen.json','r',encoding='utf8')
yiwen=json.load(yiwen)
namedic=json.load(open('namedic.json','r',encoding='utf8'))


transdic={}
transdic_dn={}
for dic in yiwen:
    transdic[dic["pre_jp"]]=dic["post_zh_preview"]
    transdic_dn[dic["pre_jp"].replace('\\n','')]=dic["post_zh_preview"].replace('\\n','')
transdic.update(namedic)

def deln(text):
    text=re.sub('\[[^\[]*\]','',text)
    text=text.replace('\\n','')
    text=re.sub("n.{7};",'',text)
    text=re.sub("n.{6};",'',text)
    return text

def trans(t,deln=False):
    global transdic
    t=chuli(t)
    t=t.replace('　','')
    t=re.sub('\[[^\[]*\]','',t)
    texts_=re.split('\%|;',t)
    texts=[]
    for i in range(len(texts_)):
        if i%2:
            continue
        texts.append(texts_[i])
    for i in texts:
        if i=='':
            continue
        try:
            if i not in t:
                raise KeyError
            t=t.replace(i,transdic[i])
        except KeyError:
            print(i)
    return t
i=1
for file in filenames:
    percentage = round(i / len(filenames) * 100)
    print(f"\r进度: {i}/{len(filenames)}: ", "▓" * (percentage // 2), end="")
    sys.stdout.flush()

    json_file=open(scnpath+file,'r',encoding='utf8')
    json_file=json.load(json_file)

    if "scenes" not in json_file:
        continue
        
    outfile=open(outpath+file,'w',encoding='utf8')
    
    for scene_id in range(len(json_file['scenes'])):
        if "texts" in json_file['scenes'][scene_id]:
            for text_id in range(len(json_file['scenes'][scene_id]["texts"])):
                text=json_file['scenes'][scene_id]["texts"][text_id]
                if text[0]!=None:
                    json_file['scenes'][scene_id]["texts"][text_id][0]=trans(json_file['scenes'][scene_id]["texts"][text_id][0])
                if text[1]!=None:
                    json_file['scenes'][scene_id]["texts"][text_id][1]=trans(json_file['scenes'][scene_id]["texts"][text_id][1])
                json_file['scenes'][scene_id]["texts"][text_id][2]=trans(json_file['scenes'][scene_id]["texts"][text_id][2])

                if type(text[-2])==type(''):
                    json_file['scenes'][scene_id]["texts"][text_id][-2]=deln(json_file['scenes'][scene_id]["texts"][text_id][2])
                if type(text[-1])==type(''):
                    json_file['scenes'][scene_id]["texts"][text_id][-1]=deln(json_file['scenes'][scene_id]["texts"][text_id][2])

        if 'selects' in json_file['scenes'][scene_id]: 
            for sel_id in range(len(json_file['scenes'][scene_id]['selects'])):
                json_file['scenes'][scene_id]['selects'][sel_id]["text"]=trans(json_file['scenes'][scene_id]['selects'][sel_id]["text"])

    json.dump(json_file,outfile,ensure_ascii=False,indent=4)
    outfile.close()


    os.system(f'PsBuild.exe -p krkr {outpath+file}')
    file_=file.replace('.json','')
    os.system(f'ren {file_}.pure.scn {file_}.scn')
    os.system(f'move {file_}.scn patch\\')
    i+=1

