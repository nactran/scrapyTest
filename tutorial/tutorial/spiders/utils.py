import json
import re
import jieba
import math

'''
Pre Process
'''

urlList = []
stopword = set()
with open('stopword.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        stopword.add(line.strip())

with open("items.json",'r') as load_f:
    load_dict = json.load(load_f)

'''
Url List Construction
'''
allEntry = {}
for item in load_dict:
    kwStr = item['keyword']
    desStr = item['description']
    if(kwStr):
        '''
        re.sub()
        '''
        if ('/' in kwStr and not(re.search('://',kwStr))):
            keywords = kwStr.split('/')
        elif('|' in kwStr):
            keywords = kwStr.split('|')
        elif('、' in kwStr):
            keywords = kwStr.split('、')
        elif('，' in kwStr):
            keywords = kwStr.split('，')
        else:
            keywords = kwStr.split(',')
        try:
            tempMap = map(lambda x : x.strip(),keywords)
            keywords = {} #keywords: a dictionary
            for word in tempMap:
                if word not in allEntry:
                    allEntry[word]=0
                    keywords[word] = 1
                elif word not in keywords:
                    keywords[word] = 1
                else:
                    keywords[word] += 1
                jieba.add_word(word) #网站自定义关键词加进字典，方便切description
            item['keyword'] = keywords
        except:
            pass
    else:
        item['keyword'] = {}

    if(desStr):
        cutList = jieba.lcut(desStr)
        for word in cutList:
            if not word is ' ' and not word in stopword:
                if word not in allEntry:
                     allEntry[word]=0
                     item['keyword'][word] = 1
                elif word not in item['keyword']:
                    item['keyword'][word] = 1
                else:
                    item['keyword'][word] += 1

    if(item['keyword']):
        urlList.append(item)
#print(allEntry)

'''
TF-IDF
'''

docNum = len(urlList)
for item in urlList:
    for word in allEntry.keys():
        if word in item['keyword']:
            allEntry[word] += 1

    tempDict = {}
    for key in item['keyword'].keys():
        tempDict[key] = float(item['keyword'][key]) /len(item['keyword'])
    item['keyword'] = tempDict


for item in urlList:
    tempDict = {}
    for word in item['keyword'].keys():
        idf = math.log(docNum/float(allEntry[word]))
        tf_idf = item['keyword'][word]*idf
        tempDict[word] = tf_idf
    item['keyword'] = tempDict
    #print(item['keyword'])

'''
VSM Construction
'''
for item in urlList:
    tempList = []
    for word in allEntry.keys():
        if word in item['keyword']:
            tempList.append(item['keyword'][word])
        else:
            tempList.append(0)
    item['vector'] = tempList
    print (item['vector'])



