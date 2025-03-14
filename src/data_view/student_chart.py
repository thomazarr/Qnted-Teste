import streamlit as st
import matplotlib.pyplot as plt

def student_chart(detalhes):
    """
    Plota um único ponto representando o resultado final do aluno:
      - Calcula internamente:
        * num_questoes = len(detalhes)
        * num_acertos = quantidade de 'acertou' == True
        * media_conf = média de 'conf'
      - Eixo X: (2 * num_acertos) - num_questoes (varia de -n..+n)
      - Eixo Y: média de confiança (0..3)
      - Cor do ponto: número de acertos (0..n) => vermelho p/ 0, verde p/ n
      - Nome do aluno fixo ou "PreviewUser" como label do círculo
    detalhes: lista de dicts, ex.:
      [
        {"numero_questao": 1, "acertou": True, "conf": 2, "score_questao": 0.857},
        {"numero_questao": 2, "acertou": False, "conf": 0, "score_questao": -0.077},
        ...
      ]
    """

    if not detalhes:
        st.write("Nenhum dado para exibir.")
        return

    # 1) Calcular métricas finais
    num_questoes = len(detalhes)
    num_acertos = sum(1 for d in detalhes if d["acertou"])
    media_conf = sum(d["conf"] for d in detalhes) / num_questoes if num_questoes else 0

    # 2) Definir "nome_aluno" (pode ser fixo no preview ou derivado de outro local)
    nome_aluno = "PreviewUser"

    # 3) Eixo X = (2 * num_acertos) - num_questoes
    x_value = (2 * num_acertos) - num_questoes
    # Eixo Y = média de confiança
    y_value = media_conf

    # A cor do ponto será o número de acertos (0..n)
    color_value = num_acertos

    # 4) Criar figura
    fig, ax = plt.subplots(figsize=(6,4))

    # 5) Plotar o ponto
    scatter = ax.scatter(
        [x_value],
        [y_value],
        c=[color_value],
        cmap='RdYlGn',      # vermelho p/ 0, verde p/ n
        edgecolors='black',
        s=200,
        vmin=0, vmax=num_questoes  # define a faixa de cor de 0..n
    )

    # Adicionar colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label(f"Acertos (0..{num_questoes})")

    # Ajustar eixos
    ax.set_xlim(-num_questoes - 1, num_questoes + 1)
    ax.set_ylim(0, 3.2)

    ax.set_xlabel(f"#Acertos - #Erros (varia de -{num_questoes} a +{num_questoes})")
    ax.set_ylabel("Média de Confiança (0..3)")

    # 6) Rótulo do ponto (nome do aluno)
    ax.annotate(
        nome_aluno,
        xy=(x_value, y_value),
        xytext=(5, 5),
        textcoords="offset points",
        ha='left',
        va='bottom',
        fontsize=9,
        color='black'
    )

    # 7) Exibir no Streamlit
    st.pyplot(fig)