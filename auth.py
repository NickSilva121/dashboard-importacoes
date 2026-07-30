import streamlit as st
import pandas as pd
from sheets import conectar_planilha


def carregar_usuarios():
    planilha = conectar_planilha()
    aba = planilha.worksheet("Usuarios")
    return pd.DataFrame(aba.get_all_records())


def autenticar(usuario, senha):
    usuarios = carregar_usuarios()

    resultado = usuarios[
        (usuarios["usuario"] == usuario) &
        (usuarios["senha"] == senha)
    ]

    if resultado.empty:
        return None

    return resultado.iloc[0].to_dict()


def login(usuario, senha):
    usuario_encontrado = autenticar(usuario, senha)

    if usuario_encontrado is None:
        return False

    st.session_state["logado"] = True
    st.session_state["usuario"] = usuario_encontrado["usuario"]
    st.session_state["perfil"] = usuario_encontrado["perfil"]

    return True


def logout():
    st.session_state.clear()


def usuario_logado():
    return st.session_state.get("logado", False)


def perfil():
    return st.session_state.get("perfil", "")