import streamlit as st
from auth import logout


def show():
    """Exibe a sidebar e retorna a página selecionada."""

    with st.sidebar:

        # Logo
        st.image("logo.jpeg", use_container_width=True)

        st.divider()

        # Usuário
        st.write(f"👤 **{st.session_state['usuario']}**")
        st.caption(st.session_state["perfil"])

        st.divider()

        opcoes = []

        if st.session_state["perfil"] in ["admin", "dashboard"]:
            opcoes.append("📊 Dashboard")

        if st.session_state["perfil"] in ["admin", "upload"]:
            opcoes.append("📤 Upload")

        pagina = st.radio(
            "Menu",
            opcoes,
            label_visibility="collapsed"
        )

        st.divider()

        if st.button("🚪 Sair", use_container_width=True):
            logout()
            st.rerun()

    return pagina