import streamlit as st
import requests

from datetime import datetime, timezone

from banco import conectar


# ============================================================
# CONFIGURAÇÕES
# ============================================================

VERSAO_APP = "1.0.0"


# ============================================================
# COLETA DOS DADOS DO ACESSO
# ============================================================

def obter_dados_acesso():

    dados = {
        "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ip": None,
        "pais": None,
        "estado": None,
        "cidade": None,
        "fuso_horario": None,
        "dispositivo": None,
        "sistema_operacional": None,
        "navegador": None,
        "versao_navegador": None,
        "versao_app": VERSAO_APP,
    }

    # ========================================================
    # USER-AGENT
    # ========================================================

    try:

        headers = st.context.headers

        user_agent = headers.get("User-Agent", "")

        # ----------------------------------------------------
        # DISPOSITIVO
        # ----------------------------------------------------

        if "Mobile" in user_agent:
            dados["dispositivo"] = "Mobile"

        elif "Tablet" in user_agent:
            dados["dispositivo"] = "Tablet"

        else:
            dados["dispositivo"] = "Desktop"

        # ----------------------------------------------------
        # SISTEMA OPERACIONAL
        # ----------------------------------------------------

        if "iPhone" in user_agent:
            dados["sistema_operacional"] = "iOS"

        elif "iPad" in user_agent:
            dados["sistema_operacional"] = "iPadOS"

        elif "Android" in user_agent:
            dados["sistema_operacional"] = "Android"

        elif "Windows" in user_agent:
            dados["sistema_operacional"] = "Windows"

        elif "Mac OS X" in user_agent:
            dados["sistema_operacional"] = "macOS"

        elif "Linux" in user_agent:
            dados["sistema_operacional"] = "Linux"

        # ----------------------------------------------------
        # NAVEGADOR
        # ----------------------------------------------------

        if "Edg/" in user_agent:
            dados["navegador"] = "Edge"

        elif "OPR/" in user_agent:
            dados["navegador"] = "Opera"

        elif "Chrome/" in user_agent:
            dados["navegador"] = "Chrome"

        elif "Firefox/" in user_agent:
            dados["navegador"] = "Firefox"

        elif "Safari/" in user_agent:
            dados["navegador"] = "Safari"

        # ----------------------------------------------------
        # VERSÃO DO NAVEGADOR
        # ----------------------------------------------------

        if "Edg/" in user_agent:

            dados["versao_navegador"] = (
                user_agent.split("Edg/")[1].split(" ")[0]
            )

        elif "Chrome/" in user_agent:

            dados["versao_navegador"] = (
                user_agent.split("Chrome/")[1].split(" ")[0]
            )

        elif "Firefox/" in user_agent:

            dados["versao_navegador"] = (
                user_agent.split("Firefox/")[1].split(" ")[0]
            )

        elif "Version/" in user_agent:

            dados["versao_navegador"] = (
                user_agent.split("Version/")[1].split(" ")[0]
            )

    except Exception:
        pass


    # ========================================================
    # IP
    # ========================================================

    try:

        headers = st.context.headers

        ip = (
            headers.get("X-Forwarded-For")
            or headers.get("X-Real-IP")
            or headers.get("CF-Connecting-IP")
        )

        if ip:

            # X-Forwarded-For pode conter vários IPs
            dados["ip"] = ip.split(",")[0].strip()

    except Exception:
        pass


    # ========================================================
    # GEOLOCALIZAÇÃO APROXIMADA PELO IP
    # ========================================================

    if dados["ip"]:

        try:

            resposta = requests.get(
                f"https://ipinfo.io/{dados['ip']}/json",
                timeout=3
            )

            if resposta.status_code == 200:

                info = resposta.json()

                dados["pais"] = info.get("country")
                dados["estado"] = info.get("region")
                dados["cidade"] = info.get("city")
                dados["fuso_horario"] = info.get("timezone")

        except Exception:
            pass


    return dados


# ============================================================
# CRIA UM NOVO ACESSO
# ============================================================

