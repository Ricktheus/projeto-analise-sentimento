// Objetivo: Contar a proporção de sentimentos (positivo, negativo, neutro) no dataset inteiro.
// Usar na aba "Aggregation" do MongoDB Atlas.
[
  { "$group": { "_id": "$model_sentiment", "total": { "$sum": 1 } } },
  { "$project": { "sentimento": "$_id", "contagem": "$total", "_id": 0 } }
] 