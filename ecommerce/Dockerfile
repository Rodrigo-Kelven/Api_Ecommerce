# Usar a imagem base 'leve' do Python,
FROM python:3.11-slim

# Definir o diretório de trabalho
WORKDIR /code

# Copiar o arquivo de requisitos e instalar as dependências
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt

# Copiar o restante dos arquivos da aplicação
COPY ./main.py /code/
# copiar tudo para o diretorio criado no workdir
COPY . .

# Expor a porta que a aplicação vai usar
EXPOSE 8000

# Comando para executar a aplicação usando Uvicorn, se nao colocar o host, a aplicacao nao aparece
CMD ["fastapi","dev", "main.py", "--host","0.0.0.0", "--reload", "--port", "8000"]
