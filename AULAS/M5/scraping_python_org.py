import requests
from bs4 import BeautifulSoup

# ----------------------------------------------------------------------
# PASSO 1: Acessar a página com requests
# ----------------------------------------------------------------------
# Usamos um User-Agent para "simular" um navegador real.
# Muitos sites bloqueiam requisições sem um User-Agent definido.
URL = "https://www.python.org/community/"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    )
}

print("PASSO 1: Acessando a página com requests...")
print(f"URL: {URL}")
resposta = requests.get(URL, headers=headers)

# Verificamos se a requisição foi bem-sucedida (status 200 = OK)
print(f"Status da requisição: {resposta.status_code}")
resposta.raise_for_status()  # Lança erro se a requisição falhar

# ----------------------------------------------------------------------
# PASSO 2: Fazer o parse do HTML com BeautifulSoup
# ----------------------------------------------------------------------
print("\nPASSO 2: Fazendo o parse do HTML com BeautifulSoup...")
sopa = BeautifulSoup(resposta.text, "html.parser")
print("HTML carregado e convertido em objeto BeautifulSoup com sucesso!")

# ----------------------------------------------------------------------
# PASSO 3: Escolher UM elemento específico da página
# ----------------------------------------------------------------------
# Vamos escolher o primeiro título <h2> da página.
# O método .find() retorna o primeiro elemento encontrado.
print("\nPASSO 3: Procurando o primeiro elemento <h2> da página...")
elemento_h2 = sopa.find("h2")

if elemento_h2 is None:
    # Se não houver <h2>, o script avisa e encerra de forma segura.
    print("Nenhum elemento <h2> encontrado na página.")
    exit()

print(f"Elemento encontrado: <{elemento_h2.name}>")

# ----------------------------------------------------------------------
# PASSO 4: Extrair o texto desse elemento
# ----------------------------------------------------------------------
print("\nPASSO 4: Extraindo o texto do elemento...")
texto_extraido = elemento_h2.get_text()
print(f"Texto extraído: '{texto_extraido}'")

# ----------------------------------------------------------------------
# PASSO 5: Manipular o texto extraído
# ----------------------------------------------------------------------
print("\nPASSO 5: Manipulando o texto extraído...")

# 5.1 - Remover espaços extras do início e do fim
texto_limpo = texto_extraido.strip()
print(f"5.1 - Texto sem espaços extras: '{texto_limpo}'")

# 5.2 - Dividir o texto em palavras (separando por espaços)
palavras = texto_limpo.split()
print(f"5.2 - Lista de palavras: {palavras}")

# 5.3 - Contar quantas palavras existem
quantidade_palavras = len(palavras)
print(f"5.3 - Quantidade de palavras: {quantidade_palavras}")

# 5.4 - Transformar em MAIÚSCULAS
texto_maiusculo = texto_limpo.upper()
print(f"5.4 - Texto em MAIÚSCULAS: '{texto_maiusculo}'")

# 5.5 - Transformar em minúsculas
texto_minusculo = texto_limpo.lower()
print(f"5.5 - Texto em minúsculas: '{texto_minusculo}'")

# 5.6 - Salvar as palavras em uma lista (já criada no passo 5.2)
# Aqui apenas confirmamos que temos uma lista pronta para uso futuro.
lista_de_palavras = palavras
print(f"5.6 - Lista final de palavras salva: {lista_de_palavras}")

# ----------------------------------------------------------------------
# FIM DO SCRIPT
# ----------------------------------------------------------------------
print("\nFIM! Estes são os passos básicos de um web scraping simples.")