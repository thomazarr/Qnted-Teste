# src/data_view/radar_view.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from .utils import split_label  # se quiser
import pandas as pd

def plot_radar_chart(df, student_name):
    """
    Cria e exibe um gráfico radar para um aluno específico com base nos conteúdos.
    """
    student_data = df[df['Nome'] == student_name]
    if student_data.empty:
        st.write("Aluno não encontrado.")
        return

    # Exemplo de radar chart, adaptado
    content_columns = [col for col in df.columns if "_Contents" in col]
    if not content_columns:
        st.write("Colunas de conteúdo não encontradas no arquivo.")
        return

    accuracy_per_content = {}
    for col in content_columns:
        content_name = student_data[col].iloc[0]
        acertou_col = col.replace("_Contents", "_Acertou")
        accuracy = 1 if student_data[acertou_col].iloc[0] == 1 else 0
        if content_name not in accuracy_per_content:
            accuracy_per_content[content_name] = []
        accuracy_per_content[content_name].append(accuracy)

    accuracy_means = {content: np.mean(values) for content, values in accuracy_per_content.items()}
    labels = list(accuracy_means.keys())
    values = list(accuracy_means.values())

    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='blue', alpha=0.3)
    ax.plot(angles, values, marker='o', color='blue')

    for angle, value in zip(angles[:-1], values[:-1]):
        ax.text(angle, value + 0.05, f"{value*100:.1f}%", ha='center', va='center', fontsize=10, color='black')

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_yticklabels([])
    ax.set_ylim(0, 1.2)

    st.pyplot(fig)

def display_all_radar_charts(df):
    student_list = df['Nome'].unique()
    for student in student_list:
        st.subheader(f"Gráfico Radar - {student}")
        plot_radar_chart(df, student)