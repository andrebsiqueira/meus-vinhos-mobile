import streamlit as st
import pandas as pd

from banco import conectar

def show_people():

    if "pessoa_selecionada" not in st.session_state:
        st.session_state.pessoa_selecionada = None

    # ==========================================================
    # TÍTULO
    # ==========================================================

    st.markdown(
        '<div class="secao" style="font-size: 28px;">A Turma do Vinho</div>',
        unsafe_allow_html=True
    )

    st.info(
        "Quem está sempre por perto quando chega a hora de abrir uma garrafa? 😄"
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
        font-size: 15px;
        white-space: nowrap;
    }
    .people-vinhos {
        display: inline-block;
        background: #6A1B29;
        color: #FFFFFF;
        border-radius: 18px;
        padding: 6px 12px;
        font-size: 15px;
        white-space: nowrap;
    }
    .last-wines {
        font-size: 15px;
        color: #292929;
        margin: 4px 0 4px 8px;
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

    filtro_pessoa = ""
    parametros = []

    if st.session_state.pessoa_selecionada is not None:
        filtro_pessoa = "WHERE p.id = ?"
        parametros.append(st.session_state.pessoa_selecionada)

    df = pd.read_sql_query(
        f"""
        SELECT
            p.id,
            p.nome,
            p.abreviacao,
            p.foto,

            COUNT(v.id) AS quantidade_vinhos

        FROM pessoas p

        LEFT JOIN vinhos v
            ON (
                ',' ||
                REPLACE(
                    REPLACE(
                        COALESCE(v.pessoas, ''),
                        ' e ',
                        ', '
                    ),
                    ' ',
                    ''
                )
                || ','
            ) LIKE
                '%,' || REPLACE(p.abreviacao, ' ', '') || ',%'

        {filtro_pessoa}

        GROUP BY
            p.id,
            p.nome,
            p.abreviacao,
            p.foto

        ORDER BY
            quantidade_vinhos DESC,
            p.nome
        """,
        conn,
        params=parametros
    )

    conn.close()

    # ==========================================================
    # NENHUMA PESSOA
    # ==========================================================

    if df.empty:
        st.warning("No people found in your wine collection.")
        return

    # ==========================================================
    # BUSCAR OS ÚLTIMOS VINHOS DE CADA PESSOA
    # ==========================================================

    conn = conectar()

    df_ultimos_vinhos = pd.read_sql_query(
        """
        SELECT
            p.id AS pessoa_id,
            v.id AS vinho_id,
            v.nome AS vinho,
            v.data_vinho
        FROM pessoas p
        JOIN vinhos v
            ON (
                ',' ||
                REPLACE(
                    REPLACE(
                        COALESCE(v.pessoas, ''),
                        ' e ',
                        ', '
                    ),
                    ' ',
                    ''
                )
                || ','
            ) LIKE
                '%,' || REPLACE(p.abreviacao, ' ', '') || ',%'
        ORDER BY
            p.id,
            v.data_vinho DESC,
            v.id DESC
        """,
        conn
    )

    conn.close()

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
        # Últimos vinhos
        # ------------------------------------------------------

        vinhos_pessoa = df_ultimos_vinhos[
            df_ultimos_vinhos["pessoa_id"] == pessoa["id"]
        ]

        if st.session_state.pessoa_selecionada is not None:

            # Pessoa selecionada → todos os vinhos
            nomes_ultimos = vinhos_pessoa["vinho"].tolist()

        else:

            # Lista normal → apenas os 3 últimos
            nomes_ultimos = vinhos_pessoa["vinho"].head(3).tolist()

        if nomes_ultimos:

            texto_ultimos = "<br>".join(nomes_ultimos)

        else:

            texto_ultimos = "No wines recorded yet"

        # ------------------------------------------------------
        # Texto da quantidade
        # ------------------------------------------------------

        if quantidade == 1:
            texto_garrafas = "1 vinho"
        else:
            texto_garrafas = f"{quantidade} vinhos"

        # ------------------------------------------------------
        # Medalha
        # ------------------------------------------------------

        if ranking == 1:
            medalha = "🥇 Top"
        elif ranking == 2:
            medalha = "🥈 Top"
        elif ranking == 3:
            medalha = "🥉 Top"
        else:
            medalha = "#"

        # ------------------------------------------------------
        # Foto
        # ------------------------------------------------------

        foto = pessoa["foto"]

        # ------------------------------------------------------
        # CARD
        # ------------------------------------------------------

        with st.container(border=True):

            st.markdown(
                f"""
                <div class="people-card">
                    <div class="people-header">
                            <div class="people-initials">{abreviacao}</div>
                        <div>
                            <div class="people-name">
                                {nome}
                            </div>
                            <div>
                            <div class="people-ranking">
                                {medalha} {ranking}
                            </div>
                            <div class="people-vinhos">
                                {texto_garrafas}
                            </div>
                            </div>
                        </div>
                    </div>
                    <div class="people-divider"></div>
                    <div class="people-info">
                        🍷 Últimos vinhos:
                    </div>
                    <div class="last-wines">
                        {texto_ultimos}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("""
            <style>
            /* Botão Explorar Vinícola */
            div.stButton > button {
                background-color: #6A1B29 !important;
                color: white !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 4px 8px !important;
            }
            /* Texto dentro do botão */
            div.stButton > button p {
                font-size: 14px !important;
                font-weight: 500 !important;
                margin: 0 !important;
            }
            /* Hover */
            div.stButton > button:hover {
                opacity: 0.9 !important;
            }
            </style>
            """, unsafe_allow_html=True)

            if st.session_state.get("pessoa_selecionada") is None:

                if st.button(
                    "Ver todos os Vinhos →",
                    key=f"view_person_{pessoa['id']}",
                    width="stretch"
                ):
                    st.session_state.pessoa_selecionada = pessoa["id"]
                    st.rerun()

            elif st.session_state.pessoa_selecionada == pessoa["id"]:

                if st.button(
                    "← Voltar",
                    key=f"back_people_{pessoa['id']}",
                    width="stretch"
                ):
                    st.session_state.pessoa_selecionada = None
                    st.rerun()