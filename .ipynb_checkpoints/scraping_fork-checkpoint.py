import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# URL 
base_url = "https://github.com/petrobras/3W/forks"

data = []

# Função scraping
def scrape_forks():
    page = 1
    while True:
        # Construir URL 
        url = f"{base_url}?page={page}"
        response = requests.get(url, verify=False)

        # Verificar página existe
        if response.status_code != 200:
            print("Fim das páginas ou erro ao acessar.")
            break

        # Intepetrar HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Selecionar os elementos
        forks = soup.select('a[data-hovercard-type="user"]')

        # Se forks=0, finalizar
        if not forks:
            break

        # Extrair dados
        for fork in forks:
            username = fork.text.strip()  # Nome de usuário
            profile_link = f"https://github.com{fork['href']}"  # URL do perfil

            # Requisição perfil usuário
            profile_response = requests.get(profile_link, verify=False)
            if profile_response.status_code == 200:
                profile_soup = BeautifulSoup(profile_response.text, "html.parser")

                # Extrair detalhes do perfil
                name_tag = profile_soup.find("span", class_="p-name")
                full_name = name_tag.text.strip() if name_tag else ""

                location_tag = profile_soup.find("span", class_="p-label")
                location = location_tag.text.strip() if location_tag else ""

                company_tag = profile_soup.find("span", class_="p-org")
                company = company_tag.text.strip() if company_tag else ""

                utc_tag = profile_soup.find("relative-time")
                utc = utc_tag["datetime"] if utc_tag else ""

                # Captura links
                links = [a['href'] for a in profile_soup.find_all('a', class_='Link--primary') if 'href' in a.attrs]

                # Add dados na lista
                dados = {
                    "GitHub": username,
                    "URL": profile_link,
                    "Nome": full_name,
                    "Localização": location,
                    "Empresa": company,
                    "UTC": utc
                }

                # Add links em colunas
                for i, link in enumerate(links):
                    dados[f"Link {i+1}"] = link

                data.append(dados)

            time.sleep(1) 

        page += 1

scrape_forks()

# Converter os dados
df = pd.DataFrame(data)

# Salva Excel
output_path = r"C:\Users\Public\scraping_fork.xlsx"
df.to_excel(output_path, index=False)

print(f"Dados salvos no arquivo Excel: '{output_path}'")
