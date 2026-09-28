import streamlit as st
import pandas as pd

from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

import sqlite3

from banco import conectar

def show_settings():

    st.markdown(
        '<div class="secao" style="font-size: 28px;">💻 Settings</div>',
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    selectbox_options = [
        " ",
        "Database Information",
        "Check Wine Photos in Folder",
        "Register a New Winery with AI Assistance",
        "Register a New Person (Wine Lover)",
        "Register a New Wine with AI Assistance"
    ]

    selected_option = st.selectbox(
        "Select an option",
        selectbox_options
    )

    if selected_option == "Database Information":

        # ==========================================================
        # WINE DATA
        # ==========================================================

        st.markdown(
            '<div style="font-size: 18px; font-weight: 600; margin-top: 10px;">Wine Data</div>',
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

        # ----------------------------------------------------------
        # COUNTS
        # ----------------------------------------------------------

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM vinhos")
        total_vinhos = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM vinicolas")
        total_vinicolas = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM vinicolas v
            LEFT JOIN vinhos w
                ON w.vinicola_id = v.id
            WHERE w.id IS NULL
        """)

        vinicolas_sem_vinhos = cursor.fetchone()[0]

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

        PASTA_REGION_IMAGES = Path(__file__).resolve().parent.parent / "region_images"

        if PASTA_REGION_IMAGES.exists():
            total_region_images = sum(
                1 for arquivo in PASTA_REGION_IMAGES.iterdir()
                if arquivo.is_file()
            )
        else:
            total_region_images = 0

        conn.close()

        # ==========================================================
        # PERCENTAGES
        # ==========================================================

        percent_wine_photos = (
            (vinhos_com_fotos / total_vinhos) * 100
            if total_vinhos > 0
            else 0
        )

        percent_wineries_without_wines = (
            (vinicolas_sem_vinhos / total_vinicolas) * 100
            if total_vinicolas > 0
            else 0
        )

        percent_region_images = (
            (total_region_images / total_regioes) * 100
            if total_regioes > 0
            else 0
        )

        percent_wine_photos_text = f"{percent_wine_photos:.1f}".replace(".", ",")

        percent_wineries_without_wines_text = (
            f"{percent_wineries_without_wines:.1f}".replace(".", ",")
        )

        percent_region_images_text = f"{percent_region_images:.1f}".replace(".", ",")

        # ----------------------------------------------------------
        # ROW 1
        # ----------------------------------------------------------

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
                        Wines
                    </div>
                    <div style="
                        font-size: 24px;
                        font-weight: 600;
                        margin-top: 4px;
                    ">
                        {total_vinhos}
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
                        Wine Photos
                    </div>
                    <div style="
                        font-size: 24px;
                        font-weight: 600;
                        margin-top: 4px;
                    ">
                        {vinhos_com_fotos} ({percent_wine_photos_text}%)
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


        # ----------------------------------------------------------
        # ROW 2
        # ----------------------------------------------------------

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
                        Wineries
                    </div>
                    <div style="
                        font-size: 24px;
                        font-weight: 600;
                        margin-top: 4px;
                    ">
                        {total_vinicolas}
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
                        Wineries without Wines
                    </div>
                    <div style="
                        font-size: 24px;
                        font-weight: 600;
                        margin-top: 4px;
                    ">
                        {vinicolas_sem_vinhos} ({percent_wineries_without_wines_text}%)
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


        # ----------------------------------------------------------
        # ROW 3
        # ----------------------------------------------------------

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
                        Regions
                    </div>
                    <div style="
                        font-size: 24px;
                        font-weight: 600;
                        margin-top: 4px;
                    ">
                        {total_regioes}
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
                        Region Images
                    </div>
                    <div style="
                        font-size: 24px;
                        font-weight: 600;
                        margin-top: 4px;
                    ">
                        {total_region_images} ({percent_region_images_text}%)
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


        # ----------------------------------------------------------
        # ROW 4
        # ----------------------------------------------------------

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
                        Bottle Images
                    </div>
                    <div style="
                        font-size: 24px;
                        font-weight: 600;
                        margin-top: 4px;
                    ">
                        {vinhos_com_imagem_garrafa}
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
                        People
                    </div>
                    <div style="
                        font-size: 24px;
                        font-weight: 600;
                        margin-top: 4px;
                    ">
                        {total_pessoas}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # ==========================================================
        # DATABASE
        # ==========================================================

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

        # Database file
        db_path = Path(__file__).resolve().parent.parent / "vinhos.db"

        if db_path.exists():

            # Database size
            tamanho_mb = db_path.stat().st_size / (1024 * 1024)

            # Last updated - Brasília time
            ultima_atualizacao = datetime.fromtimestamp(
                db_path.stat().st_mtime,
                tz=ZoneInfo("America/Sao_Paulo")
            )

            ultima_atualizacao_formatada = ultima_atualizacao.strftime(
                "%d/%m/%Y %H:%M"
            )

            sqlite_version = sqlite3.sqlite_version

            st.markdown(
                f"""
                <div style="
                    width: 100%;
                    padding: 10px 5px;
                ">
                <div style="
                    display: flex;
                    justify-content: space-between;
                    margin-bottom: 8px;
                ">
                    <span style="font-size: 14px;">
                        SQLite version
                    </span>
                    <span style="
                        font-size: 14px;
                        font-weight: 600;
                    ">
                        {sqlite_version}
                    </span>
                    </div>
                    <div style="
                        display: flex;
                        justify-content: space-between;
                        margin-bottom: 8px;
                    ">
                        <span style="font-size: 14px;">
                            Database file
                        </span>
                        <span style="
                            font-size: 14px;
                            font-weight: 600;
                        ">
                            {db_path.name}
                        </span>
                    </div>
                    <div style="
                        display: flex;
                        justify-content: space-between;
                        margin-bottom: 8px;
                    ">
                        <span style="font-size: 14px;">
                            Database size
                        </span>
                        <span style="
                            font-size: 14px;
                            font-weight: 600;
                        ">
                            {tamanho_mb:.2f} MB
                        </span>
                    </div>
                    <div style="
                        display: flex;
                        justify-content: space-between;
                    ">
                        <span style="font-size: 14px;">
                            Last updated
                        </span>
                        <span style="
                            font-size: 14px;
                            font-weight: 600;
                        ">
                            {ultima_atualizacao_formatada}
                        </span>
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.warning("Database file not found.")

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

            # ==========================================================
            # PERCENTAGES
            # ==========================================================

            total_fotos_banco = len(fotos_banco)

            total_fotos_encontradas = total_fotos_banco - len(fotos_faltando)

            percent_files_in_folder = (
                (total_fotos_encontradas / total_fotos_banco) * 100
                if total_fotos_banco > 0
                else 0
            )

            percent_files_in_folder_text = (
                f"{percent_files_in_folder:.1f}".replace(".", ",")
            )

            # ----------------------------------------------------------
            # RESULTADOS
            # ----------------------------------------------------------

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
                            Photos in database
                        </div>
                        <div style="
                            font-size: 24px;
                            font-weight: 600;
                            margin-top: 4px;
                        ">
                            {len(fotos_banco)}
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
                            Files in wine_photos
                        </div>
                        <div style="
                            font-size: 24px;
                            font-weight: 600;
                            margin-top: 4px;
                        ">
                            {len(arquivos_pasta)} ({percent_files_in_folder_text}%)
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

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

    elif selected_option == "Register a New Person (Wine Lover)":

        # ==========================================================
        # REGISTER A NEW PERSON
        # ==========================================================

        st.write()

    elif selected_option == "Register a New Wine with AI Assistance":

        # ==========================================================
        # REGISTER A NEW WINE
        # ==========================================================

        st.write()

        