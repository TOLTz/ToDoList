# app.py
import streamlit as st
from database import load_tasks, add_task
from styles import get_theme_colors, apply_global_styles
from ui_components import display_header, display_task_list, display_progress_chart

# Configuração inicial da página (deve ser o primeiro comando Streamlit)
st.set_page_config(page_title='Task Manager', layout='wide')

def main():
    """Função principal que executa o aplicativo Streamlit."""
    
    # 1. Cabeçalho e Tema
    theme = display_header()
    colors = get_theme_colors(theme)
    apply_global_styles(colors)

    # 2. Título e Entrada de Tarefas
    st.title('📝 Gerenciador de tarefas pessoal')
    st.text_input('Insira uma nova tarefa:', key='entrada_tarefa', on_change=add_task)
    st.button('Adicionar Tarefa', on_click=add_task)

    # 3. Carregar dados
    tasks_df = load_tasks()

    # 4. Layout principal com duas colunas
    col_left, col_right = st.columns(2)

    with col_left:
        display_task_list(tasks_df, colors)
    
    with col_right:
        display_progress_chart(tasks_df, colors)

if __name__ == '__main__':
    main()