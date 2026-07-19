import gspread
from google.oauth2.service_account import Credentials

# Escopos necessários
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Credenciais
creds = Credentials.from_service_account_file(
    "tough-plate-354500-7526720d6b28.json",  # coloque o nome do seu arquivo JSON
    scopes=scopes
)

# Conecta ao Google Sheets
client = gspread.authorize(creds)

# Abre a planilha pelo nome
planilha = client.open("Dashboard Importações")

# Primeira aba
aba = planilha.sheet1

# Escreve uma mensagem
aba.update(values=[["Conexão realizada com sucesso!"]], range_name="A1")

print("Tudo certo!")