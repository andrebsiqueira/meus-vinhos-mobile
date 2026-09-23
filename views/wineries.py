import streamlit as st
import pandas as pd

from banco import conectar

def mostrar_detalhes_vinicola(vinicola_id):

    st.markdown(
        """
        <style>
        /* Botões das vinícolas */
        div[data-testid="stButton"] button {
            text-align: center !important;
            justify-content: flex-start !important;
        }

        div[data-testid="stButton"] button p {
            text-align: center !important;
            width: 100%;
            font-size: 18px !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    conexao = conectar()

    df = pd.read_sql_query(
        """
        SELECT
            v.id,
            v.nome,
            v.pais,
            v.regiao,
            v.subregiao,
            v.cidade,
            v.site,
            v.instagram,
            v.visitada,
            v.descricao,
            COUNT(DISTINCT vi.id) AS quantidade_vinhos
        FROM vinicolas v
        LEFT JOIN vinhos vi
            ON v.id = vi.vinicola_id
        WHERE v.id = ?
        GROUP BY
            v.id,
            v.nome,
            v.pais,
            v.regiao,
            v.subregiao,
            v.cidade,
            v.site,
            v.instagram,
            v.visitada,
            v.descricao
        """,
        conexao,
        params=(vinicola_id,)
    )

    df_vinhos = pd.read_sql_query(
        """
        SELECT
            id,
            nome,
            uva,
            safra,
            tipo,
            data_vinho,
            ano_vinho
        FROM vinhos
        WHERE vinicola_id = ?
        """,
        conexao,
        params=(vinicola_id,)
    )

    conexao.close()

    if df.empty:
        st.session_state["vinicola_selecionada"] = None
        st.rerun()

    vinicola = df.iloc[0]

    st.markdown(
        f"""
        <div class="secao" style="font-size: 28px;">
            🏛️ {vinicola["nome"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    # PAÍS / REGIÃO
    pais = vinicola["pais"]

    if pd.isna(pais) or str(pais).strip() == "":
        pais = "Country not specified"

    regiao = vinicola["regiao"]

    if pd.isna(regiao) or str(regiao).strip() == "":
        regiao = ""

    subregiao = vinicola["subregiao"]

    if pd.isna(subregiao) or str(subregiao).strip() == "":
        subregiao = ""

    cidade = vinicola["cidade"]

    if pd.isna(cidade) or str(cidade).strip() == "":
        cidade = ""

    st.markdown(
        f"""
        <div style="
            text-align: left;
            font-size: 16px;
            line-height: 1.7;
            margin-bottom: 15px;
        ">
            🌎 <b>{pais}</b><br>
            📍 {regiao}
        </div>
        """,
        unsafe_allow_html=True
    )

    # DESCRIÇÃO
    descricao = vinicola["descricao"]

    if (
        not pd.isna(descricao)
        and str(descricao).strip() != ""
    ):
        st.markdown("### About")
        st.markdown(str(descricao))

    # SITE
    site = vinicola["site"]

    if (
        not pd.isna(site)
        and str(site).strip() != ""
    ):
        st.markdown("### Website")
        st.markdown(f"[{site}]({site})")

    # INSTAGRAM
    instagram = vinicola["instagram"]

    if (
        not pd.isna(instagram)
        and str(instagram).strip() != ""
    ):
        st.markdown("### Instagram")
        st.markdown(str(instagram))

    st.markdown(f'### My Experience with {vinicola["nome"]}')

    # QUANTIDADE DE VINHOS
    quantidade = int(vinicola["quantidade_vinhos"] or 0)

    texto_vinhos = (
        "1 wine"
        if quantidade == 1
        else f"{quantidade} wines"
    )

    # VISITADA
    texto_visitada = vinicola["visitada"]

    if (
        texto_visitada is True
        or texto_visitada == 1
        or str(texto_visitada).lower() == "true"
    ):
        texto_visitada = "✓ <b>Visited</b>"
    else:
         texto_visitada = "-"       

    st.markdown(
        f"""
        <div style="
                    display: flex;
                    width: 100%;
                    gap: 10px;
                    margin-top: 10px;
                    margin-bottom: 10px;
                ">
                    <div style="
                        flex: 1;
                        text-align: center;
                        padding: 10px 5px;
                        border: 1px solid rgba(128,128,128,0.25);
                        border-radius: 8px;
                    ">
                        <div style="
                            font-size: 24px;
                            font-weight: 600;
                            margin-top: 4px;
                        ">
                            🍷 {texto_vinhos}
                        </div>
                    </div>
                    <div style="
                        flex: 1;
                        text-align: center;
                        padding: 10px 5px;
                        border: 1px solid rgba(128,128,128,0.25);
                        border-radius: 8px;
                    ">
                        <div style="
                            font-size: 24px;
                            font-weight: 600;
                            margin-top: 4px;
                        ">
                            {texto_visitada}
                        </div>
                    </div>
                </div>
        """,
        unsafe_allow_html=True
    )

    if df_vinhos.empty:

        st.info("No wines from this winery are in your collection yet.")

    else:

        # Ordenação por safra e depois por nome
        df_vinhos["safra_ordem"] = pd.to_numeric(
            df_vinhos["safra"],
            errors="coerce"
        )

        df_vinhos = df_vinhos.sort_values(
            by=["safra_ordem", "nome"],
            ascending=[False, True],
            na_position="last"
        )

        for _, vinho in df_vinhos.iterrows():

            nome_vinho = str(vinho["nome"])

            safra = vinho["safra"]

            if pd.isna(safra) or str(safra).strip() == "":
                texto_safra = ""
            else:
                texto_safra = f" · {safra}"

            uva = vinho["uva"]

            if pd.isna(uva) or str(uva).strip() == "":
                texto_uva = ""
            else:
                texto_uva = f" · {uva}"

            st.markdown(
                f"""
                <div style="
                    padding: 10px 0;
                    border-bottom: 1px solid #dddddd;
                    text-align: left;
                ">
                    <div style="
                        font-size: 17px;
                        font-weight: 600;
                    ">
                        🍷 {nome_vinho} {texto_safra}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # VOLTAR
    if st.button(
        "← Back to Wineries",
        width="stretch"
    ):
        st.session_state["vinicola_selecionada"] = None
        st.rerun()


def show_wineries():

    st.markdown(
        '<div class="secao" style="font-size: 28px;">🍷 Wineries & Producers</div>',
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    vinicola_selecionada = st.session_state.get("vinicola_selecionada")

    if vinicola_selecionada:
        mostrar_detalhes_vinicola(vinicola_selecionada)
        return

    st.markdown(
        """
        <style>
        /* Botões das vinícolas */
        div[data-testid="stButton"] button {
            text-align: center !important;
            justify-content: flex-start !important;
        }

        div[data-testid="stButton"] button p {
            text-align: center !important;
            width: 100%;
            font-size: 18px !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # =========================================================
    # LIMPAR VINHO SELECIONADO
    # =========================================================

    st.session_state["vinho_selecionado"] = None

    # =========================================================
    # VERIFICA REGIÃO SELECIONADA
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
                "Exploring wineries from this region only."
            )

    # =========================================================
    # TODAS AS VINÍCOLAS
    # =========================================================

    else:

        pesquisa_vinicola = st.text_input(
            "🔎 Search Wineries",
            placeholder="Enter winery or producer name..."
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
                    "No wineries found."
                )

            else:

                st.info(
                    f"Found {len(df_filtrado_vinicola)} "
                    f"winery/wineries matching your search."
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
            "No wineries registered."
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
        # PAÍS E REGIÃO
        # -----------------------------------------------------

        pais = linha["pais"]

        regiao = linha["regiao"]

        if pd.isna(pais) or str(pais).strip() == "":
            pais = "Country not specified"
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
            "1 wine"
            if quantidade_vinhos == 1
            else f"{quantidade_vinhos} wines"
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
            indicador_visitada = " · ✓ Visited"
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
                "← View ALL Wineries & Producers",
                key="ver_todas_vinicolas",
                width="stretch"
            ):


            st.session_state["regiao_selecionada"] = None

            st.rerun()
