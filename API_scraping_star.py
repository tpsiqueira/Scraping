import requests
import pandas as pd

# Função para obter os stargazers de um repositório
def obter_stargazers(owner, repo, token=None):
    url = f"https://api.github.com/repos/{owner}/{repo}/stargazers"
    headers = {
        "Accept": "application/vnd.github.v3.star+json",
    }
    if token:
        headers["Authorization"] = f"token {token}"

    stargazers = []
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
            user_info = obter_informacoes_usuario(item["user"]["url"], headers)
            stargazers.append({
                "Usuário": item["user"]["login"],
                "Nome": user_info.get("name"),
                "Empresa": user_info.get("company"),
                "Localização": user_info.get("location"),
                "URL Perfil": item["user"]["html_url"],            
            })
        page += 1

    return stargazers

# Função para obter informações detalhadas do usuário
def obter_informacoes_usuario(user_url, headers):
    response = requests.get(user_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao acessar informações do usuário: {response.status_code}")
        return {}

# Informações do repositório
owner = "petrobras"
repo = "3W"

# Token de autenticação
token = "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"

# Obter os stargazers
stargazers = obter_stargazers(owner, repo, token)

# Gerar arquivo Excel
if stargazers:
    df = pd.DataFrame(stargazers)
    caminho_excel = r"C:\Users\Public\API_stargazers.xlsx"
    df.to_excel(caminho_excel, index=False)
    print(f"Arquivo Excel gerado com sucesso: {caminho_excel}")
else:
    print("Nenhum stargazer encontrado ou erro na API.")
