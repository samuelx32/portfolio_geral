from flask import render_template, request, redirect, url_for, session, flash, jsonify
from app import app
import sqlite3, requests
from datetime import datetime, timedelta
import os
import threading
# import subprocess
from app import model # todas operações com banco de dados vão para o model, conforme padrão MVC
from app.utils.db import get_db_connection
from app.utils.validadores import valida_conta_bb
from app.utils.gerar_gru import run_gerar_gru
from app.utils.siafi import run_playwright 
from app.utils.base_de_noticias import atualizar_base_de_noticias
from app.utils.conversores import converter_valor
from app.utils.atualizar_logs import logging #sistema de logging que armazena as ações dos usuários

# Variáveis Globais: As variáveis abaixo vão automaticamente para os templates HTML Jinja2.
@app.context_processor
def inject_global_variables():
    notificacoes = model.retornar_todas_notificacoes('p_702809')
    usuario = 'CORAL'
    return {
        'usuario': usuario,
        'notificacoes':notificacoes,
    }



#PRIMEIRO ACESSO: Verificações de identidade e autenticação    
@app.route('/')
def home():
    usuario = True
    if usuario:
        # Variáveis De Sessão 
        session['logged_in'] = True          
        session['nome_usuario'] = 'CORAL' 
        
        # abaixo é a mensagem de notificação e seu tipo: error ou success
        mensagem = session.get('mensagem', None)
        tipo = session.get('tipo', None)
        
       
        return render_template('index.html', tabela='nenhuma',mensagem=mensagem,tipo=tipo)
    else:
        session['logged_in'] = False
        return render_template('tela_de_nao_logado.html')
    
# ABAIXO ESTÃO ALGUMAS ROTAS RÁPIDAS, UTILIZADAS PARA ATUALIZAÇÕES NO SISTEMA OU NAS VARIÁVEIS DE SESSÃO
@app.route('/resetar_msg')
def resetar_msg():
    session['mensagem'] = None
    session['tipo'] = None
    resposta = {
        'resposta': 'Mensagem foi resetada com sucesso!'
    }
    return jsonify(resposta)

@app.route('/atualizar_noticias')
def atualizar_noticias():
    atualizar_base_de_noticias()
    logging('Atualizou as notícias.')
    session['mensagem'] = "Notícias Atualizadas."
    session['tipo'] = "sucess"
    return redirect(url_for('home'))


    
# Rota para a página de Cálculo de Diárias
@app.route('/vertente_index',methods=['GET'])
def vertente_index():
    if session.get('logged_in'):
        vertente = request.args.get("vertente",None)
        materias = model.retornar_materias(vertente)
        return render_template('vertente_index.html',materias=materias,vertente=vertente)
    else:
        return redirect(url_for('home'))
    

@app.route('/vertente_formulario_mat')
def vertente_formulario_mat():
    if session.get('logged_in'):
        mensagem = session.get('mensagem', None)
        tipo = session.get('tipo', None)
        return render_template('vertente_formulario_materia.html',mensagem=mensagem,tipo=tipo)
    else:
        return redirect(url_for('home'))


@app.route('/adicionar_materia', methods=['POST'])
def adicionar_materia():
    if session.get('logged_in'):
        materia = request.form['materia']
        vertente = request.form['vertente']

        session['mensagem'],session['tipo'] = model.adicionar_materia(materia,vertente)
    
        return redirect(url_for('vertente_formulario_mat')) 
    else:
        return redirect(url_for('home')) 
    

@app.route('/adicionar_conteudo', methods=['POST'])
def adicionar_conteudo():
    if session.get('logged_in'):
        materia = request.form['materia']
        vertente = request.form['vertente']
        titulo = request.form['titulo']
        submateria = request.form['submateria']
        texto = request.form['texto']

        session['mensagem'],session['tipo'] = model.adicionar_conteudo(materia,vertente,titulo,submateria,texto)
    
        return redirect(url_for('vertente_formulario_conteudo')) 
    else:
        return redirect(url_for('home')) 


