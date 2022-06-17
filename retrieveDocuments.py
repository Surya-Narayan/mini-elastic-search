import pickle
import os

with open("index2.pkl", "rb") as f:
    auxIndex, mainIndex, snip_doc= pickle.load(f)
  # print(auxIndex.keys())

with open("idf_scores.pkl", "rb") as f:
    idf_score = pickle.load(f)


def convertKeyToPath(key):
    document, row = key.split(":::")
    document = auxIndex[int(document)]
    return os.path.join(document, row)

def retrieveDocumentsWIDF(query):
    # print(query)
    tokens = query.split(" ")
    tmpDocs = []
    token_list= []
    final_tokens=[]
    for token in tokens:
        if(idf_score.get(token)==None):
            token_list.append((token,0))
        else :
            token_list.append((token,idf_score[token]))
    token_list.sort(key= lambda x : x[1], reverse=True)

    for token in token_list:
        if(mainIndex.get(token[0])!=None):
            tmpDocs.append(list(mainIndex[token[0]].keys()))
            final_tokens.append(token)
            # print(mainIndex.values())


    if(len(tmpDocs)==0):
        return []
    resultSet = set(tmpDocs[0])

    for i in range(1, len(tokens)):
        try:
            # resultSet = resultSet.intersection(tmpDocs[i])
            # print(len(bigd))
            resultSet = resultSet | set(tmpDocs[i])
        except:
            continue
    snippet = []
    # print(resultSet)
    resultList = list(map(convertKeyToPath, list(resultSet)))
    final_res = [resultSet,final_tokens,resultList]
    # return resultSet,final_tokens,resultList
    return final_res

def retrieveDocuments(query):
    # print(query)
    tokens = query.split(" ")
    tmpDocs = []
    token_list= []
    final_tokens=[]
    for token in tokens:
        if(idf_score.get(token)==None):
            token_list.append((token,0))
        else :
            token_list.append((token,idf_score[token]))
    token_list.sort(key= lambda x : x[1], reverse=True)

    for token in token_list:
        if(mainIndex.get(token[0])!=None):
            tmpDocs.append(list(mainIndex[token[0]].keys()))
            final_tokens.append(token)
            # print(mainIndex.values())


    if(len(tmpDocs)==0):
        return []
    resultSet = set(tmpDocs[0])

    for i in range(1, len(tokens)):
        try:
            temp = resultSet
            resultSet = resultSet.intersection(tmpDocs[i])
            # print(len(bigd))
            # resultSet = resultSet | set(tmpDocs[i])

        except:
            continue
        if(len(resultSet)<50):
            resultSet = temp | set(tmpDocs[i-1]) | set(tmpDocs[i])
            # resultSet = resultSet.intersection(tmpDocs[i])
            break
    snippet = []
    # print(resultSet)
    resultList = list(map(convertKeyToPath, list(resultSet)))
    final_res = [resultSet,final_tokens,resultList]
    # return resultSet,final_tokens,resultList
    return final_res


# query = "industry airline"
# retrieveDocuments(query)
