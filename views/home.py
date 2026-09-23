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
                            🍷 Regions
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