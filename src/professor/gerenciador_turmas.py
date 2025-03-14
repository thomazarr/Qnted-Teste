import streamlit as st
from src.repository_factory import get_repository

def gerenciar_turmas(repo):
    """
    Ajustado para:
    1. Não mostrar o ID da turma
    2. Exibir checkboxes para cada aluno sem turma
    """
    st.title("Gerenciar Turmas")

    # 1. Criar Nova Turma
    st.markdown("### Criar Nova Turma")
    nome_turma = st.text_input("Nome da Turma")
    disciplina = st.text_input("Disciplina (opcional)")
    if st.button("Criar Turma"):
        if nome_turma.strip():
            nova_turma = {
                "nome": nome_turma.strip(),
                "disciplina": disciplina.strip() if disciplina else None
            }
            repo.salvar_turma(nova_turma)
            st.success(f"Turma '{nome_turma}' criada com sucesso!")
            st.rerun()
        else:
            st.error("O nome da turma não pode ficar vazio.")

    st.markdown("---")

    # 2. Listar Turmas Existentes
    turmas = repo.listar_turmas()
    if not turmas:
        st.info("Nenhuma turma cadastrada ainda.")
        return

    st.markdown("### Turmas Cadastradas")
    for turma in turmas:
        turma_id = turma.get("id")
        turma_nome = turma.get("nome")
        turma_disciplina = turma.get("disciplina")

        # Expand
        with st.expander(f"{turma_nome} ({turma_disciplina or 'Sem disciplina'})"):
            # 3. Exibir Alunos da Turma
            # (Ocultando o ID da turma)
            # st.write(f"ID da Turma: {turma_id}")  # Não exibimos

            usuarios = repo.listar_usuarios()  # todos os usuários
            # Filtra alunos da turma
            alunos_da_turma = [u for u in usuarios if u.get("turma_id") == turma_id]

            for aluno in alunos_da_turma:
                st.write(f"- {aluno.get('nome', aluno.get('email'))} ({aluno.get('email')})")
                # Botão remover etc.

            st.markdown(f"**Alunos nesta Turma:** {len(alunos_da_turma)}")
            for aluno in alunos_da_turma:
                # Botão remover
                if st.button(f"Remover_{aluno['id']}", key=f"rem_{aluno['id']}_{turma_id}"):
                    repo.atualizar_usuario(aluno["id"], {"turma_id": None})
                    st.success(f"Aluno {aluno.get('nome')} removido da turma {turma_nome}.")
                    st.rerun()

            st.markdown("---")

            # 4. Atribuir novos alunos via checkboxes
            st.markdown("**Atribuir novos alunos a esta turma**")
            # Lista de usuários sem turma
            usuarios_sem_turma = [u for u in usuarios if not u.get("turma_id")]

            if usuarios_sem_turma:
                # Precisamos de um container para os checkboxes
                # e um botão para confirmar as seleções
                selecoes = {}
                for aluno in usuarios_sem_turma:
                    # Cada checkbox retorna True/False
                    key_checkbox = f"checkbox_{aluno['id']}_{turma_id}"
                    selecoes[aluno["id"]] = st.checkbox(
                        f"{aluno.get('nome')} ({aluno.get('email')})", 
                        key=key_checkbox
                    )
                # Botão para confirmar atribuição
                if st.button(f"Atribuir"):
                    # Filtra os alunos marcados como True
                    alunos_selecionados = [aid for aid, marcado in selecoes.items() if marcado]
                    for user_id in alunos_selecionados:
                        repo.atualizar_usuario(user_id, {"turma_id": turma_id})
                    st.success(f"{len(alunos_selecionados)} alunos atribuídos à turma {turma_nome}.")
                    st.rerun()
            else:
                st.write("Não há alunos disponíveis para adicionar (todos já possuem turma).")


# ============================================
# Exemplo de Repositório (Simples)
# ============================================
class SupabaseRepository:
    def __init__(self, client):
        self.client = client

    def salvar_turma(self, turma):
        # Ex: {"nome":..., "disciplina":...}
        response = self.client.table("turmas").insert(turma).execute()
        return response.data

    def listar_turmas(self):
        response = self.client.table("turmas").select("*").execute()
        return response.data or []

    def listar_usuarios(self):
        response = self.client.table("usuarios").select("*").execute()
        return response.data or []

    def atualizar_usuario(self, user_id, dados):
        response = self.client.table("usuarios").update(dados).eq("id", user_id).execute()
        return response.data

    # Se quiser inserir o "nome" do aluno no cadastro, garanta que a tabela "usuarios" tenha esse campo        st.info("Nenhuma turma cadastrada.")