import requests

def baixar_pdf(url: str, caminho_pdf: str):
    print("Baixando o PDF diretamente da URL...")
    
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(caminho_pdf, 'wb') as file:
            file.write(response.content)
        print(f"PDF salvo com sucesso em: {caminho_pdf}")
    else:
        print(f"Erro ao baixar o PDF. Código de status HTTP: {response.status_code}")

# URL da GRU e o caminho onde o PDF será salvo
url = "https://pagtesouro.tesouro.gov.br/api/gru/portal/boleto-gru?codigoUg=010001&codigoRecolhimento=98815-4&cpfCnpjContribuinte=011.242.755-33&nomeContribuinte=JAQUELLINE+LIMA+FERNANDES&numeroReferencia=215&competencia=02%2F2025&vencimento=17%2F03%2F2025&valorPrincipal=514%2C18"
caminho_pdf = "gru_jaquelline_lima.pdf"

# Baixar o PDF diretamente
baixar_pdf(url, caminho_pdf)