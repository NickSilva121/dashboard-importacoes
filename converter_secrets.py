import json

# Nome do seu arquivo JSON
ARQUIVO_JSON = "tough-plate-354500-7526720d6b28.json"

with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
    cred = json.load(f)

print("[gcp_service_account]")

for chave, valor in cred.items():

    if isinstance(valor, str):
        valor = valor.replace("\\n", "\n")
        print(f'{chave} = """{valor}"""')
    else:
        print(f"{chave} = {json.dumps(valor)}")