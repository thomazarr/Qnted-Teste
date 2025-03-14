import streamlit as st

def show():
    st.subheader("Configurações do Professor")

    st.write("Aqui você pode implementar ajustes de perfil, preferências, etc.")
    # Exemplo fictício:
    nome = st.text_input("Nome do Professor", value="Professor X")
    if st.button("Salvar Configurações"):
        st.success("Configurações salvas (exemplo).")