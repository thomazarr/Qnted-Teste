# src/data_view/utils.py
import pandas as pd

# Dicionários com probabilidades condicionais e valores alpha
P_C_given_A = {0: 0.308, 1: 0.632, 2: 0.857, 3: 0.973}
alpha_values = {0: 0.25, 1: 0.5, 2: 0.75, 3: 1.0}

def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ajusta o DataFrame para converter colunas '_Acertou' em valores numéricos (0 ou 1).
    """
    acertos_cols = df.filter(like='_Acertou').replace({'Sim': 1, 'Não': 0}).apply(pd.to_numeric, errors='coerce').fillna(0)
    df.update(acertos_cols)
    return df

def calculate_score(resposta, confidence) -> float:
    """
    Calcula a pontuação para uma questão, dado acerto/erro (resposta) e confiança.
    resposta = 1 (acerto) ou 0 (erro).
    confidence = nível de confiança (0..3).
    """
    if pd.isna(confidence) or pd.isna(resposta):
        return 0.0
    confidence = int(confidence)
    P_C_E = 1 - P_C_given_A.get(confidence, 0)
    # Se acertou => P_C_given_A[conf]; se errou => -alpha[conf] * (1 - P_C[conf])
    return P_C_given_A[confidence] if resposta == 1 else -alpha_values[confidence] * P_C_E

# src/data_view/utils.py

def split_label(label, max_length=20):
    """
    Quebra um rótulo longo em múltiplas linhas para melhor exibição.
    """
    words = label.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + 1 <= max_length:
            current_line += (" " if current_line else "") + word
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return "\n".join(lines)