@app.route('/vertente_materia', methods=['GET'])
def vertente_materia():
    if session.get('logged_in'):
        materia = request.args.get("materia", None)
        vertente = request.args.get("vertente", None)
        conteudos = model.retornar_conteudos(vertente,materia)
        print(conteudos)
        
        return render_template('vertente_materia.html',materia=materia,vertente=vertente,conteudos=conteudos)
    else:
        return redirect(url_for('home'))  
    
@app.route('/vertente_estudos', methods=['GET'])
def vertente_estudos():
    if session.get('logged_in'):
        materia = request.args.get("materia", None)
        vertente = request.args.get("vertente", None)
        submateria = request.args.get("submateria", None)
        estudos = model.retornar_estudos(vertente,materia,submateria)
        
        return render_template('vertente_estudos.html',materia=materia,vertente=vertente,submateria=submateria,estudos=estudos)
    else:
        return redirect(url_for('home')) 
    
@app.route('/vertente_formulario_conteudo')
def vertente_formulario_conteudo():
    if session.get('logged_in'):
        mensagem = session.get('mensagem', None)
        tipo = session.get('tipo', None)
        materia = request.args.get("materia", None)
        vertente = request.args.get("vertente", None)
        submateria = request.args.get("submateria", None)
        return render_template('vertente_formulario_conteudo.html',mensagem=mensagem,tipo=tipo,materia=materia,vertente=vertente,submateria=submateria)
    else:
        return redirect(url_for('home'))  

    
# Rota para entrar no SIAFI
@app.route('/entrar_siafi')
def entrar_siafi_route():
    if session.get('logged_in'):

        # Função que irá rodar em thread
        def run_siafi():
            # Chame a função para entrar no SIAFI e GERCOMP aqui
            run_playwright(action="gercomp")

        threading.Thread(target=run_siafi).start()
        return "Entrando no SIAFI, por favor aguarde..."

    else:
        return redirect(url_for('home'))

#USUARIOS_CONTROL
@app.route('/usuarios')
def usuarios():
    if session['logged_in']:
        mensagem = session.get('mensagem', None)
        tipo = session.get('tipo', None)
        inject_global_variables()
        return render_template('usuarios.html',mensagem=mensagem,tipo=tipo)
    else:
        return redirect(url_for('home'))
    

@app.route('/visualizar_usuario',methods=["GET","POST"])
def visualizar_usuario():
    if session['logged_in']:
            ponto = request.form['pt-usuario']
        
            dados_usuario = model.retornar_um_usuario(ponto)
            tarefas = model.retornar_todas_tarefas(ponto,True)
            return render_template('tela_usuario.html',dados_usuario=dados_usuario,tarefas=tarefas)
    else:
        return redirect(url_for('home'))
    
@app.route('/usuarios_form',methods=["GET"])
def usuarios_form():
    if session['logged_in']:
        mensagem = session.get('mensagem', None)
        tipo = session.get('tipo', None)
        return render_template('usuarios_form.html',mensagem=mensagem,tipo=tipo)
    else:
        return redirect(url_for('home'))
    
@app.route('/adicionar_usuario',methods=["POST"])
def adicionar_usuario():
    if session['logged_in']:
        nome = request.form['nome']
        ponto = request.form['ponto']
        status = 'offline'
        cargo = request.form['cargo']
        nivel = request.form['nivel']
        session['mensagem'],session['tipo'] = model.adicionar_usuario(nome,ponto,status,cargo,nivel)
        
        return redirect(url_for('usuarios_form'))
    else:
        return redirect(url_for('home'))


# ABAIXO TODAS AS ROTAS DO CONTROLE DE DEVEDORES
# Rota para lista de Empresas no banco
@app.route('/lista_devedores')
def lista_devedores():

    if session.get('logged_in'):
        mensagem = session.get('mensagem', None)
        tipo = session.get('tipo', None)
        #verifica se o usuário digitou o filtro de cnpj
        cnpj = request.args.get("cnpj", "")
        
        if cnpj == "":
            resultados = model.retornar_todos_devedores()
        else:
            resultados = model.retornar_devedores_filtrados(cnpj)


        return render_template('lista.html',resultados=resultados,mensagem=mensagem,tipo=tipo,tabela='devedores')
    else:
        return redirect(url_for('home')) 

#Rota para o formulário de cadastro de Devedores
@app.route('/formulario_devedores')
def formulario_devedores():
    mensagem = session.get('mensagem', None)
    tipo = session.get('tipo', None)
    if session.get('logged_in'):
        nome_usuario = session.get('nome_usuario', 'Usuário Desconhecido')

        return render_template('devedores_form.html',mensagem=mensagem,tipo=tipo,funcao='inserir')
    else:
        return redirect(url_for('home'))
    
# Rota para inserir Empresa no banco de dados
@app.route('/inserir_devedor', methods=['POST'])
def inserir_devedor():
    nome = request.form['nome']
    cnpj = request.form['cnpj']
    endereco = request.form['endereco']
    email = request.form['email']
    email = email.lower()
    contrato = request.form['contrato']
    contato = request.form['contato']
    pronome = request.form['pronome']
    tratamento = request.form['tratamento']
    cpf = request.form['cpf']
    if cpf != None and cpf != '':
        cnpj = cpf
    
    
    mensagem,tipo = model.inserir_devedor(nome, cnpj, endereco,email,contrato,contato,pronome,tratamento)
    
    session['mensagem'] = mensagem
    session['tipo'] = tipo
    
    if tipo == "success":
        logging('ADICIONOU UM NOVO DEVEDOR NO SISTEMA.')
    
    return redirect(url_for('formulario_devedores'))

# Rota para o formulário de devedores para alteração dos dados 
@app.route('/alterar_devedores_form', methods=['POST'])
def alterar_devedores_form():
    chave = request.form['chave']
    auxiliar = request.form['auxiliar']
    juridica = True
    if len(auxiliar) < 15:
        juridica = False
    

    if session.get('logged_in'):
        resultados = model.retornar_um_devedor(chave)


        return render_template('devedores_form.html',resultados=resultados,juridica=juridica,funcao='alterar')
    else:
        return redirect(url_for('home'))
    
@app.route('/alterar_devedor', methods=['POST'])
def alterar_devedor():
    id = request.form['id']
    nome = request.form['nome']
    cnpj = request.form['cnpj']
    endereco = request.form['endereco']
    email = request.form['email']
    email = email.lower()
    contrato = request.form['contrato']
    contatos = request.form['contatos']
    pronome = request.form['pronome']
    tratamento = request.form['tratamento']
    cpf = request.form['cpf']
    if cpf != None and cpf != '':
        cnpj = cpf
    
    mensagem, tipo = model.alterar_devedor(nome, cnpj, endereco,email,contrato,contatos,pronome,tratamento,id)

    session['mensagem'] = mensagem
    session['tipo'] = tipo
    
    if tipo == "success":
        logging(f'ALTEROU UM DEVEDOR DE CNPJ {cnpj}.')
    
    
    return redirect(url_for('lista_devedores'))

# Rota para deletar o devedor do banco de dados
@app.route('/deletar_devedor', methods=['POST'])
def deletar_devedor():
    id = request.form['chave']

    mensagem,tipo = model.deletar_devedor(id)

    session['mensagem'],session['tipo'] = mensagem, tipo
    
    if tipo == "success":
        logging('DELETOU UM DEVEDOR DO SISTEMA.')
    
    
    return redirect(url_for('lista_devedores'))

# ABAIXO AS ROTAS DE CONTROLE DOS DÉBITOS
# Rota para lista de Débitos no banco
@app.route('/lista_debitos')
def lista_debitos():
    if session.get('logged_in'):
        mensagem = session.get('mensagem', None)
        tipo = session.get('tipo', None)
        status = request.args.get("status", None)
        cnpj = request.args.get("cnpj", None)
    
        resultados = model.retornar_debitos(cnpj,status)    

        return render_template('lista.html',resultados=resultados,mensagem=mensagem,tipo=tipo,tabela='debitos')
    else:
        return redirect(url_for('home'))

