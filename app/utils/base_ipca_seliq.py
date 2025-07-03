from bcb import sgs
from datetime import date,datetime
from dateutil.relativedelta import relativedelta
import sqlite3
import calendar
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
import plotly.graph_objects as go
import plotly.io as pio
import json

def retornar_selic(codigo):
    data_inicial = date.today()
    data_final = data_inicial + relativedelta(months=12)
    serie = sgs.get(codigo,start=data_inicial,end=data_final).dropna()   # Remove valores NaN
    
    # Pegar a última data e o último valor
    ultima_data = serie.index[-1]
    ultimo_valor = serie.iloc[-1].values[-1]

    dt = f"{ultima_data.day:02}/{ultima_data.month:02}/{ultima_data.year}"
    valor = float(ultimo_valor)
    
    return {'data': dt, 'valor': valor}

def retornar_ipca():
    meses_pt = {
    "01": "Jan", "02": "Fev", "03": "Mar", "04": "Abr",
    "05": "Mai", "06": "Jun", "07": "Jul", "08": "Ago",
    "09": "Set", "10": "Out", "11": "Nov", "12": "Dez"
    }
    url_base = "https://servicodados.ibge.gov.br/api/v3/agregados"

    # IPCA - Número-índice
    url_indice = f"{url_base}/6691/periodos/-1/variaveis/2266?localidades=N1[all]"
    dados_indice = requests.get(url_indice).json()[0]['resultados'][0]['series'][0]['serie']
    df_indice = pd.DataFrame(dados_indice.items(), columns=['Periodo', 'Fator_Acumulado'])

    # IPCA - Variação Mensal
    url_mensal = f"{url_base}/7060/periodos/-1/variaveis/63?localidades=N1[all]"
    dados_mensal = requests.get(url_mensal).json()[0]['resultados'][0]['series'][0]['serie']
    df_mensal = pd.DataFrame(dados_mensal.items(), columns=['Periodo', 'IPCA_Mensal'])

    # IPCA - Acumulado em 12 meses
    url_12m = f"{url_base}/7060/periodos/-1/variaveis/2265?localidades=N1[all]"
    dados_12m = requests.get(url_12m).json()[0]['resultados'][0]['series'][0]['serie']
    df_12m = pd.DataFrame(dados_12m.items(), columns=['Periodo', 'IPCA_12meses'])

    # Combinar os dados
    df = df_indice.merge(df_mensal, on="Periodo", how="outer")
    df = df.merge(df_12m, on="Periodo", how="outer")

    # Ordenar por período decrescente
    df = df.sort_values("Periodo", ascending=False).reset_index(drop=True)

    # Ajuste do período para exibição
    df["Periodo"] = df["Periodo"].apply(lambda x: f"{meses_pt[x[4:]]}/{x[:4]}")

    # Formatação dos números
    df["Fator_Acumulado"] = df["Fator_Acumulado"].astype(float).map("{:.4f}".format)
    df["IPCA_Mensal"] = df["IPCA_Mensal"].astype(float).map("{:.2f}".format)
    df["IPCA_12meses"] = df["IPCA_12meses"].astype(float).map("{:.2f}".format)

    valor = df["IPCA_Mensal"].iloc[0]
    valor12 = df["IPCA_12meses"].iloc[0]
    acumulado = df["Fator_Acumulado"].iloc[0]
    dt = df["Periodo"].iloc[0]

    # Obter próximo mês para iniciar calendário (índice de um mês é divulgado no mês seguinte)
    ultimo_periodo = df["Periodo"].iloc[0]  # Ex: "Fev/2025"
    mes_str, ano_str = ultimo_periodo.split("/")
    mes_num = int([k for k, v in meses_pt.items() if v == mes_str][0])

    # Dois meses à frente para início da coleta
    proximo_mes = mes_num + 2
    ano_calendario = int(ano_str)
    if proximo_mes > 12:
        proximo_mes -= 12
        ano_calendario += 1

    meses = list(range(proximo_mes, proximo_mes + 1))

    proximo = coletar_calendario_ipca(ano_calendario, meses, meses_pt)


    return {'data': dt,'valor': valor,'valor12': valor12,'proximo': proximo,'acumulado': acumulado}