def criar_usuario_acesso():

    # --------------------------------------------------------
    # Se já existe um acesso nesta sessão, não cria outro
    # --------------------------------------------------------

    if "acesso_id" in st.session_state:

        return st.session_state["acesso_id"]


    # --------------------------------------------------------
    # Coleta os dados
    # --------------------------------------------------------

    dados = obter_dados_acesso()


    # --------------------------------------------------------
    # Insere no banco
    # --------------------------------------------------------

    conexao = conectar()

    print("BANCO:", conexao.execute(
        "PRAGMA database_list"
    ).fetchall())

    cursor = conexao.cursor()


    cursor.execute(
        """
        INSERT INTO usuario_acessos (
            data_hora,
            ip,
            pais,
            estado,
            cidade,
            fuso_horario,
            dispositivo,
            sistema_operacional,
            navegador,
            versao_navegador,
            versao_app
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            dados["data_hora"],
            dados["ip"],
            dados["pais"],
            dados["estado"],
            dados["cidade"],
            dados["fuso_horario"],
            dados["dispositivo"],
            dados["sistema_operacional"],
            dados["navegador"],
            dados["versao_navegador"],
            dados["versao_app"],
        )
    )


    acesso_id = cursor.lastrowid


    conexao.commit()

    print("ACESSO GRAVADO:", acesso_id)
    
    resultado = conexao.execute(
        "SELECT COUNT(*) FROM usuario_acessos"
    ).fetchone()
    
    print("TOTAL DE ACESSOS:", resultado[0])
    
    conexao.close()


    # --------------------------------------------------------
    # Guarda o ID da sessão
    # --------------------------------------------------------

    st.session_state["acesso_id"] = acesso_id


    return acesso_id


# ============================================================
# ATUALIZA O NOME DO USUÁRIO
# ============================================================

def atualizar_nome_acesso(nome):

    acesso_id = st.session_state.get("acesso_id")

    if not acesso_id:
        return False


    conexao = conectar()
    cursor = conexao.cursor()


    cursor.execute(
        """
        UPDATE usuario_acessos
        SET nome = ?
        WHERE id = ?
        """,
        (
            nome,
            acesso_id
        )
    )


    conexao.commit()
    conexao.close()


    # Guarda também na sessão
    st.session_state["nome_usuario"] = nome


    return True


# ============================================================
# REGISTRA UMA PÁGINA ACESSADA
# ============================================================

def registrar_pagina(pagina):

    acesso_id = st.session_state.get("acesso_id")

    if not acesso_id:
        return


    # --------------------------------------------------------
    # Evita registrar a mesma página várias vezes devido
    # aos reruns do Streamlit
    # --------------------------------------------------------

    if st.session_state.get("ultima_pagina") == pagina:
        return


    data_hora = datetime.now(timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    conexao = conectar()
    cursor = conexao.cursor()


    cursor.execute(
        """
        INSERT INTO usuario_acessos_paginas (
            acesso_id,
            pagina,
            data_hora
        )
        VALUES (?, ?, ?)
        """,
        (
            acesso_id,
            pagina,
            data_hora
        )
    )


    conexao.commit()
    conexao.close()


    # Guarda a última página registrada
    st.session_state["ultima_pagina"] = pagina


# ============================================================
# BUSCA OS ACESSOS
# ============================================================

def buscar_acessos():

    conexao = conectar()


    df = None

    try:

        import pandas as pd

        df = pd.read_sql_query(
            """
            SELECT
                id,
                nome,
                data_hora,
                ip,
                pais,
                estado,
                cidade,
                fuso_horario,
                dispositivo,
                sistema_operacional,
                navegador,
                versao_navegador,
                versao_app
            FROM usuario_acessos
            ORDER BY data_hora DESC
            """,
            conexao
        )

    finally:

        conexao.close()


    return df


# ============================================================
# BUSCA AS PÁGINAS DE UM ACESSO
# ============================================================

def buscar_paginas_acesso(acesso_id):

    conexao = conectar()


    df = None

    try:

        import pandas as pd

        df = pd.read_sql_query(
            """
            SELECT
                id,
                acesso_id,
                pagina,
                data_hora
            FROM usuario_acessos_paginas
            WHERE acesso_id = ?
            ORDER BY data_hora ASC
            """,
            conexao,
            params=(acesso_id,)
        )

    finally:

        conexao.close()


    return df
