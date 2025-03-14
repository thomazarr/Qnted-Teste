# src/professor/question_repository.py

class SupabaseRepository:
    def __init__(self, client):
        self.client = client

    def salvar_questao(self, questao):
        # insert ou upsert no Supabase
        response = self.client.table("questoes").insert(questao).execute()
        return response.data

    def update_questao(self, questao):
        # Exemplo de update, supondo que questao tenha "id"
        id_ = questao["id"]
        response = self.client.table("questoes").update(questao).eq("id", id_).execute()
        return response.data

    def excluir_questao(self, questao_id):
        response = self.client.table("questoes").delete().eq("id", questao_id).execute()
        return response.data

    def listar_questoes(self):
        # Retorna todas as questões
        response = self.client.table("questoes").select("*").execute()
        return response.data or []

    # Se quiser DISTINCT no banco:
    def listar_distinct_contents(self):
        # Exemplo usando RPC ou raw SQL. 
        # Se "content" for uma coluna de texto, algo como:
        sql = "SELECT DISTINCT content FROM questoes WHERE content IS NOT NULL;"
        resp = self.client.rpc("executesql", {"sql": sql}).execute()
        # Ajustar conforme a forma que você chama o raw SQL no Supabase
        # Ou se tiver uma view ou outro método
        contents = []
        if resp.data:
            for row in resp.data:
                contents.append(row["content"])
        return contents

    def listar_distinct_topics(self, contents):
        # Semelhante, mas filtra pelos contents selecionados
        # Lógica depende da forma que você guarda os dados
        pass

    def listar_distinct_subtopics(self, topics):
        pass

    def filtrar_questoes(self, contents, topics, subtopics):
        # Se quiser filtrar direto no banco, pode usar "in_"
        # Ou faça raw SQL. Exemplo fictício:
        pass