import os
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


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

    return client.open("Dashboard Importações")