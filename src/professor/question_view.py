# src/professor/question_view.py

import streamlit as st

def mostrar_questao_formatada(q, exibir_id=False):
    if exibir_id and q.get("id"):
        st.markdown(f"**ID:** {q['id']}")

    enunciado_html = f"<h3>{q.get('question', '')}</h3>"
    st.markdown(enunciado_html, unsafe_allow_html=True)

    options = q.get("options", [])
    labels = ["A", "B", "C", "D"]
    st.markdown("**Alternativas:**")
    for i, alt in enumerate(options):
        label = labels[i] if i < len(labels) else str(i+1)
        if alt == q.get("answer"):
            correct_html = f"<h5 style='color: green; font-weight: bold;'>{label}) {alt} (Correta)</h5>"
            st.markdown(correct_html, unsafe_allow_html=True)
        else:
            alt_html = f"<h5>{label}) {alt}</h5>"
            st.markdown(alt_html, unsafe_allow_html=True)

    content = q.get("content") or "None"
    topic = q.get("topic") or "None"
    subtopic = q.get("subtopic") or "None"
    st.write(f"Conteúdo: {content} | Tópico: {topic} | Subtópico: {subtopic}")

    dificuldade = q.get("dificuldade") or "None"
    st.write(f"Dificuldade: {dificuldade}")