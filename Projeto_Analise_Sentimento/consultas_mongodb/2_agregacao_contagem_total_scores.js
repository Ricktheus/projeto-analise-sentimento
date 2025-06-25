// Objetivo: Contar a quantidade total de avaliações para cada score (1 a 5).
// Usar na aba "Aggregation" do MongoDB Atlas.
[
  { "$group": { "_id": "$score", "total": { "$sum": 1 } } },
  { "$project": { "score": "$_id", "contagem": "$total", "_id": 0 } },
  { "$sort": { "score": 1 } }
] 