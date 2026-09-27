import streamlit as st
import pandas as pd

from banco import conectar
from datetime import datetime
import html

from funcoes import (
    imagem_base64,
    localizar_imagem_garrafa,
    localizar_imagem_foto
)


def show_my_wines():

    st.markdown(
        '<div class="secao" style="font-size: 28px;">🍷 My Wines</div>',
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    pesquisa = ""

    regiao_selecionada = st.session_state.get(
        "regiao_selecionada"
    )

    vinho_selecionado = st.session_state.get(
        "vinho_selecionado"
    )

    ano_selecionado = st.session_state.get(
        "ano_selecionado",
        "TODOS"
    )

    # ============================================================
    # FORM DE PESQUISA E FILTRO POR ANO DA DEGUSTAÇÃO DO VINHO
    # ============================================================

    if not vinho_selecionado and not regiao_selecionada:

        conexao = conectar()

        anos_disponiveis = pd.read_sql_query(
            """
            SELECT DISTINCT ano_vinho
            FROM vinhos
            WHERE ano_vinho IS NOT NULL
            ORDER BY ano_vinho DESC
            """,
            conexao
        )["ano_vinho"].tolist()

        conexao.close()

        # Converter os anos para inteiros
        anos_disponiveis = [
            int(ano) for ano in anos_disponiveis
            if str(ano).strip().isdigit()
        ]

        anos_disponiveis = sorted(
            set(anos_disponiveis),
            reverse=True
        )

        #Adicionar a opção TODOS no início
        filtro_ano_vinho = ["TODOS"] + anos_disponiveis

        #col_pesquisa, col_ano = st.columns([3, 1])

        #with col_pesquisa:

        pesquisa = st.text_input(
                "🔎 Search ALL Wines",
                placeholder="Enter wine name, winery, grape..."
            )


        #with col_ano:

        ano_selecionado = st.selectbox(
                "📅 Tasting Year",
                options=filtro_ano_vinho,
                index=(
                    filtro_ano_vinho.index(ano_selecionado)
                    if ano_selecionado in filtro_ano_vinho
                    else 0
                ),
                key="ano_selecionado"
            )

    if vinho_selecionado:
        #UM VINHO SELECIONADO

        regiao_selecionada = None
        pesquisa = ""

        conexao = conectar()

        df_vinho_filtrado = pd.read_sql_query("""
        SELECT
            v.id,
            v.nome,
            v.vinicola_id,
            vi.nome AS vinicola,
            vi.pais,
            vi.regiao,
            v.uva,
            v.safra,
            v.tipo,
            v.nota_vivino,
            v.data_vinho,
            v.observacoes,
            v.pessoas,
            v.foto_arquivo,
            v.imagem_garrafa
        FROM vinhos v
        LEFT JOIN vinicolas vi
            ON v.vinicola_id = vi.id
        WHERE v.id = ?
        ORDER BY v.data_vinho DESC
        """, 
        conexao,
        params=(vinho_selecionado,))

        nome = df_vinho_filtrado.iloc[0]["nome"]
        safra = df_vinho_filtrado.iloc[0]["safra"]

        if safra == None:
            safra = " "

        st.markdown(
            f"### {nome} {safra}"
        )

        st.info(
            f"Você está visualizando somente os dados deste vinho. "
        )

        conexao.close()

        vinho = df_vinho_filtrado.iloc[0]

        vinho_id = vinho["id"]
        nome = vinho["nome"]
        tipo = vinho["tipo"]
        uva = vinho["uva"]
        vinicola = vinho["vinicola"]
        regiao = vinho["regiao"]
        pais = vinho["pais"]
        nota_vivino = vinho["nota_vivino"]
        observacoes = vinho["observacoes"]
        data_vinho = vinho["data_vinho"]
        pessoas = vinho["pessoas"]
        foto_arquivo = vinho["foto_arquivo"]
        imagem_garrafa = vinho["imagem_garrafa"]

        if data_vinho:
                data_vinho = datetime.strptime(str(data_vinho), "%Y:%m:%d %H:%M:%S").strftime("%d-%m-%Y")
        else:
                data_vinho = "."

        if uva is None or str(uva).lower() == "nan" or str(uva).strip() == "":
                uva = "Não informada ou não registrada"
        else:
                uva = html.escape(str(uva))

        if pd.notna(vinho["safra"]):
                safra = vinho["safra"]
        else:
                safra = "não informada"

        if nota_vivino is None or str(nota_vivino).lower() == "nan" or str(nota_vivino).strip() == "":
                nota = "⭐ Não disponível"
        else:                    
                nota = f"⭐ App Vivino: {vinho['nota_vivino']}"

        if observacoes is None or str(observacoes).lower() == "nan" or str(observacoes).strip() == "":
                observacoes = "."
        else:
                observacoes = html.escape(str(observacoes))

        if pessoas is None or str(pessoas).lower() == "nan" or str(pessoas).strip() == "":
                pessoas = "."
        else:
                pessoas = html.escape(str(pessoas))

        if foto_arquivo is None or str(foto_arquivo).lower() == "nan" or str(foto_arquivo).strip() == "":
                foto_arquivo = "-"
        else:
                foto_arquivo = str(foto_arquivo)

        imagem_garrafa_path = localizar_imagem_garrafa(imagem_garrafa)

        imagem_b64, mime_type = imagem_base64(imagem_garrafa_path)

        if imagem_b64:

                            if not mime_type:
                                mime_type = "image/png"

                            imagem_html = f"""
                                <img
                                    src="data:{mime_type};base64,{imagem_b64}"
                                    style="
                                        width: 100%;
                                        height: 250px;
                                        object-fit: contain;
                                        display: block;
                                        margin: auto;
                                    "
                                >
                            """

        else:

                            imagem_html = """
                                <div style="
                                    height: 250px;
                                    display: flex;
                                    align-items: center;
                                    justify-content: center;
                                    font-size: 40px;
                                ">
                                    🍷
                                </div>
                            """

        st.markdown(f"""
                        <div class="card">
                            <!-- NOME DO VINHO -->
                            <div class="card-texto-bold">{nome}</div>
                            <!-- ÁREA DA IMAGEM DA GARRAFA + INFORMAÇÕES -->
                            <div style="
                                display: flex;
                                width: 100%;
                                margin-top: 15px;
                                align-items: flex-start;
                            ">
                                <!-- FOTO DA GARRAFA -->
                                <div style="
                                    width: 27%;
                                    display: flex;
                                    align-items: center;
                                    justify-content: center;
                                    padding: 10px;
                                    box-sizing: border-box;
                                ">{imagem_html}</div>
                                <!-- INFORMAÇÕES -->
                                <div style="
                                    width: 73%;
                                    padding: 5px 10px;
                                    box-sizing: border-box;
                                ">
                                    <div class="card-texto">
                                        Vinho {tipo}
                                    </div>
                                    <div class="card-texto">
                                        Safra {safra}
                                    </div>
                                    <div style="height: 14px;"><br></div>
                                    <div class="card-texto">
                                        🏛️ {vinicola}
                                    </div>
                                    <div class="card-texto">
                                        📍 {regiao}, {pais}
                                    </div>
                                    <div style="height: 14px;"><br></div>
                                    <div class="card-texto">
                                        🍇 Variedades:
                                    </div>
                                    <div class="card-texto">{uva}</div>
                                    <div style="height: 14px;"><br></div>
                                    <div class="card-texto">
                                    {nota}
                                    </div>
                                </div>
                            </div>
                                <div class="card-texto-obs">
                                Minhas anotações:
                                </div>
                                <div class="card-texto-obs">
                                {data_vinho} - {observacoes}
                                </div>
                                <div class="card-texto-obs">
                                {pessoas}
                                </div>
                            <!-- FOTO DA GARRAFA -->
                                <div style="
                                    text-align: right;
                                ">
                                    <div class="card-texto">
                                        {foto_arquivo}
                                    </div>
                                </div>
                        </div>
                        """, unsafe_allow_html=True)

        caminho_foto = localizar_imagem_foto(foto_arquivo)

        if caminho_foto:
                    st.image(
                        str(caminho_foto),
                        width="stretch"
                    )

        if st.button("← Ver TODOS os vinhos cadastrados", key="ver_todos_vinhos"):
            st.session_state["regiao_selecionada"] = None
            st.session_state["vinho_selecionado"] = None
            st.rerun()

    elif regiao_selecionada:
        #REGIÃO SELECIONADA

        vinho_selecionado = None
        pesquisa = ""

        conexao = conectar()

        df_regiao_filtrada = pd.read_sql_query("""
        SELECT
            v.id,
            v.nome,
            v.vinicola_id,
            vi.nome AS vinicola,
            vi.pais,
            vi.regiao,
            v.uva,
            v.safra,
            v.tipo,
            v.nota_vivino,
            v.data_vinho,
            v.observacoes,
            v.pessoas,
            v.foto_arquivo,
            v.imagem_garrafa
        FROM vinhos v
        LEFT JOIN vinicolas vi
            ON v.vinicola_id = vi.id
        WHERE vi.regiao = ?
        ORDER BY v.data_vinho DESC
        """, 
        conexao,
        params=(regiao_selecionada,))

        pesquisa = ""

        pais = ""

        if not df_regiao_filtrada.empty:
            pais = df_regiao_filtrada.iloc[0]["pais"]

        st.markdown(
            f"### 🌎 {regiao_selecionada}, {pais}"
        )

        st.info(
            f"You are viewing only the wines from this region."
        )

        conexao.close()

        #colunas = st.columns(3)

        for i, (_, vinho) in enumerate(df_regiao_filtrada.iterrows()):

                    vinho_id = vinho["id"]
                    nome = vinho["nome"]
                    tipo = vinho["tipo"]
                    uva = vinho["uva"]
                    vinicola = vinho["vinicola"]
                    regiao = vinho["regiao"]
                    pais = vinho["pais"]
                    nota_vivino = vinho["nota_vivino"]
                    observacoes = vinho["observacoes"]
                    data_vinho = vinho["data_vinho"]
                    pessoas = vinho["pessoas"]
                    foto_arquivo = vinho["foto_arquivo"]
                    imagem_garrafa = vinho["imagem_garrafa"]

                    if data_vinho:
                        data_vinho = datetime.strptime(str(data_vinho), "%Y:%m:%d %H:%M:%S").strftime("%d-%m-%Y")
                    else:
                        data_vinho = "."

                    if uva is None or str(uva).lower() == "nan" or str(uva).strip() == "":
                        uva = "Não informada ou não registrada"
                    else:
                        uva = html.escape(str(uva))

                    if pd.notna(vinho["safra"]):
                        safra = vinho["safra"]
                    else:
                        safra = "não informada"

                    if nota_vivino is None or str(nota_vivino).lower() == "nan" or str(nota_vivino).strip() == "":
                        nota = "⭐ Não disponível"
                    else:                    
                        nota = f"⭐ App Vivino: {vinho['nota_vivino']}"

                    if observacoes is None or str(observacoes).lower() == "nan" or str(observacoes).strip() == "":
                        observacoes = "."
                    else:
                        observacoes = html.escape(str(observacoes))

                    if pessoas is None or str(pessoas).lower() == "nan" or str(pessoas).strip() == "":
                        pessoas = "."
                    else:
                        pessoas = html.escape(str(pessoas))

                    if foto_arquivo is None or str(foto_arquivo).lower() == "nan" or str(foto_arquivo).strip() == "":
                        foto_arquivo = "-"
                    else:
                        foto_arquivo = str(foto_arquivo)


                    imagem_garrafa_path = localizar_imagem_garrafa(imagem_garrafa)

                    imagem_b64, mime_type = imagem_base64(imagem_garrafa_path)

                    if imagem_b64:

                        if not mime_type:
                            mime_type = "image/png"

                        imagem_html = f"""
                            <img
                                src="data:{mime_type};base64,{imagem_b64}"
                                style="
                                    width: 100%;
                                    height: 250px;
                                    object-fit: contain;
                                    display: block;
                                    margin: auto;
                                "
                            >
                        """

                    else:

                        imagem_html = """
                            <div style="
                                height: 250px;
                                display: flex;
                                align-items: center;
                                justify-content: center;
                                font-size: 40px;
                            ">
                                🍷
                            </div>
                        """

                    st.markdown(f"""
                    <div class="card">
                        <!-- NOME DO VINHO -->
                        <div class="card-texto-bold">{nome}</div>
                        <!-- ÁREA DA IMAGEM DA GARRAFA + INFORMAÇÕES -->
                        <div style="
                            display: flex;
                            width: 100%;
                            margin-top: 15px;
                            align-items: flex-start;
                        ">
                            <!-- FOTO DA GARRAFA -->
                            <div style="
                                width: 27%;
                                display: flex;
                                align-items: center;
                                justify-content: center;
                                padding: 10px;
                                box-sizing: border-box;
                            ">{imagem_html}</div>
                            <!-- INFORMAÇÕES -->
                            <div style="
                                width: 73%;
                                padding: 5px 10px;
                                box-sizing: border-box;
                            ">
                                <div class="card-texto">
                                    Vinho {tipo}
                                </div>
                                <div class="card-texto">
                                    Safra {safra}
                                </div>
                                <div style="height: 14px;"><br></div>
                                <div class="card-texto">
                                    🏛️ {vinicola}
                                </div>
                                <div class="card-texto">
                                    📍 {regiao}, {pais}
                                </div>
                                <div style="height: 14px;"><br></div>
                                <div class="card-texto">
                                    🍇 Variedades:
                                </div>
                                <div class="card-texto">{uva}</div>
                                <div style="height: 14px;"><br></div>
                                <div class="card-texto">
                                {nota}
                                </div>
                            </div>
                        </div>
                            <div class="card-texto-obs">
                            Minhas anotações:
                            </div>
                            <div class="card-texto-obs">
                            {data_vinho} - {observacoes}
                            </div>
                            <div class="card-texto-obs">
                            {pessoas}
                            </div>
                        <!-- FOTO DA GARRAFA -->
                            <div style="
                                text-align: right;
                            ">
                                <div class="card-texto">
                                    {foto_arquivo}
                                </div>
                            </div>
                    </div>
                    """, unsafe_allow_html=True)


                    if foto_arquivo != "-":

                        if st.button(
                            "Exibir foto do vinho",
                            key=f"vinho_{vinho_id}",
                            width="stretch"
                        ):
                            st.session_state["vinho_selecionado"] = vinho_id
                            st.session_state["regiao_selecionada"] = None
                            st.rerun()

                    else:

                        st.button(
                            " ",
                            key=f"vinho_{vinho_id}",
                            width="stretch",
                            disabled=True
                        )


        if st.button("← Ver TODOS os vinhos cadastrados", key="ver_todos_vinhos"):
            st.session_state["regiao_selecionada"] = None
            st.session_state["vinho_selecionado"] = None
            st.session_state["pesquisa_vinhos"] = ""
            st.rerun()

