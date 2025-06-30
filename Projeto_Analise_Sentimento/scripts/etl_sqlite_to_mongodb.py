import sqlite3
from pymongo import MongoClient
import os

# Caminho correto para o banco SQLite
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.abspath(os.path.join(script_dir, '../banco_de_dados_sqlite/database.db'))

# Conexão com o SQLite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Conexão com o MongoDB (localhost padrão)
client = MongoClient('mongodb://localhost:27017/')
db = client['analise_sentimento']
apps_collection = db['aplicativos']
reviews_collection = db['reviews']

# Limpar coleções para evitar duplicidade
apps_collection.delete_many({})
reviews_collection.delete_many({})

# Extrair aplicativos
dict_apps = {}
for row in cursor.execute('SELECT id_app, nome FROM Aplicativos'):
    app_doc = {'_id': row[0], 'nome': row[1]}
    apps_collection.insert_one(app_doc)
    dict_apps[row[0]] = row[1]

# Extrair reviews e inserir no MongoDB
for row in cursor.execute('SELECT id_review_sqlite, review_uuid, score, id_app FROM Reviews'):
    review_doc = {
        '_id': row[0],
        'review_uuid': row[1],
        'score': row[2],
        'id_app': row[3],
        'nome_app': dict_apps.get(row[3], None)
    }
    reviews_collection.insert_one(review_doc)

print('ETL concluído: dados do SQLite migrados para o MongoDB.') 