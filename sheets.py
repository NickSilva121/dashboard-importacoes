import os

import streamlit as st
import gspread

from google.oauth2.service_account import Credentials


# ======================================================
# CONFIGURAÇÃO
# ======================================================

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

PLANILHA_ID = "1k0Y_nl8KVuGtgFIssJKZrWOu1nv1Xa74RN8QTsm8PHM"


# ======================================================
# CONEXÃO COM GOOGLE SHEETS
# ======================================================

def conectar_planilha():

    if os.path.exists("tough-plate-354500-7526720d6b28.json"):

        # Execução local
        creds = Credentials.from_service_account_file(
            "tough-plate-354500-7526720d6b28.json",
            scopes=SCOPES
        )

    else:

        # Streamlit Cloud
        creds = Credentials.from_service_account_info(
            dict(st.secrets["gcp_service_account"]),
            scopes=SCOPES
        )

    client = gspread.authorize(creds)

    # Abre diretamente pela ID
    planilha = client.open_by_key(PLANILHA_ID)

    return planilha