def coletar_calendario_ipca(ano, meses_desejados=None, meses_pt=None):
    lista = []
    for mes in meses_desejados if meses_desejados else range(1, 13):
        url = f"https://www.ibge.gov.br/calendario-de-divulgacoes-novoportal.html?mes={mes}&ano={ano}"
        resposta = requests.get(url)
        if resposta.status_code != 200:
            continue

        soup = BeautifulSoup(resposta.text, "html.parser")
        blocos = soup.select("ul.agenda--lista > li")

        for bloco in blocos:
            data_tag = bloco.select_one("div.agenda--lista__data span")
            evento_tag = bloco.select_one("div.agenda--lista__evento a")
            referencia_tag = bloco.select_one("p.metadados.metadados--agenda")

            if not (data_tag and evento_tag and referencia_tag):
                continue

            nome_evento = evento_tag.get_text(strip=True)
            if nome_evento.strip() == "Índice Nacional de Preços ao Consumidor Amplo":
                data_div = data_tag.get_text(strip=True)
                ref = referencia_tag.get_text(strip=True).replace("Período de referência: ", "")
                mes_ref, ano_ref = ref.split("/")
                ref_formatada = f"{meses_pt.get(mes_ref.zfill(2), mes_ref)}/{ano_ref}"
                lista.append({
                    "Data de Divulgação": data_div,
                    "Referência IPCA": ref_formatada
                })

    df = pd.DataFrame(lista)
    df["Data de Divulgação"] = pd.to_datetime(df["Data de Divulgação"], dayfirst=True, errors="coerce")
    df = df.sort_values("Data de Divulgação").reset_index(drop=True)
    df["Data de Divulgação"] = df["Data de Divulgação"].dt.strftime("%d/%m/%Y")


    return df["Data de Divulgação"].iloc[0]


