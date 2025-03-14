import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(__file__)
env_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path=env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Defina o repositório de dados a ser utilizado: "supabase" ou "mongodb"
DATA_REPOSITORY = "supabase"