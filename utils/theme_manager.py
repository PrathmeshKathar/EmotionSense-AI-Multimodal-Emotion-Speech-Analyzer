import streamlit as st

def toggle_theme():
    st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'

def apply_theme():
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'

    themes = {
        'light': {'bg_primary': '#ffffff', 'text_primary': '#262730'},
        'dark': {'bg_primary': '#0e1117', 'text_primary': '#fafafa'}
    }
    theme = themes[st.session_state.theme]

    css = f"""
    <style>
    .stApp {{
        background-color: {theme['bg_primary']};
        color: {theme['text_primary']};
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
    return theme
