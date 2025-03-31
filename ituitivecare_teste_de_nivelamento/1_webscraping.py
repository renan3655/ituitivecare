import os
import time
import requests
import zipfile
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
driver.get(url)
time.sleep(3)

# LOCALIZA OS ANEXOS I E II
anexo1 = driver.find_element(By.XPATH, '//a[contains(@href, "Anexo_I")]').get_attribute("href")
anexo2 = driver.find_element(By.XPATH, '//a[contains(@href, "Anexo_II")]').get_attribute("href")

# FUNÇÃO PARA BAIXAR OS PDFS
def download_pdf(url, nome_arquivo):
    resposta = requests.get(url)
    if resposta.status_code == 200:
        with open(nome_arquivo, 'wb') as arquivo:
            arquivo.write(resposta.content)
        print(f"Download concluído: {nome_arquivo}")
    else:
        print(f"Erro ao baixar {nome_arquivo}: Status {resposta.status_code}")

download_pdf(anexo1, "Anexo_I.pdf")
download_pdf(anexo2, "Anexo_II.pdf")

# 4. Compactar em ZIP os PDFs baixados
# Verifica se os arquivos existem antes de compactar
caminho_zip = os.path.join(os.getcwd(), "Anexos_ANS.zip")
with zipfile.ZipFile(caminho_zip, 'w') as zipf:
    zipf.write(os.path.join(os.getcwd(), "Anexo_I.pdf"), "Anexo_I.pdf") 
    zipf.write(os.path.join(os.getcwd(), "Anexo_II.pdf"), "Anexo_II.pdf")
print(f"ZIP criado em: {caminho_zip}")


driver.quit()
