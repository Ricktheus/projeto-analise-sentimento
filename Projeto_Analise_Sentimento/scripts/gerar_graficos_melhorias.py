#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar gráficos das análises melhoradas do SQLite
Baseado nas novas funcionalidades implementadas
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import numpy as np
from pathlib import Path

# Configurações de estilo
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
plt.rcParams['font.size'] = 10
plt.rcParams['figure.figsize'] = (12, 8)

# Configurar para português
plt.rcParams['font.family'] = 'DejaVu Sans'

def conectar_sqlite():
    """Conecta ao banco SQLite"""
    try:
        conn = sqlite3.connect('../banco_de_dados_sqlite/database.db')
        return conn
    except:
        # Se não existir, criar dados simulados
        return None

def criar_dados_simulados():
    """Cria dados simulados para demonstração"""
    np.random.seed(42)
    
    # Dados simulados baseados no CSV original
    apps = ['WhatsApp', 'Facebook Messenger', 'Skype', 'Viber', 'LINE']
    
    dados = []
    for app in apps:
        n_reviews = np.random.randint(800, 1200)
        
        for i in range(n_reviews):
            score = np.random.choice([1, 2, 3, 4, 5], p=[0.1, 0.15, 0.2, 0.3, 0.25])
            word_count = np.random.randint(1, 50)
            char_count = word_count * 5 + np.random.randint(-10, 10)
            has_noise = np.random.choice([0, 1], p=[0.7, 0.3])
            
            # Sentimento baseado no score
            if score >= 4:
                sentiment = 'positivo'
            elif score <= 2:
                sentiment = 'negativo'
            else:
                sentiment = 'neutro'
            
            dados.append({
                'app': app,
                'score': score,
                'word_count': word_count,
                'char_count': char_count,
                'has_noise': has_noise,
                'sentiment_label': sentiment,
                'model_sentiment': sentiment
            })
    
    return pd.DataFrame(dados)

