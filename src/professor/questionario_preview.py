import streamlit as st
import time
import pandas as pd

from src.quiz_calc import calcular_resultados

# Importações das views
from src.data_view.table_view import display_general_table
from src.data_view.radar_view import plot_radar_chart
from src.data_view.student_stats import display_student_stats
from src.data_view.student_chart import student_chart

def preview_questionario(repo, questionario_id):
    """
    Exemplo de 'preview_questionario' que, ao terminar,
    chama as funções de visualização do 'data_view'
    (table_view, radar_view, student_stats).
    """

    # 1) Carregar questionário e questões
    qs_data = repo.listar_questionarios()
    questionario = next((q for q in qs_data if q["id"] == questionario_id), None)
    if not questionario:
        st.error("Questionário não encontrado.")
        return

    questoes = repo.listar_questoes_de_questionario(questionario_id)
    if not questoes:
        st.info("Nenhuma questão associada.")
        return

    # 2) Inicializar estados
    if "preview_started" not in st.session_state:
        st.session_state.preview_started = False
    if "preview_idx" not in st.session_state:
        st.session_state.preview_idx = 0
        st.session_state.preview_respostas = []
    if "preview_inicio" not in st.session_state:
        st.session_state.preview_inicio = 0.0

    # 3) Se quiz não começou
    if not st.session_state.preview_started:
        st.markdown(f"<h2>{questionario['titulo']}</h2>", unsafe_allow_html=True)
        st.markdown(questionario.get('instrucoes', ''))
        if st.button("Iniciar Quiz"):
            st.session_state.preview_started = True
            st.session_state.preview_inicio = time.time()
            st.session_state.preview_idx = 0
            st.session_state.preview_respostas = []
            st.rerun()
        return

    # 4) Se quiz acabou (idx >= len(questoes))
    idx = st.session_state.preview_idx
    if idx >= len(questoes):
        tempo_fim = time.time()
        resultados = calcular_resultados(
            questoes,
            st.session_state.preview_respostas,
            st.session_state.preview_inicio,
            tempo_fim
        )

        # Exibe resumo
        st.markdown("## Resultado Final (Preview)")
        st.success(f"Tempo total: {resultados['tempo_minutos']:.1f} min")
        st.info(f"Acertos: {resultados['num_acertos']}/{resultados['num_questoes']}")
        st.write(f"Pontuação Ajustada: **{resultados['score_total']:.2f}**")
        st.write(f"Média de Confiança: **{resultados['media_confianca']:.2f}**")

        # Agora, se quisermos usar as views do data_view, precisamos de um DataFrame "df".
        # As funções 'display_general_table', 'plot_radar_chart', 'display_student_stats'
        # tipicamente esperam colunas como 'Nome', 'X_Acertou', 'X_Confiança', etc.
        # Podemos criar um df "falso" apenas para exibição do preview.

        # Exemplo: criar df com 1 linha "Nome=PreviewUser" e colunas "Questao1_Acertou", "Questao1_Confiança", etc.
        # OU criar algo compatível com as colunas que as views esperam.
        # Abaixo é só um exemplo simples, ajustando a nomenclatura ao que as views esperam.

        # Montamos colunas do tipo: "Q1_Acertou", "Q1_Confiança", ...
        # E 'Nome' = "PreviewUser"
        data = {}
        data["Nome"] = ["PreviewUser"]

        # Precisamos iterar sobre cada questão respondida
        for i, det in enumerate(resultados["detalhes"], start=1):
            # Colunas: f"Q{i}_Acertou" => 1 ou 0
            #          f"Q{i}_Confiança" => valor
            acertou = 1 if det["acertou"] else 0
            conf = det["conf"]
            data[f"Q{i}_Acertou"] = [acertou]
            data[f"Q{i}_Confiança"] = [conf]

        # Cria o DataFrame
        df_preview = pd.DataFrame(data)

        st.write("### DataFrame para Visualização (Exemplo)")
        st.dataframe(df_preview)

        # Agora podemos chamar as funções do data_view:
        with st.expander("Ver Gráfico de Desempenho (Preview)"):
            # 'display_general_table' espera um df com colunas '_Acertou', etc.
            # Nossos colunas são "Q1_Acertou", etc. Ele filtra por 'like="_Acertou"'.
            student_chart(resultados["detalhes"])

        with st.expander("Ver Radar Chart (Preview)"):
            # 'plot_radar_chart' normalmente procura colunas "X_Contents" e "X_Acertou".
            # Se no preview não temos colunas "X_Contents", esse chart não fará sentido.
            # Exemplo de como chamá-lo:
            plot_radar_chart(df_preview, "PreviewUser")

        with st.expander("Ver Estatísticas do Aluno (Preview)"):
            # 'display_student_stats' filtra 'Nome' == 'PreviewUser'
            display_student_stats(df_preview, "PreviewUser")

        # Botão para reiniciar
        if st.button("Reiniciar Preview"):
            st.session_state.preview_started = False
            st.session_state.preview_idx = 0
            st.session_state.preview_respostas = []
            st.session_state.preview_inicio = 0.0
            st.rerun()
        return

    # 5) Caso o quiz ainda esteja rolando
    questao = questoes[idx]
    st.markdown(f"<h4>Questão {idx+1} de {len(questoes)}</h4>", unsafe_allow_html=True)
    enunciado = questao.get("question", "[Sem Enunciado]")
    st.markdown(f"<h4>{enunciado}</h4>", unsafe_allow_html=True)

    alternativas = questao.get("options", [])
    label_alternativas = [f"{chr(65+i)}) {alt}" for i, alt in enumerate(alternativas)]
    escolha = st.radio(
        "Selecione sua resposta:",
        options=range(len(label_alternativas)),
        format_func=lambda i: label_alternativas[i],
        key=f"resp_{idx}"
    )

    # Slider de confiança
    confianca = st.slider("Nível de Confiança (0=Baixa, 3=Alta)", 0, 3, 0, key=f"conf_{idx}")

    # Determinar se acertou
    resposta_correta = questao["answer"]
    alternativa_escolhida = alternativas[escolha] if escolha < len(alternativas) else ""
    acertou = (alternativa_escolhida == resposta_correta)

    # Botão
    if idx < len(questoes) - 1:
        if st.button("Avançar"):
            st.session_state.preview_respostas.append({
                "questao_id": questao["id"],
                "resposta_idx": escolha,
                "confianca": confianca,
                "acertou": acertou
            })
            st.session_state.preview_idx += 1
            st.rerun()
    else:
        if st.button("Finalizar Quiz"):
            st.session_state.preview_respostas.append({
                "questao_id": questao["id"],
                "resposta_idx": escolha,
                "confianca": confianca,
                "acertou": acertou
            })
            st.session_state.preview_idx += 1
            st.rerun()