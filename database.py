# database.py
import sqlite3
from contextlib import closing

DB_NAME = "universidade.db"
MEMBER_TABLE = "membro_universidade"
OLD_TABLE = "membro_univerisade"  # manter se você quiser migrar de uma tabela com typo


def get_conn():
    """
    Abre uma nova conexão. NÃO compartilhe conexões entre threads.
    """
    return sqlite3.connect(DB_NAME)


def init_db():
    """
    Inicializa o banco: tenta renomear tabela antiga (se existir)
    e garante que a tabela correta exista.
    """
    with closing(get_conn()) as conn:
        cursor = conn.cursor()
        # Tenta renomear a tabela antiga para a nova (caso exista)
        try:
            cursor.execute(f"ALTER TABLE {OLD_TABLE} RENAME TO {MEMBER_TABLE}")
            conn.commit()
        except sqlite3.OperationalError:
            # tabela antiga não existe — ok
            pass

        # Cria tabela se não existir
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {MEMBER_TABLE} (
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                matricula TEXT PRIMARY KEY
            )
            """
        )
        conn.commit()


def criar_membro(nome, email, matricula):
    """
    Insere um membro. Lança sqlite3.IntegrityError se matricula já existir.
    """
    with closing(get_conn()) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO {MEMBER_TABLE} (nome, email, matricula) VALUES (?, ?, ?)",
            (nome, email, matricula),
        )
        conn.commit()


def buscar_membro(matricula):
    """
    Retorna tupla (nome, email, matricula) ou None.
    """
    with closing(get_conn()) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT nome, email, matricula FROM {MEMBER_TABLE} WHERE matricula = ?",
            (matricula,),
        )
        return cursor.fetchone()


def atualizar_membro(nome, email, matricula):
    """
    Atualiza nome/email por matricula. Retorna número de linhas afetadas.
    """
    with closing(get_conn()) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"UPDATE {MEMBER_TABLE} SET nome = ?, email = ? WHERE matricula = ?",
            (nome, email, matricula),
        )
        conn.commit()
        return cursor.rowcount


def deletar_membro(matricula):
    """
    Deleta um membro por matricula. Retorna número de linhas deletadas.
    """
    with closing(get_conn()) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"DELETE FROM {MEMBER_TABLE} WHERE matricula = ?",
            (matricula,),
        )
        conn.commit()
        return cursor.rowcount


# Inicializa o banco ao importar o módulo
init_db()
