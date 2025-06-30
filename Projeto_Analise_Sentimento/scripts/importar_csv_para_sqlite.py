import pandas as pd
import sqlite3
from tqdm import tqdm

# Caminhos
csv_path = 'Projeto_Analise_Sentimento/dados_fonte/mensageiros_processado.csv'
db_path = 'Projeto_Analise_Sentimento/banco_de_dados_sqlite/database.db'

# Ler CSV
print('Lendo CSV...')
df = pd.read_csv(csv_path)

# Conectar ao SQLite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Popular Aplicativos (sem duplicatas)
apps = df['app'].drop_duplicates().reset_index(drop=True)
app_id_map = {}
print('Populando tabela Aplicativos...')
for nome in tqdm(apps):
    cursor.execute('INSERT OR IGNORE INTO Aplicativos (nome) VALUES (?)', (nome,))
    cursor.execute('SELECT id_app FROM Aplicativos WHERE nome = ?', (nome,))
    app_id_map[nome] = cursor.fetchone()[0]

# Popular Reviews
print('Populando tabela Reviews...')
for _, row in tqdm(df.iterrows(), total=len(df)):
    cursor.execute(
        'INSERT INTO Reviews (review_uuid, score, id_app) VALUES (?, ?, ?)',
        (row['reviewId'], row['score'], app_id_map[row['app']])
    )

conn.commit()
conn.close()
print('Importação concluída!') 