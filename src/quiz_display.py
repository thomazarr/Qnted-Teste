import streamlit as st

def gerar_barra_confianca(conf):
    """Retorna um st.progress para representar a confiança (0..3)."""
    # Em layout tabular manual, usaremos st.progress() por colunas
    return conf / 3.0  # valor 0..1

def exibir_resultado_final(resultados):
    """
    resultados: {
      'tempo_minutos': float,
      'score_total': float,
      'num_acertos': int,
      'num_questoes': int,
      'media_confianca': float,
      'detalhes': [
         {
           'numero_questao': int,
           'acertou': bool,
           'conf': int,          # 0..3
           'score_questao': float
         },
         ...
      ]
    }
    """

    tempo = resultados["tempo_minutos"]
    score_total = resultados["score_total"]
    num_acertos = resultados["num_acertos"]
    num_questoes = resultados["num_questoes"]
    media_conf = resultados["media_confianca"]
    detalhes = resultados["detalhes"]

    # 1) Exibir informações gerais de forma destacada com Markdown e emojis
    st.markdown("""
    <div style="background-color: #FFECB3; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
      <h2 style="margin-top: 0;">Resultados Finais 🎉</h2>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    **⏱ Tempo total:** {tempo:.1f} minutos  
    **❓ Você respondeu:** {num_questoes} questões, acertando {num_acertos}.  
    **💯 Pontuação Ajustada Total:** {score_total:.3f}  
    **📊 Média de Confiança:** {media_conf:.2f}
    """)
    st.markdown("</div>", unsafe_allow_html=True)

    # 2) Expander para "Ver detalhes"
    with st.expander("Ver detalhes das questões"):
        # Cabeçalho da "tabela"
        col_header = st.columns([1, 1, 3, 2])
        col_header[0].markdown("**Questão**")
        col_header[1].markdown("**Acerto?**")
        col_header[2].markdown("**Confiança**")
        col_header[3].markdown("**Pontuação**")

        # Exibir cada questão em uma "linha"
        for det in detalhes:
            col_line = st.columns([1, 1, 3, 2])

            numero = det["numero_questao"]
            acertou = det["acertou"]
            conf = det["conf"]
            score_questao = det["score_questao"]

            # Emojis e barra de confiança
            emoji_acerto = "✅" if acertou else "❌"
            progress_value = gerar_barra_confianca(conf)  # valor 0..1

            # Preencher colunas
            col_line[0].write(numero)
            col_line[1].write(emoji_acerto)

            # Barra de confiança com st.progress
            with col_line[2]:
                st.write(f"Nível: {conf}/3")
                st.progress(progress_value)

            col_line[3].write(f"{score_questao:.3f}")

        # 3) Última linha da tabela: resumo (acertos/total, média conf, pontuação)
        col_line = st.columns([1, 1, 3, 2])
        col_line[0].markdown("**Total**")
        col_line[1].markdown(f"**{num_acertos}/{num_questoes}**")  # acertos
        with col_line[2]:
            st.markdown(f"**Média Conf:** {media_conf:.2f}")
        col_line[3].markdown(f"**{score_total:.3f}**")

    # 4) Botão opcional para "Reiniciar Preview"
    if st.button("Reiniciar Preview"):
        st.session_state.preview_started = False
        st.session_state.preview_idx = 0
        st.session_state.preview_respostas = []
        st.session_state.preview_inicio = 0.0
        st.erun()