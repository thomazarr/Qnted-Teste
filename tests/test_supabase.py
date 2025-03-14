import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.supabase_repo import SupabaseRepository

def test_supabase_connection():
    repo = SupabaseRepository()
    user_email = "aluno@example.com"  # Altere para um email existente no seu Supabase
    user_data = repo.carregar_usuario(user_email)
    print("User data:", user_data)

if __name__ == "__main__":
    test_supabase_connection()