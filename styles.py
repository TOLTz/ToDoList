# styles.py
import streamlit as st

def get_theme_colors(theme):
    """Retorna um dicionário de cores com base no tema selecionado."""
    if theme == "Claro":
        return {
            "bg_color": "#f0f2f6", "card_color": "#ffffff", "text_color": "#000000",
            "input_bg": "#ffffff", "select_bg": "#ffffff", "select_text": "#000000",
            "button_bg": "#3b82f6", "button_color": "#ffffff", "plot_bg": "#ffffff",
            "plot_paper": "#ffffff",
        }
    else: # Escuro
        return {
            "bg_color": "#12151a", "card_color": "#222426", "text_color": "#ffffff",
            "input_bg": "#222426", "select_bg": "#222426", "select_text": "#ffffff",
            "button_bg": "#3b82f6", "button_color": "#ffffff", "plot_bg": "#12151a",
            "plot_paper": "#12151a",
        }

def apply_global_styles(colors):
    """Aplica o estilo CSS global à página com base nas cores do tema."""
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
            border: 1px solid #3b82f6; border-radius: 5px; padding: 8px;
        }}
        button[kind="primary"], .stButton > button {{
            background-color: {colors['button_bg']} !important;
            color: {colors['button_color']} !important; border-radius: 5px;
        }}
        .stSelectbox > div, .stSelectbox > div > div {{
            background-color: {colors['select_bg']} !important;
            color: {colors['select_text']} !important; border-radius: 5px;
        }}
        .stSelectbox label {{
            color: {colors['text_color']} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )