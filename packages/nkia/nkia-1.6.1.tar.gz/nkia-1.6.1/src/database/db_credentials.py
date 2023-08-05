import os
from termcolor import colored

def mongo_credentials(environment):
    """
    Método responsável por retornar as credenciais do banco MONGODB de acordo com o ambiente de execução
    """
    credentials = {
        "uri": os.getenv("MONGO_URI_CONN") or "mongodb://localhost:27017/test",
        "ssl": os.getenv("MONGO_SSL") or True
    }

    if not credentials["uri"]:
        print(
            colored("Erro: ", "red"),
            colored(
                "MONGODB: Variável de ambiente uri não definida", "yellow"
            )
        )

    return credentials

def neo4j_credentials(environment):
    """
    Método responsável por retornar as credenciais do banco NEO4J de acordo com o ambiente de execução
    """
    credentials = {
        "host": os.getenv("BOT_NEO4J_HOST") or 'localhost',
        "port": os.getenv("BOT_NEO4J_PORT") or 7687,
        "user": os.getenv("BOT_NEO4J_USER") or 'neo4j',
        "db_name": os.getenv("BOT_NEO4J_NAME") or 'neo4j',
        "passwd": os.getenv("BOT_NEO4J_PASSWORD") or 'neo4j'

    }

    return credentials