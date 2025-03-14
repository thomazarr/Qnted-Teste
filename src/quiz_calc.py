# src/quiz_calc.py
import time

def calcular_resultados(questoes, respostas, tempo_inicio, tempo_fim):
    """
    Calcula o resultado final do quiz:
      - Tempo em minutos
      - Pontuação total (score_total)
      - Número de acertos (num_acertos)
      - Número de questões respondidas (num_questoes)
      - Média de confiança (media_confianca)
      - Detalhes de cada questão (lista 'detalhes')
    onde cada item em 'respostas' deve ter:
      { "questao_id": ..., "resposta_idx": int, "confianca": int }
    e 'questoes' é a lista/dict do repositório com
      { "id": ..., "options": [...], "answer": ... }
    """

    # Calcula tempo total
    tempo_total = tempo_fim - tempo_inicio
    tempo_minutos = tempo_total / 60.0

    score_total = 0.0
    num_acertos = 0
    num_questoes = len(respostas)
    soma_confianca = 0.0
    
    detalhes = []

    # Para cada resposta do aluno, recalculamos se acertou ou não
    for i, r in enumerate(respostas):
        conf = r["confianca"]
        questao_id = r["questao_id"]
        resposta_idx = r["resposta_idx"]

        # Localiza a questão correspondente
        questao = next((q for q in questoes if q["id"] == questao_id), None)
        if questao is None:
            # Se não encontrou a questão, pula ou trata como erro
            continue

        # Pega a alternativa escolhida
        alternativas = questao.get("options", [])
        if resposta_idx < len(alternativas):
            alt_escolhida = alternativas[resposta_idx]
        else:
            alt_escolhida = ""

        # Verifica acerto
        acertou = (alt_escolhida == questao.get("answer", ""))

        # Define a pontuação individual, conforme seu modelo:
        # Exemplo do seu mapeamento:
        #  - P_C(conf) => 0.308, 0.632, 0.857, 0.973
        #  - alpha(conf) => 0.25, 0.5, 0.75, 1.0
        p_c_conf = [0.308, 0.632, 0.857, 0.973][conf]  # simplificando
        alpha = [0.25, 0.5, 0.75, 1.0][conf]

        if acertou:
            score_questao = p_c_conf
            num_acertos += 1
        else:
            score_questao = - alpha * p_c_conf

        score_total += score_questao
        soma_confianca += conf

        detalhes.append({
            "numero_questao": i+1,
            "acertou": acertou,
            "conf": conf,
            "score_questao": score_questao
        })

    media_confianca = soma_confianca / num_questoes if num_questoes > 0 else 0

    return {
        "tempo_minutos": tempo_minutos,
        "score_total": score_total,
        "num_acertos": num_acertos,
        "num_questoes": num_questoes,
        "media_confianca": media_confianca,
        "detalhes": detalhes
    }