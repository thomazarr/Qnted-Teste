import streamlit as st

def configurar_sidebar(usuario):
    """
    Configura a sidebar com informações do usuário e posiciona o botão de logout na parte inferior.
    """
    # Informações do usuário
    st.sidebar.write(f"Logado como: {usuario['email']} ({usuario['role']})")
    
    # CSS para posicionar o botão de logout no final da sidebar
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
    
    st.sidebar.markdown('<div class="sidebar-footer">', unsafe_allow_html=True)
    if st.sidebar.button("Sair"):
        st.session_state.usuario = None
        # Limpa a variável de página ao sair
        if "page" in st.session_state:
            del st.session_state.page
        st.sidebar.success("Logout realizado com sucesso!")
    st.sidebar.markdown('</div>', unsafe_allow_html=True)