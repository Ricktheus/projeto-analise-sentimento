# Relatório Técnico - Sistema de Análise de Sentimento em Avaliações de Aplicativos Mensageiros

## 1. Introdução

### 1.1 Contexto e Objetivo
Este projeto implementa um sistema híbrido de bancos de dados para análise de sentimento em avaliações de aplicativos mensageiros, demonstrando a integração entre diferentes tecnologias de armazenamento e processamento de dados. O sistema visa extrair insights valiosos sobre a satisfação dos usuários e qualidade das avaliações.

### 1.2 Tema Escolhido
**Análise de Sentimento em Avaliações de Aplicativos Mensageiros**
- Foco: WhatsApp, Facebook Messenger, Skype, Viber e LINE
- Objetivo: Identificar padrões de satisfação e qualidade das reviews
- Abordagem: Sistema híbrido com múltiplas análises avançadas

## 2. Arquitetura do Sistema

### 2.1 Visão Geral
O sistema utiliza uma arquitetura híbrida composta por:
- **SQLite**: Armazenamento de dados estruturados e análises avançadas
- **MongoDB**: Armazenamento de dados não estruturados (texto das reviews)
- **Looker Studio**: Visualização e dashboard de BI

### 2.2 Componentes Principais

#### 2.2.1 Banco de Dados Relacional (SQLite)
**Função**: Armazenamento de dados estruturados e análises complexas
- Tabelas principais: Aplicativos, Reviews
- Métricas de texto: contagem de caracteres, palavras, presença de ruído
- Sistema de categorização inteligente
- Detecção de anomalias

#### 2.2.2 Banco de Dados NoSQL (MongoDB)
**Função**: Armazenamento de dados não estruturados
- Texto completo das reviews
- Análise de sentimento processada
- Metadados de processamento

#### 2.2.3 Dashboard de BI (Looker Studio)
**Função**: Visualização e análise de dados
- Gráficos interativos
- Relatórios automatizados
- Análises comparativas

## 3. Modelagem e Implementação

### 3.1 Modelagem do Banco Relacional (SQLite)

#### 3.1.1 Schema Principal
```sql
-- Tabela de Aplicativos
CREATE TABLE Aplicativos (
    id_app INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(255) NOT NULL UNIQUE
);

-- Tabela de Reviews (Expandida)
CREATE TABLE Reviews (
    id_review_sqlite INTEGER PRIMARY KEY AUTOINCREMENT,
    review_uuid TEXT NOT NULL,
    score INTEGER,
    id_app INTEGER,
    char_count INTEGER,
    word_count INTEGER,
    has_noise BOOLEAN,
    sentiment_label VARCHAR(20),
    model_sentiment VARCHAR(20),
    FOREIGN KEY(id_app) REFERENCES Aplicativos(id_app)
);
```

#### 3.1.2 Sistema de Categorização Inteligente
```sql
-- Tabela de Categorias
CREATE TABLE Categorias_Reviews (
    id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_categoria VARCHAR(100),
    descricao TEXT,
    criterios TEXT
);

-- Relacionamento Reviews-Categorias
CREATE TABLE Reviews_Categorias (
    id_review_sqlite INTEGER,
    id_categoria INTEGER,
    confianca DECIMAL(3,2),
    PRIMARY KEY(id_review_sqlite, id_categoria)
);
```

### 3.2 Categorias Implementadas
1. **Reviews Detalhadas Positivas**: word_count > 10 AND sentiment = "positivo"
2. **Reviews Críticas Detalhadas**: word_count > 10 AND sentiment = "negativo"
3. **Reviews Simples Positivas**: word_count ≤ 5 AND sentiment = "positivo"
4. **Reviews com Ruído**: has_noise = 1
5. **Reviews de Alta Qualidade**: has_noise = 0 AND word_count > 10
6. **Reviews Neutras Detalhadas**: word_count > 10 AND sentiment = "neutro"
7. **Reviews Extremas**: score = 1 OR score = 5
8. **Reviews Balanceadas**: score BETWEEN 3 AND 4

### 3.3 Views Analíticas Implementadas

#### 3.3.1 Análise de Qualidade
```sql
CREATE VIEW analise_qualidade_reviews AS
SELECT 
    a.nome as app,
    COUNT(*) as total_reviews,
    AVG(r.score) as media_score,
    COUNT(CASE WHEN r.word_count <= 5 THEN 1 END) as reviews_curtas,
    COUNT(CASE WHEN r.word_count BETWEEN 6 AND 20 THEN 1 END) as reviews_medias,
    COUNT(CASE WHEN r.word_count > 20 THEN 1 END) as reviews_longas,
    COUNT(CASE WHEN r.has_noise = 1 THEN 1 END) as reviews_com_ruido,
    COUNT(CASE WHEN r.has_noise = 0 THEN 1 END) as reviews_sem_ruido
FROM Reviews r
JOIN Aplicativos a ON r.id_app = a.id_app
GROUP BY a.nome;
```

