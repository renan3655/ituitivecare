import pdfplumber
import pandas as pd
import zipfile


pdf_path = "Anexo_I.pdf"
csv_path = "dados.csv"
zip_path = f"Teste_Renan_Quintanilha.zip"

 #Extrair dados do PDF e salvar como CSV
with pdfplumber.open(pdf_path) as pdf:
    dados_tabelas = []  # Lista para armazenar os dados

    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            dados_tabelas.extend(table)  #Adicionar os dados à lista

df = pd.DataFrame(dados_tabelas)  #Converter os dados para um DataFrame

#Substituir abreviações nas colunas OD e AMB
if 'OD' in df.columns:
    df['OD'] = df['OD'].replace({
        'OD': 'Seg. Odontológica'
    })
if 'AMB' in df.columns:
    df['AMB'] = df['AMB'].replace({
        'AMB': 'Seg. Ambulatorial'
    })

#Salvar o DataFrame em um arquivo CSV
df.to_csv(csv_path, index=False, encoding="utf-8")
print(f"Os dados foram extraídos e salvos no arquivo: {csv_path}")

#Compactar o arquivo CSV
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(csv_path)
    print(f"O arquivo foi compactado e salvo como: {zip_path}")
