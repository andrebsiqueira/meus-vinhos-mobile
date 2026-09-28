import streamlit as st
import pandas as pd

from pathlib import Path

from banco import conectar

def show_settings():

    st.markdown(
        '<div class="secao" style="font-size: 28px;">🍷 Settings</div>',
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    selectbox_options = [
        " ",
        "Database Information",
        "Check Wine Photos in Folder",
        "Register a New Winery with AI Assistance"
    ]

    selected_option = st.selectbox(
        "Select an option",
        selectbox_options
    )

    if selected_option == "Database Information":

        # ==========================================================
        # DATABASE INFORMATION
        # ==========================================================

        st.markdown(
            '<div class="secao" style="font-size: 22px; text-align: left;">Database Information</div>',
            unsafe_allow_html=True
        )

        try:

            conn = conectar()
            cursor = conn.cursor()

            # ------------------------------------------------------
            # COLLECTION
            # ------------------------------------------------------

            cursor.execute("SELECT COUNT(*) FROM vinhos")
            total_vinhos = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM vinicolas")
            total_vinicolas = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COUNT(DISTINCT regiao)
                FROM vinicolas
                WHERE regiao IS NOT NULL
                AND TRIM(regiao) <> ''
            """)
            total_regioes = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COUNT(DISTINCT pais)
                FROM vinicolas
                WHERE pais IS NOT NULL
                AND TRIM(pais) <> ''
            """)
            total_paises = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM pessoas")
            total_pessoas = cursor.fetchone()[0]

            # ------------------------------------------------------
            # WINE DATA
            # ------------------------------------------------------

            cursor.execute("""
                SELECT COUNT(*)
                FROM vinhos
                WHERE foto_arquivo IS NOT NULL
                AND TRIM(foto_arquivo) <> ''
            """)
            vinhos_com_fotos = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COUNT(*)
                FROM vinhos
                WHERE imagem_garrafa IS NOT NULL
                AND TRIM(imagem_garrafa) <> ''
            """)
            vinhos_com_imagem_garrafa = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COUNT(*)
                FROM vinhos
                WHERE data_vinho IS NOT NULL
                AND TRIM(data_vinho) <> ''
            """)
            vinhos_com_data = cursor.fetchone()[0]

            conn.close()

            # ======================================================
            # COLLECTION
            # ======================================================

            st.markdown(
                '<div style="font-size: 18px; font-weight: 600; margin-top: 10px;">Collection</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div style="'
                'border-bottom: 1px solid rgba(128,128,128,0.20);'
                'margin-top: 5px;'
                'margin-bottom: 15px;'
                '"></div>',
                unsafe_allow_html=True
            )

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Wines", total_vinhos)

            with col2:
                st.metric("Wineries", total_vinicolas)

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Regions", total_regioes)

            with col2:
                st.metric("Countries", total_paises)

            col1, col2 = st.columns(2)

            with col1:
                st.metric("People", total_pessoas)

            # ======================================================
            # WINE DATA
            # ======================================================

            st.markdown(
                '<div style="font-size: 18px; font-weight: 600; margin-top: 25px;">Wine Data</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div style="'
                'border-bottom: 1px solid rgba(128,128,128,0.20);'
                'margin-top: 5px;'
                'margin-bottom: 15px;'
                '"></div>',
                unsafe_allow_html=True
            )

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Wines with photos", vinhos_com_fotos)

            with col2:
                st.metric("Bottle images", vinhos_com_imagem_garrafa)

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Tasting dates", vinhos_com_data)

            # ======================================================
            # DATABASE FILE
            # ======================================================

            st.markdown(
                '<div style="font-size: 18px; font-weight: 600; margin-top: 25px;">Database</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div style="'
                'border-bottom: 1px solid rgba(128,128,128,0.20);'
                'margin-top: 5px;'
                'margin-bottom: 15px;'
                '"></div>',
                unsafe_allow_html=True
            )

            # settings.py está dentro da pasta pages
            db_path = Path(__file__).resolve().parent.parent / "vinhos.db"

            if db_path.exists():

                tamanho_mb = db_path.stat().st_size / (1024 * 1024)

                data_atualizacao = db_path.stat().st_mtime

                from datetime import datetime

                ultima_atualizacao = datetime.fromtimestamp(
                    data_atualizacao
                ).strftime("%d/%m/%Y %H:%M")

                st.write(f"**Database file:** {db_path.name}")
                st.write(f"**Database size:** {tamanho_mb:.2f} MB")
                st.write(f"**Last updated:** {ultima_atualizacao}")

            else:

                st.warning("Database file not found.")

        except Exception as e:

            st.error(f"Unable to load database information: {e}")

    elif selected_option == "Check Wine Photos in Folder":

        # ==========================================================
        # WINE PHOTOS FOLDER CHECK
        # ==========================================================

        PASTA_FOTOS = Path(__file__).resolve().parent.parent / "wine_photos"

        def normalizar_nome_arquivo(caminho):
            if not caminho:
                return None

            return Path(str(caminho)).name.strip().lower()


        try:

            # ------------------------------------------------------
            # FOTOS CADASTRADAS NO BANCO
            # ------------------------------------------------------

            conn = conectar()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, nome, foto_arquivo
                FROM vinhos
                WHERE foto_arquivo IS NOT NULL
                AND TRIM(foto_arquivo) <> ''
                ORDER BY nome
            """)

            registros = cursor.fetchall()

            conn.close()

            # ------------------------------------------------------
            # ARQUIVOS EXISTENTES NA PASTA
            # ------------------------------------------------------

            if PASTA_FOTOS.exists():

                arquivos_pasta = {
                    arquivo.name.lower(): arquivo
                    for arquivo in PASTA_FOTOS.iterdir()
                    if arquivo.is_file()
                }

            else:

                arquivos_pasta = {}

            # ------------------------------------------------------
            # COMPARAÇÃO
            # ------------------------------------------------------

            fotos_banco = {}

            for registro in registros:

                vinho_id = registro[0]
                nome_vinho = registro[1]
                foto_arquivo = registro[2]

                foto = normalizar_nome_arquivo(foto_arquivo)

                if foto:
                    fotos_banco[foto] = {
                        "id": vinho_id,
                        "nome": nome_vinho,
                        "arquivo": foto_arquivo
                    }

            fotos_faltando = []

            for nome_arquivo, registro in fotos_banco.items():

                if nome_arquivo not in arquivos_pasta:

                    fotos_faltando.append(registro)

            # ------------------------------------------------------
            # RESULTADOS
            # ------------------------------------------------------

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Photos in database",
                    len(fotos_banco)
                )

            with col2:
                st.metric(
                    "Files in wine_photos",
                    len(arquivos_pasta)
                )

            with col3:
                st.metric(
                    "Missing files",
                    len(fotos_faltando)
                )

            #st.markdown("<br>", unsafe_allow_html=True)

            # ------------------------------------------------------
            # FOTOS FALTANDO
            # ------------------------------------------------------

            if fotos_faltando:

                st.warning(
                    f"{len(fotos_faltando)} wine photo(s) registered in the database "
                    "were not found in the wine_photos folder."
                )

                for foto in fotos_faltando:

                    st.markdown(
                        f"""
                        <div style="
                            padding: 8px 5px;
                            border-bottom: 1px solid rgba(128,128,128,0.20);
                            margin-bottom: 8px;
                        ">
                            <div style="
                                font-size: 16px;
                                font-weight: 600;
                            ">
                                {foto["nome"] or "Unknown Wine"}
                            </div>
                            <div style="
                                font-size: 13px;
                                opacity: 0.70;
                                margin-top: 3px;
                            ">
                                {foto["arquivo"]}
                            </div>
                            <div style="
                                font-size: 12px;
                                opacity: 0.55;
                                margin-top: 2px;
                            ">
                                Wine ID: {foto["id"]}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            else:

                st.success(
                    "All wine photos registered in the database "
                    "were found in the wine_photos folder."
                )

        except Exception as e:

            st.error(f"Unable to check wine photos: {e}")

    elif selected_option == "Register a New Winery with AI Assistance":

        # ==========================================================
        # REGISTER A NEW WINERY WITH AI ASSISTANCE
        # ==========================================================

        st.write()