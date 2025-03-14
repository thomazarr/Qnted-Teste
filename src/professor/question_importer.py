import json
import streamlit as st
from src.professor.question_repository import SupabaseRepository
from src.professor.question_view import mostrar_questao_formatada

def importar_arquivo_json(repo):
    """
    Recebe um 'repo' (instância de SupabaseRepository) para salvar as questões.
    Faz upload do arquivo JSON, insere no banco, e exibe as questões importadas.
    """
    st.header("Importar Arquivo JSON")

    uploaded_file = st.file_uploader("Selecione um arquivo JSON", type=["json"])
    imported_questions = []

    if uploaded_file is not None:
        if st.button("Importar Questões"):
            try:
                data = json.load(uploaded_file)
                if isinstance(data, list):
                    for questao_json in data:
                        # Extrair campos do JSON
                        question = questao_json.get("question", "")
                        options = questao_json.get("options", [])
                        answer = questao_json.get("answer", "")
                        dificuldade = questao_json.get("dificuldade", "")
                        tags = questao_json.get("tags", {})
                        content = tags.get("content")
                        topic = tags.get("topic")
                        subtopic = tags.get("subtopic")

                        nova_questao = {
                            "question": question,
                            "options": options,
                            "answer": answer,
                            "dificuldade": dificuldade,
                            "content": content,
                            "topic": topic,
                            "subtopic": subtopic
                        }

                        # Se quiser passar "id" caso exista no JSON:
                        if "id" in questao_json:
                            nova_questao["id"] = questao_json["id"]

                        # Salva no banco
                        repo.salvar_questao(nova_questao)
                        # Adiciona à lista local para exibir
                        imported_questions.append(nova_questao)

                    st.success(f"Foram importadas {len(imported_questions)} questões com sucesso!")
                else:
                    st.error("O arquivo JSON não contém uma lista de questões.")
            except Exception as e:
                st.error(f"Erro ao processar o arquivo JSON: {e}")

    # Exibir as questões importadas
    if imported_questions:
        st.subheader("Questões Importadas")
        for q in imported_questions:
            mostrar_questao_formatada(q, exibir_id=False)