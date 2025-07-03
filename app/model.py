# Nesse arquivo ficarão todas as operações que envolverão o banco de dados sqlite3

from app.utils.db import get_db_connection
from app.utils.atualizar_logs import logging

# OPERAÇÕES DE USUÁRIOS

def retornar_todos_usuarios():
    conn = get_db_connection("banco_comof")
    cursor = conn.cursor()
    cursor.execute("SELECT nome,ponto,status,cargo,nivel,id FROM usuarios ORDER BY status DESC")
    resultados = cursor.fetchall()
    conn.close()
    if resultados:
        return resultados
    else:
        return []

def retornar_um_usuario(chave):
    conn = get_db_connection("banco_comof")
    cursor = conn.cursor()
    cursor.execute("SELECT nome,ponto,cargo,nivel,status,id FROM usuarios WHERE id=? or nome=? or ponto=?",(chave,chave,chave,))
    resultado = cursor.fetchone()
    conn.close()
    if resultado:
        return resultado
    else: 
        return None
    
def adicionar_usuario(nome,ponto,status,cargo,nivel):
    try:
        conn = get_db_connection("banco_comof")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nome,ponto,status,cargo,nivel) values (?,?,?,?,?)",(nome,ponto,status,cargo,nivel))
        conn.commit()
        conn.close()

        mensagem = f"{nome} adicionado com sucesso."
        tipo = "success"

    except Exception as e:
        mensagem = f"Ocorreu algum erro ao tentar alterar o débito\n {e}"
        tipo = "error"

    return mensagem, tipo
    
    
def atualiza_status_usuario(status,ponto):
    conn = get_db_connection("banco_comof")
    cursor = conn.cursor()
    
    if status == "offline" or status == "online":
        cursor.execute("UPDATE usuarios SET status = ? WHERE ponto = ?",(status,ponto,))
        resposta = "atualizado"
    else:
        resposta = "valor inválido."
    conn.commit()
    conn.close()
   
    if status == 'offline':
        logging('Saiu do sistema.')
    else:
        logging('Acessou o sistema.')

    return resposta
    
    

# OPERAÇÕES DE INDICES MONETÁRIOS E NOTÍCIAS

def retornar_ipca_selic_mais_recente():
    conn = get_db_connection("indices_monetarios")
    cursor = conn.cursor()

    cursor.execute("SELECT data,indice,indice12,proximo FROM Ipca ORDER BY id DESC LIMIT 1")
    ipca = cursor.fetchone()

    cursor.execute("SELECT data,indice FROM Selic ORDER BY id DESC LIMIT 1")
    selic = cursor.fetchone()

    ipca = ipca if ipca else []
    selic = selic if selic else []

    return ipca,selic


def retornar_noticias_camaranet():
    conn = get_db_connection("banco_comof")
    cursor = conn.cursor()

    cursor.execute("SELECT n.texto,n.link FROM noticias as n")
    resultados = cursor.fetchall()

    if resultados:
        return resultados
    else: 
        return None
    

# OPERAÇÕES RELACIONADAS A TABELA DE DEVEDORES

def retornar_todos_devedores():
    conn = get_db_connection("sicod_gru")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Devedores ORDER BY id DESC")
    resultados = cursor.fetchall()

    if resultados:
        return resultados
    else: 
        return None
    
def retornar_devedores_filtrados(cnpj):
    id = cnpj
    if len(id) == 10:
        id = f'0{id}'
    if len(id) == 11:
        id = f"{id[0]}{id[1]}{id[2]}.{id[3]}{id[4]}{id[5]}.{id[6]}{id[7]}{id[8]}-{id[9]}{id[10]}"
    elif len(id) == 14 and id[3] != '.':
        id = f"{id[0]}{id[1]}.{id[2]}{id[3]}{id[4]}.{id[5]}{id[6]}{id[7]}/{id[8]}{id[9]}{id[10]}{id[11]}-{id[12]}{id[13]}"
    
    conn = get_db_connection("sicod_gru")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Devedores WHERE cnpj = ? ORDER BY id DESC",(id,))
    resultados = cursor.fetchall()

    if resultados:
        return resultados
    else: 
        return None
    
