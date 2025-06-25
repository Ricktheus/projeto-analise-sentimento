// Objetivo: Relacionar as notas (score) com o sentimento identificado pelo modelo.
// Usar na aba "Aggregation" do MongoDB Atlas.
[
  { "$group": { "_id": { "score": "$score", "sentimento": "$model_sentiment" }, "total": { "$sum": 1 } } },
  { "$sort": { "_id.score": 1 } },
  { "$project": { "score": "$_id.score", "sentimento": "$_id.sentimento", "contagem": "$total", "_id": 0 } }
] 