import streamlit as st

st.set_page_config(layout="wide")

# Injeção de CSS
st.markdown(
    """
    <style>
    .card {
        border: 2px solid red;
        padding: 20px;
        margin: 20px 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)
with col1:
    st.markdown(
        """
        <div class="card">
            <h2>Coluna 1</h2>
            <p>Teste de CSS</p>
        </div>
        """,
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        """
        <div class="card">
            <h2>Coluna 2</h2>
            <p>Teste de CSS</p>
        </div>
        """,
        unsafe_allow_html=True
    )