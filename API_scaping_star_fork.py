import requests
import pandas as pd
from opencage.geocoder import OpenCageGeocode

# Bypass SSL warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Configuração da API do OpenCage
API_KEY = 'xxxx'
geocoder = OpenCageGeocode(API_KEY)

# Função para obter o país a partir da localização
def obter_pais(location):
    try:
        resultado = geocoder.geocode(location)
        if resultado:
            return resultado[0]['components'].get('country', 'País não encontrado')
        else:
            return 'País não encontrado'
    except Exception as e:
        print(f"Erro ao processar a localização '{location}': {e}")
        return 'Erro ao obter país'

# Função para obter informações detalhadas do usuário
def obter_informacoes_usuario(user_url, headers):
    response = requests.get(user_url, headers=headers, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao acessar informações do usuário: {response.status_code}")
        return {}

# Função para obter stargazers e adicionar país
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
        response = requests.get(url, headers=headers, params={"page": page, "per_page": 100}, verify=False)
        if response.status_code != 200:
            print(f"Erro ao acessar API: {response.status_code} - {response.json()}")
            break

        data = response.json()
        if not data:
            break

        for item in data:
            user_info = obter_informacoes_usuario(item["user"]["url"], headers)
            localizacao = user_info.get("location", "")
            pais = obter_pais(localizacao) if localizacao else "Localização não informada"
            stargazers.append({
                "Usuário": item["user"]["login"],
                "URL Perfil": item["user"]["html_url"],
                "Nome": user_info.get("name"),
                "Empresa": user_info.get("company"),
                "Localização": localizacao,
                "País": pais,
            })
        page += 1

    return stargazers

# Função para obter forks e adicionar país
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
        response = requests.get(url, headers=headers, params={"page": page, "per_page": 100}, verify=False)
        if response.status_code != 200:
            print(f"Erro ao acessar API: {response.status_code} - {response.json()}")
            break

        data = response.json()
        if not data:
            break

        for item in data:
            user_info = obter_informacoes_usuario(item["owner"]["url"], headers)
            localizacao = user_info.get("location", "")
            pais = obter_pais(localizacao) if localizacao else "Localização não informada"
            forks.append({
                "Usuário": item["owner"]["login"],
                "URL Perfil": item["owner"]["html_url"],
                "Nome": user_info.get("name"),
                "Empresa": user_info.get("company"),
                "Localização": localizacao,
                "URL Repositório": item["html_url"],
                "País": pais,
            })
        page += 1

    return forks

# Informações do repositório
owner = "petrobras"
repo = "3W"

# Token de autenticação
token = "xxxx"

# Obter os stargazers e forks
stargazers = obter_stargazers(owner, repo, token)
forks = obter_forks(owner, repo, token)

# Gerar arquivo Excel
caminho_excel = r"C:\\Users\\Public\\API_stargazers_forks.xlsx"

with pd.ExcelWriter(caminho_excel, engine="openpyxl") as writer:
    if stargazers:
        df_stars = pd.DataFrame(stargazers)
        df_stars.to_excel(writer, sheet_name="Star", index=False)

    if forks:
        df_forks = pd.DataFrame(forks)
        df_forks.to_excel(writer, sheet_name="Fork", index=False)

print(f"Arquivo Excel gerado com sucesso: {caminho_excel}")
