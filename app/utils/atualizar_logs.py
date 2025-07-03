import sqlite3
import os
from datetime import datetime

# Níveis de LOG:
# DEBUG – Para desenvolvedores, contém detalhes técnicos.
# INFO – Ações normais do sistema (login, navegação).
# WARNING – Algo inesperado, mas que não quebrou o sistema.
# ERROR – Problemas que precisam de atenção imediata.
# CRITICAL – Falhas graves que impedem a operação. 


def logging(acao):
    nivel = 'INFO'
    ponto = os.getlogin().lower()
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conexao = sqlite3.connect(os.path.join(r"C:\Users\p_702809\Desktop\Projeto_CONAB\data", "banco_comof.db"))
    cursor = conexao.cursor()
    
    cursor.execute("INSERT INTO logs (autor,nivel,acao,data_hora) values (?,?,?,?)",(ponto,nivel,acao,agora))

    conexao.commit()
    conexao.close()