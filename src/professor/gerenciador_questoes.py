import streamlit as st
from src.repository_factory import get_repository
from src.professor.question_view import mostrar_questao_formatada
import json
import random

import streamlit as st
from src.repository_factory import get_repository

def editor_questao():
    st.title("Editor de Questão")

    if "ultima_questao_salva" not in st.session_state:
        st.session_state.ultima_questao_salva = None

    # === 1. Edição da Questão ===
    st.markdown("### Enunciado (com Markdown)")
    enunciado = st.text_area("Escreva o enunciado usando Markdown (ex.: `![imagem](URL)`)", height=120)

    st.markdown("### Imagem (Opcional)")
    uploaded_image = st.file_uploader("Faça upload de uma imagem (png, jpg, jpeg, gif)", type=["png","jpg","jpeg","gif"])
    
    st.markdown("### Alternativas (4)")
    alt1 = st.text_input("Alternativa 1")
    alt2 = st.text_input("Alternativa 2")
    alt3 = st.text_input("Alternativa 3")
    alt4 = st.text_input("Alternativa 4")

    st.markdown("**Resposta Correta** (selecione uma das 4 alternativas acima)")
    resposta_correta = st.selectbox("Resposta Correta", options=["1", "2", "3", "4"])

    st.markdown("### Tags (Hierarquia)")
    content = st.text_input("Conteúdo (ex.: 'Estrutura Atômica')")
    topic = st.text_input("Tópico (ex.: 'Partículas Subatômicas')")
    subtopic = st.text_input("Subtópico (ex.: 'Prótons')")

    st.markdown("### Dificuldade")
    dificuldade = st.selectbox("Selecione a dificuldade", ["Fácil", "Médio", "Difícil"])

    # --- Botão Salvar Questão ---
    if st.button("Salvar Questão"):
        map_resposta = {"1": alt1, "2": alt2, "3": alt3, "4": alt4}
        texto_resposta_correta = map_resposta.get(resposta_correta, "")

        questao = {
            "question": enunciado.strip(),
            "options": [alt1, alt2, alt3, alt4],
            "answer": texto_resposta_correta,
            "dificuldade": dificuldade,
            "tags": {
                "content": content.strip(),
                "topic": topic.strip(),
                "subtopic": subtopic.strip()
            }
        }

        repo = get_repository()
        response = repo.salvar_questao(questao)

        if response is not None:
            st.success("Questão salva com sucesso!")
            st.session_state.ultima_questao_salva = questao

            if uploaded_image is not None:
                st.session_state.ultima_questao_salva["uploaded_image"] = uploaded_image.getvalue()
        else:
            st.error("Falha ao salvar a questão.")

    # --- Botão Pré-visualizar Questão ---
    if st.session_state.ultima_questao_salva is not None:
        if st.button("Pré-visualizar Questão"):
            mostrar_questao_formatada(st.session_state.ultima_questao_salva)




