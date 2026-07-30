import streamlit as st

from auth import login, logout, usuario_logado
from components.sidebar import show as sidebar
from views import dashboard
from views import upload

st.set_page_config(
    page_title="Sistema de Importações",
    page_icon="📦",
    layout="wide"
)

# ======================================================
# LOGIN
# ======================================================

if not usuario_logado():

    st.title("🔐 Sistema de Importações")

    st.write("Faça login para continuar.")

    usuario = st.text_input("Usuário")

    senha = st.text_input(
        "Senha",
        type="password"
    )

    if st.button("Entrar", use_container_width=True):

        if login(usuario, senha):
            st.rerun()

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