import os
from supabase import create_client
from .data_interface import DataRepository
import config

class SupabaseRepository(DataRepository):
    def __init__(self):
        self.url = config.SUPABASE_URL
        self.key = config.SUPABASE_KEY
        if not self.url or not self.key:
            raise Exception("SUPABASE_URL ou SUPABASE_KEY não estão definidos.")
        self.client = create_client(self.url, self.key)

    # Usuários
    def carregar_usuario(self, email):
        response = self.client.table("usuarios").select("*").eq("email", email).execute()
        return response.data[0] if response.data else None

    def salvar_usuario(self, usuario):
        # usuario: {"nome":..., "email":..., "senha":..., "cpf":..., "turma_id":...}
        response = self.client.table("usuarios").insert(usuario).execute()
        return response.data

    def listar_usuarios(self):
        response = self.client.table("usuarios").select("*").execute()
        return response.data or []

    def atualizar_usuario(self, user_id, dados):
        response = self.client.table("usuarios").update(dados).eq("id", user_id).execute()
        return response.data

    # Questões
    def salvar_questao(self, questao):
        # Exemplo de 'questao': {"enunciado": "...", "alternativas": [...], "resposta": "...", ...}
        response = self.client.table("questoes").insert(questao).execute()
        return response.data

    def listar_questoes(self):
        response = self.client.table("questoes").select("*").execute()
        return response.data

    def excluir_questao(self, questao_id):
        response = self.client.table("questoes").delete().eq("id", questao_id).execute()
        return response.data

    # Turmas
    def salvar_turma(self, turma):
        # Exemplo: {"nome": "...", "disciplina": "..."}
        response = self.client.table("turmas").insert(turma).execute()
        return response.data

    def listar_turmas(self):
        response = self.client.table("turmas").select("*").execute()
        return response.data

    def listar_usuarios(self):
        # Ajuste o nome da tabela se não for "usuarios"
        response = self.client.table("usuarios").select("*").execute()
        return response.data or []

    # Se quiser salvar, excluir, atualizar usuário, adicione métodos
    def salvar_usuario(self, usuario):
        response = self.client.table("usuarios").insert(usuario).execute()
        return response.data

    # Questionários
    def salvar_questionario(self, questionario):
        # Exemplo: {"nome": "...", "questoes": [...], "turmas": [...], "data_inicio": "...", "data_fim": "..."}
        response = self.client.table("questionarios").insert(questionario).execute()
        return response.data

    def listar_questionarios(self):
        response = self.client.table("questionarios").select("*").execute()
        return response.data
    
    def criar_questionario(self, dados):
        response = self.client.table("questionarios").insert(dados).execute()
        return response.data

    def adicionar_questao_ao_questionario(self, questionario_id, questao_id):
        payload = {
            "questionario_id": questionario_id,
            "questao_id": questao_id
        }
        resp = self.client.table("questionarios_questoes").insert(payload).execute()
        return resp.data
    
    def listar_questoes_de_questionario(self, questionario_id):
        """
        Retorna as questões associadas a um determinado questionário.
        """
        # 1) Pegar os registros em questionarios_questoes
        assoc_resp = self.client.table("questionarios_questoes").select("*").eq("questionario_id", questionario_id).execute()
        assoc_data = assoc_resp.data or []

        questoes = []
        for assoc in assoc_data:
            qid = assoc["questao_id"]
            # 2) Buscar a questão na tabela questoes
            questao_resp = self.client.table("questoes").select("*").eq("id", qid).execute()
            if questao_resp.data:
                questoes.append(questao_resp.data[0])

        return questoes 