#### 3.3.2 Detecção de Anomalias
```sql
CREATE VIEW detecao_anomalias AS
WITH estatisticas_app AS (
    SELECT 
        id_app,
        AVG(score) as media_score,
        COUNT(*) as total_reviews
    FROM Reviews
    GROUP BY id_app
    HAVING COUNT(*) > 10
)
SELECT 
    a.nome as app,
    r.review_uuid,
    r.score,
    ROUND(ea.media_score, 2) as media_app,
    ABS(r.score - ea.media_score) as diferenca_media,
    CASE 
        WHEN ABS(r.score - ea.media_score) > 2 THEN 'Anomalia'
        WHEN ABS(r.score - ea.media_score) > 1 THEN 'Variação Significativa'
        ELSE 'Normal'
    END as classificacao
FROM Reviews r
JOIN Aplicativos a ON r.id_app = a.id_app
JOIN estatisticas_app ea ON r.id_app = ea.id_app
WHERE ABS(r.score - ea.media_score) > 1;
```

## 4. Casos de Uso Implementados

### 4.1 Caso de Uso 1: Análise de Qualidade das Reviews
**Objetivo**: Identificar a qualidade das avaliações por aplicativo
**Implementação**: View `analise_qualidade_reviews`
**Métricas**:
- Média de score por app
- Distribuição por tamanho de texto
- Percentual de reviews com/sem ruído
- Análise de sentimentos

### 4.2 Caso de Uso 2: Correlação entre Tamanho e Score
**Objetivo**: Analisar se reviews mais detalhadas têm scores diferentes
**Implementação**: Análise estatística com categorização por tamanho
**Insights**:
- Reviews longas tendem a ter scores mais extremos
- Reviews curtas são mais comuns em scores altos
- Correlação entre detalhamento e sentimento

### 4.3 Caso de Uso 3: Sistema de Categorização Inteligente
**Objetivo**: Classificar automaticamente as reviews em categorias
**Implementação**: Sistema de categorização baseado em múltiplos critérios
**Benefícios**:
- Identificação de padrões de comportamento
- Análise de qualidade por categoria
- Insights para melhorias de produto

### 4.4 Caso de Uso 4: Detecção de Anomalias
**Objetivo**: Identificar reviews atípicas que merecem atenção
**Implementação**: Algoritmo de detecção baseado em desvio da média
**Aplicação**:
- Identificação de reviews falsas
- Detecção de problemas específicos
- Monitoramento de qualidade

### 4.5 Caso de Uso 5: Ranking Comparativo
**Objetivo**: Comparar aplicativos em múltiplas dimensões
**Implementação**: Análise multidimensional com ranking
**Métricas**:
- Score médio
- Qualidade das reviews
- Detalhamento médio
- Sentimento predominante

## 5. Consultas e Análise de Dados

### 5.1 Consultas Complexas Implementadas

#### 5.1.1 Análise Comparativa Entre Apps
```sql
SELECT 
    a.nome as app,
    COUNT(*) as total_reviews,
    ROUND(AVG(r.score), 2) as media_score,
    ROUND(AVG(r.word_count), 1) as media_palavras,
    ROUND(COUNT(CASE WHEN r.has_noise = 0 THEN 1 END) * 100.0 / COUNT(*), 2) as pct_qualidade,
    ROUND(COUNT(CASE WHEN r.sentiment_label = 'positivo' THEN 1 END) * 100.0 / COUNT(*), 2) as pct_positivo,
    RANK() OVER (ORDER BY AVG(r.score) DESC) as rank_score,
    RANK() OVER (ORDER BY AVG(r.word_count) DESC) as rank_detalhamento,
    RANK() OVER (ORDER BY COUNT(CASE WHEN r.has_noise = 0 THEN 1 END) * 100.0 / COUNT(*) DESC) as rank_qualidade
FROM Reviews r
JOIN Aplicativos a ON r.id_app = a.id_app
GROUP BY a.nome
ORDER BY media_score DESC;
```

#### 5.1.2 Análise de Correlação por Tamanho
```sql
SELECT 
    a.nome as app,
    CASE 
        WHEN r.word_count <= 5 THEN 'Muito Curta (≤5 palavras)'
        WHEN r.word_count <= 10 THEN 'Curta (6-10 palavras)'
        WHEN r.word_count <= 20 THEN 'Média (11-20 palavras)'
        ELSE 'Longa (>20 palavras)'
    END as tamanho_review,
    COUNT(*) as total_reviews,
    AVG(r.score) as media_score,
    AVG(r.word_count) as media_palavras
FROM Reviews r
JOIN Aplicativos a ON r.id_app = a.id_app
GROUP BY a.nome, 
    CASE 
        WHEN r.word_count <= 5 THEN 'Muito Curta (≤5 palavras)'
        WHEN r.word_count <= 10 THEN 'Curta (6-10 palavras)'
        WHEN r.word_count <= 20 THEN 'Média (11-20 palavras)'
        ELSE 'Longa (>20 palavras)'
    END
ORDER BY a.nome, media_score DESC;
```

### 5.2 Integração Entre Bancos de Dados

