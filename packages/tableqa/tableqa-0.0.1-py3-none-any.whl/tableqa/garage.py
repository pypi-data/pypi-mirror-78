# # #!/usr/bin/env python3
# # # -*- coding: utf-8 -*-
# # """
# # Created on Tue Aug 25 05:36:54 2020

# # @author: abhijithneilabraham
# # """

# from data_utils import data_utils
# import os
# import pandas as pd
# import nltk
# import json
# data_process=data_utils("cleaned_data","schema")
# schema_dir=""
# data_dir="cleaned_data"
# from nltk.corpus import wordnet 
# from nltk.stem import PorterStemmer 
# ps = PorterStemmer().stem 
# syns = wordnet.synsets
# # a=syns(ps("Male"))
# # s=list(set([i.lemmas()[0].name().lower() for i in  a]))
# # print(s)
# def get_schema_for_csv(csv_path):    
#     data=data_process.get_dataframe(csv_path)


#     columns=data.columns.tolist()
#     if "unnamed" in columns[0].lower():
#         columns[0]="index"
#     data.columns=columns   
#     try:
#         with open(os.path.join(schema_dir, csv_path[len(data_dir) + 1:-4]) + '.json', 'r') as f:
#             schema=json.load(f)
#         if "columns" not in schema.keys():
#             schema["columns"]=[]
#         if "keywords" not in schema.keys():
#             schema_keywords=[]
#             for name in schema["name"].split("_"):
#                 schema_syns=syns(ps(name))
#                 schema_keywords.extend(list(set([i.lemmas()[0].name().lower() for i in  schema_syns])))
            
#             if schema_keywords:
#                 schema["keywords"]=schema_keywords
            
            
#     except Exception as e:
#         print("Could not load schema, generating a new one")
#         schema={}
                 
#         schema["name"]=os.path.splitext(os.path.basename(csv_path))[0]
#         schema["name"]='_'.join([i for i in schema["name"].lower().split() if i.isalnum()])
#         schema_keywords=[]
#         for name in schema["name"].split("_"):
#             schema_syns=syns(ps(name))
#             schema_keywords.extend(list(set([i.lemmas()[0].name().lower() for i in  schema_syns])))
        
#         if schema_keywords:
#             schema["keywords"]=schema_keywords
#         categorical_maps={i:list(set(data[i].dropna())) for i in data.columns if len(list(set(data[i].dropna())))==2}
#         cat_kwd_maps={i:0 for i in categorical_maps}
#         for k,v in categorical_maps.items():
#             cat1syn,cat2syn=syns(ps(v[0])),syns(ps(v[1]))
#             cat1=list(set([i.lemmas()[0].name().lower() for i in  cat1syn]))
#             cat2=list(set([i.lemmas()[0].name().lower() for i in  cat2syn]))
#             if not cat1:
#                 cat1=[v[0]]
#             if not cat2:
#                 cat2=[v[1]]
#             mapped_column={v[0]:cat1,v[1]:cat2}
#             cat_kwd_maps[k]=mapped_column
#         schema["columns"]=[]
#         for column in columns:
            
#             if column in categorical_maps:
#                 schema["columns"].append({"name":column,"mapping":cat_kwd_maps[column]})
#             else:
#                 schema["columns"].append({"name":column})
        

   

#     types=data.dtypes.apply(lambda x:x.name).to_dict()
    
#     for k,v in types.items():
#         if 'int' in v:
#             types[k]="Integer"
#         if 'float' in v:
#             types[k]="Decimal"
#         if "age" in k.lower():
#                 types[k]="Age"
#         if "year" in k.lower():
#                 types[k]="Year"        
#         if 'object' in v:
#             for col in schema["columns"]:
#                 if "mapping" in col:
#                     types[col["name"]]="Categorical"
#                 else:
#                     types[k]="FuzzyString"
                    
#         collist=[]          
#         for col in schema["columns"]:
#             collist.append(col["name"])
#             col["type"]=types[col["name"]]
        
#         for column in columns:
#             if column not in collist:
#                 schema["columns"].append({"name":column,"type":types[column],"keywords":[" ".join(column.lower().split('_'))]})
        
                    
            
            
#         print(schema)
#         return schema


# # print(get_schema_for_csv(data_process.get_csvs()[4]))
# d=data_utils(data_dir,schema_dir)
# print(d.get_csvs()[3])

# print(d.get_schema_for_csv(d.get_csvs()[1]))
# # j=os.path.splitext(os.path.basename(d.get_csvs()[4]))[0]

# j="district_wise_details"
# k=""
# for i in j.lower():
#     if i.isalnum():
#         k+=i
#     else:
#         k+="_"
# print(k)

# # # print('_'.join([i for i in j if i.isalnum()]))
# # print(k)
# # import tensorflow as tf

        
# # from nlp import qa,extract_keywords_from_query
# # class Clause:
# #     def __init__(self):
        
# #         self.base_q="what is {} here"
# #         self.types={"the entity":'SELECT {} FROM {}', "the maximum":'SELECT MAX({}) FROM {}', "the minimum":'SELECT MIN({}) FROM {}', "counted":'SELECT COUNT({}) FROM {}', "summed":'SELECT SUM({}) FROM {}', "averaged":'SELECT AVG({}) FROM {}'}

# #     def adapt(self,q,inttype=False,priority=False):
# #         scores={}
# #         keywords=extract_keywords_from_query(q)
# #         print(keywords)
# #         kwd_scores={k:0 for k in self.types.keys()}
# #         for keyword in keywords:
# #             for k,v in self.types.items():
# #                 kwd_scores[k]+=qa(keyword,self.base_q.format(k),return_score=True)[1]
            
# #         # for k,v in self.types.items():
# #         #     scores[k]=0
# #         #     for keyword in keywords:

# #         #         kwd_scores[keyword]+=qa(keyword,self.base_q.format(k),return_score=True)[1]
# #         #         scores[k]+=kwd_scores[keyword][1]
# #         print(kwd_scores)

# #         return self.types[max(kwd_scores, key=kwd_scores.get)]
         


    
import os
print(os.path.join(os.path.abspath(os.path.dirname(__file__)),"vocabfile"))
                
print(os.path.basename("cc/asd.csv"))



            


