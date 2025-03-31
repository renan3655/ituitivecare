import pdfplumber
import pandas as pd


pdf_path = "Anexo_I.pdf"
csv_path = "dados.csv"  

# Abrir o PDF com pdfplumber
with pdfplumber.open(pdf_path) as pdf:
    dados_tabelas = []  # Lista para armazenar os dados

    for page in pdf.pages:
        # Verificar se a página contém tabelas
        tables = page.extract_tables()

        for table in tables:
            # Adicionar os dados da tabela à lista
            dados_tabelas.extend(table)


df = pd.DataFrame(dados_tabelas)# Converter os dados para um DataFrame

df.to_csv(csv_path, index=False, header=False, encoding="utf-8") # Salvar o DataFrame em um arquivo CSV

print(f"Os dados foram extraídos e salvos no arquivo: {csv_path}")
