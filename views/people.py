import streamlit as st
import pandas as pd

from banco import conectar

def show_people():

    # ==========================================================
    # TÍTULO
    # ==========================================================

    st.markdown(
        '<div class="secao" style="font-size: 28px;">🤵🏻 People</div>',
        unsafe_allow_html=True
    )

    st.info(
        "Who is always there when it's time to open a bottle? 😄"
    )

    # ==========================================================
    # CSS DOS CARDS
    # ==========================================================

    st.markdown("""
    <style>
    /* Container geral */
    .people-card {
        background: rgba(255, 255, 255, 0.96);
        border: 1px solid #d8c9a5;
        border-radius: 22px;
        padding: 22px;
        margin: 0 0 18px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.10);
    }
    /* Cabeçalho do card */
    .people-header {
        display: flex;
        align-items: center;
        gap: 18px;
        margin-bottom: 18px;
    }
    /* Foto */
    .people-photo {
        width: 82px;
        height: 82px;
        min-width: 82px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid #d8c9a5;
    }
    /* Foto com abreviação */
    .people-initials {
        width: 82px;
        height: 82px;
        min-width: 82px;
        border-radius: 50%;
        background: #8b1e2d;
        color: #e8d39a;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        font-weight: 400;
        border: 2px solid #d8c9a5;
    }
    /* Nome */
    .people-name {
        font-family: Georgia, serif;
        font-size: 25px;
        color: #4a1720;
        margin-bottom: 8px;
    }
    /* Ranking */
    .people-ranking {
        display: inline-block;
        background: #ead9a7;
        color: #5a4314;
        border-radius: 18px;
        padding: 6px 12px;
        font-size: 13px;
        white-space: nowrap;
    }
    /* Separador */
    .people-divider {
        border-top: 1px solid #dedede;
        margin: 14px 0;
    }
    /* Informações */
    .people-info {
        font-size: 16px;
        color: #292929;
        margin: 8px 0;
    }
    .people-icon {
        font-size: 21px;
        margin-right: 10px;
    }
    /* Mobile */
    @media (max-width: 600px) {
        .people-card {
            padding: 18px;
            border-radius: 20px;
        }
        .people-header {
            gap: 14px;
        }
        .people-photo,
        .people-initials {
            width: 72px;
            height: 72px;
            min-width: 72px;
        }
        .people-name {
            font-size: 22px;
        }
        .people-ranking {
            font-size: 12px;
            padding: 5px 9px;
        }
        .people-info {
            font-size: 15px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # ==========================================================
    # BUSCAR PESSOAS
    # ==========================================================

    conn = conectar()

    df = pd.read_sql_query(
        """
        SELECT
            p.id,
            p.nome,
            p.abreviacao,
            p.foto,

            COUNT(v.id) AS quantidade_vinhos

        FROM pessoas p

        LEFT JOIN vinhos v
            ON (
                ',' || REPLACE(COALESCE(v.pessoas, ''), ' ', '') || ','
            ) LIKE
                '%,' || REPLACE(p.abreviacao, ' ', '') || ',%'

        GROUP BY
            p.id,
            p.nome,
            p.abreviacao,
            p.foto

        ORDER BY
            quantidade_vinhos DESC,
            p.nome
        """,
        conn
    )

    conn.close()

    # ==========================================================
    # NENHUMA PESSOA
    # ==========================================================

    if df.empty:
        st.warning("No people found in your wine collection.")
        return

    # ==========================================================
    # RANKING
    # ==========================================================

    df["ranking"] = range(1, len(df) + 1)

    # ==========================================================
    # CARDS
    # ==========================================================

    for _, pessoa in df.iterrows():

        nome = pessoa["nome"] or "Unknown"
        abreviacao = pessoa["abreviacao"] or "?"
        quantidade = int(pessoa["quantidade_vinhos"])
        ranking = int(pessoa["ranking"])

        # ------------------------------------------------------
        # Texto da quantidade
        # ------------------------------------------------------

        if quantidade == 1:
            texto_garrafas = "1 bottle"
        else:
            texto_garrafas = f"{quantidade} bottles"

        # ------------------------------------------------------
        # Medalha
        # ------------------------------------------------------

        if ranking == 1:
            medalha = "🥇"
        elif ranking == 2:
            medalha = "🥈"
        elif ranking == 3:
            medalha = "🥉"
        else:
            medalha = "🏅"

        # ------------------------------------------------------
        # Foto
        # ------------------------------------------------------

        foto = pessoa["foto"]

        # ------------------------------------------------------
        # CARD
        # ------------------------------------------------------

        st.markdown(
            f"""
            <div class="people-card">
                <div class="people-header">
                        <div class="people-initials">{abreviacao}</div>
                    <div>
                        <div class="people-name">
                            {nome}
                        </div>
                        <div class="people-ranking">
                            {medalha} Top {ranking} • {texto_garrafas}
                        </div>
                    </div>
                </div>
                <div class="people-divider"></div>
                <div class="people-info">
                    <span class="people-icon">🍷</span>
                    Wine collection: {texto_garrafas}
                </div>
                <div class="people-info">
                    <span class="people-icon">🥂</span>
                    Always ready for another toast!
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )