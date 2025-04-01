import os
import requests
from bs4 import BeautifulSoup


urls_diretorios = [
    "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2023/",
    "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2024/"
]
url_operadoras = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv"

# Criar pasta se não existir
def criar_pasta(nome_pasta):
    if not os.path.exists(nome_pasta):
        os.makedirs(nome_pasta)

# Baixar arquivo individual
def baixar_arquivo(url, nome_arquivo):
    print(f"Baixando {nome_arquivo}...")
    resposta = requests.get(url)
    if resposta.status_code == 200:
        with open(nome_arquivo, 'wb') as arquivo:
            arquivo.write(resposta.content)
        print(f"{nome_arquivo} baixado com sucesso!")
    else:
        print(f"Erro ao baixar {nome_arquivo}: {resposta.status_code}")

# Baixar todos os arquivos de um diretório
def baixar_diretorio(url, nome_pasta):
    criar_pasta(nome_pasta)
    resposta = requests.get(url)
    if resposta.status_code == 200:
        soup = BeautifulSoup(resposta.text, 'html.parser')
        links = soup.find_all('a')
        for link in links:
            if link['href'].endswith('.zip'):
                url_arquivo = url + link['href']
                nome_arquivo = os.path.join(nome_pasta, link['href'])
                baixar_arquivo(url_arquivo, nome_arquivo)
    else:
        print(f"Erro ao acessar o diretório {url}: {resposta.status_code}")


for url_diretorio in urls_diretorios:
    nome_pasta = "demonstracoes_contabeis_" + url_diretorio.split('/')[-2]
    baixar_diretorio(url_diretorio, nome_pasta)


baixar_arquivo(url_operadoras, "Relatorio_cadop.csv")
