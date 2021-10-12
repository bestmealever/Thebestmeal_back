from pymongo import MongoClient
import pandas as pd
import os

data = pd.read_csv('food_final.csv', encoding='utf-8-sig', index_col=False)

# 배포서버
client = MongoClient(os.environ.get("MONGO_DB_PATH_DATA"))

# 로컬서버
# client = MongoClient('localhost', 27017)

db = client.team_project

for i in range(len(data)):
    doc = {'name': data.iloc[i]['title'], 'category': data.iloc[i]['category'].split(','),
           'emotion': data.iloc[i]['emotion'].split(','), 'url': data.iloc[i]['url']}
    db.team_project.insert_one(doc)
