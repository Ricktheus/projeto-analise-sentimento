# Sistema de Análise de Sentimento em Avaliações de Apps Mensageiros

## Visão Geral
Projeto acadêmico que implementa um sistema híbrido de bancos de dados para análise de sentimento em avaliações de aplicativos mensageiros (WhatsApp, Facebook Messenger, Skype, Viber, LINE). O objetivo é extrair insights sobre satisfação e qualidade das avaliações, utilizando SQLite para dados estruturados, MongoDB para texto completo e Python para análise e geração de gráficos.

## Arquitetura
- **SQLite**: Armazena dados estruturados, realiza análises e consultas complexas.
- **MongoDB**: Guarda texto completo das reviews e metadados.
- **Python**: Processa dados, executa análises e gera gráficos.

## Fonte da Verdade
- Toda a documentação, objetivos, metodologia e resultados finais estão descritos em [`apresentacao_analise_sentimento_alinhada.md`](apresentacao_analise_sentimento_alinhada.md). Este arquivo deve ser sempre consultado para garantir alinhamento do projeto.

## Funcionalidades Principais
- Análise de qualidade das avaliações por app
- Correlação entre tamanho da review e score
- Sistema de categorização inteligente (8 categorias automáticas)
- Detecção de anomalias estatísticas
- Ranking comparativo entre aplicativos

## Estrutura do Projeto
```
Projeto_Analise_Sentimento/
├── banco_de_dados_sqlite/
├── dashboard_bi/
├── documentacao/
├── scripts/
├── dados_fonte/
├── dados_exportados_csv/
├── consultas_mongodb/
```

## Como Executar
1. **Preparar o banco SQLite:**
   - Execute `schema.sql` em `banco_de_dados_sqlite/`.
   - Importe os dados reais usando o script `importar_csv_para_sqlite.py`.
2. **Executar melhorias (opcional):**
   - `sqlite3 database.db < melhorias_avaliacao.sql`
3. **Gerar gráficos (pipeline automatizado):**
   - `cd scripts && python gerar_graficos_melhorias.py`
   - Todos os gráficos e outputs devem ser gerados por este script, utilizando dados reais do banco/CSV.
4. **Importar dados para BI:**
   - Use os CSVs exportados em `dados_exportados_csv/` no Looker Studio ou outra ferramenta de BI.

## Principais Gráficos

### Análise de Qualidade por App
![Qualidade por App](../dashboard_bi/01_analise_qualidade_por_app.png)

### Correlação Tamanho-Score
![Correlação Tamanho-Score](../dashboard_bi/02_correlacao_tamanho_score.png)

### Categorização Inteligente
![Categorização Inteligente](../dashboard_bi/03_categorizacao_inteligente.png)

### Detecção de Anomalias
![Detecção de Anomalias](../dashboard_bi/04_deteccao_anomalias.png)

### Ranking Comparativo
![Ranking Comparativo](../dashboard_bi/05_ranking_comparativo.png)

## Consultas Úteis
```sql
-- Análise de qualidade
SELECT * FROM analise_qualidade_reviews;
-- Detecção de anomalias
SELECT * FROM detecao_anomalias WHERE classificacao = 'Anomalia';
-- Ranking comparativo
SELECT * FROM correlacao_metricas ORDER BY media_score DESC;
```

## Principais Insights
- WhatsApp lidera em score médio e qualidade
- LINE tem maior percentual de reviews detalhadas
- Reviews detalhadas indicam maior engajamento
- Sistema de categorização identifica padrões valiosos
- Detecção de anomalias melhora a qualidade dos dados

## Documentação
- `documentacao/relatorio_tecnico_melhorado.md`: Relatório técnico completo
- `apresentacao_analise_sentimento_alinhada.md`: Apresentação final e fonte da verdade

---

> Projeto desenvolvido para fins acadêmicos. Para detalhes técnicos, consulte os scripts e documentação na pasta `documentacao/`. 
