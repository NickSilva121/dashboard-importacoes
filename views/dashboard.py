import streamlit as st
import pandas as pd

from sheets import conectar_planilha
from auth import usuario_logado, perfil


def show():

    # ======================================================
    # AUTENTICAÇÃO
    # ======================================================

    if not usuario_logado():
        st.warning("Faça login para acessar esta página.")
        st.stop()

    if perfil() not in ["admin", "dashboard"]:
        st.error("Você não possui permissão para acessar esta página.")
        st.stop()

    # ======================================================
    # TÍTULO
    # ======================================================

    st.title("📦 Follow Up de Importações")

    # ======================================================
    # GOOGLE SHEETS
    # ======================================================

    planilha = conectar_planilha()
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
            ).dt.strftime("%d/%m/%Y")

    # ======================================================
    # CAMPOS VAZIOS
    # ======================================================

    df = df.fillna("-")

    # ======================================================
    # FORMATAÇÃO DO VALOR FOB
    # ======================================================

    if "VALOR FOB" in df.columns:

        def formatar_valor_fob(valor):

            if valor == "-" or valor == "":
                return "-"

            try:
                # Trata valores que possam vir no formato brasileiro
                valor_str = str(valor).strip()

                # Se tiver ponto e vírgula, assume formato brasileiro
                # Exemplo: 1.500,50
                if "." in valor_str and "," in valor_str:
                    valor_str = valor_str.replace(".", "")
                    valor_str = valor_str.replace(",", ".")

                # Se tiver apenas vírgula
                # Exemplo: 1500,50
                elif "," in valor_str:
                    valor_str = valor_str.replace(",", ".")

                numero = float(valor_str)

                # Formato brasileiro
                valor_formatado = f"{numero:,.2f}"

                valor_formatado = (
                    valor_formatado
                    .replace(",", "X")
                    .replace(".", ",")
                    .replace("X", ".")
                )

                return f"US$ {valor_formatado}"

            except (ValueError, TypeError):
                return str(valor)

        df["VALOR FOB"] = df["VALOR FOB"].apply(
            formatar_valor_fob
        )

    # ======================================================
    # SIDEBAR
    # ======================================================

    st.sidebar.title("🔎 Filtros")

    # ======================================================
    # FILTRO - COMPRADOR
    # ======================================================

    if "COMPRADOR" in df.columns:

        compradores = sorted(
            df["COMPRADOR"]
            .dropna()
            .astype(str)
            .unique()
        )

        comprador = st.sidebar.selectbox(
            "Comprador",
            ["Todos"] + list(compradores)
        )

    else:

        comprador = "Todos"

    # ======================================================
    # FILTRO - REF PO
    # ======================================================

    ref_po = st.sidebar.text_input(
        "Referência PO"
    )

    # ======================================================
    # FILTROS - DATAS
    # ======================================================

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

    # ------------------------------------------------------
    # Comprador
    # ------------------------------------------------------

    if comprador != "Todos" and "COMPRADOR" in filtro.columns:

        filtro = filtro[
            filtro["COMPRADOR"] == comprador
        ]

    # ------------------------------------------------------
    # Referência PO
    # ------------------------------------------------------

    if ref_po and "REF PO" in filtro.columns:

        filtro = filtro[
            filtro["REF PO"]
            .astype(str)
            .str.contains(
                ref_po,
                case=False,
                na=False
            )
        ]

    # ------------------------------------------------------
    # Prontidão
    # ------------------------------------------------------

    if prontidao and "PRONTIDÃO" in filtro.columns:

        data_filtro = prontidao.strftime("%d/%m/%Y")

        filtro = filtro[
            filtro["PRONTIDÃO"] == data_filtro
        ]

    # ------------------------------------------------------
    # Chegada
    # ------------------------------------------------------

    if chegada and "CHEGADA" in filtro.columns:

        data_filtro = chegada.strftime("%d/%m/%Y")

        filtro = filtro[
            filtro["CHEGADA"] == data_filtro
        ]

    # ------------------------------------------------------
    # Entrega
    # ------------------------------------------------------

    if entrega and "ENTREGA" in filtro.columns:

        data_filtro = entrega.strftime("%d/%m/%Y")

        filtro = filtro[
            filtro["ENTREGA"] == data_filtro
        ]

    # ======================================================
    # PROCESSOS
    # ======================================================

    if "STATUS" in filtro.columns:

        status = filtro["STATUS"].astype(str).str.upper()

        processos_finalizados = filtro[
            status.str.contains("FINAL", na=False)
        ]

        processos_andamento = filtro[
            ~status.str.contains("FINAL", na=False)
        ]

    else:

        processos_finalizados = pd.DataFrame(
            columns=filtro.columns
        )

        processos_andamento = filtro.copy()

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

    # ======================================================
    # PROCESSOS EM ANDAMENTO
    # ======================================================

    with aba1:

        st.dataframe(
            processos_andamento,
            use_container_width=True,
            hide_index=True
        )

    # ======================================================
    # PROCESSOS FINALIZADOS
    # ======================================================

    with aba2:

        st.dataframe(
            processos_finalizados,
            use_container_width=True,
            hide_index=True
        )