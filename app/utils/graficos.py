import sqlite3
import pandas as pd
import plotly.express as px
import os

def conectar_banco(banco):
    try:
        conn = sqlite3.connect(os.path.join(r"\data", banco))
    except:
        conn = sqlite3.connect(fr'Z:\Mapa de Gastos\Samuel\Programa Principal Trabalho\data\{banco}')

    return conn


def retornar_todos_usuarios():
    conn = conectar_banco("banco_comof.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nome,ponto,status,cargo,nivel,id FROM usuarios ORDER BY status DESC")
    resultados = cursor.fetchall()
    conn.close()
    if resultados:
        return resultados
    else:
        return []

def grafico_status_devedores():
    try:
        conn = conectar_banco("sicod_gru.db")
        
        cursor = conn.cursor()
        cursor.execute("SELECT dev.nome,dev.cnpj,deb.valor,deb.status FROM Debitos as deb JOIN Devedores as dev WHERE dev.id = deb.id_devedor")
        resultados = cursor.fetchall()
        df = pd.DataFrame(resultados, columns=['nome','cnpj','valor','status'])
        conn.close()


        qtn_cob = (df['status'] == 'cobranca').sum()
        qtn_par = (df['status'] == 'parcial').sum()
        qtn_pago = (df['status'] == 'pago').sum()
        qtn_venc = (df['status'] == 'vencido').sum()

        dados_status = {
            'Status': ['EM COBRANÇA', 'PARCIAIS', 'PAGOS','VENCIDOS'],
            'Quantidade': [qtn_cob, qtn_par, qtn_pago,qtn_venc]
        }

        cores = {
            'EM COBRANÇA': 'yellow',
            'PARCIAIS': 'blue',
            'PAGOS': 'green',
            'VENCIDOS': 'red'
        }

        fig = px.pie(df, names=dados_status['Status'], values=dados_status['Quantidade'], title='Distribuição dos Débitos por Status',color=dados_status['Status'],color_discrete_map=cores)
        
        html_grafico = fig.to_html(full_html=False, include_plotlyjs='cdn')
    except:
        html_grafico = None

    return html_grafico

def grafico_tarefas_usuario():
    try:
        conn = conectar_banco("banco_comof.db")
        cursor = conn.cursor()
        cursor.execute("SELECT u.nome, t.titulo, t.concluida FROM tarefas as t JOIN usuarios as u WHERE u.ponto = t.ponto and t.concluida = 'SIM'")
        #cursor.execute("SELECT dev.nome,dev.cnpj,deb.valor,deb.status FROM Debitos as deb JOIN Devedores as dev WHERE dev.id = deb.id_devedor")
        resultados = cursor.fetchall()
        df = pd.DataFrame(resultados, columns=['nome','tarefa','concluida'])
        conn.close() 
        
        usuarios = retornar_todos_usuarios()

        tarefas_feitas = []
        for usuario in usuarios:
            contador = 0
            for i in range(len(df)):
                if usuario[0] == df['nome'][i]:
                    contador += 1

            tarefas_feitas.append({'nome': usuario[0],'tarefas': contador})

        df_tarefas = pd.DataFrame(tarefas_feitas, columns=['nome','tarefas'])
        
        fig = px.bar(df_tarefas, x='nome', y='tarefas',labels={'nome':'Nome','tarefas':'Tarefas Concluídas'}, title='Tarefas feitas por usuário')
        
        html_grafico = fig.to_html(full_html=False, include_plotlyjs='cdn')
        
        
    except:
        html_grafico = None

    return html_grafico




