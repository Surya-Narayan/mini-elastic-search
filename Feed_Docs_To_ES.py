import csv
import os
from elasticsearch import Elasticsearch

FOLDER="../data/TelevisionNews"

files=os.listdir(FOLDER)
es=Elasticsearch([{'host':'34.68.24.40','port':9200}])
try:
  es.indices.create(index="air_project")
except:
  pass

for file in files:
  print(file)
  path=os.path.join(FOLDER,file)
  with open(path, "r") as f:
    csvReader = csv.reader(f)
    try:
      rows = list(csvReader)
    except UnicodeDecodeError:
      continue
    for i in range(1,len(rows)):
      json_content={}
      row=rows[i]
      json_content["csv_file"]=file
      json_content["row_num"]=str(i+1)

      json_content["URL"]=row[0]
      json_content["MatchDateTime"]=row[1]
      json_content["Station"]=row[2]
      json_content["Show"]=row[3]
      json_content["IAShowID"]=row[4]
      json_content["IAPreviewThumb"]=row[5]
      json_content["Snippet"]=row[6]
      # print(json_content)
      
      id=file+"/"+str(i+1)
      # print(id,json_content)
    
      #Upload json_content
      if es.exists(index="air_project", id=id)==False:
        resp=es.index(index="air_project",id=id,doc_type='snippets',body=json_content)
        # print(resp['created'],i)