#Rota para o formulário de cadastro de Débitos
@app.route('/formulario_debitos')
def formulario_debitos():
    mensagem = session.get('mensagem', None)
    tipo = session.get('tipo', None)
    if session.get('logged_in'):
        resultados = model.retornar_todos_devedores()
        return render_template('debitos_form.html',mensagem=mensagem,resultados=resultados,tipo=tipo)
    else:
        return redirect(url_for('home'))
    
# Rota para inserir o débito no banco de dados
@app.route('/inserir_debito', methods=['POST'])
def inserir_debito():
    num_oficio = request.form['num_oficio']
    valor = request.form['valor']
    processo = request.form['processo']
    data_oficio = request.form['data_oficio']
    vencimento = request.form['vencimento']
    id_devedor = request.form['id_devedor']
    status = request.form['status']
    saldo_atual = request.form['saldo_atual']

    mensagem, tipo = model.inserir_debito(num_oficio, data_oficio, vencimento, valor, processo, id_devedor,status,saldo_atual)
    
    session['mensagem'], session['tipo'] = mensagem, tipo 
    
    return redirect(url_for('formulario_debitos'))

# Rota para o formulário de devedores para alteração dos dados 
@app.route('/alterar_debitos_form', methods=['POST'])
def alterar_debitos_form():
    chave = request.form['chave']

    if session.get('logged_in'):
        resultados = model.retornar_um_debito(chave)
        devedores = model.retornar_todos_devedores()
        
        return render_template('debitos_form.html',resultados=resultados,devedores=devedores,funcao='alterar')
    else:
        return redirect(url_for('home'))

# Rota para deletar a GRU do banco de dados
@app.route('/deletar_debito', methods=['POST'])
def deletar_debito():
    id = request.form['chave']
    mensagem, tipo = model.deletar_debito(id)
    if tipo == 'success':
        logging('DELETOU UM DÉBITO DO SISTEMA.')
    session['mensagem'],session['tipo'] = mensagem, tipo
        
    return redirect(url_for('lista_debitos'))
    
@app.route('/alterar_debito', methods=['POST'])
def alterar_debito():

    id = request.form['id']
    num_oficio = request.form['num_oficio']
    data_oficio = request.form['data_oficio']
    vencimento = request.form['vencimento']
    processo = request.form['processo']
    valor = request.form['valor']
    id_devedor = request.form['id_devedor']
    status = request.form['status']
    saldo_atual = request.form['saldo_atual']
    
    mensagem, tipo = model.alterar_debito(num_oficio, data_oficio, vencimento,processo,valor,id_devedor,status,saldo_atual,id)

    if tipo == 'success':
        logging(f'ALTEROU UM DEBITO CUJA NÚMERO DO OFICIO É {num_oficio}.')
    session['mensagem'],session['tipo'] = mensagem, tipo
    
    return redirect(url_for('lista_debitos'))
        
# Rota para lista de Baixas
@app.route('/lista_baixas')
def lista_baixas():
    
    if session.get('logged_in'):
        mensagem = session.get('mensagem', None)
        tipo = session.get('tipo', None)
        num_ra = request.args.get("num_ra", "") # recebe o valor digitado no filtro de RAs

        resultados = model.retornar_baixas(num_ra)

        return render_template('lista.html',resultados=resultados,mensagem=mensagem,tipo=tipo,tabela='baixas')
    else:
        return redirect(url_for('home'))
    
@app.route('/mais_informacoes', methods=['POST'])
def mais_informacoes():
    if session.get('logged_in'):
        id = request.form['chave']
        tabela = request.form['tabela']
        if tabela == "devedores":
            resultados = model.retornar_um_devedor(id)
            resultados2 = model.retornar_debitos_filtrados(id)
        else:
            resultados = model.retornar_debitos_devedores_join(id)
            resultados2 = None
            if resultados['status'] == 'pago' or resultados['status'] == 'parcial':
                # Se o débito já tiver pago, Baixado, então ele busca com Join os dados da Baixa também.
                resultados2 = model.retornar_baixas_filtradas(id)
        
        return render_template('mais_informacoes.html',resultados=resultados,tabela=tabela,resultados2=resultados2)
    else:
        return redirect(url_for('home'))
    
