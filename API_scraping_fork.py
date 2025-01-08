import requests
import pandas as pd

# Função para obter informações detalhadas do usuário
def obter_informacoes_usuario(user_url, headers):
    response = requests.get(user_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao acessar informações do usuário: {response.status_code}")
        return {}

# Função para obter os forks de um repositório
def obter_forks(owner, repo, token=None):
    url = f"https://api.github.com/repos/{owner}/{repo}/forks"
    headers = {
        "Accept": "application/vnd.github.v3+json",
    }
    if token:
        headers["Authorization"] = f"token {token}"

    forks = []
    page = 1

    while True:
        response = requests.get(url, headers=headers, params={"page": page, "per_page": 100})
        if response.status_code != 200:
            print(f"Erro ao acessar API: {response.status_code} - {response.json()}")
            break

        data = response.json()
        if not data:
            break

        for item in data:
            user_info = obter_informacoes_usuario(item["owner"]["url"], headers)
            forks.append({
                "Usuário": item["owner"]["login"],
                "URL Perfil": item["owner"]["html_url"],
                "Nome": user_info.get("name"),
                "Empresa": user_info.get("company"),
                "Localização": user_info.get("location"),
                "URL Repositório": item["html_url"],
            })
        page += 1

    return forks

# Informações do repositório
owner = "petrobras"
repo = "3W"

# Token de autenticação
token = "XXX"

# Obter os forks
forks = obter_forks(owner, repo, token)

# Gerar arquivo Excel
if forks:
    df = pd.DataFrame(forks)
    caminho_excel = r"C:\Users\Public\API_forks.xlsx"
    df.to_excel(caminho_excel, index=False)
    print(f"Arquivo Excel gerado com sucesso: {caminho_excel}")
else:
    print("Nenhum fork encontrado ou erro na API.")
