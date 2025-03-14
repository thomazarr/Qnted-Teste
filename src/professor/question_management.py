# src/professor/question_management.py

import streamlit as st
from src.professor.question_repository import SupabaseRepository
from src.professor.question_view import mostrar_questao_formatada
from src.professor.question_filters import filtrar_questoes_local

def gerenciar_questoes_salvas(repo):
    """
    Exibe os filtros (multiselect) e lista as questões com botões de editar/excluir/exportar.
    """
    st.header("Gerenciar Questões Salvas")

    # 1. Carregar todas as questões do banco
    questoes = repo.listar_questoes()
    if not questoes:
        st.info("Nenhuma questão cadastrada no banco.")
        return

    # 2. Carregar distinct contents/topics/subtopics (se quiser local)
    all_contents = sorted(list(set(q.get("content", "None") for q in questoes if q.get("content"))))
    all_topics = sorted(list(set(q.get("topic", "None") for q in questoes if q.get("topic"))))
    all_subtopics = sorted(list(set(q.get("subtopic", "None") for q in questoes if q.get("subtopic"))))

    # 3. Filtros encadeados (simples, local)
    selected_contents = st.multiselect("Conteúdos disponíveis", options=all_contents)
    selected_topics = st.multiselect("Tópicos disponíveis", options=all_topics)
    selected_subtopics = st.multiselect("Subtópicos disponíveis", options=all_subtopics)

    questoes_filtradas = filtrar_questoes_local(questoes, selected_contents, selected_topics, selected_subtopics)

    st.markdown(f"Total de questões filtradas: {len(questoes_filtradas)}")

    # 4. Exibir formulário de edição, se existir
    if "editando_questao" not in st.session_state:
        st.session_state.editando_questao = None

    if st.session_state.editando_questao:
        editar_questao_form(repo)

    # 5. Listar cada questão
    for q in questoes_filtradas:
        # Se for a mesma questão que estamos editando, talvez ocultar
        if st.session_state.editando_questao and st.session_state.editando_questao.get("id") == q.get("id"):
            continue

        mostrar_questao_formatada(q, exibir_id=False)
        col1, col2, col3 = st.columns([0.2, 0.2, 0.2])
        with col1:
            if st.button("Editar", key=f"edit_{q.get('id')}"):
                st.session_state.editando_questao = q
                st.rerun()
        with col2:
            if st.button("Excluir", key=f"del_{q.get('id')}"):
                repo.excluir_questao(q.get('id'))
                st.success("Questão excluída com sucesso!")
                st.rerun()
        with col3:
            if st.button("Exportar", key=f"export_{q.get('id')}"):
                if "questoes_para_questionario" not in st.session_state:
                    st.session_state.questoes_para_questionario = []
                st.session_state.questoes_para_questionario.append(q)
                st.success("Questão exportada para questionário!")
        st.divider()

def editar_questao_form(repo):
    """
    Exibe form de edição para st.session_state.editando_questao
    """
    questao = st.session_state.editando_questao
    st.markdown("### Editando Questão")

    new_enunciado = st.text_area("Enunciado", value=questao.get("question", ""), height=100)
    alt = questao.get("options", ["", "", "", ""])
    alt1 = st.text_input("Alternativa 1", value=alt[0] if len(alt) > 0 else "")
    alt2 = st.text_input("Alternativa 2", value=alt[1] if len(alt) > 1 else "")
    alt3 = st.text_input("Alternativa 3", value=alt[2] if len(alt) > 2 else "")
    alt4 = st.text_input("Alternativa 4", value=alt[3] if len(alt) > 3 else "")
    new_answer = st.text_input("Resposta Correta", value=questao.get("answer", ""))
    new_dificuldade = st.selectbox("Dificuldade", ["Fácil", "Médio", "Difícil"], 
                                   index=["Fácil","Médio","Difícil"].index(questao.get("dificuldade","Fácil")) 
                                   if questao.get("dificuldade","Fácil") in ["Fácil","Médio","Difícil"] else 0)
    new_content = st.text_input("Conteúdo", value=questao.get("content", ""))
    new_topic = st.text_input("Tópico", value=questao.get("topic", ""))
    new_subtopic = st.text_input("Subtópico", value=questao.get("subtopic", ""))

    if st.button("Salvar Alterações"):
        questao_atualizada = {
            "id": questao.get("id"),
            "question": new_enunciado.strip(),
            "options": [alt1, alt2, alt3, alt4],
            "answer": new_answer.strip(),
            "dificuldade": new_dificuldade,
            "content": new_content.strip(),
            "topic": new_topic.strip(),
            "subtopic": new_subtopic.strip()
        }
        repo.update_questao(questao_atualizada)
        st.success("Questão atualizada com sucesso!")
        st.session_state.editando_questao = None
        st.rerun()

    if st.button("Cancelar Edição"):
        st.session_state.editando_questao = None
        st.rerun()