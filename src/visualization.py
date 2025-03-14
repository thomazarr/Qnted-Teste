import streamlit as st
import matplotlib.pyplot as plt

def plot_resultados(dados):
    # Exemplo simples de gráfico de barras
    fig, ax = plt.subplots()
    ax.bar(range(len(dados)), list(dados.values()))
    st.pyplot(fig)
    