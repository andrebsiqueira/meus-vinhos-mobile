import streamlit as st
import pandas as pd

from banco import conectar

def show_wineries():

    st.markdown(
        '<div class="secao" style="font-size: 28px;">🍷 Wineries & Producers</div>',
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================================================
    # LIMPAR VINHO SELECIONADO
    # =========================================================

    st.session_state["vinho_selecionado"] = None

    # =========================================================
    # 
    # =========================================================

    regiao_selecionada = st.session_state.get(
        "regiao_selecionada"
    )

    # =========================================================
    # CONEXÃO COM O BANCO
    # =========================================================

    conexao = conectar()

    # =========================================================
    # VINÍCOLAS DE UMA REGIÃO ESPECÍFICA
    # =========================================================

    if regiao_selecionada:

        df_vinicolas = pd.read_sql_query(
            """
            SELECT
                v.id AS vinicola_id,
                v.nome,
                v.regiao,
                v.subregiao,
                v.pais,
                v.visitada,
                COUNT(DISTINCT vi.id) AS quantidade_vinhos,
                v.instagram
            FROM vinicolas v
            LEFT JOIN vinhos vi
                ON v.id = vi.vinicola_id
            WHERE v.regiao = ?
            GROUP BY
                v.id,
                v.nome,
                v.regiao,
                v.subregiao,
                v.pais,
                v.visitada,
                v.instagram
            ORDER BY v.nome ASC
            """,
            conexao,
            params=(regiao_selecionada,)
        )

        if not df_vinicolas.empty:

            pais = df_vinicolas.iloc[0]["pais"]

            if pd.isna(pais) or str(pais).strip() == "":
                pais = "País não informado"

            st.markdown(
                f"### 🌎 {regiao_selecionada}, {pais}"
            )

            st.info(
                "Você está visualizando somente as vinícolas "
                "desta região."
            )

    # =========================================================
    # TODAS AS VINÍCOLAS
    # =========================================================

    else:

        pesquisa_vinicola = st.text_input(
            "🔎 Pesquisar vinícolas",
            placeholder="Digite o nome da vinícola ou produtor..."
        )

        # =====================================================
        # CARREGA TODAS AS VINÍCOLAS
        # =====================================================

        df_vinicolas = pd.read_sql_query(
            """
            SELECT
                v.id AS vinicola_id,
                v.nome,
                v.regiao,
                v.subregiao,
                v.pais,
                v.visitada,
                COUNT(DISTINCT vi.id) AS quantidade_vinhos,
                v.instagram
            FROM vinicolas v
            LEFT JOIN vinhos vi
                ON v.id = vi.vinicola_id
            GROUP BY
                v.id,
                v.nome,
                v.regiao,
                v.subregiao,
                v.pais,
                v.visitada,
                v.instagram
            ORDER BY v.nome ASC
            """,
            conexao
        )

        # =====================================================
        # FILTRO DE PESQUISA
        # =====================================================

        df_filtrado_vinicola = df_vinicolas.copy()

        if pesquisa_vinicola.strip() != "":

            termo_vinicola = pesquisa_vinicola.lower()

            df_filtrado_vinicola = df_filtrado_vinicola[
                df_filtrado_vinicola.astype(str)
                .apply(
                    lambda coluna:
                    coluna.str.lower().str.contains(
                        termo_vinicola,
                        na=False
                    )
                )
                .any(axis=1)
            ]

            if len(df_filtrado_vinicola) == 0:

                st.info(
                    "Nenhuma vinícola encontrada."
                )

            else:

                st.info(
                    f"Encontrei {len(df_filtrado_vinicola)} "
                    f"vinícola(s) na pesquisa."
                )

        # =====================================================
        # MANTÉM SOMENTE AS COLUNAS NECESSÁRIAS
        # =====================================================

        df_vinicolas = df_filtrado_vinicola[
            [
                "vinicola_id",
                "nome",
                "regiao",
                "subregiao",
                "pais",
                "quantidade_vinhos",
                "visitada",
                "instagram"
            ]
        ]

    # =========================================================
    # FECHAR CONEXÃO
    # =========================================================

    conexao.close()

    # =========================================================
    # VERIFICAR SE EXISTEM VINÍCOLAS
    # =========================================================

    pesquisa_atual = ""

    if not regiao_selecionada:
        pesquisa_atual = pesquisa_vinicola

    if (
        len(df_vinicolas) == 0
        and len(pesquisa_atual.strip()) == 0
    ):
        st.info(
            "Nenhuma vinícola cadastrada."
        )
        return

    # =========================================================
    # LISTA MOBILE DE VINÍCOLAS
    # =========================================================

    df_lista = df_vinicolas.copy()

    # Garantir nome como texto
    df_lista["nome"] = (
        df_lista["nome"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    # Ordenação alfabética
    df_lista = df_lista.sort_values(
        by="nome",
        ascending=True
    )

    letra_atual = ""

    # =========================================================
    # EXIBIÇÃO DAS VINÍCOLAS
    # =========================================================

    for _, linha in df_lista.iterrows():

        nome = linha["nome"]

        if not nome:
            continue

        # -----------------------------------------------------
        # PRIMEIRA LETRA DO NOME
        # -----------------------------------------------------

        primeira_letra = nome[0].upper()

        # -----------------------------------------------------
        # CABEÇALHO DA LETRA
        # -----------------------------------------------------

        if primeira_letra != letra_atual:

            letra_atual = primeira_letra

            st.markdown(
                f"""
                <div style="
                    font-size: 22px;
                    font-weight: 700;
                    margin-top: 18px;
                    margin-bottom: 6px;
                    color: #8B0000;
                ">
                    {letra_atual}
                </div>
                """,
                unsafe_allow_html=True
            )

        # -----------------------------------------------------
        # PAÍS
        # -----------------------------------------------------

        pais = linha["pais"]

        if pd.isna(pais) or str(pais).strip() == "":
            pais = "País não informado"
        else:
            pais = str(pais).strip()

        # -----------------------------------------------------
        # QUANTIDADE DE VINHOS
        # -----------------------------------------------------

        quantidade_vinhos = linha["quantidade_vinhos"]

        if pd.isna(quantidade_vinhos):
            quantidade_vinhos = 0

        quantidade_vinhos = int(
            quantidade_vinhos
        )

        texto_vinhos = (
            "1 vinho"
            if quantidade_vinhos == 1
            else f"{quantidade_vinhos} vinhos"
        )

        # -----------------------------------------------------
        # VISITADA
        # -----------------------------------------------------

        visitada = linha["visitada"]

        if (
            visitada is True
            or visitada == 1
            or str(visitada).lower() == "true"
        ):
            indicador_visitada = " · ✓ Visitada"
        else:
            indicador_visitada = ""

        # -----------------------------------------------------
        # TEXTO SECUNDÁRIO
        # -----------------------------------------------------

        texto_secundario = (
            f"🌎 {pais} · 🍷 {texto_vinhos}"
            f"{indicador_visitada}"
        )

        # -----------------------------------------------------
        # BOTÃO DA VINÍCOLA
        # -----------------------------------------------------

        if st.button(
            f"🏛️ {nome}\n\n{texto_secundario}",
            key=f"vinicola_{linha['vinicola_id']}",
            width="stretch"
        ):

            st.session_state["vinicola_selecionada"] = (
                linha["vinicola_id"]
            )

            st.rerun()

    # =========================================================
    # FILTRO POR REGIÃO
    # =========================================================

    if regiao_selecionada:

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button(
            "← Ver TODAS as Vinícolas e Produtores",
            key="ver_todas_vinicolas",
            width="stretch"
        ):

            st.session_state["regiao_selecionada"] = None

            st.rerun()
