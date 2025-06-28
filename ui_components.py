# ui_components.py
import streamlit as st
import plotly.express as px
from database import update_status, delete_task # Importa as funções de callback

def display_header():
    """Exibe o cabeçalho da página com o seletor de tema."""
    col1, col2 = st.columns([10, 1])
    with col2:
        theme = st.selectbox("🎨 Tema:", ["Claro", "Escuro"], key="theme_select", label_visibility="collapsed")
    return theme

def display_task_list(tasks_df, colors):
    """Exibe a lista interativa de tarefas."""
    if tasks_df.empty:
        st.info("Você não tem tarefas pendentes. Adicione uma acima! 🎉")
        return
        
    for _, row in tasks_df.iterrows():
        c1, c2, c3 = st.columns([5, 2, 1])

        with c1:
            st.markdown(f"""
                <div style="padding: 1rem; margin: 1rem; background: {colors['card_color']};
                border-radius:8px; border-left:4px solid #3b82f6;
                box-shadow: 2px 2px 6px rgba(0, 0, 0, 0.05); color: {colors['text_color']};">
                    📍 {row['tarefa']}
                </div>
            """, unsafe_allow_html=True)

        options_status = ["Pendente", "Concluida"]
        current_status = row["status"].capitalize()
        new_status = c2.selectbox(
            "Status", options_status, index=options_status.index(current_status),
            key=f"status_{row['id']}", label_visibility="collapsed"
        )
        if new_status != current_status:
            update_status(row['id'], new_status)

        if c3.button("🗑️", key=f'delete_{row["id"]}'):
            delete_task(row['id'])

def display_progress_chart(tasks_df, colors):
    """Exibe o gráfico de pizza com o progresso das tarefas."""
    if tasks_df.empty:
        return
        
    progress_data = tasks_df['status'].value_counts().reset_index()
    progress_data.columns = ['Status', 'Amount']
    progress_data["Status"] = progress_data["Status"].str.strip().str.capitalize()

    custom_colors = {"Pendente": "#fbbf24", "Concluida": "#10b981"}

    fig = px.pie(
        progress_data, names="Status", values="Amount", title="📊 Progresso das Tarefas",
        color="Status", color_discrete_map=custom_colors, hole=0.4
    )
    fig.update_traces(
        textposition="inside", textinfo="percent+label",
        marker=dict(line=dict(color='#ffffff', width=2)),
        pull=[0.05 if s == "Pendente" else 0 for s in progress_data["Status"]],
    )
    fig.update_layout(
        title_font_size=22, font=dict(family="Segoe UI", size=16, color=colors['text_color']),
        paper_bgcolor=colors['plot_paper'], plot_bgcolor=colors['plot_bg'],
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5, font=dict(size=14))
    )
    st.plotly_chart(fig, use_container_width=True)