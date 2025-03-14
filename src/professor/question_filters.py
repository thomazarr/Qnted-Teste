# src/professor/question_filters.py

def filtrar_questoes_local(questoes, contents, topics, subtopics):
    # Se o usuário não selecionou nada, podem ser None ou listas vazias
    contents = contents or []
    topics = topics or []
    subtopics = subtopics or []

    result = []
    for q in questoes:
        c = q.get("content") or ""
        t = q.get("topic") or ""
        s = q.get("subtopic") or ""

        # Se a lista 'contents' não estiver vazia, verificar se c está nela
        # Se quiser "case-insensitive", converta para lower
        # Exemplo: se contents contiver strings, faça algo assim:
        if contents and c.lower() not in [x.lower() for x in contents]:
            continue

        if topics and t.lower() not in [x.lower() for x in topics]:
            continue

        if subtopics and s.lower() not in [x.lower() for x in subtopics]:
            continue

        result.append(q)

    return result