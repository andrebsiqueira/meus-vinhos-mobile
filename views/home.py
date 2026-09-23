import streamlit as st
import pandas as pd

import plotly.express as px

from banco import conectar

def show_home():

    st.markdown(
        '<div class="secao" style="font-size: 28px;">🍷 Home</div>',
        unsafe_allow_html=True
    )

    st.info(
            "A personal catalog to record, organize, and rediscover your wines."
        )

    conexao = conectar()

    # ============================================================
    # WINES
    # ============================================================

    df_vinhos = pd.read_sql_query(
        """
        SELECT
            v.id,
            v.nome,
            vi.nome AS vinicola,
            vi.pais,
            vi.regiao,
            v.uva,
            v.safra,
            v.tipo,
            v.nota_vivino
        FROM vinhos v
        LEFT JOIN vinicolas vi
            ON v.vinicola_id = vi.id
        ORDER BY v.id DESC
        """,
        conexao
    )

    # ============================================================
    # WINERIES
    # ============================================================

    df_vinicolas = pd.read_sql_query(
        """
        SELECT
            id,
            nome,
            pais,
            regiao
        FROM vinicolas
        ORDER BY nome ASC
        """,
        conexao
    )

    conexao.close()

    # =================================================
    # METRICS
    # =================================================

    countries = (
            df_vinicolas["pais"]
            .dropna()
            .nunique()
            if len(df_vinicolas) > 0
            else 0
    )

    regions = (
            df_vinicolas["regiao"]
            .dropna()
            .nunique()
            if len(df_vinicolas) > 0
            else 0
    )

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
                        <div style="font-size: 14px;">
                            🍷 Wines
                        </div>
                        <div style="
                            font-size: 24px;
                            font-weight: 600;
                            margin-top: 4px;
                        ">
                            {len(df_vinhos)}
                        </div>
                    </div>
                    <div style="
                        flex: 1;
                        text-align: center;
                        padding: 10px 5px;
                        border: 1px solid rgba(128,128,128,0.25);
                        border-radius: 8px;
                    ">
                        <div style="font-size: 14px;">
                            🏛️ Wineries
                        </div>
                        <div style="
                            font-size: 24px;
                            font-weight: 600;
                            margin-top: 4px;
                        ">
                            {len(df_vinicolas)}
                        </div>
                    </div>
                </div>
        """,
        unsafe_allow_html=True
    )

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
                        <div style="font-size: 14px;">
                            📍 Regions
                        </div>
                        <div style="
                            font-size: 24px;
                            font-weight: 600;
                            margin-top: 4px;
                        ">
                            {regions}
                        </div>
                    </div>
                    <div style="
                        flex: 1;
                        text-align: center;
                        padding: 10px 5px;
                        border: 1px solid rgba(128,128,128,0.25);
                        border-radius: 8px;
                    ">
                        <div style="font-size: 14px;">
                            🌎 Countries
                        </div>
                        <div style="
                            font-size: 24px;
                            font-weight: 600;
                            margin-top: 4px;
                        ">
                            {countries}
                        </div>
                    </div>
                </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ==========================================================
    # CHART 1 - TOP 10 GRAPE VARIETIES
    # ==========================================================

    # Título do gráfico
    st.markdown(
        '<div class="secao" style="font-size: 22px; text-align: left;">Chart 1: Top 10 Grape Varieties</div>',
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Remove valores vazios
    df_uvas = df_vinhos["uva"].dropna()

    # Separa as uvas pela vírgula
    uvas = (
            df_uvas
            .str.split(",")
            .explode()
            .str.strip()
        )

    # Remove percentuais e qualquer conteúdo entre parênteses
    uvas = (
            uvas
            .str.replace(r"\s*\([^)]*\)", "", regex=True)
            .str.strip()
        )

    # Remove valores vazios
    uvas = uvas[uvas != ""]

    # Conta cada variedade individualmente
    qtd_por_uva = (
            uvas
            .value_counts()
            .head(10)
            .reset_index()
        )

    qtd_por_uva.columns = ["Uva", "Quantidade"]

    # Gráfico horizontal
    st.vega_lite_chart(
            qtd_por_uva,
            {
                "mark": {
                "type": "bar",
                "color": "#722F37"
            },
                "encoding": {
                    "y": {
                        "field": "Uva",
                        "type": "nominal",
                        "sort": "-x",
                        "title": None
                    },
                    "x": {
                        "field": "Quantidade",
                        "type": "quantitative",
                        "title": "Quantidade"
                    }
                },
                "height": 330
            },
            width="stretch"
        )