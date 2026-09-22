from pathlib import Path
import base64
import mimetypes

from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()


# ============================================================
# CAMINHOS DO PROJETO
# ============================================================

PASTA_PROJETO = Path(__file__).resolve().parent

PASTA_IMAGENS_FOTOS = (
    PASTA_PROJETO / "Fotos"
)

PASTA_IMAGENS_PESSOAS = (
    PASTA_PROJETO / "pessoas"
)

PASTA_IMAGENS_GARRAFAS = (
    PASTA_PROJETO / "imagens_garrafas"
)

PASTA_IMAGENS_REGIOES = (
    PASTA_PROJETO / "imagens_regioes"
)

# ============================================================
# IMAGEM EM BASE64
# ============================================================

def imagem_base64(caminho):

    caminho = Path(caminho)

    if not caminho.exists():
        return None, None

    try:

        with open(caminho, "rb") as arquivo:
            imagem_b64 = base64.b64encode(
                arquivo.read()
            ).decode("utf-8")

        mime_type, _ = mimetypes.guess_type(
            caminho
        )

        return imagem_b64, mime_type

    except Exception:
        return None, None


# ============================================================
# LOCALIZAR IMAGEM DA GARRAFA
# ============================================================

def localizar_imagem_garrafa(nome_arquivo):

    if not nome_arquivo:
        return (
            PASTA_IMAGENS_GARRAFAS
            / "sem_garrafa.png"
        )

    caminho = (
        PASTA_IMAGENS_GARRAFAS
        / str(nome_arquivo)
    )

    if caminho.exists():
        return caminho

    return (
        PASTA_IMAGENS_GARRAFAS
        / "sem_garrafa.png"
    )

# ============================================================
# LOCALIZAR IMAGEM DA PESSOA
# ============================================================

def localizar_imagem_pessoa(nome_arquivo):

    if not nome_arquivo:
        return None

    caminho = PASTA_IMAGENS_PESSOAS / str(nome_arquivo)

    if caminho.exists():
        return caminho

    return None

# ============================================================
# LOCALIZAR EMOJI DA BANDEIRA
# ============================================================

def localizar_emoji_bandeira(pais):

    if not pais:
        return None

    emoji_bandeiras = {
        "Brasil": "🇧🇷",
        "Argentina": "🇦🇷",
        "Portugal": "🇵🇹",
    }

    bandeira = emoji_bandeiras.get(pais)

    if bandeira:
        return bandeira

    return None


# ============================================================
# LOCALIZAR IMAGEM DA FOTO
# ============================================================

def localizar_imagem_foto(nome_arquivo):

    if not nome_arquivo:
        return None

    caminho = PASTA_IMAGENS_FOTOS / str(nome_arquivo)

    if caminho.exists():
        return caminho

    return None

# ============================================================
# LOCALIZAR IMAGEM DA REGIÃO
# ============================================================

def localizar_imagem_regiao(nome_arquivo):

    if not nome_arquivo:
        return None

    caminho = (
        PASTA_IMAGENS_REGIOES
        / str(nome_arquivo)
    )

    if caminho.exists():
        return caminho

    return None

def listar_pessoas(texto):
    """
    Converte o conteúdo do campo vinhos.pessoas
    em uma lista de abreviações.

    Exemplos:
        "AS" → ["AS"]

        "AS, DN, PA" → ["AS", "DN", "PA"]

        "AS, DN, PA e RE" → ["AS", "DN", "PA", "RE"]
    """

    if not texto:
        return []

    texto = str(texto).strip()

    # Normaliza o " e " usado antes da última pessoa
    texto = texto.replace(" e ", ", ")

    pessoas = [
        pessoa.strip().upper()
        for pessoa in texto.split(",")
        if pessoa.strip()
    ]

    return pessoas