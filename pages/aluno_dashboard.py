import streamlit as st

# Verifica se o usuário está autenticado e tem o role "aluno"
if "usuario" not in st.session_state or st.session_state.usuario.get("role") != "Aluno":
    st.error("Acesso negado. Você não tem permissão para ver esta página.")
    st.stop()

st.title("Dashboard do Aluno")
st.write("Bem-vindo! Aqui você pode iniciar quizzes, ver seu histórico de resultados e acompanhar seu progresso.")

# Funções adicionais:
# - Lista de quizzes disponíveis
# - Histórico de resultados
# - Visualização do progresso (gráficos, mapas de conhecimento, etc.)