@app.route('/gerar_gru',methods=['POST'])
def gerar_gru():
    cnpj = request.form['cnpj']
    nome = request.form['nome']
    valor = request.form['valor']
    valor = converter_valor(valor) 
    tipo_gru = request.form['tipo_gru']
    
    resultado_operacao = run_gerar_gru(cnpj,nome,valor,tipo_gru)

    if resultado_operacao == "Sucesso":
        logging(f'GEROU UMA GRU PARA O CNPJ/CPF: {cnpj}.')
        session['mensagem'] = "GRU gerada com Sucesso."
        session['tipo'] = "success"
    else:
        session['mensagem'] = resultado_operacao
        session['tipo'] = "error"

    return redirect(url_for('lista_debitos'))

# Adicionar Baixa do Documento
@app.route('/adicionar_baixa',methods=['POST'])
def adicionar_baixa():
    num_ra = request.form['num_ra']
    valor = request.form['valor']
    data_pag = request.form['data_pag']
    id_debito = request.form['id_debito']

    try:
        conn = get_db_connection("sicod_gru")
        cur = conn.cursor()
        cur.execute("INSERT INTO Baixas (num_ra,valor,data_pagamento,id_debito) VALUES (?,?,?,?)",(num_ra,valor,data_pag,id_debito,))
        cur.execute("select saldo_atual from Debitos WHERE id = ?",(id_debito,))
        saldo_debito = cur.fetchone()
        saldo_debito = saldo_debito['saldo_atual']
        c_valor = converter_valor(valor)
        c_saldo = converter_valor(saldo_debito)
        if c_valor == c_saldo:
            novo_valor = "R$ 0,00"
            cur.execute("UPDATE Debitos SET status = ?,saldo_atual = ? WHERE id = ?",('pago',novo_valor,id_debito,))
            
        elif c_valor < c_saldo:
            novo_valor = c_saldo - c_valor
            novo_valor = converter_valor(novo_valor)
            cur.execute("UPDATE Debitos SET status = ?,saldo_atual = ? WHERE id = ?",('parcial',novo_valor,id_debito,))
            
        else:
            session['mensagem'] = "Erro: O valor da baixa foi maior que o do débito."
            session['tipo'] = "error" 
            return redirect(url_for('lista_debitos'))
        
        conn.commit()
        conn.close()
        logging(f'BAIXOU UM DÉBITO CUJA RA: {num_ra}')
        session['mensagem'] = "Baixa Adicionada com Sucesso"
        session['tipo'] = "success" 

    except sqlite3.Error as e:
        session['mensagem'] = f"Erro ao executar o comando SQL: {e}"
        session['tipo'] = "error" 
    except Exception as e:
        session['mensagem'] = f"Ocorreu algum erro ao tentar adicionar a Empresa\n {e}"
        session['tipo'] = "error"

    return redirect(url_for('lista_debitos'))

@app.route('/alterar_baixa', methods=['POST'])
def alterar_baixa():
    id = request.form['id']
    num_ra = request.form['num_ra']
    valor = request.form['valor']
    data_pag = request.form['data_pag']

    try:
        conn = get_db_connection("sicod_gru")
        cur = conn.cursor()
        cur.execute("UPDATE Baixas SET num_ra=?,valor=?,data_pagamento=? WHERE id = ?",(num_ra,valor,data_pag,id,))
        conn.commit()
        conn.close()
        logging(f'ALTEROU UMA BAIXA CUJA RA: {num_ra}')
        session['mensagem'] = "Baixa Alterada com Sucesso"
        session['tipo'] = "success" 

    except sqlite3.Error as e:
        session['mensagem'] = f"Erro ao executar o comando SQL: {e}"
        session['tipo'] = "error" 
    except Exception as e:
        session['mensagem'] = f"Ocorreu algum erro ao tentar alterar a Baixa\n {e}"
        session['tipo'] = "error"

    return redirect(url_for('lista_baixas'))

