import streamlit as st
from src.professor.gerenciador_questoes import editor_questao
from src.professor.question_management import gerenciar_questoes_salvas
from src.professor.question_importer import importar_arquivo_json
from src.professor.question_repository import SupabaseRepository
from src.professor.gerenciador_turmas import gerenciar_turmas
from src.professor.questionario_repository import QuestionarioRepository
from src.professor.questionario_criacao import criar_questionario
from src.professor.questionario_gerencia import gerenciar_questionarios
from src.professor.questionario_preview import preview_questionario
from src.repository_factory import get_repository

repo = get_repository()

def professor_dashboard():
    st.title("Painel do Professor")

    # Em vez de get_repository() que devolve SupabaseRepository, instancie QuestionarioRepository
    client = criar_cliente_supabase()  # ou algo que devolva o client
    repo = QuestionarioRepository(client)

    # Agora repo tem criar_questionario(...)
    turmas = repo.listar_turmas()  # se esse método existir em QuestionarioRepository ou se você tiver outro repositório
    questoes = repo.listar_questoes() # idem

    criar_questionario(repo, turmas, questoes)

# Verificação de acesso
if "usuario" not in st.session_state or st.session_state.usuario is None:
    st.error("Você não está logado.")
    st.stop()

if st.session_state.usuario.get("role") != "Professor":
    st.error("Acesso negado. Somente professores podem acessar esta página.")
    st.stop()

# Título geral da página
st.title("Painel do Professor")
st.write("Bem-vindo(a), Professor(a)! Aqui você pode gerenciar questões, turmas e questionários.")

# Cria quatro abas
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Gerenciar Questões", "Gerenciar Turmas", "Criar Questionários", "Gerenciar Questionários", "Questionário Preview"])

# 1. Aba: Gerenciar Questões
with tab1:
    opcao = st.selectbox(
            "Selecione uma opção:",
            ["Editor de Questão", "Importar JSON", "Gerenciar Banco de Questões"]
        )

    if opcao == "Editor de Questão":
        editor_questao()
    elif opcao == "Importar JSON":
        importar_arquivo_json(repo)
    elif opcao == "Gerenciar Banco de Questões":
        gerenciar_questoes_salvas(repo)

# 2. Aba: Gerenciar Turmas
with tab2:
    gerenciar_turmas(repo)

# 3. Aba: Criar Questionários
with tab3:
    turmas = repo.listar_turmas()  # se tiver método no repositório
    questoes = repo.listar_questoes()  # se tiver método no repositório
    criar_questionario(repo, turmas, questoes)
    

# 4. Aba: Gerenciar Questionários
with tab4:
    gerenciar_questionarios(repo)

# 5. Aba: Questionário Preview
with tab5:
    st.markdown("## Pré-visualizar Questionário")
    questionarios = repo.listar_questionarios()
    if not questionarios:
        st.info("Nenhum questionário disponível.")
    else:
        opcoes = [f"{q['id']} - {q['titulo']}" for q in questionarios]
        selec = st.selectbox("Selecione o questionário", ["Nenhum"] + opcoes)
        if selec != "Nenhum":
            qid = selec.split(" - ")[0]  # Extrai apenas o ID
            preview_questionario(repo, qid)