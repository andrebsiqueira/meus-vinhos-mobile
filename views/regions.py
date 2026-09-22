import streamlit as st
import pandas as pd

from banco import conectar

from funcoes import (
    localizar_imagem_regiao
)

def show_regions():

    st.markdown(
        '<div class="secao" style="font-size: 28px;">🌎 Regions</div>',
        unsafe_allow_html=True
    )

    conexao = conectar()

    df_paises = pd.read_sql_query(
        """
        SELECT
            pais,
            COUNT(DISTINCT regiao) AS quantidade_regioes
        FROM vinicolas
        WHERE pais IS NOT NULL
        AND TRIM(pais) <> ''
        AND regiao IS NOT NULL
        AND TRIM(regiao) <> ''
        GROUP BY pais
        ORDER BY pais ASC
        """,
        conexao
    )

    conexao.close()

    # Montar as opções do selectbox
    filtro_pais_regiao = ["TODOS"]

    for _, linha in df_paises.iterrows():

        pais = linha["pais"]
        quantidade = int(linha["quantidade_regioes"])

        texto = (
            f"{pais}: "
            f"{quantidade} "
            f"{'região' if quantidade == 1 else 'regiões'}"
        )

        filtro_pais_regiao.append(texto)

    st.info(
            "Explore your wine collection by wine-producing regions."
        )

    col1, col2 = st.columns([2, 1])

    with col1:

        pais_exibido = st.selectbox(
                "Filter regions by country",
                options=filtro_pais_regiao,
                index=0,
                key="pais_selecionado"
            )

    with col2:

        st.write("")

    # Recuperar somente o nome do país
    if pais_exibido == "TODOS":
        pais_selecionado = None
    else:
        pais_selecionado = pais_exibido.split(":")[0].strip()


    # =========================================================
    # IMAGENS
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


    # =========================================================
    # BUSCAR REGIÕES
    # =========================================================

    conexao = conectar()

    sql = """
        SELECT
            v.regiao,
            v.pais,
            COUNT(DISTINCT v.id) AS quantidade_vinicolas,
            COUNT(DISTINCT vin.id) AS quantidade_vinhos
        FROM vinicolas v
        LEFT JOIN vinhos vin
            ON vin.vinicola_id = v.id
        WHERE v.regiao IS NOT NULL
        AND TRIM(v.regiao) <> ''
    """

    params = []

    if pais_selecionado != "TODOS" and pais_selecionado != None:
        sql += """
            AND v.pais = ?
        """
        params.append(pais_selecionado)

    sql += """
        GROUP BY v.regiao, v.pais
        ORDER BY quantidade_vinicolas DESC
    """

    df_regioes = pd.read_sql_query(
        sql,
        conexao,
        params=params
    )

    conexao.close()

    # =========================================================
    # EXIBIR REGIÕES - MOBILE
    # =========================================================

    @st.cache_data
    def carregar_imagem_regiao(caminho):
        return caminho.read_bytes()

    if df_regioes.empty:

        st.info("Nenhuma região encontrada.")

    else:

        for i, (_, linha) in enumerate(df_regioes.iterrows()):

            nome_regiao = str(linha["regiao"])

            nome_arquivo = imagens_regioes.get(nome_regiao)

            caminho_imagem = None

            if nome_arquivo:
                caminho_imagem = localizar_imagem_regiao(
                    nome_arquivo
                )

            pais = (
                str(linha["pais"])
                if linha["pais"]
                else "País não informado"
            )

            quantidade_vinicolas = int(
                linha["quantidade_vinicolas"]
            )

            quantidade_vinhos = int(
                linha["quantidade_vinhos"]
            )

            # =================================================
            # IMAGEM
            # =================================================

            if (
                caminho_imagem is not None
                and caminho_imagem.is_file()
            ):

                imagem = carregar_imagem_regiao(
                    caminho_imagem
                )

                st.image(
                    imagem,
                    width="stretch"
                )

            else:

                st.info(
                    f"Imagem não encontrada para {nome_regiao}"
                )

            # =================================================
            # INFORMAÇÕES
            # =================================================

            st.markdown(
                f"### {nome_regiao}"
            )

            st.caption(
                f"{pais}"
            )

            # =================================================
            # MÉTRICAS
            # =================================================

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "🏛️ Vinícolas",
                    quantidade_vinicolas
                )

            with col2:

                st.metric(
                    "🍷 Vinhos",
                    quantidade_vinhos
                )

            # =================================================
            # BOTÃO
            # =================================================

            if st.button(
                "🍷 Explorar região",
                key=f"explorar_regiao_{i}",
                width="stretch"
            ):

                st.session_state["regiao_selecionada"] = nome_regiao
                st.session_state["vinho_selecionado"] = None
                
