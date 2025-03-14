import streamlit as st
from src import auth, quiz
from config import DATA_REPOSITORY 
from src import auth, aluno_dashboard, professor_dashboard

def configurar_sidebar(usuario):
    """
    Configura a sidebar com informações do usuário e posiciona o botão de logout no final.
    """
    # Exibe informações do usuário na sidebar
    st.sidebar.write(f"Logado como: {usuario['email']} ({usuario['role']})")
    
    # Injeção de CSS para fixar o botão de logout na parte inferior
    st.sidebar.markdown(
        """
        <style>
        .sidebar-footer {
            position: absolute;
            bottom: 0;
            width: 100%;
            text-align: center;
            padding: 10px 0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Container para o botão de logout
    st.sidebar.markdown('<div class="sidebar-footer">', unsafe_allow_html=True)
    if st.sidebar.button("Sair"):
        st.session_state.usuario = None
        st.sidebar.success("Logout realizado com sucesso!")
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="qntED", layout="wide")

    if "usuario" not in st.session_state:
        st.session_state.usuario = None

    if st.session_state.usuario is None:
        tab1, tab2 = st.tabs(["Login", "Cadastro"])
        with tab1:
            auth.login_page()
        with tab2:
            auth.cadastro_page()
    else:
        usuario = st.session_state.usuario
        st.sidebar.write(f"Logado como: {usuario['email']} ({usuario['role']})")
        if st.sidebar.button("Sair"):
            st.session_state.usuario = None
            st.experimental_rerun()
        st.success("Use o menu lateral 'Pages' para navegar.")

if __name__ == "__main__":
    main()