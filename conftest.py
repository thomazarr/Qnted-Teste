import os
from dotenv import load_dotenv

# Obtém o caminho absoluto para a raiz do projeto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
env_path = os.path.join(BASE_DIR, '.env')

# Carrega as variáveis de ambiente a partir do arquivo .env
load_dotenv(dotenv_path=env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Para depuração: imprima os valores carregados
print("In config.py, SUPABASE_URL:", SUPABASE_URL)
print("In config.py, SUPABASE_KEY:", SUPABASE_KEY)