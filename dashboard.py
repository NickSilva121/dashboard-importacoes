import streamlit as st
import pandas as pd
import gspread
import os
from google.oauth2.service_account import Credentials
from PIL import Image

# ======================================================
# CONFIGURAÇÃO DA PÁGINA
# ======================================================

st.set_page_config(
    page_title="Dashboard de Importações",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Dashboard de Importações")

# ======================================================
# GOOGLE SHEETS
# ======================================================

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

if os.path.exists("tough-plate-354500-7526720d6b28.json"):
    # Executando localmente
    creds = Credentials.from_service_account_file(
        "tough-plate-354500-7526720d6b28.json",
        scopes=SCOPES
    )
else:
    # Executando no Streamlit Cloud
    creds = Credentials.from_service_account_info(
        dict(st.secrets["gcp_service_account"]),
        scopes=SCOPES
    )

client = gspread.authorize(creds)

planilha = client.open("Dashboard Importações")
aba = planilha.sheet1

# ======================================================
# CARREGA OS DADOS
# ======================================================

dados = aba.get_all_records()

df = pd.DataFrame(dados)

# ======================================================
# TRATAMENTO DAS DATAS
# ======================================================

colunas_data = [
    "PRONTIDÃO",
    "PARTIDA",
    "CHEGADA",
    "ENTREGA",
    "FECHAMENTO"
]

for coluna in colunas_data:

    if coluna in df.columns:

        df[coluna] = pd.to_datetime(
            df[coluna],
            errors="coerce",
            dayfirst=True
        ).dt.date

# ======================================================
# SIDEBAR
# ======================================================

logo = Image.open("logo.jpeg")

st.sidebar.image(
    logo,
    use_container_width=True
)

st.sidebar.title("🔎 Filtros")

# Comprador
compradores = sorted(df["COMPRADOR"].dropna().unique())

comprador = st.sidebar.selectbox(
    "Comprador",
    ["Todos"] + list(compradores)
)

# REF PO

ref_po = st.sidebar.text_input(
    "Referência PO"
)

# Datas

prontidao = st.sidebar.date_input(
    "Prontidão",
    value=None
)

chegada = st.sidebar.date_input(
    "Chegada",
    value=None
)

entrega = st.sidebar.date_input(
    "Entrega",
    value=None
)

# ======================================================
# FILTROS
# ======================================================

filtro = df.copy()

if comprador != "Todos":

    filtro = filtro[
        filtro["COMPRADOR"] == comprador
    ]

if ref_po:

    filtro = filtro[
        filtro["REF PO"]
        .astype(str)
        .str.contains(
            ref_po,
            case=False,
            na=False
        )
    ]

if prontidao:

    filtro = filtro[
        filtro["PRONTIDÃO"] == prontidao
    ]

if chegada:

    filtro = filtro[
        filtro["CHEGADA"] == chegada
    ]

if entrega:

    filtro = filtro[
        filtro["ENTREGA"] == entrega
    ]

# ======================================================
# PROCESSOS
# ======================================================

status = filtro["STATUS"].astype(str).str.upper()

processos_finalizados = filtro[
    status.str.contains("FINAL")
]

processos_andamento = filtro[
    ~status.str.contains("FINAL")
]

# ======================================================
# INDICADORES
# ======================================================

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total de Processos",
    len(filtro)
)

col2.metric(
    "Em andamento",
    len(processos_andamento)
)

col3.metric(
    "Finalizados",
    len(processos_finalizados)
)

st.divider()

# ======================================================
# ABAS
# ======================================================

aba1, aba2 = st.tabs([
    "🚧 Processos em andamento",
    "✅ Processos finalizados"
])

with aba1:

    st.dataframe(
        processos_andamento,
        use_container_width=True,
        hide_index=True
    )

with aba2:

    st.dataframe(
        processos_finalizados,
        use_container_width=True,
        hide_index=True
    )