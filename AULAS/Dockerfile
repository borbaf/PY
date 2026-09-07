#Usar uma imagem base do Python 3.12.4-slim
FROM python:3.12.4-slim 

#Definir o diretório de trabalho dentro do contêiner
WORKDIR /app


RUN apt-get update && apt-get install -y gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*


#Copiar os arquivos de requisitos para o contêiner
COPY requirements.txt /app/

#Instalar as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

#Copiar o restante do código da aplicação para o contêiner
COPY . /app/

#Comando para rodar a aplicação quando o contêiner iniciar
CMD ["python", "M5/scraping_python_org.py"]
