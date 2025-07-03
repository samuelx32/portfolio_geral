import sqlite3
import os


def get_db_connection(nome):
    # diretorio = r"Z:\Mapa de Gastos\Samuel\Programa Principal Trabalho\data"
    diretorio = os.path.join(r"C:\Users\samue\OneDrive\Ambiente de Trabalho\Projeto_CONAB\Projeto_CONAB\data", f"{nome}.db")
    # diretorio = r"\\redecamara\DfsData\Comof\Mapa de Gastos\Samuel\Programa Principal Trabalho\data"
    # connection = sqlite3.connect(f'{diretorio}\\{nome}.db')
    connection = sqlite3.connect(f'{diretorio}')
    connection.row_factory = sqlite3.Row
    return connection
