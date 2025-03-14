# src/data_view/student_stats.py
import streamlit as st
import pandas as pd
import numpy as np
from .utils import calculate_score, P_C_given_A, alpha_values
from .radar_view import plot_radar_chart  # se quiser importar para uso aqui

def display_student_stats(df, student_name):
    """
    Exibe estatísticas (acertos, pontuação ajustada, média de confiança) de um aluno específico.
    """
    student_data = df[df['Nome'] == student_name]
    if student_data.empty:
        st.write("Aluno não encontrado.")
        return

    acertos_cols = student_data.filter(like='_Acertou').apply(pd.to_numeric, errors='coerce').fillna(0)
    confidence_cols = student_data.filter(like='_Confiança').apply(pd.to_numeric, errors='coerce').fillna(0)
    
    total_questoes = min(acertos_cols.shape[1], confidence_cols.shape[1])
    acertos = acertos_cols.values.flatten()
    confs = confidence_cols.values.flatten()

    total_acertos = int(sum(acertos))
    media_conf_total = np.mean(confs)

    # Cálculo da pontuação ajustada
    pontuacao_acertos = sum([P_C_given_A.get(int(c), 0) for a, c in zip(acertos, confs) if a == 1])
    pontuacao_erros = sum([-alpha_values.get(int(c), 0) * (1 - P_C_given_A.get(int(c), 0)) for a, c in zip(acertos, confs) if a == 0])
    pontuacao_ajustada = pontuacao_acertos + pontuacao_erros

    st.write(f"**Número de acertos:** {total_acertos} de {total_questoes}")
    st.write(f"**Pontuação ajustada:** {pontuacao_ajustada:.2f}")
    st.write(f"**Média dos níveis de confiança:** {media_conf_total:.2f}")

    # Exemplo de tabela de desempenho
    desempenho_df = pd.DataFrame({
        'Questão': list(range(1, total_questoes + 1)),
        'Acerto': ["✅" if x == 1 else "❌" for x in acertos[:total_questoes]],
        'Confiança': confs[:total_questoes],
        'Pontuação': [calculate_score(a, c) for a, c in zip(acertos[:total_questoes], confs[:total_questoes])]
    })
    st.write(desempenho_df)

    # Opcional: exibir um radar chart
    # plot_radar_chart(df, student_name)  # se quiser

def compute_student_stats(df, student_name):
    """
    Retorna um dicionário de estatísticas para um aluno (para uso em visualizações gerais).
    """
    student_data = df[df['Nome'] == student_name]
    if student_data.empty:
        return None

    acertos_cols = student_data.filter(like='_Acertou').apply(pd.to_numeric, errors='coerce').fillna(0)
    confidence_cols = student_data.filter(like='_Confiança').apply(pd.to_numeric, errors='coerce').fillna(0)

    total_questoes = min(acertos_cols.shape[1], confidence_cols.shape[1])
    acertos = acertos_cols.values.flatten()
    confs = confidence_cols.values.flatten()

    total_acertos = int(sum(acertos))
    media_conf_total = np.mean(confs)

    pontuacao_acertos = sum([P_C_given_A.get(int(c), 0) for a, c in zip(acertos, confs) if a == 1])
    pontuacao_erros = sum([-alpha_values.get(int(c), 0) * (1 - P_C_given_A.get(int(c), 0)) for a, c in zip(acertos, confs) if a == 0])
    pontuacao_ajustada = pontuacao_acertos + pontuacao_erros

    return {
        "total_questoes": total_questoes,
        "total_acertos": total_acertos,
        "media_conf_total": media_conf_total,
        "pontuacao_ajustada": pontuacao_ajustada
    }