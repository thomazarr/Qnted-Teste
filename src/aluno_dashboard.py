import streamlit as st

def show():
    # Verifica se o usuário é realmente um aluno
    if st.session_state.get("usuario", {}).get("role") != "aluno":
        st.error("Acesso negado.")
        st.stop()
    
    st.title("Dashboard do Aluno")
    st.write("Bem-vindo! Aqui você pode iniciar quizzes, ver seu histórico e acompanhar seu progresso.")
    # Implemente as funcionalidades específicas para alunos