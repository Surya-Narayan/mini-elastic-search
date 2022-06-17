from retrieveDocuments import retrieveDocuments,retrieveDocumentsWIDF
from preProcessor import preProcess
import csv
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time
from elasticsearch import Elasticsearch
import pprint 
import pickle

FOLDER="../data/TelevisionNews"

with open("index2.pkl", "rb") as f:
    auxIndex, mainIndex, bigd = pickle.load(f)

#query->string
#data->list of strings, each string is a document
def rank_docs(resultSet,query,final_tokens,docs):
  row_docs = dict()
  docs_data=[]
  index = []

  # for file in docs:
  #   name=os.path.join(FOLDER,file.split("/")[0]+".csv")
  #   rownum=int(file.split("/")[1])
  #   if(row_docs.get(name)==None):
  #     row_docs[name]=[]
  #   row_docs[name].append(rownum)
  
  # for key in row_docs.keys():
  #   with open(key, "r") as f:
  #     csvReader = csv.reader(f)
  #     try:
  #       row = list(csvReader)
  #     except UnicodeDecodeError:
  #       continue
  #     for i in range(len(row_docs[key])):
  #       rownum = row_docs[key][i] - 1
  #       r = row[rownum][-1]
  #       tokens=preProcess(r)
  #       docs_data.append(" ".join(tokens))
  #       index.append(key.split("/")[-1]+"/"+str(rownum+1))

  for token in final_tokens:
    for i in resultSet:
      try:
        a = mainIndex[token[0]][i]
        # print(a)
        # for j in a:
        docs_data.append(a)
      except:
        continue
  
  # docs_data = list(set(docs_data))

  vectorizer = TfidfVectorizer()
  docs_data.append(query)
  #Vectors of all documents
  X = vectorizer.fit_transform(docs_data)
  query_vector=X[-1]

  ranks=[]
  # for i in range(len(docs_data)-1):
  #   val = cosine_similarity(query_vector,X[i])
  #   ranks.append((val[0][0],index[i]))
  # ranks.sort(reverse=True)

  val = cosine_similarity(query_vector,X)[0]
  var = list(zip(docs,val.tolist()))
  var.sort(key= lambda x : x[1], reverse=True)
  # print(var)
  return list(set(var))


def get_es_result(q):
  es = Elasticsearch([{'host':'34.68.24.40','port':9200}])
  query = {
      "query":{        
          "match":{
              "Snippet":q
          }
      }
  }
  res = es.search(index='air_project',size=94000,body=query)
  # res=es.search(index="air_project",size=94858,body=q1)
  # pp = pprint.PrettyPrinter(indent=4)
  # pp.pprint(res)
  es_resp_time = res['took']
  # print("ES Resp time:",es_resp_time)
  l = []
  for doc in res['hits']['hits']: 
    l.append(doc['_id'])
  return l,es_resp_time

def get_metrics(es_result,ranked_docs):
  l = []
  for i in ranked_docs:
    # l.append(i[0])
    m = i[0].split("/")
    l.append(m[0]+".csv/"+m[1])
  intersection = list(set(es_result) & set(l))
  precision = len(intersection)/len(l)
  recall = len(intersection)/len(es_result)
  f1_score = (2*(precision*recall))/(precision+recall)
  return precision, recall, f1_score

if __name__=="__main__":
  query = input("Enter the query: ")
  print()
  # query = "move to reduce carbon"
  # query = "industry airline"
  # query = "ozone layer"
  # query = "affordable healthcare"
  # query = "rainy sports weather channel"
  # query = "modi india"
  # query = "global warming"
  # query = "climate change india"
  # query = "fossil fuels green house gases"
  # query = "green new deal"
  # print("Input Query:",query)
  query = " ".join(preProcess(query))
  start_time = time.time()
  # resultSet, final_tokens, docs = retrieveDocuments(query)
  # docs = retrieveDocuments(query)
  docs = retrieveDocumentsWIDF(query)
  if(len(docs)==0):
    print("No relevant documents found.")
    exit()
  resultSet, final_tokens, docs = docs[0], docs[1], docs[2]
  ranked_docs = rank_docs(resultSet,query,final_tokens,docs)
  ranked_docs.sort(key= lambda x : x[1], reverse=True)
  # print("Our results:")
  # print(ranked_docs[:10])
  resp_time = (time.time() - start_time)
  es_result, es_resp_time = get_es_result(query)
  if(len(es_result)==0 or len(ranked_docs)==0):
    print("No relevant documents found .")
    exit()
  print("Our Search Engine Results:")
  for i in range(len(ranked_docs[:10])):
    with open(os.path.join(FOLDER,ranked_docs[i][0].split("/")[0]+".csv"), "r") as f:
      csvReader = csv.reader(f)
      snippet = list(csvReader)[int(ranked_docs[i][0].split("/")[1])-1][-1]
    print(ranked_docs[i][0], ranked_docs[i][1],snippet,sep="  ")
  # print(es_result[:10])
  print()
  print("Number of relavant documents:")
  print("ElasticSearch:",len(es_result))
  print("Our search engine:",len(ranked_docs))
  # print(len(es_result),len(ranked_docs))
  precision, recall, f1_score = get_metrics(es_result,ranked_docs)
  print()
  print("Response Time:")
  print("Elastic Search: ",es_resp_time/1000,"s",sep="")
  print("Our search engine: ",resp_time,"s",sep="")
  print()
  print("Precision:",precision)
  print("Recall:",recall)
  print("f1-score:",f1_score)
 