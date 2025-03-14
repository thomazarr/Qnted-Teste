import config
from .supabase_repo import SupabaseRepository

def get_repository():
    if config.DATA_REPOSITORY == "supabase":
        return SupabaseRepository()
    else:
        raise ValueError("Repositório de dados não configurado corretamente.")