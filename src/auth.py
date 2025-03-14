import streamlit as st
from src.repository_factory import get_repository

def login_page():
    st.header("Login")
    email = st.text_input("Email", key="login_email")
    senha = st.text_input("Senha", type="password", key="login_senha")
    if st.button("Entrar"):
        repo = get_repository()
        user = repo.carregar_usuario(email)
        if user and user.get("senha") == senha:
            st.session_state.usuario = {"email": email, "role": user.get("role")}
            st.success("Login bem-sucedido!")
        else:
            st.error("Credenciais inválidas!")

def cadastro_page():
    st.header("Cadastro")
    nome = st.text_input("Nome Completo", key = "nome")
    email = st.text_input("Email para cadastro", key="cadastro_email")
    senha = st.text_input("Senha", type="password", key="cadastro_senha")
    role = st.selectbox("Perfil", options=["Aluno", "Professor"], key="cadastro_role")
    if st.button("Cadastrar"):
        repo = get_repository()
        # Verifica se o usuário já existe no Supabase
        user = repo.carregar_usuario(email)
        if user:
            st.error("Usuário já cadastrado!")
        else:
            novo_usuario = {"email": email, "senha": senha, "role": role}
            response = repo.salvar_usuario(novo_usuario)
            if response:
                st.success("Cadastro realizado com sucesso!")
            else:
                st.error("Erro ao cadastrar o usuário!")

def logout():
    if st.button("Sair"):
        st.session_state.usuario = None
        st.success("Logout realizado com sucesso!")