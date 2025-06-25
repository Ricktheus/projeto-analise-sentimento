// Objetivo: Calcular a distribuição de sentimentos (positivo, negativo, neutro) para cada aplicativo.
// Usar na aba "Aggregation" do MongoDB Atlas.
[
  { "$group": { "_id": { "app": "$app", "sentimento": "$model_sentiment" }, "total": { "$sum": 1 } } },
  { "$group": { "_id": "$_id.app", "sentimentos": { "$push": { "sentimento": "$_id.sentimento", "contagem": "$total" } } } },
  { "$project": { "app": "$_id", "sentimentos": 1, "_id": 0 } }
] 