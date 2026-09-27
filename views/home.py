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
            "A personal catalog to record, organize and rediscover your wines."
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

    qtd_por_uva.columns = ["Grape", "Quantidade"]

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
                        "field": "Grape",
                        "type": "nominal",
                        "sort": "-x",
                        "title": None
                    },
                    "x": {
                        "field": "Quantidade",
                        "type": "quantitative",
                        "title": "Number of Bottles"
                    }
                },
                "height": 330
            },
            width="stretch"
        )

    # ==========================================================
    # CHART 2 - WINES BY PRODUCING COUNTRY
    # ==========================================================

    st.markdown(
        '<div class="secao" style="font-size: 22px; text-align: left;">Chart 2: Wine by Producing Country</div>',
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    qtd_por_pais = (
        df_vinhos["pais"]
        .fillna("Não informado")
        .value_counts()
        .sort_values(ascending=False)
        .reset_index()
    )

    qtd_por_pais.columns = ["Country", "Quantidade"]

    st.vega_lite_chart(
        qtd_por_pais,
        {
            "mark": {
            "type": "bar",
            "color": "#722F37"
        },
            "encoding": {
                "y": {
                    "field": "Country",
                    "type": "nominal",
                    "sort": "-x",
                    "title": None
                },
                "x": {
                    "field": "Quantidade",
                    "type": "quantitative",
                    "title": "Number of Bottles"
                }
            },
            "height": 300
        },
        #use_container_width=True
    )

    # ==========================================================
    # TOP 10 WINES BY VIVINO APP RATING
    # ==========================================================

    st.markdown(
        '<div class="secao" style="font-size: 22px; text-align: left;">Top 10 Wines by Vivino App Rating</div>',
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Convert Vivino rating to numeric
    df_vivino = df_vinhos.copy()

    df_vivino["nota_vivino"] = pd.to_numeric(
        df_vivino["nota_vivino"],
        errors="coerce"
    )

    # Remove wines without a Vivino rating
    df_vivino = df_vivino.dropna(subset=["nota_vivino"])

    # Sort by Vivino rating and select Top 10
    top_10_vivino = (
        df_vivino
        .sort_values(
            by="nota_vivino",
            ascending=False
        )
        .head(10)
        .reset_index(drop=True)
    )

    # Display wines
    for i, (_, vinho) in enumerate(top_10_vivino.iterrows(), start=1):

        nome = vinho["nome"] or "Unknown Wine"
        vinicola = vinho["vinicola"] or "Unknown Winery"
        nota = vinho["nota_vivino"]

        st.markdown(
            f"""
            <div style="
                display: flex;
                align-items: center;
                width: 100%;
                padding: 10px 5px;
                border-bottom: 1px solid rgba(128,128,128,0.20);
            ">
                <div style="
                    width: 35px;
                    font-size: 18px;
                    font-weight: 600;
                    text-align: center;
                ">
                    {i}
                </div>

                <div style="
                    flex: 1;
                    padding-left: 8px;
                ">
                    <div style="
                        font-size: 16px;
                        font-weight: 600;
                    ">
                        {nome}
                    </div>

                    <div style="
                        font-size: 13px;
                        opacity: 0.70;
                        margin-top: 2px;
                    ">
                        {vinicola}
                    </div>
                </div>

                <div style="
                    font-size: 16px;
                    font-weight: 600;
                    white-space: nowrap;
                ">
                    ⭐ {nota:.1f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