def retornar_um_devedor(id):
    conn = get_db_connection("sicod_gru")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Devedores WHERE id = ?",(id,))
    resultado = cursor.fetchone()

    if resultado:
        return resultado
    else: 
        return None

    
def inserir_devedor(nome, cnpj, endereco,email,contrato,contato,pronome,tratamento):
    try:
        conn = get_db_connection("sicod_gru")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Devedores (nome, cnpj, endereco,email,contrato,contatos,pronome,tratamento) values (?,?,?,?,?,?,?,?)",(nome, cnpj, endereco,email,contrato,contato,pronome,tratamento))
        conn.commit()
        conn.close()
        
        mensagem = "Devedor Adicionado com Sucesso"
        tipo = "success"
    except Exception as e:
        mensagem = f"Ocorreu um erro: {e}"
        tipo = "error"

    return mensagem,tipo

def alterar_devedor(nome, cnpj, endereco,email,contrato,contato,pronome,tratamento,id):
    try:
        conn = get_db_connection("sicod_gru")
        cursor = conn.cursor()
        cursor.execute("UPDATE Devedores SET nome=?,cnpj=?,endereco=?,email=?,contrato=?,contatos=?,pronome=?,tratamento=? WHERE id = ?",(nome, cnpj, endereco,email,contrato,contato,pronome,tratamento,id))
        conn.commit()
        conn.close()

        mensagem = "Devedor Alterado com Sucesso"
        tipo = "success"
    except Exception as e:
        mensagem = f"Ocorreu um erro: {e}"
        tipo = "error"

    return mensagem,tipo

def deletar_devedor(id):
    try:
        conn = get_db_connection("sicod_gru")
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute("DELETE FROM Devedores WHERE id = ?",(id,))
        conn.commit()
        conn.close()

        mensagem = "Devedor Deletado com Sucesso"
        tipo = "success"
    except Exception as e:
        erro = str(e)
        if "FOREIGN KEY constraint failed" in erro:
            mensagem = f"Esse devedor possui débitos vinculados!!"
        else:
            mensagem = f"Ocorreu um erro: {e}"
        tipo = "error"

    return mensagem, tipo


# OPERAÇÕES RELACIONADAS A TABELA DE DÉBITOS
    
def retornar_debitos(cnpj,status):
  
    conn = get_db_connection("sicod_gru")
    cursor = conn.cursor()
    parametros = []
    query = "SELECT d.id,v.nome,v.cnpj,d.num_oficio,d.data_oficio,d.vencimento,d.valor,d.processo,d.status,d.saldo_atual FROM Devedores as v JOIN Debitos as d ON d.id_devedor = v.id WHERE 1=1"
        
    if status:
        query += " AND status = ?"
        parametros.append(status)
        
    if cnpj:
        id = cnpj
        if len(id) == 10:
            id = f'0{id}'
        if len(id) == 11:
            id = f"{id[0]}{id[1]}{id[2]}.{id[3]}{id[4]}{id[5]}.{id[6]}{id[7]}{id[8]}-{id[9]}{id[10]}"
        elif len(id) == 14 and id[3] != '.':
            id = f"{id[0]}{id[1]}.{id[2]}{id[3]}{id[4]}.{id[5]}{id[6]}{id[7]}/{id[8]}{id[9]}{id[10]}{id[11]}-{id[12]}{id[13]}"

        query += " AND cnpj = ?"
        parametros.append(id)
        
    query += " ORDER BY d.id DESC"
    cursor.execute(query,parametros)
    resultados = cursor.fetchall()

    if resultados:
        return resultados
    else: 
        return None

def retornar_um_debito(id):
    conn = get_db_connection("sicod_gru")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Debitos WHERE id = ?",(id,))
    resultado = cursor.fetchone()

    if resultado:
        return resultado
    else: 
        return None