#### 5.2.1 Fluxo de Dados
1. **Extração**: Dados do CSV original
2. **Transformação**: Processamento de texto e análise de sentimento
3. **Carregamento**: SQLite (dados estruturados) + MongoDB (texto completo)
4. **Análise**: Consultas complexas no SQLite
5. **Visualização**: Dashboard no Looker Studio

#### 5.2.2 Pontos de Integração
- **UUID das reviews**: Chave de ligação entre SQLite e MongoDB
- **Métricas de texto**: Calculadas no processamento, armazenadas no SQLite
- **Sentimentos**: Processados externamente, sincronizados entre bancos

## 6. Análise de Dados com Ferramentas de BI

### 6.1 Gráficos Implementados

#### 6.1.1 Análise de Qualidade por App
- Média de score por aplicativo
- Distribuição de sentimentos
- Percentual de reviews sem ruído
- Média de palavras por review

#### 6.1.2 Correlação Tamanho-Score
- Média de score por categoria de tamanho
- Distribuição de tamanhos por app
- Scatter plot: palavras vs score
- Percentual de sentimentos por tamanho

#### 6.1.3 Categorização Inteligente
- Distribuição de categorias por app
- Média de score por categoria
- Percentual de categorias por app
- Análise de qualidade por categoria

#### 6.1.4 Detecção de Anomalias
- Distribuição de scores com anomalias destacadas
- Top anomalias por Z-Score
- Número de anomalias por app
- Box plot de scores por app

#### 6.1.5 Ranking Comparativo
- Ranking por score médio
- Ranking por qualidade
- Comparação multidimensional (radar chart)
- Correlação entre métricas (heatmap)

### 6.2 Insights Extraídos

#### 6.2.1 Padrões de Qualidade
- Apps com reviews mais detalhadas tendem a ter scores mais equilibrados
- Reviews sem ruído são mais comuns em apps com melhor avaliação
- Correlação positiva entre tamanho da review e qualidade da avaliação

#### 6.2.2 Anomalias Detectadas
- Reviews com scores extremos (1 ou 5) em apps com média alta/baixa
- Padrões de comportamento suspeito identificados
- Variações significativas que merecem investigação

#### 6.2.3 Rankings e Comparações
- WhatsApp lidera em score médio e qualidade
- LINE tem maior percentual de reviews detalhadas
- Skype apresenta maior variação nos scores

## 7. Tecnologias Utilizadas

### 7.1 Banco de Dados
- **SQLite 3**: Banco relacional para análises estruturadas
- **MongoDB**: Banco NoSQL para dados não estruturados
- **Python**: Processamento e análise de dados

### 7.2 Ferramentas de BI
- **Looker Studio**: Dashboard e visualizações
- **Matplotlib/Seaborn**: Geração de gráficos
- **Pandas**: Manipulação de dados

### 7.3 Desenvolvimento
- **Git**: Controle de versão
- **SQL**: Linguagem de consulta
- **Python**: Scripts de processamento

## 8. Resultados e Conclusões

### 8.1 Resultados Alcançados
- ✅ Sistema híbrido funcional com integração entre SQLite e MongoDB
- ✅ Análises avançadas implementadas (categorização, anomalias, correlações)
- ✅ Dashboard completo com 5 tipos de visualizações
- ✅ Consultas complexas demonstrando proficiência técnica
- ✅ Detecção de padrões e insights valiosos

### 8.2 Complexidade Demonstrada
- **Arquitetura**: Sistema híbrido com múltiplos bancos
- **Análises**: Estatísticas avançadas e detecção de anomalias
- **Categorização**: Sistema inteligente baseado em múltiplos critérios
- **Visualização**: Dashboard interativo com múltiplas perspectivas

### 8.3 Benefícios do Sistema
- **Para Desenvolvedores**: Insights sobre qualidade das reviews
- **Para Usuários**: Melhoria na qualidade dos aplicativos
- **Para Análise**: Ferramentas avançadas de análise de sentimento
- **Para Negócio**: Tomada de decisão baseada em dados

### 8.4 Limitações e Melhorias Futuras
- Implementação de análise temporal (se dados disponíveis)
- Processamento em tempo real de novas reviews
- Machine Learning para categorização automática
- Alertas automáticos para anomalias críticas

## 9. Contribuições e Aprendizados

### 9.1 Contribuições Técnicas
- Sistema de categorização inteligente inovador
- Detecção de anomalias baseada em estatísticas
- Análises de correlação entre múltiplas métricas
- Dashboard multidimensional para análise de apps

### 9.2 Aprendizados
- Integração entre diferentes tipos de banco de dados
- Análise estatística aplicada a dados reais
- Visualização eficaz de dados complexos
- Implementação de casos de uso práticos

### 9.3 Impacto Acadêmico
- Demonstração de proficiência em múltiplas tecnologias
- Aplicação prática de conceitos de banco de dados
- Análise crítica e interpretação de resultados
- Comunicação técnica eficaz

---

**Equipe**: [Nomes dos integrantes]  
**Data**: [Data de entrega]  
**Disciplina**: [Nome da disciplina]  
**Professor**: [Nome do professor] 