import streamlit as st
import pandas as pd

from banco import conectar

import base64
from pathlib import Path

from funcoes import (
    localizar_imagem_regiao
)

@st.cache_data
def obter_bandeira_png(country_code, width=20):
    """
    Busca o arquivo .png na pasta flag_images, converte para Base64
    e retorna a tag HTML <img> pronta.
    """

    # Não existe código de país
    if pd.isna(country_code):
        return ""

    # Converte para texto e remove espaços
    country_code = str(country_code).strip()

    # Código vazio
    if not country_code:
        return ""

    base_dir = Path(__file__).resolve().parent.parent

    file_path = (
        base_dir
        / "flag_images"
        / f"{country_code.lower()}.png"
    )

    if not file_path.exists():
        return ""

    with open(file_path, "rb") as f:
        data = f.read()

    encoded = base64.b64encode(data).decode("utf-8")

    return (
        f'<img src="data:image/png;base64,{encoded}" '
        f'width="{width}" '
        f'style="vertical-align: middle; '
        f'border-radius: 2px; margin-right: 6px;">'
    )

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
            v.bandeira,
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
            v.descricao,
            v.bandeira
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
        ORDER BY data_vinho DESC
        """,
        conexao,
        params=(vinicola_id,)
    )

    conexao.close()

    if df.empty:
        st.session_state["vinicola_selecionada"] = None
        st.rerun()

    vinicola = df.iloc[0]

    # =========================================================
    # IMAGENS REGIÕES
    # =========================================================

    imagens_regioes = {
        "Mendoza": "mendoza.jpg",
        "Alentejo": "alentejo.jpg",
        "Montevidéu": "montevideu.jpg",
        "Serra Gaúcha": "serragaucha.jpg",
        "Rías Baixas": "riasbaixas.jpg",
        "Valle del Colchagua": "valledelcolchagua.jpg",
        "Douro": "douro.jpg",
        "Ontario": "ontario.jpg",
        "Bairrada": "bairrada.jpg",
        "Valle del Cachapoal": "valledelcachapoal.jpg",
        "Salta": "salta.jpg",
        "Lisboa": "lisboa.jpg",
        "Dão": "dao.jpg",
        "Friuli-Venezia Giulia": "friuli-venezia giulia.jpg",
        "Vallée du Rhône": "rhone.jpg",
        "Toscana": "toscana.jpg",
        "Rioja": "rioja.jpg",
        "Veneto": "veneto.jpg",
        "Puglia": "puglia.jpg",
        "Vinhos Verdes": "vinhosverdes.jpg",
        "Península de Setúbal": "setubal.jpg",
        "Catalunha": "catalunha.jpg",
        "Serra Catarinense": "serracatarinense.jpg",
        "Valle del Maipo": "valledelmaipo.jpg"
    }

    nome_regiao = str(vinicola["regiao"])

    nome_arquivo = imagens_regioes.get(nome_regiao)

    caminho_imagem = None

    if nome_arquivo:
        caminho_imagem = localizar_imagem_regiao(
            nome_arquivo
        )
    else:
        caminho_imagem = localizar_imagem_regiao(
            "sem_imagem_regiao.jpg"
        )

    bandeira = vinicola["bandeira"]

    #Puxa a bandeira em PNG (usando a função de base64 criada)
    bandeira_html = obter_bandeira_png(bandeira, width=18)

    #base_dir = Path(__file__).resolve().parent.parent
    #caminho_imagem = base_dir / "region_images" / "serragaucha.jpg"

    with open(caminho_imagem, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")

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
    else:
        subregiao = "/ " + vinicola["subregiao"]

    cidade = vinicola["cidade"]

    if pd.isna(cidade) or str(cidade).strip() == "":
        cidade = ""

    st.markdown(
        f"""
        <div style="
            position: relative;
            height: 180px;
            border-radius: 12px;
            overflow: hidden;
            background-image: url('data:image/png;base64,{encoded}');
            background-size: cover;
            background-position: center;
        ">
            <div style="
                position: absolute;
                bottom: 0;
                left: 0;
                right: 0;
                padding: 30px 16px 14px 16px;
                background: linear-gradient(
                    transparent,
                    rgba(0,0,0,0.75)
                );
                color: white;
            ">
                <div style="
                    font-size: 30px;
                    font-weight: 600;
                ">
                    {vinicola["nome"]}
                </div>
                <div style="
                    font-size: 15px;
                    margin-top: 4px;
                ">
                    {bandeira_html} {pais} • {regiao} {subregiao}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    #st.markdown(f'### {vinicola["nome"]}')

    # DESCRIÇÃO
    descricao = vinicola["descricao"]

    if (
        not pd.isna(descricao)
        and str(descricao).strip() != ""
    ):
        st.markdown("### Sobre")
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

    st.markdown(f'### Minha experiência com a Vinícola')

    # QUANTIDADE DE VINHOS
    quantidade = int(vinicola["quantidade_vinhos"] or 0)

    texto_vinhos = (
        "1 vinho"
        if quantidade == 1
        else f"{quantidade} vinhos"
    )

    # VISITADA
    texto_visitada = vinicola["visitada"]

    if (
        texto_visitada is True
        or texto_visitada == 1
        or str(texto_visitada).lower() == "true"
    ):
        texto_visitada = "✓ <b>Visitada</b>"
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

        st.info("No wines from this winery are in my collection yet.")

    else:

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
                        {nome_vinho} {texto_safra}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # CSS customizado para o botão "Explorar Vinícola"
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

    # VOLTAR
    if st.button(
        "← Voltar para TODAS as Vinícolas",
        width="stretch"
    ):
        st.session_state["vinicola_selecionada"] = None
        st.rerun()


