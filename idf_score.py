import pickle
import csv
import os
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

FOLDER = "../data/TelevisionNews"

def get_idf_score():
    data = []
    for doc in os.listdir(FOLDER):
        with open(os.path.join(FOLDER,doc), "r") as f:
            csvReader = csv.reader(f)
            t = list(csvReader)
            for row in t:
                data.append(row[-1])


    cv = CountVectorizer()
    # convert text data into term-frequency matrix
    data = cv.fit_transform(data)

    tfidf_transformer = TfidfTransformer()

    # convert term-frequency matrix into tf-idf
    tfidf_matrix = tfidf_transformer.fit_transform(data)

    # create dictionary to find a tfidf word each word
    idf_score = dict(zip(cv.get_feature_names(), tfidf_transformer.idf_))
    with open("idf_scores.pkl", "wb") as f:
		    pickle.dump(idf_score, f)
    return idf_score

get_idf_score()