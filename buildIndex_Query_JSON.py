import os
import csv
from preProcessor import preProcess
import json
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
# FOLDER = "../Processed_TelevisionNews"
FOLDER = "../data/Processed_TelevisionNews_JSON"
import pickle


def getFilesRecursive(folder):
	# folder = rewritePath(folder)
	files = []
	for root,d_names,f_names in os.walk(folder):
		files.extend(list(map(lambda x:os.path.join(root, x), f_names)))
	return files



def createindex():
	fileIndex = {}
	fileIndexKey = -1
	index = {}
  
	for document in os.listdir(FOLDER):
		print(document)
		fileIndexKey += 1 
		fileIndex[fileIndexKey] = document
		tmpdoc = os.path.join(FOLDER, document)
		for jsonFile in os.listdir(tmpdoc):
			tmpfile = os.path.join(tmpdoc, jsonFile)
			terms = None
			with open(tmpfile, "r") as f:
				data = json.load(f)["Snippet"]
			terms = data.split(" ")
			for term in terms:
				if term not in index:
					index[term] = {}
				indexSubKey = str(fileIndexKey)+":::"+jsonFile.strip(".txt")
				if term=="test" and jsonFile.strip(".txt")=="205":
					print(indexSubKey, data)
				if indexSubKey not in index[term]:
					index[term][indexSubKey] = 1
				else:
					index[term][indexSubKey] += 1

	with open("index1.pkl", "wb") as f:
		pickle.dump([fileIndex, index], f)

def createindex_csv():
  #
  fileIndex = {}
  fileIndexKey = -1
  index = {}
  bigdata = []

  FOLDER="../data/TelevisionNews"
  list_of_csvs=os.listdir(FOLDER)
  for i in range(len(list_of_csvs)):
    print(i,list_of_csvs[i])
    file=os.path.join(FOLDER,list_of_csvs[i])
    fileIndexKey += 1 
    fileIndex[fileIndexKey] = list_of_csvs[i].strip(".csv")
    with open(file, "r") as f:
      csvReader = csv.reader(f)
      try:
        rows = list(csvReader)
      except UnicodeDecodeError:
        continue
      for rowNum in range(1, len(rows)):
        row = rows[rowNum][-1]
        tokens = preProcess(row)
        terms = tokens
        for term in terms:
          if term not in index:
            index[term] = {}
          indexSubKey = str(fileIndexKey)+":::"+str(rowNum+1)
          if term=="test" and str(rowNum+1)=="205":
            print(indexSubKey, row)
          if indexSubKey not in index[term]:
            index[term][indexSubKey] = row
          else:
            index[term][indexSubKey] += row
          bigdata.append(row)
  with open("index2.pkl", "wb") as f:
    pickle.dump([fileIndex, index, bigdata], f)


def getDocs(term):
	index = None
	with open("index1.pkl", "rb") as f:
		fileIndex, index = pickle.load(f)
	tmpD = index[term]
	l = []
	for i in tmpD:
		doc, row = i.split(":::")
		l.append([fileIndex[int(doc)], row, tmpD[i]])
	l.sort(key=lambda x:x[2], reverse=True)
	return l

# ans = getDocs("sport")
# print(ans)
createindex_csv()
# createindex()