def retornar_debitos_filtrados(id):
    conn = get_db_connection("sicod_gru")
    cursor = conn.cursor()

    cursor.execute("SELECT num_oficio,data_oficio,valor,saldo_atual FROM Debitos WHERE id_devedor=?",(id,))
    resultado = cursor.fetchall()

    if resultado:
        return resultado
    else: 
        return None
    
def retornar_debitos_devedores_join(id):
    conn = get_db_connection("sicod_gru")
    cursor = conn.cursor()

    cursor.execute("SELECT d.id,v.nome,v.cnpj,d.num_oficio,d.data_oficio,d.vencimento,d.valor,d.processo,d.status,d.saldo_atual FROM Devedores as v JOIN Debitos as d ON d.id_devedor = v.id WHERE d.id=?",(id,))
    resultado = cursor.fetchone()

    if resultado:
        return resultado
    else: 
        return None
    _

def inserir_debito(num_oficio, data_oficio, vencimento, valor, processo, id_devedor,status,saldo_atual):
    try:
        conn = get_db_connection("sicod_gru")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Debitos (num_oficio, data_oficio, vencimento, valor, processo, id_devedor,status,saldo_atual) values (?,?,?,?,?,?,?,?)",(num_oficio, data_oficio, vencimento, valor, processo, id_devedor,status,saldo_atual))
        conn.commit()
        conn.close()

        mensagem = "Débito Adicionado com Sucesso"
        tipo = "success"
    except Exception as e:
        mensagem = f"Ocorreu um erro: {e}"
        tipo = "error"

    return mensagem,tipo


def deletar_debito(id):
    try:
        conn = get_db_connection("sicod_gru")
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute("DELETE FROM Debitos WHERE id = ?",(id,))
        conn.commit()
        conn.close()

        mensagem = "Debito Deletado com Sucesso"
        tipo = "success"
    except Exception as e:
        erro = str(e)
        if "FOREIGN KEY constraint failed" in erro:
            mensagem = f"Esse devedor possui baixas vinculadas!!"
        else:
            mensagem = f"Ocorreu um erro: {e}"
        tipo = "error"

    return mensagem, tipo

def alterar_debito(num_oficio, data_oficio, vencimento,processo,valor,id_devedor,status,saldo_atual,id):
    try:
        conn = get_db_connection("sicod_gru")
        cur = conn.cursor()
        cur.execute("UPDATE Debitos SET num_oficio=?,data_oficio=?,vencimento=?,processo=?,valor=?,id_devedor=?,status=?,saldo_atual=? WHERE id = ?",(num_oficio, data_oficio, vencimento,processo,valor,id_devedor,status,saldo_atual,id))
        conn.commit()
        conn.close()
        
        mensagem ="Débito Alterado com Sucesso"
        tipo = "success"

    except Exception as e:
        mensagem = f"Ocorreu algum erro ao tentar alterar o débito\n {e}"
        tipo = "error"

    return mensagem, tipo


# OPERAÇÕES RELACIONADAS A TABELA DE BAIXAS

def retornar_baixas(num_ra):
    conn = get_db_connection("sicod_gru")
    cur = conn.cursor()
    query = "SELECT * FROM Baixas WHERE 1=1"
    parametros = []
    
    if num_ra: # se o usuário preencher o filtro ele adiciona essa exceção no comando sql
        query += " AND num_ra = ?"
        parametros.append(num_ra)

    query += " ORDER BY id DESC"
    cur.execute(query,parametros)
    resultados = cur.fetchall()
    
    conn.close()

    return resultados


def retornar_baixas_filtradas(id):
    conn = get_db_connection("sicod_gru")
    cursor = conn.cursor()

    cursor.execute("SELECT num_ra,valor,data_pagamento FROM Baixas WHERE id_debito=?",(id,))
    resultado = cursor.fetchall()

    if resultado:
        return resultado
    else: 
        return None


