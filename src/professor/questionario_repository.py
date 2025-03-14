# src/professor/questionario_repository.py

class QuestionarioRepository:
    def __init__(self, client):
        self.client = client

    def criar_questionario(self, dados):
        """
        dados: {
          "titulo": str,
          "turma_id": uuid ou None,
          "instrucoes": str (markdown),
          "data_inicio": datetime/string,
          "data_fim": datetime/string
        }
        Retorna o objeto inserido (com id).
        """
        response = self.client.table("questionarios").insert(dados).execute()
        if response.error:
            print("Erro ao criar questionario:", response.error)
        return response.data  # lista de objetos inseridos

    def adicionar_questao_ao_questionario(self, questionario_id, questao_id, ordem=None):
        """
        Insere um registro em questionarios_questoes.
        ordem pode ser usado para definir a posição da questão no questionário.
        """
        payload = {
            "questionario_id": questionario_id,
            "questao_id": questao_id
        }
        if ordem is not None:
            payload["ordem"] = ordem

        response = self.client.table("questionarios_questoes").insert(payload).execute()
        return response.data

    def listar_questionarios(self):
        """
        Retorna todos os questionários com suas colunas principais.
        """
        response = self.client.table("questionarios").select("*").execute()
        return response.data or []

    def listar_questoes_de_questionario(self, questionario_id):
        """
        Retorna as questões associadas ao questionário_id, consultando questionarios_questoes e questoes.
        """
        # 1) pegar as associações
        assoc_resp = self.client.table("questionarios_questoes").select("*").eq("questionario_id", questionario_id).execute()
        assoc_data = assoc_resp.data or []

        lista_questoes = []
        for assoc in assoc_data:
            qid = assoc["questao_id"]
            questao_resp = self.client.table("questoes").select("*").eq("id", qid).execute()
            if questao_resp.data:
                lista_questoes.append(questao_resp.data[0])
        return lista_questoes

    def atualizar_questionario(self, questionario_id, dados):
        """
        Atualiza colunas do questionário (titulo, instrucoes, data_inicio, data_fim, etc.)
        """
        response = self.client.table("questionarios").update(dados).eq("id", questionario_id).execute()
        return response.data

    def excluir_questionario(self, questionario_id):
        """
        Exclui o questionário e associações.
        """
        # excluir assoc. questionarios_questoes
        self.client.table("questionarios_questoes").delete().eq("questionario_id", questionario_id).execute()
        # excluir questionario
        response = self.client.table("questionarios").delete().eq("id", questionario_id).execute()
        return response.data