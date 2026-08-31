import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, date
import traceback
import os

from auth import usuario_logado, perfil


def converter(valor):
    """
    Converte qualquer valor do DataFrame para um tipo aceito pelo Google Sheets.
    """

    if pd.isna(valor):
        return ""

    # Datas
    if isinstance(valor, (pd.Timestamp, datetime, date)):
        return valor.strftime("%d/%m/%Y")

    # NumPy
    try:
        import numpy as np

        if isinstance(valor, np.integer):
            return int(valor)

        if isinstance(valor, np.floating):
            return float(valor)

        if isinstance(valor, np.bool_):
            return bool(valor)

    except Exception:
        pass

    # Demais tipos
    return str(valor)


def show():

    # ======================================================
    # AUTENTICAÇÃO
    # ======================================================

    if not usuario_logado():
        st.warning("Faça login para acessar esta página.")
        st.stop()

    if perfil() not in ["admin", "upload"]:
        st.error("Você não possui permissão para acessar esta página.")
        st.stop()

    # ======================================================
    # TÍTULO
    # ======================================================

    st.title("📤 Upload da Planilha")

    # ======================================================
    # CONEXÃO COM O GOOGLE SHEETS
    # ======================================================

    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

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

    planilha = client.open_by_key(
        "1k0Y_nl8KVuGtgFIssJKZrWOu1nv1Xa74RN8QTsm8PHM"
    )

    aba = planilha.sheet1

    # ======================================================
    # UPLOAD
    # ======================================================

    arquivo = st.file_uploader(
        "Selecione uma planilha Excel",
        type=["xlsx", "xlsm"]
    )

    if arquivo is not None:

        try:

            # ==================================================
            # LÊ O EXCEL
            # ==================================================

            df = pd.read_excel(
                arquivo,
                engine="openpyxl"
            )

            # ==================================================
            # LIMPA NOMES DAS COLUNAS
            # ==================================================

            df.columns = df.columns.astype(str).str.strip()

            # ==================================================
            # REMOVE COLUNAS SEM NOME
            # Exemplo: Unnamed: 22
            # ==================================================

            df = df.loc[
                :,
                ~df.columns.astype(str).str.startswith("Unnamed")
            ]

            st.success(
                f"Planilha carregada ({len(df)} registros)"
            )

            # ==================================================
            # LIMPA A ABA DO GOOGLE SHEETS
            # ==================================================

            aba.clear()

            # ==================================================
            # CABEÇALHO
            # ==================================================

            dados = [
                df.columns.tolist()
            ]

            # ==================================================
            # DADOS
            # ==================================================

            for _, linha in df.iterrows():

                nova_linha = []

                for valor in linha:

                    nova_linha.append(
                        converter(valor)
                    )

                dados.append(nova_linha)

            # ==================================================
            # ENVIA PARA O GOOGLE SHEETS
            # ==================================================

            aba.update(
                range_name="A1",
                values=dados
            )

            st.success(
                "✅ Upload realizado com sucesso!"
            )

        except Exception:

            st.error(
                "Ocorreu um erro durante o upload."
            )

            st.exception(
                traceback.format_exc()
            )