def show_wineries():

    st.markdown(
            '<div class="secao" style="font-size: 28px;">Vinícolas & Produtores</div>',
            unsafe_allow_html=True
        )

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

    pesquisa_vinicola = st.text_input(
            "🔎 Pesquisar Vinícolas",
            placeholder="Pesquise por vinícola, produtor, região, país..."
        )

    opcoes_filtro = [
            "Todas",
            "Brasil",
            "Portugal",
            "Argentina",
            "Chile",
            "Itália",
            "Espanha",
            "França",
            "✔️ Visitadas"
        ]

    opcoes_filtro_selecionado = st.pills(
            label="Filtro de opções",
            options=opcoes_filtro,
            default="Todas",
            selection_mode="single",
            label_visibility="collapsed"
        )

    # Feedback visual do que foi selecionado
    st.caption(f"Filtro ativo: **{opcoes_filtro_selecionado}**")

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
                v.instagram,
                v.bandeira
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
                v.instagram,
                v.bandeira
            ORDER BY v.nome ASC
            """,
            conexao
        )

    # =====================================================
    # FILTROS
    # =====================================================

    df_filtrado_vinicola = df_vinicolas.copy()

    # -----------------------------------------------------
    # FILTRO POR PAÍS / VISITADAS
    # -----------------------------------------------------

    if opcoes_filtro_selecionado == "Brasil":
            df_filtrado_vinicola = df_filtrado_vinicola[
                df_filtrado_vinicola["pais"].str.lower() == "brasil"
            ]

    elif opcoes_filtro_selecionado == "Portugal":
            df_filtrado_vinicola = df_filtrado_vinicola[
                df_filtrado_vinicola["pais"].str.lower() == "portugal"
            ]

    elif opcoes_filtro_selecionado == "Argentina":
            df_filtrado_vinicola = df_filtrado_vinicola[
                df_filtrado_vinicola["pais"].str.lower() == "argentina"
            ]

    elif opcoes_filtro_selecionado == "Chile":
            df_filtrado_vinicola = df_filtrado_vinicola[
                df_filtrado_vinicola["pais"].str.lower() == "chile"
            ]

    elif opcoes_filtro_selecionado == "Itália":
            df_filtrado_vinicola = df_filtrado_vinicola[
                df_filtrado_vinicola["pais"].str.lower() == "itália"
            ]

    elif opcoes_filtro_selecionado == "Espanha":
            df_filtrado_vinicola = df_filtrado_vinicola[
                df_filtrado_vinicola["pais"].str.lower() == "espanha"
            ]


    elif opcoes_filtro_selecionado == "França":
            df_filtrado_vinicola = df_filtrado_vinicola[
                df_filtrado_vinicola["pais"].str.lower() == "frança"
            ]

    elif opcoes_filtro_selecionado == "✔️ Visitadas":
            df_filtrado_vinicola = df_filtrado_vinicola[
                df_filtrado_vinicola["visitada"] == 1
            ]

    # -----------------------------------------------------
    # FILTRO DE PESQUISA
    # -----------------------------------------------------

    if pesquisa_vinicola.strip() != "":
            
        termo_vinicola = pesquisa_vinicola.strip().lower()

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

    # =====================================================
    # RESULTADO DA PESQUISA
    # =====================================================

    if pesquisa_vinicola.strip() != "" or opcoes_filtro_selecionado != "Todas":
            
        if len(df_filtrado_vinicola) == 0:
                st.info("Nenhuma vinícola encontrada.")
        else:
                st.info(
                    f"{len(df_filtrado_vinicola)} vinícola(s) encontrada(s)."
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
                "instagram",
                "bandeira"
            ]
        ]

    # =========================================================
    # FECHAR CONEXÃO
    # =========================================================

    conexao.close()

    # =========================================================
    # LISTA VINÍCOLAS
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

        bandeira = linha["bandeira"]

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
            indicador_visitada = "✓ Visitada"
        else:
            indicador_visitada = ""

        # -----------------------------------------------------
        # BANDEIRA
        # -----------------------------------------------------

        # Puxa a bandeira em PNG (usando a função de base64 criada)
        bandeira_html = obter_bandeira_png(bandeira, width=18)

        # -----------------------------------------------------
        # EXIBIR CARD DA VINÍCOLA
        # -----------------------------------------------------

        # Cria o card com borda nativa arredondada
        with st.container(border=True):
            # Renderiza o visual do card com nome, bandeira e informações
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                    <div>
                        <div style="font-weight: 600; font-size: 20px; color: #1a1a1a;">
                            {nome}
                        </div>
                        <div style="font-size: 15px; color: #666; display: flex; align-items: center; margin-top: 2px;">
                            {bandeira_html} <span>{pais}</span> &nbsp;•&nbsp; <span>{regiao}</span>
                        </div>
                    </div>
                    <div style="
                        background-color: #6A1B29;
                        color: white;
                        font-size: 15px;
                        font-weight: 600;
                        padding: 4px 8px;
                        border-radius: 20px;
                        white-space: nowrap;
                    ">
                        {texto_vinhos}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # CSS customizado para o botão "Explorar Vinícola"
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
            
            # Botão de ação direta dentro do card
            if st.button(
                "Explorar Vinícola →",
                key=f"vinicola_{linha['vinicola_id']}",
                width="stretch"
            ):
                st.session_state["vinicola_selecionada"] = linha["vinicola_id"]
                st.rerun()
