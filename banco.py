from pathlib import Path
import sqlite3

BANCO = Path(__file__).resolve().parent / "vinhos.db"

def conectar():
    return sqlite3.connect(BANCO)