def retornar_todas_notificacoes(ponto):
    conn = get_db_connection("banco_comof")
    cursor = conn.cursor()

    cursor.execute("SELECT texto,urgencia,lido,id FROM notificacoes WHERE ponto=? and lido=?",(ponto,'NAO'))
    resultado = cursor.fetchall()

    if resultado:
        return resultado
    else: 
        return None

def remover_notificacao(id):
    conn = get_db_connection("banco_comof")
    cursor = conn.cursor()

    cursor.execute("delete from notificacoes where id=? ;",(id,))

    conn.commit()
    conn.close()
    

def adicionar_ferias(nome,ponto,inicio,fim,categoria,situacao):
    try:
        conn = get_db_connection("banco_comof")
        c = conn.cursor()
        c.execute("INSERT INTO ferias_recessos (nome, ponto, data_inicial, data_final, categoria, situacao) values (?,?,?,?,?,?)",(nome,ponto,inicio,fim,categoria,situacao,))
        conn.commit()
        conn.close()
        mensagem ="Solicitação criada com sucesso."
        tipo = "success"

    except Exception as e:
        mensagem = f"Ocorreu algum erro ao tentar alterar o débito\n {e}"
        tipo = "error"

    return mensagem, tipo



def adicionar_notificacao(ponto,texto,urgencia):
    try:
        lido = "NAO"
        conn = get_db_connection("banco_comof")
        c = conn.cursor()
        c.execute("INSERT INTO notificacoes (ponto,texto,urgencia,lido) values (?,?,?,?)",(ponto,texto,urgencia,lido))
        conn.commit()
        conn.close()
        mensagem ="Notificação criada com sucesso."
        tipo = "success"

    except Exception as e:
        mensagem = f"Ocorreu algum erro ao tentar alterar o débito\n {e}"
        tipo = "error"

    return mensagem, tipo



def adicionar_tarefa(ponto,titulo,descricao,urgencia):
    try:
        conn = get_db_connection("banco_comof")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tarefas (ponto,titulo,descricao,urgencia,concluida) values (?,?,?,?,?)",(ponto,titulo,descricao,urgencia,'NAO'))
        cursor.execute("INSERT INTO notificacoes (ponto,texto,urgencia,lido) values (?,?,?,?)",(ponto,"Uma nova tarefa foi solicitada.",urgencia,"NAO"))
        conn.commit()
        conn.close()
        
        mensagem = f"Tarefa adicionada com sucesso."
        tipo = "success"

    except Exception as e:
        mensagem = f"Ocorreu algum erro ao tentar alterar o débito\n {e}"
        tipo = "error"

    return mensagem, tipo


def retornar_todas_tarefas(ponto,todas):
    conn = get_db_connection("banco_comof")
    cursor = conn.cursor()
    if todas:
        cursor.execute("SELECT titulo,descricao,urgencia,concluida,ponto,id FROM tarefas WHERE ponto=? ORDER BY id DESC",(ponto,))
    else:
        cursor.execute("SELECT titulo,descricao,urgencia,concluida,ponto,id FROM tarefas WHERE ponto=? ORDER BY id DESC LIMIT 5",(ponto,))
    resultado = cursor.fetchall()
    conn.commit()
    conn.close()
    if resultado:
        return resultado
    else: 
        return None
    
def retornar_uma_tarefa(id):
    conn = get_db_connection("banco_comof")
    cursor = conn.cursor()

    cursor.execute("SELECT titulo,descricao,urgencia,concluida,ponto,id FROM tarefas WHERE id=?",(id,))
    resultado = cursor.fetchone()
    conn.commit()
    conn.close()
    if resultado:
        return resultado
    else: 
        return None
    

