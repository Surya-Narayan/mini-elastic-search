import csv
import os
import json
from preProcessor import preProcess

FOLDER = "../data/TelevisionNews"
# FOLDER = "TelevisionNews"
# PROCESSED_FOLDER = "/content/drive/My Drive/Search Engine/data/Processed_TelevisionNews"

LOGFILE = "log.txt"

def getFilesRecursive(folder):
    files = []
    for root,d_names,f_names in os.walk(folder):
      files.extend(list(map(lambda x:os.path.join(root, x), f_names)))
    return files


def storeData(json_content, path, number):
    path = path.replace("TelevisionNews", "Processed_TelevisionNews_JSON")
    print("New path:",path,sep=" ")
    try:
        os.makedirs(path)
    except FileExistsError:
        pass
    fileName = str(number) + ".json"
    print("New fileName:",fileName,sep=" ")
    with open(os.path.join(path, fileName), "w") as f:
        # f.write(" ".join(data))
        json.dump(json_content,f,indent=4)
files = getFilesRecursive(FOLDER)

skippedCount = 0
skippedFiles = []

for file in files:
    # print(file)
    with open(file, "r") as f:
        csvReader = csv.reader(f)
        try:
            rows = list(csvReader)
        except UnicodeDecodeError:
            print("Skipping", file)
            skippedCount += 1
            skippedFiles.append(file)
    
    for rowNum in range(1, len(rows)):
        
        row = rows[rowNum]
        
        tokens = preProcess(row[-1])
        
        csv_file=file.split("/")[-1]
        csv_file=csv_file.strip(".csv")
        #Dictionary
        json_content={}
        json_content["csv_file"]=csv_file
        json_content["row_num"]=rowNum+1
        
        json_content["URL"]=row[0]
        json_content["MatchDateTime"]=row[1]
        json_content["Station"]=row[2]
        json_content["Show"]=row[3]
        json_content["IAShowID"]=row[4]
        json_content["IAPreviewThumb"]=row[5]
        json_content["Snippet"]=" ".join(tokens)
        
        # print(json_content)
        folderPath =".."+ file.strip(".csv")

        storeData(json_content, folderPath, rowNum+1)

with open(LOGFILE, "w") as f:
	  f.writelines([str(skippedCount)] + skippedFiles)

