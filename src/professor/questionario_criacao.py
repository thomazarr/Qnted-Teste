import streamlit as st
from datetime import datetime
from src.professor.questionario_repository import QuestionarioRepository
from src.professor.question_filters import filtrar_questoes_local  # Exemplo de filtro local

def criar_questionario(repo, turmas, questoes):
    """
    Cria questionário sem mostrar ID da turma nem das questões.
    Filtra questões por conteúdo, tópico, subtópico e permite selecionar.
    """

    st.title("Criar Novo Questionário")

    # Formulário Básico
    titulo = st.text_input("Título do Questionário")
    turma_opcoes = [t["nome"] for t in turmas]  # só exibe nome
    turma_escolhida = st.selectbox("Selecione a Turma", options=["Nenhuma"] + turma_opcoes)
    instrucoes_md = st.text_area("Instruções (Markdown)", height=100)

    data_inicio = st.date_input("Data de Início")
    hora_inicio = st.time_input("Hora de Início")
    data_fim = st.date_input("Data de Fim")
    hora_fim = st.time_input("Hora de Fim")

    dt_inicio = datetime.combine(data_inicio, hora_inicio)
    dt_fim = datetime.combine(data_fim, hora_fim)

    st.markdown("---")
    st.markdown("### Filtros para Selecionar Questões")

    # Exemplo de distinct values
    all_contents = sorted(list(set(q.get("content","") for q in questoes if q.get("content"))))
    all_topics = sorted(list(set(q.get("topic","") for q in questoes if q.get("topic"))))
    all_subtopics = sorted(list(set(q.get("subtopic","") for q in questoes if q.get("subtopic"))))

    selected_contents = st.multiselect("Filtrar por Conteúdos", options=all_contents)
    selected_topics = st.multiselect("Filtrar por Tópicos", options=all_topics)
    selected_subtopics = st.multiselect("Filtrar por Subtópicos", options=all_subtopics)

    # Filtra as questões localmente (exemplo)
    questoes_filtradas = filtrar_questoes_local(
        questoes, selected_contents, selected_topics, selected_subtopics
    )

    st.markdown(f"**Total de questões filtradas:** {len(questoes_filtradas)}")

    # Checkboxes para selecionar
    st.markdown("### Selecione as Questões para o Questionário")
    questoes_selecionadas = []
    for q in questoes_filtradas:
        # exibir só enunciado
        enunciado_curto = q.get("question","[Sem Enunciado]")[:50]
        label_questao = f"{enunciado_curto}..."
        if st.checkbox(label_questao, key=f"q_{q['id']}"):
            questoes_selecionadas.append(q["id"])

    if st.button("Criar Questionário"):
        if not titulo.strip():
            st.error("Título não pode ficar vazio.")
            return

        turma_id = None
        if turma_escolhida != "Nenhuma":
            # Achar a turma no array turmas
            for t in turmas:
                if t["nome"] == turma_escolhida:
                    turma_id = t["id"]
                    break

        dados_questionario = {
            "titulo": titulo.strip(),
            "turma_id": turma_id,
            "instrucoes": instrucoes_md.strip(),
            "data_inicio": dt_inicio.isoformat(),
            "data_fim": dt_fim.isoformat()
        }

        result = repo.criar_questionario(dados_questionario)
        if result and len(result) > 0:
            questionario_criado = result[0]
            questionario_id = questionario_criado["id"]
            for qid in questoes_selecionadas:
                repo.adicionar_questao_ao_questionario(questionario_id, qid)
            st.success("Questionário criado com sucesso!")
        else:
            st.error("Falha ao criar questionário.")