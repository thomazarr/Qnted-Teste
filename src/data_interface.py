class DataRepository:
    # Usuários
    def carregar_usuario(self, email):
        raise NotImplementedError
    
    def salvar_usuario(self, usuario):
        raise NotImplementedError
    
    # Questões
    def salvar_questao(self, questao):
        raise NotImplementedError

    def listar_questoes(self):
        raise NotImplementedError

    def excluir_questao(self, questao_id):
        raise NotImplementedError

    # Turmas
    def salvar_turma(self, turma):
        raise NotImplementedError
    
    def listar_turmas(self):
        raise NotImplementedError

    # Questionários
    def salvar_questionario(self, questionario):
        raise NotImplementedError
    
    def listar_questionarios(self):
        raise NotImplementedError

    # Etc... adicione conforme necessidade