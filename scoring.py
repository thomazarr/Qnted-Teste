import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Definição dos níveis de confiança e suas respectivas pontuações
confidence_levels = [0, 1, 2, 3]
P_S_C_A = [0.308, 0.632, 0.857, 0.973]

# Interface com sliders para ajustar os valores de penalização (α)
st.sidebar.header("Ajuste da Penalização (α)")
alpha_values = []
for C in confidence_levels:
    alpha_values.append(st.sidebar.slider(f'α (Confiança {C})', min_value=0.0, max_value=2.0, value=0.25 * (C + 1), step=0.05))

# Definição do eixo X (probabilidade de acerto)
x = np.linspace(0, 1, 100)

# Criando o gráfico
fig, ax = plt.subplots(figsize=(8, 6))

for i, C in enumerate(confidence_levels):
    score_correct = P_S_C_A[i]
    score_wrong = -alpha_values[i] * P_S_C_A[i]
    expected_score = x * score_correct + (1 - x) * score_wrong
    ax.plot(x, expected_score, label=f'Confiança {C} (α={alpha_values[i]:.2f})')

ax.set_xlabel('Probabilidade de Acerto')
ax.set_ylabel('Pontuação Esperada')
ax.set_title('Pontuação Esperada vs Probabilidade de Acerto')
ax.legend()
ax.grid(True)

# Exibir gráfico no Streamlit
st.pyplot(fig)