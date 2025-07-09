from flask import render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
from app import app
from app import model # todas operações com banco de dados vão para o model, conforme padrão MVC
from app.utils.base_de_noticias import atualizar_base_de_noticias
from app.utils.atualizar_logs import logging #sistema de logging que armazena as ações dos usuários

# Variáveis Globais: As variáveis abaixo vão automaticamente para os templates HTML Jinja2.
@app.context_processor
def inject_global_variables():
    usuario = 'CORAL'
    return {
        'usuario': usuario,
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
    
@app.route('/alterar_conteudo', methods=['POST'])
def alterar_conteudo():
    if session.get('logged_in'):
        id = request.form['id']
        materia = request.form['materia']
        vertente = request.form['vertente']
        titulo = request.form['titulo']
        submateria = request.form['submateria']
        texto = request.form['texto']

        session['mensagem'],session['tipo'] = model.alterar_conteudo(id,materia,vertente,titulo,submateria,texto)
    
        return redirect(url_for('vertente_formulario_mat')) 
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
    

@app.route('/vertente_formulario_alterar_conteudo',methods=['POST'])
def vertente_formulario_alterar_conteudo():
    if session.get('logged_in'):
        mensagem = session.get('mensagem', None)
        tipo = session.get('tipo', None)
        id = request.form['id_conteudo']
        resultado = model.retornar_um_conteudo(id)
        return render_template('vertente_formulario_alterar_conteudo.html',mensagem=mensagem,tipo=tipo,resultado=resultado)
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
    
    

@app.route('/remover_notificacao',methods=["GET"])
def remover_notificacao():
    id = request.args.get('id')
    model.remover_notificacao(id)

    return redirect(url_for('home'))





