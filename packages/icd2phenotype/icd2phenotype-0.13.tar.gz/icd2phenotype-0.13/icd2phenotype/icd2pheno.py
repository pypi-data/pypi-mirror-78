# import patient, lab, observation

from os import listdir
from os.path import isfile, join
import os
import pandas as pd
import json
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

## load data to memory
data_folder = os.path.dirname(__file__)+ '/res/'

x=os.getcwd()
onlyfiles = [f for f in listdir(data_folder) if (isfile(join(data_folder, f)) & ('.json' in f))]
varMapping = {}
for i in onlyfiles:
    f = None
    name =  i.split('.')[0]
    n = name

#     f = open('data.json',)
    exec('f=open(' + "'"+ data_folder + i+"'"+')' )
#     print(name +'=json.load('+ f+')')
    exec(name+' =json.load(f)')
    exec('f.close(' + ')' )
    varMapping[n] = name


# onlyfiles

var =[]
varNames = []
for key,val in (varMapping.items()):
    exec('var.append('+key+')')
    exec('varNames.append('+ "'"+ key +"'"+')')


def mapping(df,map_dic):
#     print(df)
    v1 = df.values
#     print(df[0])
    v2 = map_dic[df['index']]
#     print(v1)
#     print(v2)
    return bool(len(list(set(v1) & set(v2))))

# p.apply(mapping, args=(icd9_map_ahrq,), axis=0)

def icd2phenotype(icd, map_dic_name):
    map_dic=eval(map_dic_name)
    p = pd.DataFrame(columns = map_dic.keys())
    for v in p.columns.values:
        p[v] = icd
    pt = p.transpose().reset_index()
    d=pd.DataFrame(pt.apply(mapping, args=(map_dic,),axis=1)).transpose()
    d.columns = map_dic.keys()
    return d

def printrepos():
    return varNames

def getrepo(dic_name):
    return eval(dic_name)

def printphenotypes(dic_name):
    keys=[]
    for key,val in (eval(dic_name).items()):
        keys.append(key)
    return keys
