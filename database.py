# database.py
import sqlite3
import pandas as pd
import streamlit as st

def conect_db():
    """Conecta ao banco de dados SQLite e cria a tabela se não existir."""
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tarefas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tarefa TEXT NOT NULL,
            status TEXT NOT NULL
        )
        """
    )
    conn.commit()
    return conn

EMAIL = "test@test.com"

def load_tasks():
    """Carrega todas as tarefas do banco de dados para um DataFrame."""
    conn = conect_db()
    df = pd.read_sql("SELECT * FROM tarefas", conn)
    conn.close()
    return df

def add_task():
    """Adiciona uma nova tarefa ao banco de dados com base na entrada do usuário."""
    task = st.session_state.get("entrada_tarefa", "").strip()
    if not task:
        st.error('⚠️ Tarefa não pode estar vazia! ⚠️')
        return
    conn = conect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tarefas (tarefa, status) VALUES (?, ?)", (task, 'Pendente'))
    conn.commit()
    conn.close()
    st.session_state['entrada_tarefa'] = '' # Limpa o campo de entrada

def update_status(task_id, status):
    """Atualiza o status de uma tarefa específica."""
    conn = conect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE tarefas SET status = ? WHERE id = ?", (status, task_id))
    conn.commit()
    conn.close()
    st.rerun() # Recarrega a página para refletir a mudança

def delete_task(task_id):
    """Deleta uma tarefa específica do banco de dados."""
    conn = conect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tarefas WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    st.rerun() # Recarrega a página