def concluir_tarefa(id):
    try:
        conn = get_db_connection("banco_comof")
        cursor = conn.cursor()
        cursor.execute("UPDATE tarefas SET concluida=? WHERE id=?",('SIM',id,))
        
        #cursor.execute("INSERT INTO notificacoes (ponto,texto,urgencia,lido) values (?,?,?,?)",("p_7315","x Concluiu uma tarefa",urgencia,"NAO"))

        conn.commit()
        conn.close()
        
        mensagem = f"Tarefa concluida com sucesso."
        tipo = "success"

    except Exception as e:
        mensagem = f"Ocorreu algum erro ao tentar alterar o débito\n {e}"
        tipo = "error"

    return mensagem, tipo

def retornar_contagem(condicao,ponto):
    try:
        conn = get_db_connection("banco_comof")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM tarefas WHERE concluida=? and ponto=?",(condicao,ponto))
        quantidade = cursor.fetchone()[0]
        conn.commit()
        conn.close()

    except Exception as e:
        return 0

    return quantidade


def atualizar_ferias(id,situacao):
    conn = get_db_connection("banco_comof")
    c = conn.cursor()
    c.execute("UPDATE ferias_recessos SET situacao=? WHERE id=?",(situacao,id,)) 
    conn.commit()
    conn.close()

    conn = get_db_connection("banco_comof")
    c = conn.cursor()
    c.execute("SELECT ponto FROM ferias_recessos WHERE id=?",(id,))
    ponto = c.fetchone()
    conn.commit()
    conn.close()
    
    return ponto['ponto']


def adicionar_materia(materia,vertente):
    try:
        conn = get_db_connection("banco_estudos")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS materias (id INTEGER PRIMARY KEY, materia TEXT NOT NULL, vertente TEXT NOT NULL)")
        c.execute("INSERT INTO materias (materia,vertente) VALUES (?,?)",(materia,vertente,))
        conn.commit()
        conn.close()

        mensagem = "Matéria Adicionada"
        tipo = "success"
    except Exception as e:
        mensagem = f"Ocorreu um erro: {e}"
        tipo = "error"

    return mensagem,tipo


def adicionar_conteudo(materia,vertente,titulo,submateria,texto):
    try:
        conn = get_db_connection("banco_estudos")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS conteudos (id INTEGER PRIMARY KEY, vertente TEXT NOT NULL, materia TEXT NOT NULL, titulo TEXT NOT NULL, submateria TEXT NOT NULL, texto TEXT NOT NULL)")
        c.execute("INSERT INTO conteudos (vertente,materia,titulo,submateria,texto) VALUES (?,?,?,?,?)",(vertente,materia,titulo,submateria,texto))
        conn.commit()
        conn.close()

        mensagem = "Conteúdo Adicionado"
        tipo = "success"
    except Exception as e:
        mensagem = f"Ocorreu um erro: {e}"
        tipo = "error"

    return mensagem,tipo


def retornar_materias(vertente):
    try:
        conn = get_db_connection("banco_estudos")
        c = conn.cursor()
        c.execute("SELECT materia FROM materias WHERE vertente = ?",(vertente,))

        resultados = c.fetchall()

        conn.commit()
        conn.close()

    except Exception as e:
        resultados = None

    return resultados

def retornar_conteudos(vertente,materia):
    try:
        conn = get_db_connection("banco_estudos")
        c = conn.cursor()
        c.execute("SELECT id,titulo,submateria FROM conteudos WHERE vertente = ? and materia = ? GROUP BY submateria HAVING COUNT(*) >= 1",(vertente,materia,))
        resultados = c.fetchall()
        conn.commit()
        conn.close()

    except Exception as e:
        resultados = None

    return resultados


def retornar_estudos(vertente,materia,submateria):
    try:
        conn = get_db_connection("banco_estudos")
        c = conn.cursor()
        c.execute("SELECT id,titulo,texto FROM conteudos WHERE vertente = ? and materia = ? and submateria = ?",(vertente,materia,submateria,))
        resultados = c.fetchall()
        conn.commit()
        conn.close()

    except Exception as e:
        resultados = None

    return resultados