import streamlit as st
import os
import sys

# Garante que o diretório atual do script está no PATH do Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import upload
import dashboard

# Configuração global da página do Streamlit
st.set_page_config(
    page_title="Dashboard de Importações",
    page_icon="📦",
    layout="wide"
)

# Inicialização de variáveis globais da sessão
if "nome_planilha_sheets" not in st.session_state:
    st.session_state["nome_planilha_sheets"] = "Dashboard Importações"

# Menu lateral de navegação
st.sidebar.image("https://img.icons8.com/color/96/delivery-box.png", width=80)
st.sidebar.title("Controle de Importação")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navegação:",
    [
        "📊 Dashboard",
        "📤 Upload & Sincronização",
        "⚙️ Configuração da API"
    ]
)

st.sidebar.markdown("---")

# Renderização de acordo com a seleção de página
if page == "📊 Dashboard":
    dashboard.show()

elif page == "📤 Upload & Sincronização":
    upload.show()

elif page == "⚙️ Configuração da API":
    st.header("⚙️ Configuração da API do Google Sheets")
    st.markdown("Siga o passo a passo abaixo para conectar esta aplicação à sua planilha do Google Sheets de forma permanente:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            """
            ### Passo 1: Criar o Projeto no Google Cloud
            1. Acesse o [Google Cloud Console](https://console.cloud.google.com/).
            2. Crie um novo projeto ou selecione um existente.
            3. No menu lateral, acesse **APIs e Serviços** > **Biblioteca** (Library).
            4. Pesquise por **Google Sheets API** e clique em **Ativar** (Enable).
            5. Pesquise por **Google Drive API** e clique em **Ativar** (Enable).
            
            ### Passo 2: Criar a Conta de Serviço (Service Account)
            1. Acesse **APIs e Serviços** > **Credenciais** (Credentials).
            2. Clique em **+ Criar Credenciais** > **Conta de Serviço** (Service Account).
            3. Dê um nome para a conta (ex: `dashboard-importacoes`) e conclua.
            4. Na lista de contas de serviço, clique sobre o e-mail da conta recém-criada.
            5. Vá na aba **Chaves** (Keys) > **Adicionar Chave** > **Criar Nova Chave**.
            6. Selecione o formato **JSON** e clique em **Criar**. O download do arquivo iniciará automaticamente.
            """
        )
        
    with col2:
        st.markdown(
            """
            ### Passo 3: Colocar o JSON na pasta do Projeto
            1. Renomeie o arquivo JSON baixado ou mantenha o nome padrão, desde que comece com `dashboard-importacoes-` (exemplo: `dashboard-importacoes-87f54c2.json`).
            2. Coloque esse arquivo dentro da pasta do projeto:
               `c:\\Users\\onick\\OneDrive\\Documentos\\Projetos\\Projeto\\`
               *(Se já houver o arquivo template `dashboard-importacoes-xxxx.json`, você pode deletá-lo ou substituí-lo).*
               
            ### Passo 4: Compartilhar a Planilha
            1. Crie ou abra a planilha desejada no seu **Google Drive**.
            2. Clique no botão azul **Compartilhar** no canto superior direito.
            3. Cole o e-mail da sua conta de serviço (ele termina em `@...gserviceaccount.com`) e selecione a permissão como **Editor**.
            4. Defina o nome exato da planilha na página **Upload & Sincronização** e sincronize os dados!
            """
        )
        
    st.divider()
    
    # Validação do status atual
    st.subheader("Verificação do Sistema")
    cred_file = upload.find_credentials()
    
    if cred_file:
        st.success(f"✅ Arquivo de credenciais ativo: `{os.path.basename(cred_file)}`")
    else:
        st.error("❌ Nenhum arquivo de credenciais válido encontrado na pasta `Projeto/`.")
