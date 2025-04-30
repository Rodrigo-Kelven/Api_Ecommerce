from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from fastapi import status
import logging
import time
from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.middleware.base import BaseHTTPMiddleware
from logging.handlers import RotatingFileHandler
import os



logging.basicConfig(level=logging.INFO)

class LogRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Loga os detalhes da requisição
        logging.debug(f"Requisição recebida: {request.method} {request.url}")
        
        # Chama o próximo middleware ou rota
        response = await call_next(request)
        
        # Loga os detalhes da resposta
        logging.debug(f"Resposta enviada com status {response.status_code}")
        
        return response
    

RATE_LIMIT = 200 # Número máximo de requisições por minuto
TIME_WINDOW = 60  # Janela de tempo em segundos (1 minuto)
request_counts = {}  # Dicionário para rastrear o número de requisições por IP


# middleware
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    now = int(time.time())

    if client_ip not in request_counts:
        request_counts[client_ip] = {"count": 0, "timestamp": now}

    if now - request_counts[client_ip]["timestamp"] > TIME_WINDOW:
        request_counts[client_ip] = {"count": 0, "timestamp": now}

    if request_counts[client_ip]["count"] >= RATE_LIMIT:
        remaining_time = TIME_WINDOW - (now - request_counts[client_ip]["timestamp"])
        headers = {
            "X-RateLimit-Limit": str(RATE_LIMIT),
            "X-RateLimit-Remaining": "0",
            "X-RateLimit-Reset": str(remaining_time)
        }
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many requests", headers=headers)

    request_counts[client_ip]["count"] += 1
    headers = {
        "X-RateLimit-Limit": str(RATE_LIMIT),
        "X-RateLimit-Remaining": str(RATE_LIMIT - request_counts[client_ip]["count"]),
        "X-RateLimit-Reset": str(TIME_WINDOW - (now - request_counts[client_ip]["timestamp"]))
    }
    response = await call_next(request)
    response.headers.update(headers)
    return response

"""
# O código define um middleware que intercepta todas as requisições HTTP1.
# RATE_LIMIT define o número máximo de requisições permitidas por minuto1.
# TIME_WINDOW define a janela de tempo em segundos (neste caso, 1 minuto)1.
# request_counts é um dicionário que rastreia o número de requisições por endereço IP1.
# O middleware verifica se o endereço IP do cliente já está no dicionário request_counts. Se não estiver, ele adiciona o endereço IP com uma contagem inicial de 0 e o timestamp atual1.
# Se o tempo desde a primeira requisição do cliente for maior que TIME_WINDOW, a contagem é resetada1.
# Se o número de requisições exceder o RATE_LIMIT, uma exceção HTTPException é levantada com o código de status 429 (Too Many Requests)1.
# Os cabeçalhos X-RateLimit-Limit, X-RateLimit-Remaining e X-RateLimit-Reset são adicionados à resposta para informar o cliente sobre o limite de requisições1.
"""


def cors(app):
    from fastapi.middleware.cors import CORSMiddleware

    origins = [
        "http://localhost.tiangolo.com",
        "https://localhost.tiangolo.com",
        "http://localhost:5173/", # react
        "http://localhost:8080",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["Content-Type", "Authorization"],
        expose_headers=["X-Custom-Header"],
        max_age=3600,
    )
"""
Ao permitir todas as origens (allow_origins=["*"]), você deve ter cuidado,
pois isso pode expor sua API a riscos de segurança.
É sempre melhor restringir as origens permitidas ao mínimo necessário
"""


"""
### Resumo visual
### Nível configurado	Logs que ele aceita
-----------------------------------------------
* DEBUG	    DEBUG, INFO, WARNING, ERROR, CRITICAL
* INFO	    INFO, WARNING, ERROR, CRITICAL
* WARNING	WARNING, ERROR, CRITICAL
* ERROR	    ERROR, CRITICAL
* CRITICAL	CRITICAL
"""



os.makedirs("logs", exist_ok=True)
# Formato padrão
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def setup_logger(name, log_file, level=logging.INFO):
    """Cria e retorna um logger com arquivo próprio."""
    handler = RotatingFileHandler(log_file, maxBytes=5_000_000, backupCount=3)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.propagate = False  # Evita que os logs se repitam no console

    return logger

# Loggers separados
app_logger = setup_logger("app_logger", "logs/app.log", logging.INFO)
auth_logger = setup_logger("auth_logger", "logs/auth.log", logging.INFO)
#db_logger = setup_logger("db_logger", "logs/db.log", logging.ERROR)
db_logger = setup_logger("db_logger", "logs/db.log", logging.INFO)




# Configurar o registro
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])

logger = logging.getLogger(__name__)


# decoracor do rate limit
limiter = Limiter(
    key_func=get_remote_address,
    enabled=True,
    )
