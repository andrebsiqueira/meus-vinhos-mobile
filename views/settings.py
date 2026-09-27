import streamlit as st
import pandas as pd

from pathlib import Path

from banco import conectar

def show_settings():

    st.markdown(
        '<div class="secao" style="font-size: 28px;">🍷 Settings</div>',
        unsafe_allow_html=True
    )


    # ==========================================================
    # WINE PHOTOS - DATABASE CHECK
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

        st.markdown("<br>", unsafe_allow_html=True)

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