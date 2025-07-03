import sqlite3
from playwright.sync_api import sync_playwright
import os

def atualizar_base_de_noticias():
    with sync_playwright() as p:        
        browser = p.chromium.launch(headless=True)    
        
        page = browser.new_page()
        page.goto("https://camaranet.camara.leg.br/web/noticias-da-casa/noticias/-/resultados/avisos/10131/384295", wait_until="domcontentloaded")  
        qtn = page.locator(".resultados > li").count()
        noticias = []
        links = []
        for i in range(0,qtn):
            aux = page.locator(f".resultados > li >> nth = {i} ").inner_text()
            aux2 = page.locator(f".resultados > li > a >> nth = {i} ").get_attribute("href")
            noticias.append(aux)
            links.append(aux2)
        page.close()
        browser.close()

    # conexao = sqlite3.connect(r'Z:\Mapa de Gastos\Samuel\Programa Principal Trabalho\data\sicod_gru.db')
    conexao = sqlite3.connect(os.path.join(r"C:\Users\p_702809\Desktop\Projeto_CONAB\data", "banco_comof.db"))
    cursor = conexao.cursor()
    cursor.execute("DROP TABLE IF EXISTS noticias")
    cursor.execute("CREATE TABLE IF NOT EXISTS noticias (id INTEGER PRIMARY KEY, texto TEXT NOT NULL, link TEXT NOT NULL)")
    l = 0
    for noticia in noticias:
        cursor.execute("INSERT INTO noticias (texto,link) values (?,?)",(noticia,links[l],))
        l += 1

    cursor.execute("select * from noticias")
    resultados = cursor.fetchall()
    # for linha in resultados:
    #     print(linha)

    conexao.commit()
    conexao.close()

