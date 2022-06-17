import os
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
FOLDER = "../TelevisionNews2"
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
		# print(document)
		fileIndexKey += 1 
		fileIndex[fileIndexKey] = document
		tmpdoc = os.path.join(FOLDER, document)
		for snippet in os.listdir(tmpdoc):
			tmpfile = os.path.join(tmpdoc, snippet)
			terms = None
			with open(tmpfile, "r") as f:
				data = f.read()
			terms = data.split(" ")
			for term in terms:
				if term not in index:
					index[term] = {}
				indexSubKey = str(fileIndexKey)+":::"+snippet.strip(".txt")
				if term=="test" and snippet.strip(".txt")=="205":
					print(indexSubKey, data)
				if indexSubKey not in index[term]:
					index[term][indexSubKey] = 1
				else:
					index[term][indexSubKey] += 1

	with open("index1.pkl", "wb") as f:
		pickle.dump([fileIndex, index], f)



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

ans = getDocs("sport")
print(ans)