# test_insert.py
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

from supabase import create_client

# Agora você pode acessar os valores carregados
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

print("URL lida do .env:", url)
print("KEY lida do .env:", key)

client = create_client(url, key)

questao = {
    "question": "Teste rápido",
    "options": ["A", "B", "C", "D"],
    "answer": "A"
}

response = client.table("questoes").insert(questao).execute()
print("Resposta do Supabase:", response)