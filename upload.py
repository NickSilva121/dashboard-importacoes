import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, date
import traceback

# ===========================
# CONFIGURAÇÃO DA PÁGINA
# ===========================

st.set_page_config(
    page_title="Upload de Planilhas",
    page_icon="📤",
    layout="centered"
)

st.title("📤 Upload da Planilha")

# ===========================
# CONEXÃO COM O GOOGLE SHEETS
# ===========================

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "tough-plate-354500-7526720d6b28.json",
    scopes=SCOPES
)

client = gspread.authorize(creds)

planilha = client.open_by_key("1k0Y_nl8KVuGtgFIssJKZrWOu1nv1Xa74RN8QTsm8PHM")
aba = planilha.sheet1

# ===========================
# FUNÇÃO DE CONVERSÃO
# ===========================

def converter(valor):
    """
    Converte qualquer valor do DataFrame para um tipo aceito pelo Google Sheets.
    """

    if pd.isna(valor):
        return ""

    # Datas
    if isinstance(valor, (pd.Timestamp, datetime, date)):
        return valor.strftime("%d/%m/%Y")

    # NumPy Inteiros
    try:
        import numpy as np

        if isinstance(valor, np.integer):
            return int(valor)

        if isinstance(valor, np.floating):
            return float(valor)

        if isinstance(valor, np.bool_):
            return bool(valor)
    except:
        pass

    # Demais tipos
    return str(valor)

# ===========================
# UPLOAD
# ===========================

arquivo = st.file_uploader(
    "Selecione uma planilha Excel",
    type=["xlsx"]
)

if arquivo is not None:

    try:

        # Lê o Excel
        df = pd.read_excel(arquivo)

        # Remove espaços dos nomes das colunas
        df.columns = df.columns.str.strip()

        st.success(f"Planilha carregada ({len(df)} registros)")

        # Limpa a aba
        aba.clear()

        # Cabeçalho
        dados = [df.columns.tolist()]

        # Dados
        for _, linha in df.iterrows():

            nova_linha = []

            for valor in linha:
                nova_linha.append(converter(valor))

            dados.append(nova_linha)

        # Envia ao Google Sheets
        aba.update(
            range_name="A1",
            values=dados
        )

        st.success("✅ Upload realizado com sucesso!")

    except Exception:

        st.error("Ocorreu um erro durante o upload.")

        st.exception(traceback.format_exc())