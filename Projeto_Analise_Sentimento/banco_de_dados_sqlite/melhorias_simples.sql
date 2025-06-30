-- =====================================================
-- MELHORIAS SIMPLES PARA SQLITE - BASEADAS NOS DADOS EXISTENTES
-- =====================================================

-- Este script adiciona funcionalidades simples ao SQLite atual
-- aproveitando os dados que já existem no arquivo CSV

-- =====================================================
-- 1. ADICIONAR COLUNAS À TABELA REVIEWS EXISTENTE
-- =====================================================

-- Adicionar colunas para métricas de texto que já existem no CSV
ALTER TABLE Reviews ADD COLUMN char_count INTEGER;
ALTER TABLE Reviews ADD COLUMN word_count INTEGER;
ALTER TABLE Reviews ADD COLUMN has_noise BOOLEAN;
ALTER TABLE Reviews ADD COLUMN sentiment_label VARCHAR(20);
ALTER TABLE Reviews ADD COLUMN model_sentiment VARCHAR(20);

-- =====================================================
-- 2. CRIAR ÍNDICES PARA PERFORMANCE
-- =====================================================

CREATE INDEX idx_reviews_word_count ON Reviews(word_count);
CREATE INDEX idx_reviews_has_noise ON Reviews(has_noise);
CREATE INDEX idx_reviews_sentiment ON Reviews(sentiment_label);
CREATE INDEX idx_reviews_char_count ON Reviews(char_count);

-- =====================================================
-- 3. CRIAR VIEW PARA ANÁLISE DE QUALIDADE
-- =====================================================

CREATE VIEW analise_qualidade_reviews AS
SELECT 
    a.nome as app,
    COUNT(*) as total_reviews,
    ROUND(AVG(r.score), 2) as media_score,
    
    -- Análise por tamanho do texto
    COUNT(CASE WHEN r.word_count <= 5 THEN 1 END) as reviews_curtas,
    COUNT(CASE WHEN r.word_count BETWEEN 6 AND 20 THEN 1 END) as reviews_medias,
    COUNT(CASE WHEN r.word_count > 20 THEN 1 END) as reviews_longas,
    
    -- Análise de ruído
    COUNT(CASE WHEN r.has_noise = 1 THEN 1 END) as reviews_com_ruido,
    COUNT(CASE WHEN r.has_noise = 0 THEN 1 END) as reviews_sem_ruido,
    
    -- Análise de sentimento
    COUNT(CASE WHEN r.sentiment_label = 'positivo' THEN 1 END) as sentimentos_positivos,
    COUNT(CASE WHEN r.sentiment_label = 'negativo' THEN 1 END) as sentimentos_negativos,
    COUNT(CASE WHEN r.sentiment_label = 'neutro' THEN 1 END) as sentimentos_neutros,
    
    -- Correlação sentimento vs score
    ROUND(AVG(CASE WHEN r.sentiment_label = 'positivo' THEN r.score END), 2) as media_score_positivo,
    ROUND(AVG(CASE WHEN r.sentiment_label = 'negativo' THEN r.score END), 2) as media_score_negativo,
    ROUND(AVG(CASE WHEN r.sentiment_label = 'neutro' THEN r.score END), 2) as media_score_neutro
    
FROM Reviews r
JOIN Aplicativos a ON r.id_app = a.id_app
GROUP BY a.nome;

-- =====================================================
-- 4. CONSULTAS ÚTEIS DE EXEMPLO
-- =====================================================

-- Consulta 1: Análise de correlação entre tamanho e score
-- (Execute separadamente)
/*
SELECT 
    a.nome as app,
    CASE 
        WHEN r.word_count <= 5 THEN 'Muito Curta (≤5 palavras)'
        WHEN r.word_count <= 10 THEN 'Curta (6-10 palavras)'
        WHEN r.word_count <= 20 THEN 'Média (11-20 palavras)'
        ELSE 'Longa (>20 palavras)'
    END as tamanho_review,
    COUNT(*) as total_reviews,
    ROUND(AVG(r.score), 2) as media_score,
    ROUND(AVG(r.word_count), 1) as media_palavras
FROM Reviews r
JOIN Aplicativos a ON r.id_app = a.id_app
WHERE r.word_count IS NOT NULL
GROUP BY a.nome, 
    CASE 
        WHEN r.word_count <= 5 THEN 'Muito Curta (≤5 palavras)'
        WHEN r.word_count <= 10 THEN 'Curta (6-10 palavras)'
        WHEN r.word_count <= 20 THEN 'Média (11-20 palavras)'
        ELSE 'Longa (>20 palavras)'
    END
ORDER BY a.nome, media_score DESC;
*/

-- Consulta 2: Análise de qualidade por app
-- (Execute separadamente)
/*
SELECT 
    a.nome as app,
    COUNT(*) as total_reviews,
    ROUND(COUNT(CASE WHEN r.has_noise = 0 THEN 1 END) * 100.0 / COUNT(*), 2) as pct_reviews_limpas,
    ROUND(COUNT(CASE WHEN r.word_count > 5 THEN 1 END) * 100.0 / COUNT(*), 2) as pct_reviews_detalhadas,
    ROUND(COUNT(CASE WHEN r.sentiment_label = r.model_sentiment THEN 1 END) * 100.0 / COUNT(*), 2) as pct_sentimentos_concordantes
FROM Reviews r
JOIN Aplicativos a ON r.id_app = a.id_app
WHERE r.has_noise IS NOT NULL
GROUP BY a.nome
ORDER BY pct_reviews_limpas DESC;
*/

-- Consulta 3: Comparação entre sentimento manual vs modelo
-- (Execute separadamente)
/*
SELECT 
    a.nome as app,
    COUNT(*) as total_reviews,
    COUNT(CASE WHEN r.sentiment_label = r.model_sentiment THEN 1 END) as sentimentos_iguais,
    COUNT(CASE WHEN r.sentiment_label != r.model_sentiment THEN 1 END) as sentimentos_diferentes,
    ROUND(COUNT(CASE WHEN r.sentiment_label = r.model_sentiment THEN 1 END) * 100.0 / COUNT(*), 2) as pct_concordancia
FROM Reviews r
JOIN Aplicativos a ON r.id_app = a.id_app
WHERE r.sentiment_label IS NOT NULL AND r.model_sentiment IS NOT NULL
GROUP BY a.nome
ORDER BY pct_concordancia DESC;
*/

-- =====================================================
-- 5. INSTRUÇÕES DE USO
-- =====================================================

/*
COMO USAR ESTAS MELHORIAS:

1. Execute este script para adicionar as colunas e criar a view
2. Processe o arquivo CSV para popular as novas colunas com dados
3. Use a view para análises rápidas:
   SELECT * FROM analise_qualidade_reviews;

4. Execute as consultas comentadas para análises específicas

BENEFÍCIOS:
- Aproveita dados que já existem no CSV
- Análise de qualidade das reviews
- Correlação entre tamanho, sentimento e score
- Implementação simples e prática
- Performance otimizada com índices

DADOS QUE SERÃO ANALISADOS:
- Tamanho das reviews (caracteres e palavras)
- Presença de ruído/noise
- Sentimentos (manual vs modelo)
- Correlações entre diferentes métricas
*/ 