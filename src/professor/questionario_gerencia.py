# src/professor/questionario_gerencia.py

import streamlit as st
from datetime import datetime
from src.professor.questionario_repository import QuestionarioRepository
from src.professor.question_view import mostrar_questao_formatada

def gerenciar_questionarios(repo):
    st.title("Gerenciar Questionários")

    questionarios = repo.listar_questionarios()
    if not questionarios:
        st.info("Nenhum questionário cadastrado.")
        return

    for q in questionarios:
        qid = q["id"]
        titulo = q["titulo"]
        turma_id = q.get("turma_id")
        instrucoes = q.get("instrucoes")
        data_inicio = q.get("data_inicio")
        data_fim = q.get("data_fim")

        with st.expander(f"{titulo}"):
            st.write(f"**Turma ID:** {turma_id}")
            st.write(f"**Instruções:** {instrucoes}")
            st.write(f"**Início:** {data_inicio}  |  **Fim:** {data_fim}")

            col1, col2, col3 = st.columns([0.2,0.2,0.2])
            with col1:
                if st.button("Editar", key=f"edit_{qid}"):
                    # Armazena no session_state e recarrega
                    st.session_state.questionario_edit = q
                    st.rerun()
            with col2:
                if st.button("Excluir", key=f"del_{qid}"):
                    repo.excluir_questionario(qid)
                    st.success("Questionário excluído.")
                    st.rerun()
            with col3:
                if st.button("Pré-visualizar", key=f"prev_{qid}"):
                    st.session_state.questionario_preview = qid
                    st.rerun()

    # Se estiver editando
    if "questionario_edit" in st.session_state and st.session_state.questionario_edit:
        editar_questionario_form(repo)

    # Se estiver pré-visualizando
    if "questionario_preview" in st.session_state and st.session_state.questionario_preview:
        pre_visualizar_questionario(repo, st.session_state.questionario_preview)


def editar_questionario_form(repo):
    st.markdown("### Editar Questionário")
    q = st.session_state.questionario_edit
    titulo = st.text_input("Título", value=q["titulo"])
    instrucoes = st.text_area("Instruções (Markdown)", value=q.get("instrucoes",""))
    data_inicio = st.text_input("Data Início", value=q.get("data_inicio",""))
    data_fim = st.text_input("Data Fim", value=q.get("data_fim",""))

    if st.button("Salvar Edição"):
        dados = {
            "titulo": titulo.strip(),
            "instrucoes": instrucoes.strip(),
            "data_inicio": data_inicio,
            "data_fim": data_fim
        }
        repo.atualizar_questionario(q["id"], dados)
        st.success("Questionário atualizado.")
        st.session_state.questionario_edit = None
        st.rerun()

    if st.button("Cancelar"):
        st.session_state.questionario_edit = None
        st.rerun()


def pre_visualizar_questionario(repo, questionario_id):
    st.markdown("### Pré-visualizar Questionário")
    # Buscar questionario
    qlist = repo.listar_questionarios()
    questionario = None
    for x in qlist:
        if x["id"] == questionario_id:
            questionario = x
            break
    if not questionario:
        st.error("Questionário não encontrado.")
        return

    st.write(f"**Título:** {questionario['titulo']}")
    st.write(f"**Instruções:** {questionario.get('instrucoes','')}")
    st.write(f"**Início:** {questionario.get('data_inicio','')}  |  **Fim:** {questionario.get('data_fim','')}")

    # Listar questões
    questoes = repo.listar_questoes_de_questionario(questionario_id)
    for questao in questoes:
        mostrar_questao_formatada(questao, exibir_id=False)

    # Botão para simular resolução (opcional)
    if st.button("Simular Resolução"):
        st.info("Aqui você poderia exibir um fluxo de responder e ver resultado fictício.")