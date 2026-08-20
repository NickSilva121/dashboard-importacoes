import streamlit as st

from auth import login, logout, usuario_logado
from components.sidebar import show as sidebar
from views import dashboard
from views import upload

st.set_page_config(
    page_title="Follow Up de Importações Kyly",
    page_icon="📦",
    layout="wide"
)

# ======================================================
# LOGIN
# ======================================================

if not usuario_logado():

    st.title("🚢 Follow Up de Importações")

    st.write("Faça login para continuar.")

    with st.form("login_form"):

        usuario = st.text_input("Usuário", autocomplete="username")

        senha = st.text_input(
            "Senha",
            type="password",
            autocomplete="password"
        )

        entrar = st.form_submit_button(
            "Entrar",
            use_container_width=True
        )

    if entrar:

        if login(usuario, senha):
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos.")

    st.stop()

# ======================================================
# SISTEMA
# ======================================================

pagina = sidebar()

if pagina == "📊 Dashboard":
    dashboard.show()

elif pagina == "📤 Upload":
    upload.show()