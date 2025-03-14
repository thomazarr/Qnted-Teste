import streamlit as st
import time

def quiz_page():
    st.header("Quiz")
    
    questions = [
        {
            "questao": "Qual é a capital da França?",
            "alternativas": ["Paris", "Lyon", "Marselha", "Nice"],
            "resposta": "Paris"
        },
        {
            "questao": "Qual é a cor do céu?",
            "alternativas": ["Azul", "Verde", "Vermelho", "Amarelo"],
            "resposta": "Azul"
        }
    ]
    
    num_questoes = st.selectbox("Número de questões", [1, 2], key="num_quiz")
    
    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False

    if not st.session_state.quiz_started:
        if st.button("Iniciar Quiz"):
            st.session_state.quiz_started = True
            st.session_state.quiz_index = 0
            st.session_state.quiz_respostas = []
            st.session_state.quiz_inicio = time.time()
            st.session_state.selected_questions = questions[:num_questoes]
            # Não usamos experimental_rerun; o estado foi atualizado e a interface será reexibida na próxima execução do script.
    else:
        index = st.session_state.quiz_index
        if index < len(st.session_state.selected_questions):
            question = st.session_state.selected_questions[index]
            st.write(f"**Questão {index + 1}:** {question['questao']}")
            
            resposta_aluno = st.radio("Escolha sua resposta:", options=question["alternativas"], key=f"q{index}")
            nivel_conf = st.slider("Nível de confiança (0 a 3)", 0, 3, key=f"conf{index}")
            
            if st.button("Responder", key=f"btn{index}"):
                acerto = resposta_aluno == question["resposta"]
                st.session_state.quiz_respostas.append({
                    "questao": question["questao"],
                    "resposta_aluno": resposta_aluno,
                    "acerto": acerto,
                    "nivel_conf": nivel_conf
                })
                st.session_state.quiz_index += 1
                # Ao final do ciclo, o Streamlit re-renderiza a página automaticamente, refletindo as mudanças no st.session_state.
        else:
            tempo_total = time.time() - st.session_state.quiz_inicio
            acertos = sum(1 for resp in st.session_state.quiz_respostas if resp["acerto"])
            st.subheader("Resultado do Quiz")
            st.write(f"Número de acertos: {acertos} de {len(st.session_state.selected_questions)}")
            st.write(f"Tempo total: {int(tempo_total)} segundos")
            st.write("Detalhes das respostas:")
            st.write(st.session_state.quiz_respostas)
            
            if st.button("Reiniciar Quiz"):
                for key in ["quiz_started", "quiz_index", "quiz_respostas", "quiz_inicio", "selected_questions"]:
                    if key in st.session_state:
                        del st.session_state[key]
                # A página será reexibida com o estado atualizado.