import streamlit as st

def show():
    # Verifica se o usuário é realmente um professor
    if st.session_state.get("usuario", {}).get("role") != "professor":
        st.error("Acesso negado.")
        st.stop()
    
    st.title("Dashboard do Professor")
    st.write("Aqui você pode gerenciar quizzes, visualizar o desempenho dos alunos e muito mais.")
    # Implemente as funcionalidades específicas para professores