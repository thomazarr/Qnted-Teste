# src/data_view/general_stats.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from .student_stats import compute_student_stats

def display_all_stats(df):
    """
    Exibe um gráfico de dispersão com as estatísticas de todos os alunos.
    """
    student_list = df['Nome'].unique()
    stats_list = []
    for student in student_list:
        stats = compute_student_stats(df, student)
        if stats is not None:
            stats['Nome'] = student
            stats_list.append(stats)
    if stats_list:
        stats_df = pd.DataFrame(stats_list)
        fig, ax = plt.subplots(figsize=(9, 4))
        ax.set_title("Estatísticas dos Alunos")
        scatter = ax.scatter(
            stats_df['total_acertos'],
            stats_df['media_conf_total'],
            c=stats_df['pontuacao_ajustada'],
            cmap='RdYlGn',
            s=100,
            edgecolors='black'
        )
        for i, row in stats_df.iterrows():
            ax.annotate(row['pontuacao_ajustada'], (row['total_acertos'], row['media_conf_total']),
                        textcoords="offset points", xytext=(5, 5), fontsize=9)
        ax.set_xlabel("Número de Questões Corretas")
        ax.set_ylabel("Média do Nível de Confiança")
        ax.set_ylim(0, 3)
        cbar = plt.colorbar(scatter, label="Pontuação")
        st.pyplot(fig)
    else:
        st.write("Nenhum dado disponível para exibir estatísticas.")