def atualizar_indice_monetario():

    ipca = retornar_ipca()
    selic = retornar_selic(432)
    print(selic)
    alteracoes = 0

    #conexao = sqlite3.connect(r'Z:\Mapa de Gastos\Samuel\Programa Principal Trabalho\data\indices_monetarios.db')
    conexao = sqlite3.connect(os.path.join(f"C:\Users\p_702809\Desktop\Projeto_CONAB\data", "indices_monetarios.db"))
    cursor = conexao.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS Ipca (id INTEGER PRIMARY KEY, data TEXT NOT NULL, indice FLOAT NOT NULL, indice12 TEXT, proximo TEXT, acumulado TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS Selic (id INTEGER PRIMARY KEY, data TEXT NOT NULL, indice FLOAT NOT NULL)")

    cursor.execute("select * from Ipca ORDER BY id DESC LIMIT 1")
    resultados = cursor.fetchone()
    
    if resultados[1] != ipca['data'] or resultados[2] != float(ipca['valor']) or resultados[3] != ipca['valor12'] :
        cursor.execute("INSERT INTO Ipca (data,indice,indice12,proximo,acumulado) values (?,?,?,?,?)",(ipca['data'],ipca['valor'],ipca['valor12'],ipca['proximo'],ipca['acumulado']))
        alteracoes += 1

    cursor.execute("select * from Selic ORDER BY id DESC LIMIT 1")
    resultados = cursor.fetchone()
    
    if resultados[1] != selic['data'] or resultados[2] != selic['valor']:
        cursor.execute("INSERT INTO Selic (data,indice) values (?,?)",(selic['data'],selic['valor'],))
        alteracoes += 2

    conexao.commit()
    conexao.close()

    retornos = {1: 'Mudança no Ipca',2: 'Mudança da Selic', 3:'Mudança nos dois indices'}

    return retornos.get(alteracoes, 'Nenhuma mudança')


def teste_grafico2():
    #conexao = sqlite3.connect(r'Z:\Mapa de Gastos\Samuel\Programa Principal Trabalho\data\indices_monetarios.db')

    data_hoje = date.today()
    data_final = data_hoje + relativedelta(months=12)
    data_inicial = data_hoje - relativedelta(months=12)

    # Coletar IPCA
    serie_ipca = sgs.get(433, start=data_inicial, end=data_final).dropna()
    df_ipca = pd.DataFrame(serie_ipca).reset_index()
    df_ipca.columns = ['data', 'ipca']

    # Coletar Selic
    serie_selic = sgs.get(432, start=data_inicial, end=data_final).dropna()
    df_selic = pd.DataFrame(serie_selic).reset_index()
    df_selic.columns = ['data', 'selic']

    # Merge os dois dataframes com base na coluna 'data'
    dados_combinados = pd.merge(df_ipca, df_selic, on='data')

    # Criar o gráfico de linhas
    fig = go.Figure()

    # Adicionar a linha do IPCA
    fig.add_trace(go.Scatter(x=dados_combinados['data'], y=dados_combinados['ipca'],
                            mode='lines', name='IPCA', line=dict(color='yellow')))

    # Adicionar a linha da Selic
    fig.add_trace(go.Scatter(x=dados_combinados['data'], y=dados_combinados['selic'],
                            mode='lines', name='Selic', line=dict(color='red')))

    # Ajustar o layout
    fig.update_layout(
        title='IPCA vs Selic',
        xaxis_title='data',
        yaxis_title='Valor',
        legend_title='Índices',
        template='plotly_dark'
    )

    # Converter o gráfico para HTML
    graph_html = pio.to_html(fig, full_html=False)

    return graph_html

def teste_grafico():
    data_hoje = date.today()
    data_final = data_hoje + relativedelta(months=12)
    data_inicial = data_hoje - relativedelta(months=12)

    # Coletar IPCA
    serie_ipca = sgs.get(433, start=data_inicial, end=data_final).dropna()
    df_ipca = pd.DataFrame(serie_ipca).reset_index()
    df_ipca.columns = ['data', 'ipca']

    # Coletar Selic
    serie_selic = sgs.get(432, start=data_inicial, end=data_final).dropna()
    df_selic = pd.DataFrame(serie_selic).reset_index()
    df_selic.columns = ['data', 'selic']

    # Merge os dois dataframes com base na coluna 'data'
    dados_combinados = pd.merge(df_ipca, df_selic, on='data')

    # === Cálculo do IPCA acumulado no período ===
    fatores = (dados_combinados['ipca'] / 100 + 1)
    ipca_acumulado = (fatores.prod() - 1) * 100

    # === (Opcional) Gerar IPCA acumulado mês a mês para linha adicional ===
    dados_combinados['ipca_acumulado'] = (fatores.cumprod() - 1) * 100

    # Criar o gráfico de linhas
    fig = go.Figure()

    # Adicionar a linha do IPCA
    fig.add_trace(go.Scatter(
        x=dados_combinados['data'],
        y=dados_combinados['ipca'],
        mode='lines',
        name='IPCA Mensal',
        line=dict(color='yellow')
    ))

    # Adicionar a linha da Selic
    fig.add_trace(go.Scatter(
        x=dados_combinados['data'],
        y=dados_combinados['selic'],
        mode='lines',
        name='Selic Mensal',
        line=dict(color='red')
    ))

    # (Opcional) Adicionar linha do IPCA acumulado
    fig.add_trace(go.Scatter(
        x=dados_combinados['data'],
        y=dados_combinados['ipca_acumulado'],
        mode='lines',
        name='IPCA Acumulado (%)',
        line=dict(color='green', dash='dash')
    ))

    # Ajustar o layout com o IPCA acumulado no título
    fig.update_layout(
        title=f'IPCA vs Selic — IPCA Acumulado: {ipca_acumulado:.2f}%',
        xaxis_title='Data',
        yaxis_title='Valor (%)',
        legend_title='Índices',
        template='plotly_dark'
    )

    # Converter o gráfico para HTML
    graph_html = pio.to_html(fig, full_html=False)

    return graph_html

