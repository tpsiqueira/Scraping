import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Entrar coma URL
base_url = "https://github.com/petrobras/ccp/stargazers"

data = []

# Função scraping
def scrape_stargazers():
    page = 1
    while True:
        # Add número da página na URL
        url = f"{base_url}?page={page}"        
        response = requests.get(url, verify=False)

        # Verifica a página existente
        if response.status_code != 200:
            print("Fim das páginas ou erro ao acessar.")
            break

        # Analisa o HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Localiza os elementos 
        stargazers = soup.find_all("a", class_="d-inline-block")

        # Se perfis=0, finalizar loop
        if not stargazers:
            break

        # Extrai os dados
        for stargazer in stargazers:
            # Extrai o nome e link
            name = stargazer.find("img")["alt"].replace("@", "").strip()
            profile_link = f"https://github.com{stargazer['href']}"

            # Requisição página do perfil
            profile_response = requests.get(profile_link, verify=False)  # Desabilitar SSL
            if profile_response.status_code == 200:
                profile_soup = BeautifulSoup(profile_response.text, "html.parser")

                # Extrai informações do perfil
                name_tag = profile_soup.find("span", class_="p-name")
                full_name = name_tag.text.strip() if name_tag else ""

                location_tag = profile_soup.find("span", class_="p-label")
                location = location_tag.text.strip() if location_tag else ""

                company_tag = profile_soup.find("span", class_="p-org")
                company = company_tag.text.strip() if company_tag else ""

                utc_tag = profile_soup.find("relative-time")
                utc = utc_tag["datetime"] if utc_tag else ""

                # Captura links
                links = [a['href'] for a in profile_soup.find_all('a', {'class': 'Link--primary'}) if 'href' in a.attrs]

                # Add dados na lista
                dados = {
                    "GitHub": name,
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
          
            time.sleep(2)
        
        page += 1

scrape_stargazers()

# Converte/salva Excel
output_path = r"C:\Users\Public\scraping.xlsx"
df = pd.DataFrame(data)
df.to_excel(output_path, index=False)

print(f"Dados salvos no arquivo Excel: '{output_path}'")