# Rota para deletar a Baixa do banco de dados
@app.route('/deletar_baixa', methods=['POST'])
def deletar_baixa():
    try:
        id = request.form['chave']
        conn = get_db_connection("sicod_gru")
        cur = conn.cursor()
        # Ao deletar a baixa, eu altero o status do débito correspondente, para Em cobrança.
        cur.execute("SELECT id_debito FROM Baixas WHERE id = ?",(id,))
        result = cur.fetchone()
        id_debito = result['id_debito']
        #cur.execute("UPDATE Debitos SET status = ? WHERE id = ?",('em cobranca',id_debito,))
        cur.execute("DELETE FROM Baixas WHERE id = ?",(id,))
        conn.commit()
        conn.close()

       
        session['mensagem'] = "A baixa foi deletada com Sucesso."
        session['tipo'] = "sucess"
    except sqlite3.Error as e:
        session['mensagem'] = f"Erro: {e}"
        session['tipo'] = "error"
    except Exception as e:
        session['mensagem'] = f"Ocorreu algum erro desconhecido: {e}"
        session['tipo'] = "error"
    
    return redirect(url_for('lista_baixas'))

@app.route('/visualizar_logs') # rota para tela de vista dos loggings do sistema.
def visualizar_logs():
    if session.get('logged_in'):
        conn = get_db_connection("banco_comof")
        cur = conn.cursor()
        cur.execute("SELECT nivel,acao,data_hora,autor FROM logs ORDER BY id DESC")
        resultados = cur.fetchall()
        conn.close()


        return render_template('logging.html',tabela='logs',resultados=resultados)
    else:
        return redirect(url_for('home'))
    
    
# Rota para a função de validar contas do BB
@app.route('/validar_conta_bb', methods=['POST'])
def validar_conta_bb():
    conta = request.form['conta']
    if valida_conta_bb(conta):
        return jsonify({'mensagem': 'Válido'})
    else:
        return jsonify({'mensagem': 'Inválido'}), 400
    
# @app.route('/iniciar_copiloto')
# def iniciar_copiloto():
#     subprocess.Popen([sys.executable, r"Scripts/inserir_cadastros.py"],)
#     return redirect(url_for('home'))

@app.route('/tela_ferias_recessos')
def tela_ferias_recessos():
    if session['logged_in']:
        return render_template('tela_ferias_recessos.html',tabela='nenhuma')
    else:
        return redirect(url_for('home'))
    
@app.route('/agendamentos',methods=["GET","POST"])
def agendamentos():
    if request.method == "GET":
        conn = get_db_connection("banco_comof")
        c = conn.cursor()
        c.execute("SELECT nome, ponto, data_inicial, data_final, categoria,situacao,id FROM ferias_recessos")
        resultados = c.fetchall()
        conn.close()
        eventos = []
        for row in resultados:
            eventos.append({
                "title": f"{row[0]} - {row[4]} - {row[5]}",
                "start": row[2],
                "end": row[3],
                "allDay": True,
                "situacao": row[5],
                "identificador": row[6]
            })
            
        # adicionando feriados dos próximos 2 anos no calendário
        hoje = datetime.today()
        ano = hoje.year
        ano_seguinte = ano + 1
        url1 = f"https://brasilapi.com.br/api/feriados/v1/{ano}"
        url2 = f"https://brasilapi.com.br/api/feriados/v1/{ano_seguinte}"
        feriados = []
        #faz a requisição a api trazendo todos os feriados de 2025 e 2026
        for url in [url1, url2]:
            resp = requests.get(url)
            if resp.ok:
                feriados.extend(resp.json())
        #lista todos os feriados e adiciona a lista de eventos
        
        for feriado in feriados:
            eventos.append({
                "title": feriado['name'], #nome do feriado
                "start": feriado['date'], #data do feriado
                "allDay": True,
                "situacao": 'FERIADO'
            })

        return jsonify(eventos) #retorno para a full calendar

    elif request.method == "POST":
        dados = request.get_json()
        inicio = dados['inicio']
        fim = dados['fim']
        nome = session['nome_usuario']
        ponto = os.getlogin().lower()

        categorias = {'ferias':'FR - FÉRIAS','banco':'BH - BANCO DE HORAS','recesso':'RECESSO'}
        categoria = categorias.get(dados['categoria'],'FR - FÉRIAS')
        
        situacao = "EM ANALISE"

        mensagem,tipo = model.adicionar_ferias(nome,ponto,inicio,fim,categoria,situacao)

        if tipo != 'error':
            global notificacoes
            if mensagem == 'Solicitação criada com sucesso.':
                nota = 'Pedido de férias solicitado.'
                m,t = model.adicionar_notificacao('p_7315',nota,'NORMAL')
        
        return redirect(url_for('tela_ferias_recessos'))

