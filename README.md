
# Api Ecommerce
## Descrição
Este projeto é uma API RESTful para um sistema de e-commerce. Um simples projeto baseado num ecommerce construido em FastAPI. A ideia e criar um pequeno Ecommerce e usa-lo como base em outros projetos
Ele permite que os usuários realizem operações como criar, ler, atualizar e excluir produtos, além de gerenciar pedidos e usuários.


## Tecnologias Utilizadas
- [Python](https://www.python.org/) - Linguagem de programação
- [FastAPI](https://fastapi.tiangolo.com/) - Framework para construção de APIs
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM para interagir com o banco de dados
- [SQLite](https://www.sqlite.org/index.html) - Banco de dados leve
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Validação de dados
- [Docker](https://www.docker.com/) - Conteirização da aplicação

## Versão: 0.0.10


## Instalação
```bash
  git clone https://github.com/Rodrigo-Kelven/Api_Ecommerce
  cd Api_Ecommerce
  pip install -r requirements.txt
```
### Atençao a esta parte! Ela é crucial para o funcionamento da API.
```bash
  fastapi dev ecommerce/main.py --reload --port 8000
```
### Painel admin de usuários (Ainda está em fase de desenvolvimento)
```bash
  http://127.0.0.1:8000/ecommerce/admin/users/
```

# Contribuições
Contribuições são bem-vindas! Se você tiver sugestões ou melhorias, sinta-se à vontade para abrir um issue ou enviar um pull request.;)

## Autores
- [@Rodrigo_Kelven](https://github.com/Rodrigo-Kelven)
