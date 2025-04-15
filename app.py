import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px


# ---------- Banco de Dados ----------
def conect_db():
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

def load_tasks():
    conn = conect_db()
    df = pd.read_sql("SELECT * FROM tarefas", conn)
    conn.close()
    return df

def add_task():
    task = st.session_state.get("entrada_tarefa", "").strip()
    if not task:
        st.error('⚠️ Tarefa não pode estar vazia! ⚠️')
        return
    conn = conect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tarefas (tarefa, status) VALUES (?, ?)", (task, 'Pendente'))
    conn.commit()
    conn.close()
    st.session_state['entrada_tarefa'] = ''

def update_status(task_id, status):
    conn = conect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE tarefas SET status = ? WHERE id = ?", (status, task_id))
    conn.commit()
    conn.close()
    st.rerun()

def delete_task(task_id):
    conn = conect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tarefas WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    st.rerun()

# ---------- Configuração da Página ----------
st.set_page_config(page_title='Task Manager', layout='wide')

# ---------- Cores Dinâmicas ----------
def get_theme_colors(theme):
    if theme == "Claro":
        return {
            "bg_color": "#f0f2f6",
            "card_color": "#ffffff",
            "text_color": "#000000",
            "input_bg": "#ffffff",
            "select_bg": "#ffffff",
            "select_text": "#000000",
            "button_bg": "#3b82f6",
            "button_color": "#ffffff",
            "plot_bg": "#ffffff",
            "plot_paper": "#ffffff",
        }
    else:
        return {
            "bg_color": "#12151a",
            "card_color": "#222426",
            "text_color": "#ffffff",
            "input_bg": "#222426",
            "select_bg": "#222426",
            "select_text": "#ffffff",
            "button_bg": "#3b82f6",
            "button_color": "#ffffff",
            "plot_bg": "#12151a",
            "plot_paper": "#12151a",
        }

# ---------- Cabeçalho com seletor de tema ----------
with st.container():
    col1, col2 = st.columns([10, 1])
    with col2:
        theme = st.selectbox("🎨 Escolha o tema:", ["Claro", "Escuro"], key="theme_select")
colors = get_theme_colors(theme)

# ---------- Estilo Global ----------
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {colors['bg_color']};
        color: {colors['text_color']};
    }}
    input[type="text"], textarea, .stTextInput > div > input {{
        background-color: {colors['input_bg']} !important;
        color: {colors['text_color']} !important;
        border: 1px solid #3b82f6;
        border-radius: 5px;
        padding: 8px;
    }}
    button[kind="primary"], .stButton > button {{
        background-color: {colors['button_bg']} !important;
        color: {colors['button_color']} !important;
        border-radius: 5px;
    }}
    .stSelectbox > div, .stSelectbox > div > div {{
        background-color: {colors['select_bg']} !important;
        color: {colors['select_text']} !important;
        border-radius: 5px;
    }}
    .stSelectbox label {{
        color: {colors['text_color']} !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- Interface Principal ----------
st.title('📝 Gerenciador de tarefas pessoal')
st.text_input('Insira uma nova tarefa:', key='entrada_tarefa')
st.button('Adicionar', on_click=add_task)

list_task = load_tasks()

with st.container():
    col_left, col_right = st.columns(2)

    with col_left:
        if not list_task.empty:
            for index, row in list_task.iterrows():
                c1, c2, c3 = st.columns([5, 2, 1])

                with c1:
                    st.markdown(f"""
                        <div style="padding: 1rem; margin: 1rem; background: {colors['card_color']};
                        border-radius:8px; border-left:4px solid #3b82f6;
                        box-shadow: 2px 2px 6px rgba(0, 0, 0, 0.05); color: {colors['text_color']};">
                            📍{row['tarefa']}
                        </div>
                    """, unsafe_allow_html=True)    

                options_status = ["Pendente", "Concluida"]
                current_status = row["status"].capitalize()
                if current_status not in options_status:
                    current_status = "Pendente"

                new_status = c2.selectbox(
                    "Status",
                    options_status,
                    index=options_status.index(current_status),
                    key=f"status_{row['id']}"
                )

                if new_status != current_status:
                    update_status(row['id'], new_status)

                if c3.button("🗑️", key=f'delete_{row["id"]}'):
                    delete_task(row['id'])

    with col_right:
        if not list_task.empty:
            progress_data = list_task['status'].value_counts().reset_index()
            progress_data.columns = ['Status', 'Amount']
            progress_data["Status"] = progress_data["Status"].str.strip().str.capitalize()

            custom_colors = {
                "Pendente": "#fbbf24",
                "Concluida": "#10b981",
            }

            fig = px.pie(
                progress_data,
                names="Status",
                values="Amount",
                title="📊 Progresso das Tarefas",
                color="Status",
                color_discrete_map=custom_colors,
                hole=0.4,
            )

            fig.update_traces(
                textposition="inside",
                textinfo="percent+label",
                marker=dict(line=dict(color='#ffffff', width=2)),
                pull=[0.05 if s == "Pendente" else 0 for s in progress_data["Status"]],
            )

            fig.update_layout(
                title_font_size=22,
                font=dict(family="Segoe UI, sans-serif",
                          size=16,
                          color=colors['text_color']),
                paper_bgcolor=colors['plot_paper'],
                plot_bgcolor=colors['plot_bg'],
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.2,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=14, color=colors['text_color'])
                )
            )

            st.plotly_chart(fig, use_container_width=True)
