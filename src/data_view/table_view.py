# src/data_view/table_view.py
import streamlit as st
import pandas as pd
import numpy as np
from .utils import calculate_score

def display_general_table(df):
    """
    Exibe uma tabela geral de desempenho, substituindo 0/1 por ❌/✅ etc.
    """
    acertou_cols = df.filter(like='_Acertou').columns.tolist()
    confianca_cols = df.filter(like='_Confiança').columns.tolist()

    table_data = df[acertou_cols].copy().astype(object)
    table_data.index = df['Nome']

    table_data = table_data.applymap(lambda x: '✅' if x == 1 else '❌' if x == 0 else x)

    st.write("### Tabela Geral de Desempenho")
    st.dataframe(table_data, width=1400)

def display_confidence_table(df):
    """
    Exibe a tabela de confiança com barras horizontais, etc.
    """
    confianca_cols = df.filter(like='_Confiança').columns.tolist()
    table_conf = df[confianca_cols].copy()
    table_conf.index = df['Nome']
    table_conf["Média do Aluno"] = table_conf.mean(axis=1)

    st.write("### Tabela de Confiança por Questão")

    st.data_editor(
        table_conf, 
        width=1600,
        column_config={
            col: st.column_config.ProgressColumn(
                col,
                min_value=0,
                max_value=3,
                format="%.1f"
            ) for col in confianca_cols
        } | {
            "Média do Aluno": st.column_config.ProgressColumn(
                "Média do Aluno",
                min_value=0,
                max_value=3,
                format="%.1f"
            )
        }
    )