def gerar_grafico_1_analise_qualidade(df):
    """Gráfico 1: Análise de Qualidade por App"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Análise de Qualidade das Reviews por Aplicativo', fontsize=16, fontweight='bold')
    
    # 1. Média de Score por App
    media_scores = df.groupby('app')['score'].mean().sort_values(ascending=False)
    bars1 = ax1.bar(media_scores.index, media_scores.values, color='skyblue', alpha=0.8)
    ax1.set_title('Média de Score por Aplicativo')
    ax1.set_ylabel('Score Médio')
    ax1.set_ylim(0, 5)
    ax1.tick_params(axis='x', rotation=45)
    
    # Adicionar valores nas barras
    for bar, value in zip(bars1, media_scores.values):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, 
                f'{value:.2f}', ha='center', va='bottom', fontweight='bold')
    
    # 2. Distribuição de Sentimentos
    sentimentos = df.groupby(['app', 'sentiment_label']).size().unstack(fill_value=0)
    sentimentos.plot(kind='bar', stacked=True, ax=ax2, color=['#ff6b6b', '#4ecdc4', '#45b7d1'])
    ax2.set_title('Distribuição de Sentimentos por App')
    ax2.set_ylabel('Número de Reviews')
    ax2.tick_params(axis='x', rotation=45)
    ax2.legend(title='Sentimento')
    
    # 3. Percentual de Reviews sem Ruído
    pct_sem_ruido = df.groupby('app')['has_noise'].apply(lambda x: (x == 0).mean() * 100)
    bars3 = ax3.bar(pct_sem_ruido.index, pct_sem_ruido.values, color='lightgreen', alpha=0.8)
    ax3.set_title('Percentual de Reviews sem Ruído')
    ax3.set_ylabel('Percentual (%)')
    ax3.set_ylim(0, 100)
    ax3.tick_params(axis='x', rotation=45)
    
    # Adicionar valores nas barras
    for bar, value in zip(bars3, pct_sem_ruido.values):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                f'{value:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    # 4. Média de Palavras por App
    media_palavras = df.groupby('app')['word_count'].mean().sort_values(ascending=False)
    bars4 = ax4.bar(media_palavras.index, media_palavras.values, color='orange', alpha=0.8)
    ax4.set_title('Média de Palavras por Review')
    ax4.set_ylabel('Número de Palavras')
    ax4.tick_params(axis='x', rotation=45)
    
    # Adicionar valores nas barras
    for bar, value in zip(bars4, media_palavras.values):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2, 
                f'{value:.1f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('../dashboard_bi/01_analise_qualidade_por_app.png', dpi=300, bbox_inches='tight')
    plt.close()

def gerar_grafico_2_correlacao_tamanho_score(df):
    """Gráfico 2: Correlação entre Tamanho e Score"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Correlação entre Tamanho das Reviews e Score', fontsize=16, fontweight='bold')
    
    # Definir categorias de tamanho
    df['tamanho_categoria'] = pd.cut(df['word_count'], 
                                    bins=[0, 5, 10, 20, 100], 
                                    labels=['Muito Curta (≤5)', 'Curta (6-10)', 'Média (11-20)', 'Longa (>20)'])
    
    # 1. Média de Score por Categoria de Tamanho
    media_por_tamanho = df.groupby('tamanho_categoria')['score'].mean()
    bars1 = ax1.bar(media_por_tamanho.index, media_por_tamanho.values, color='purple', alpha=0.8)
    ax1.set_title('Média de Score por Tamanho da Review')
    ax1.set_ylabel('Score Médio')
    ax1.set_ylim(0, 5)
    ax1.tick_params(axis='x', rotation=45)
    
    # Adicionar valores nas barras
    for bar, value in zip(bars1, media_por_tamanho.values):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, 
                f'{value:.2f}', ha='center', va='bottom', fontweight='bold')
    
    # 2. Distribuição de Tamanhos por App
    tamanhos_por_app = df.groupby(['app', 'tamanho_categoria']).size().unstack(fill_value=0)
    tamanhos_por_app.plot(kind='bar', stacked=True, ax=ax2, 
                         color=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'])
    ax2.set_title('Distribuição de Tamanhos por App')
    ax2.set_ylabel('Número de Reviews')
    ax2.tick_params(axis='x', rotation=45)
    ax2.legend(title='Tamanho', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # 3. Scatter plot: Palavras vs Score
    ax3.scatter(df['word_count'], df['score'], alpha=0.6, s=20)
    ax3.set_xlabel('Número de Palavras')
    ax3.set_ylabel('Score')
    ax3.set_title('Correlação: Palavras vs Score')
    ax3.grid(True, alpha=0.3)
    
    # Adicionar linha de tendência
    z = np.polyfit(df['word_count'], df['score'], 1)
    p = np.poly1d(z)
    ax3.plot(df['word_count'], p(df['word_count']), "r--", alpha=0.8)
    
    # 4. Percentual de Sentimentos por Tamanho
    sentimentos_por_tamanho = df.groupby(['tamanho_categoria', 'sentiment_label']).size().unstack(fill_value=0)
    sentimentos_por_tamanho_pct = sentimentos_por_tamanho.div(sentimentos_por_tamanho.sum(axis=1), axis=0) * 100
    sentimentos_por_tamanho_pct.plot(kind='bar', stacked=True, ax=ax4, 
                                    color=['#ff6b6b', '#4ecdc4', '#45b7d1'])
    ax4.set_title('Percentual de Sentimentos por Tamanho')
    ax4.set_ylabel('Percentual (%)')
    ax4.tick_params(axis='x', rotation=45)
    ax4.legend(title='Sentimento', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    plt.savefig('../dashboard_bi/02_correlacao_tamanho_score.png', dpi=300, bbox_inches='tight')
    plt.close()

def gerar_grafico_3_categorizacao_inteligente(df):
    """Gráfico 3: Sistema de Categorização Inteligente"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Sistema de Categorização Inteligente de Reviews', fontsize=16, fontweight='bold')
    
    # Criar categorias baseadas nos critérios
    def categorizar_review(row):
        if row['word_count'] > 10 and row['sentiment_label'] == 'positivo':
            return 'Reviews Detalhadas Positivas'
        elif row['word_count'] > 10 and row['sentiment_label'] == 'negativo':
            return 'Reviews Críticas Detalhadas'
        elif row['word_count'] <= 5 and row['sentiment_label'] == 'positivo':
            return 'Reviews Simples Positivas'
        elif row['has_noise'] == 1:
            return 'Reviews com Ruído'
        elif row['has_noise'] == 0 and row['word_count'] > 10:
            return 'Reviews de Alta Qualidade'
        elif row['word_count'] > 10 and row['sentiment_label'] == 'neutro':
            return 'Reviews Neutras Detalhadas'
        elif row['score'] in [1, 5]:
            return 'Reviews Extremas'
        else:
            return 'Reviews Balanceadas'
    
    df['categoria'] = df.apply(categorizar_review, axis=1)
    
    # 1. Distribuição de Categorias por App
    categorias_por_app = df.groupby(['app', 'categoria']).size().unstack(fill_value=0)
    categorias_por_app.plot(kind='bar', stacked=True, ax=ax1, 
                           colormap='tab10')
    ax1.set_title('Distribuição de Categorias por App')
    ax1.set_ylabel('Número de Reviews')
    ax1.tick_params(axis='x', rotation=45)
    ax1.legend(title='Categoria', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # 2. Média de Score por Categoria
    media_score_categoria = df.groupby('categoria')['score'].mean().sort_values(ascending=False)
    bars2 = ax2.bar(range(len(media_score_categoria)), media_score_categoria.values, 
                    color=plt.cm.Set3(np.linspace(0, 1, len(media_score_categoria))))
    ax2.set_title('Média de Score por Categoria')
    ax2.set_ylabel('Score Médio')
    ax2.set_xticks(range(len(media_score_categoria)))
    ax2.set_xticklabels(media_score_categoria.index, rotation=45, ha='right')
    ax2.set_ylim(0, 5)
    
    # Adicionar valores nas barras
    for i, value in enumerate(media_score_categoria.values):
        ax2.text(i, value + 0.05, f'{value:.2f}', ha='center', va='bottom', fontweight='bold')
    
    # 3. Percentual de Categorias por App
    pct_categorias = df.groupby(['app', 'categoria']).size().unstack(fill_value=0)
    pct_categorias = pct_categorias.div(pct_categorias.sum(axis=1), axis=0) * 100
    pct_categorias.plot(kind='bar', stacked=True, ax=ax3, colormap='tab10')
    ax3.set_title('Percentual de Categorias por App')
    ax3.set_ylabel('Percentual (%)')
    ax3.tick_params(axis='x', rotation=45)
    ax3.legend(title='Categoria', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # 4. Análise de Qualidade por Categoria
    qualidade_categoria = df.groupby('categoria').agg({
        'has_noise': lambda x: (x == 0).mean() * 100,
        'word_count': 'mean'
    }).round(2)
    
    x = np.arange(len(qualidade_categoria))
    width = 0.35
    
    bars4a = ax4.bar(x - width/2, qualidade_categoria['has_noise'], width, 
                     label='% Sem Ruído', color='lightblue', alpha=0.8)
    ax4_twin = ax4.twinx()
    bars4b = ax4_twin.bar(x + width/2, qualidade_categoria['word_count'], width, 
                          label='Média Palavras', color='lightcoral', alpha=0.8)
    
    ax4.set_title('Análise de Qualidade por Categoria')
    ax4.set_ylabel('Percentual Sem Ruído (%)')
    ax4_twin.set_ylabel('Média de Palavras')
    ax4.set_xticks(x)
    ax4.set_xticklabels(qualidade_categoria.index, rotation=45, ha='right')
    
    # Adicionar valores nas barras
    for bar, value in zip(bars4a, qualidade_categoria['has_noise']):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                f'{value:.1f}%', ha='center', va='bottom', fontsize=8)
    
    for bar, value in zip(bars4b, qualidade_categoria['word_count']):
        ax4_twin.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2, 
                     f'{value:.1f}', ha='center', va='bottom', fontsize=8)
    
    ax4.legend(loc='upper left')
    ax4_twin.legend(loc='upper right')
    
    plt.tight_layout()
    plt.savefig('../dashboard_bi/03_categorizacao_inteligente.png', dpi=300, bbox_inches='tight')
    plt.close()

def gerar_grafico_4_deteccao_anomalias(df):
    """Gráfico 4: Detecção de Anomalias"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Sistema de Detecção de Anomalias', fontsize=16, fontweight='bold')
    
    # Calcular estatísticas por app
    stats_app = df.groupby('app').agg({
        'score': ['mean', 'std', 'count']
    }).round(2)
    stats_app.columns = ['media_score', 'desvio_score', 'total_reviews']
    
    # Identificar anomalias
    anomalias = []
    for app in df['app'].unique():
        app_data = df[df['app'] == app]
        media = app_data['score'].mean()
        desvio = app_data['score'].std()
        
        for _, row in app_data.iterrows():
            z_score = abs(row['score'] - media) / desvio if desvio > 0 else 0
            if z_score > 1.5:
                anomalias.append({
                    'app': app,
                    'score': row['score'],
                    'media_app': media,
                    'z_score': z_score,
                    'diferenca': abs(row['score'] - media),
                    'tipo': 'Alto' if row['score'] > media else 'Baixo'
                })
    
    anomalias_df = pd.DataFrame(anomalias)
    
    # 1. Distribuição de Scores com Anomalias Destacadas
    for app in df['app'].unique():
        app_data = df[df['app'] == app]
        app_anomalias = anomalias_df[anomalias_df['app'] == app]
        
        ax1.hist(app_data['score'], alpha=0.6, label=app, bins=5)
        
        # Destacar anomalias
        if not app_anomalias.empty:
            ax1.scatter(app_anomalias['score'], [0]*len(app_anomalias), 
                       color='red', s=100, marker='x', label=f'{app} - Anomalias')
    
    ax1.set_title('Distribuição de Scores com Anomalias')
    ax1.set_xlabel('Score')
    ax1.set_ylabel('Frequência')
    ax1.legend()
    
    # 2. Top Anomalias por Z-Score
    if not anomalias_df.empty:
        top_anomalias = anomalias_df.nlargest(10, 'z_score')
        bars2 = ax2.barh(range(len(top_anomalias)), top_anomalias['z_score'], 
                        color=['red' if x == 'Baixo' else 'orange' for x in top_anomalias['tipo']])
        ax2.set_yticks(range(len(top_anomalias)))
        ax2.set_yticklabels([f"{row['app']} (Score: {row['score']})" for _, row in top_anomalias.iterrows()])
        ax2.set_xlabel('Z-Score')
        ax2.set_title('Top 10 Anomalias por Z-Score')
        
        # Adicionar valores nas barras
        for i, (bar, value) in enumerate(zip(bars2, top_anomalias['z_score'])):
            ax2.text(value + 0.05, bar.get_y() + bar.get_height()/2, 
                    f'{value:.2f}', ha='left', va='center', fontweight='bold')
    else:
        ax2.text(0.5, 0.5, 'Nenhuma anomalia detectada', ha='center', va='center', 
                transform=ax2.transAxes, fontsize=12)
        ax2.set_title('Anomalias Detectadas')
    
    # 3. Anomalias por App
    if not anomalias_df.empty:
        anomalias_por_app = anomalias_df.groupby('app').size()
        bars3 = ax3.bar(anomalias_por_app.index, anomalias_por_app.values, color='lightcoral', alpha=0.8)
        ax3.set_title('Número de Anomalias por App')
        ax3.set_ylabel('Número de Anomalias')
        ax3.tick_params(axis='x', rotation=45)
        
        # Adicionar valores nas barras
        for bar, value in zip(bars3, anomalias_por_app.values):
            ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                    str(value), ha='center', va='bottom', fontweight='bold')
    else:
        ax3.text(0.5, 0.5, 'Nenhuma anomalia detectada', ha='center', va='center', 
                transform=ax3.transAxes, fontsize=12)
        ax3.set_title('Anomalias por App')
    
    # 4. Box Plot de Scores por App
    df.boxplot(column='score', by='app', ax=ax4)
    ax4.set_title('Distribuição de Scores por App')
    ax4.set_xlabel('Aplicativo')
    ax4.set_ylabel('Score')
    ax4.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('../dashboard_bi/04_deteccao_anomalias.png', dpi=300, bbox_inches='tight')
    plt.close()

def gerar_grafico_5_ranking_comparativo(df):
    """Gráfico 5: Ranking Comparativo Entre Apps"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Ranking Comparativo Entre Aplicativos', fontsize=16, fontweight='bold')
    
    # Calcular métricas para ranking
    ranking_metrics = df.groupby('app').agg({
        'score': ['mean', 'count'],
        'word_count': 'mean',
        'has_noise': lambda x: (x == 0).mean() * 100,
        'sentiment_label': lambda x: (x == 'positivo').mean() * 100
    }).round(2)
    
    ranking_metrics.columns = ['media_score', 'total_reviews', 'media_palavras', 'pct_sem_ruido', 'pct_positivo']
    
    # 1. Ranking por Score
    ranking_score = ranking_metrics.sort_values('media_score', ascending=False)
    bars1 = ax1.bar(range(len(ranking_score)), ranking_score['media_score'], 
                    color=plt.cm.viridis(np.linspace(0, 1, len(ranking_score))))
    ax1.set_title('Ranking por Score Médio')
    ax1.set_ylabel('Score Médio')
    ax1.set_xticks(range(len(ranking_score)))
    ax1.set_xticklabels(ranking_score.index, rotation=45)
    ax1.set_ylim(0, 5)
    
    # Adicionar valores nas barras
    for i, value in enumerate(ranking_score['media_score']):
        ax1.text(i, value + 0.05, f'{value:.2f}', ha='center', va='bottom', fontweight='bold')
    
    # 2. Ranking por Qualidade (sem ruído)
    ranking_qualidade = ranking_metrics.sort_values('pct_sem_ruido', ascending=False)
    bars2 = ax2.bar(range(len(ranking_qualidade)), ranking_qualidade['pct_sem_ruido'], 
                    color=plt.cm.plasma(np.linspace(0, 1, len(ranking_qualidade))))
    ax2.set_title('Ranking por Qualidade (Reviews sem Ruído)')
    ax2.set_ylabel('Percentual sem Ruído (%)')
    ax2.set_xticks(range(len(ranking_qualidade)))
    ax2.set_xticklabels(ranking_qualidade.index, rotation=45)
    ax2.set_ylim(0, 100)
    
    # Adicionar valores nas barras
    for i, value in enumerate(ranking_qualidade['pct_sem_ruido']):
        ax2.text(i, value + 1, f'{value:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    # 3. Radar Chart - Múltiplas Métricas
    categories = ['Score', 'Qualidade', 'Detalhamento', 'Sentimento']
    
    # Normalizar métricas para 0-100
    score_norm = (ranking_metrics['media_score'] / 5) * 100
    qualidade_norm = ranking_metrics['pct_sem_ruido']
    detalhamento_norm = (ranking_metrics['media_palavras'] / ranking_metrics['media_palavras'].max()) * 100
    sentimento_norm = ranking_metrics['pct_positivo']
    
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]  # Fechar o círculo
    
    # Plotar para cada app
    colors = plt.cm.Set3(np.linspace(0, 1, len(ranking_metrics)))
    for i, (app, color) in enumerate(zip(ranking_metrics.index, colors)):
        values = [score_norm[app], qualidade_norm[app], detalhamento_norm[app], sentimento_norm[app]]
        values += values[:1]  # Fechar o círculo
        ax3.plot(angles, values, 'o-', linewidth=2, label=app, color=color)
        ax3.fill(angles, values, alpha=0.25, color=color)
    
    ax3.set_xticks(angles[:-1])
    ax3.set_xticklabels(categories)
    ax3.set_ylim(0, 100)
    ax3.set_title('Comparação Multidimensional')
    ax3.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax3.grid(True)
    
    # 4. Heatmap de Correlação
    correlation_data = ranking_metrics[['media_score', 'pct_sem_ruido', 'media_palavras', 'pct_positivo']]
    correlation_matrix = correlation_data.corr()
    
    im = ax4.imshow(correlation_matrix, cmap='coolwarm', vmin=-1, vmax=1)
    ax4.set_xticks(range(len(correlation_matrix.columns)))
    ax4.set_yticks(range(len(correlation_matrix.columns)))
    ax4.set_xticklabels(correlation_matrix.columns, rotation=45)
    ax4.set_yticklabels(correlation_matrix.columns)
    ax4.set_title('Correlação entre Métricas')
    
    # Adicionar valores no heatmap
    for i in range(len(correlation_matrix.columns)):
        for j in range(len(correlation_matrix.columns)):
            text = ax4.text(j, i, f'{correlation_matrix.iloc[i, j]:.2f}',
                           ha="center", va="center", color="black", fontweight='bold')
    
    plt.colorbar(im, ax=ax4)
    
    plt.tight_layout()
    plt.savefig('../dashboard_bi/05_ranking_comparativo.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    """Função principal"""
    print("Gerando gráficos das análises melhoradas...")
    
    # Conectar ao banco ou criar dados simulados
    conn = conectar_sqlite()
    if conn:
        # Tentar ler dados do SQLite
        try:
            df = pd.read_sql_query("""
                SELECT a.nome as app, r.score, r.word_count, r.char_count, 
                       r.has_noise, r.sentiment_label, r.model_sentiment
                FROM Reviews r
                JOIN Aplicativos a ON r.id_app = a.id_app
                WHERE r.word_count IS NOT NULL
            """, conn)
            conn.close()
        except:
            print("Usando dados simulados...")
            df = criar_dados_simulados()
    else:
        print("Usando dados simulados...")
        df = criar_dados_simulados()
    
    # Criar diretório se não existir
    Path('../dashboard_bi').mkdir(exist_ok=True)
    
    # Gerar gráficos
    print("Gerando Gráfico 1: Análise de Qualidade...")
    gerar_grafico_1_analise_qualidade(df)
    
    print("Gerando Gráfico 2: Correlação Tamanho-Score...")
    gerar_grafico_2_correlacao_tamanho_score(df)
    
    print("Gerando Gráfico 3: Categorização Inteligente...")
    gerar_grafico_3_categorizacao_inteligente(df)
    
    print("Gerando Gráfico 4: Detecção de Anomalias...")
    gerar_grafico_4_deteccao_anomalias(df)
    
    print("Gerando Gráfico 5: Ranking Comparativo...")
    gerar_grafico_5_ranking_comparativo(df)
    
    print("Gráficos gerados com sucesso!")
    print("Arquivos salvos em: ../dashboard_bi/")

if __name__ == "__main__":
    main() 