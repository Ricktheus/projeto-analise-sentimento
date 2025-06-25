# Projeto de Banco de Dados: Análise de Sentimento de Apps Mensageiros

## Descrição do Projeto
Este projeto acadêmico tem como objetivo analisar avaliações de aplicativos de mensagens utilizando um sistema de banco de dados híbrido. O SQLite é utilizado para armazenar dados estruturados (informações dos aplicativos e notas das avaliações), enquanto o MongoDB armazena dados não estruturados (texto das avaliações e sentimento identificado por modelo). O resultado final é a extração de insights de negócio por meio de um dashboard de BI.

## Tecnologias Utilizadas
- SQLite
- MongoDB
- Looker Studio (ou Google Data Studio)
- Python (para ETL e análise, opcional)
- Ferramentas de BI

## Como Executar o Projeto
1. **Criar o banco SQLite:**
   - Execute o script `schema.sql` na pasta `/banco_de_dados_sqlite/` para criar as tabelas.
2. **Popular o banco SQLite:**
   - Execute o script `inserts_exemplo.sql` para inserir dados de exemplo.
3. **Importar os dados para o MongoDB:**
   - Exporte os dados necessários do SQLite e importe para o MongoDB, seguindo a estrutura de documento especificada.
   - **Nota:** O arquivo `mensageiros_processado.csv`, localizado na pasta `/dados_fonte`, é o dataset original utilizado para popular a coleção no MongoDB.
4. **Executar as consultas de agregação no MongoDB:**
   - Utilize os arquivos `.js` em `/consultas_mongodb/` na aba "Aggregation" do MongoDB Atlas para gerar os datasets para o BI.
5. **Análise e Resultados:**
   - Importe os dados agregados para o Looker Studio e gere os gráficos do dashboard.

## Análise e Resultados
O dashboard de BI apresenta os seguintes gráficos e insights:

- **Gráfico de Pizza: Proporção Geral de Sentimentos**
  - Mostra a distribuição percentual de sentimentos (positivo, negativo, neutro) nas avaliações. Insight: Identifica o sentimento predominante entre os usuários.
- **Gráfico de Barras: Média de Pontuação por App**
  - Exibe a média das notas (score) para cada aplicativo. Insight: Permite comparar a satisfação dos usuários entre os apps.
- **Gráfico de Barras: Distribuição Total das Pontuações (1 a 5)**
  - Mostra a quantidade de avaliações para cada nota. Insight: Revela tendências de avaliação (ex: polarização).
- **Gráfico de Barras Agrupadas: Distribuição de Pontuações por App**
  - Compara a distribuição de notas entre os diferentes aplicativos. Insight: Identifica apps com avaliações mais extremas ou equilibradas.
- **Gráfico de Barras Empilhadas 100%: Distribuição de Sentimento por App**
  - Mostra a proporção de sentimentos para cada app. Insight: Permite avaliar a reputação relativa dos aplicativos.
- **Gráfico de Barras Agrupadas: Relação entre Nota (Score) e Sentimento**
  - Relaciona as notas atribuídas com o sentimento identificado. Insight: Verifica se notas baixas sempre correspondem a sentimentos negativos, por exemplo.

---

> Para mais detalhes, consulte a documentação e os scripts nas pastas correspondentes. 