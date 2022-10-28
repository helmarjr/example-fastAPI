''''

Variaveis de Ambiente

MAC
    Criar via console
        export MY_DB_URL="localhost:1234"

    Visualizar
        printenv

    Visualizar somente uma variavel
        echo $MY_DB_URL


Windows
    Criar via console
        acessar system propiers > advanced > enviroment variabels

    Visualizar somente uma variavel
        echo %MY_DB_URL%



'''

from pydantic import BaseSettings
# import os
# my_db_url = os.getenv('MY_DB_URL')
# print(my_db_url)


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_name: str
    database_username: str
    database_password: str

    auth_secret_key: str
    auth_algorithm: str
    auth_access_token_expire_minutes: int

    class Config:
        env_file = '.env'

settings = Settings()