@app.route('/aprovar-ferias',methods=["POST"])
def aprovar_ferias():
    dados = request.get_json()
    id = int(dados['id'].split(":")[1])
    ponto = model.atualizar_ferias(id,"APROVADO")
    model.adicionar_notificacao(ponto,"Pedido de férias aprovado.","NORMAL")
    inject_global_variables()    
    return redirect(url_for('tela_ferias_recessos'))

@app.route('/recusar-ferias',methods=["POST"])
def recusar_ferias():
    dados = request.get_json()
    id = int(dados['id'].split(":")[1])
    ponto = model.atualizar_ferias(id,"RECUSADO")
    model.adicionar_notificacao(ponto,"Pedido de férias recusado.","NORMAL")
    inject_global_variables()    
    return redirect(url_for('tela_ferias_recessos'))

@app.route('/excluir-ferias',methods=["POST"])
def excluir_ferias():
    dados = request.get_json()
    id = int(dados['id'].split(":")[1])
    conn = get_db_connection("banco_comof")
    c = conn.cursor()
    c.execute("DELETE FROM ferias_recessos WHERE id=?",(id,))

    conn.commit()
    conn.close()
        
    return redirect(url_for('tela_ferias_recessos'))

    

@app.route('/atribuir_tarefa',methods=["POST"])
def atribuir_tarefa():
    if session['logged_in']:
        
        ponto = request.form['ponto_usuario']
        urgencia = request.form['urgencia']
        descricao = request.form['descricao']
        titulo = request.form['titulo'] 
        mensagem,tipo = model.adicionar_tarefa(ponto,titulo,descricao,urgencia)
        
        if tipo == 'success':
            logging(f'ADICIONOU UMA NOTIFICAÇÃO PARA O USUÁRIO: {ponto}')
        session['mensagem'],session['tipo'] = mensagem, tipo

        return redirect(url_for('usuarios'))
    else:
        return redirect(url_for('home'))
    


@app.route('/remover_notificacao',methods=["GET"])
def remover_notificacao():
    id = request.args.get('id')
    model.remover_notificacao(id)

    return redirect(url_for('home'))


@app.route('/tarefas',methods=['POST'])
def tarefas():
    if session['logged_in']:
        
        id = request.form['id_tarefa']
        ponto = request.form['ponto']
        conclusao = request.form['conclusao']
        if conclusao == 'verdadeiro':
            mensagem,tipo = model.concluir_tarefa(id)
        else:
            mensagem,tipo = None,None

        nao_concluidas = model.retornar_contagem('NAO',ponto)
        tarefas_r = model.retornar_todas_tarefas(ponto,True)
        tarefa = model.retornar_uma_tarefa(id)
        concluidas = model.retornar_contagem('SIM',ponto)

        return render_template('tela_de_tarefas.html',mensagem=mensagem,tipo=tipo,tarefas_r=tarefas_r,tarefa=tarefa,concluidas=concluidas,nao_concluidas=nao_concluidas)
    else:
        return redirect(url_for('home'))


