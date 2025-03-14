import streamlit as st
from src.repository_factory import get_repository

def show():
    st.subheader("Criar Questionários")

    repo = get_repository()

    # Formulário de criação de questionário
    with st.form("form_questionario", clear_on_submit=True):
        nome_questionario = st.text_input("Nome do Questionário")
        data_inicio = st.date_input("Data de Início")
        data_fim = st.date_input("Data de Fim")
        if st.form_submit_button("Publicar"):
            questionario = {
                "nome": nome_questionario,
                "data_inicio": str(data_inicio),
                "data_fim": str(data_fim),
                # Normalmente você relacionaria as questões e turmas aqui
            }
            repo.salvar_questionario(questionario)
            st.success("Questionário publicado com sucesso!")

    # Listagem de questionários
    st.write("### Questionários Cadastrados")
    qsts = repo.listar_questionarios()
    if qsts:
        for q in qsts:
            st.write(f"**ID:** {q.get('id')} | **Nome:** {q.get('nome')}")
    else:
        st.info("Nenhum questionário cadastrado.")