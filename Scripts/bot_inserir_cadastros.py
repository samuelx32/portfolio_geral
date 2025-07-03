from playwright.sync_api import sync_playwright,expect
import pyautogui as auto
import pandas as pd
import random

def inserir_devedores(page,qtn):
    
    path = r'\\redecamara\DfsData\Comof\Mapa de Gastos\Samuel\Programa Principal Trabalho\Tabela.xlsm'

    df = pd.read_excel(path,skiprows=1)

    inseridos = 0 
    
    for i in range(110,len(df)):
        page.goto("http://localhost:5000/formulario_devedores")
        nome = df['Nome do Devedor'][i]
        cnpj = df['Cpf/Cnpj'][i]
        if len(cnpj) > 14:
            pessoa = 'cnpj'
        else:
            pessoa = 'cpf'

        pronome = 'Ao'
        tratamento = 'Prezado'
        endereco = 'Endereco'

        email = df['E-mail'][i]

        contrato = 'contrato'
        contatos = 'contatos'

        page.locator("#pessoa").select_option(pessoa)
        page.locator("#nome").fill(nome)
        page.locator(f"#{pessoa}").fill(cnpj)
        page.locator("#pronome").select_option(pronome)
        page.locator("#tratamento").select_option(tratamento)
        page.locator("#endereco").fill(endereco)
        page.locator("#email").fill(email)
        page.locator("#contrato").fill(contrato)
        page.locator("#contatos").fill(contatos)

        page.locator("button:has-text('Cadastrar Devedor')").click()
        page.wait_for_timeout(100)
        if page.locator("'Devedor Adicionado com Sucesso'").is_visible() == True:
            inseridos += 1
        
        page.wait_for_timeout(7000)

        

        if inseridos == int(qtn):
            return 'FIM'

        



def inserir_debitos(page,qtn):

    status = 'cobranca'
    num_oficio = '2666'
    data_oficio = '24/04/2025'
    vencimento = '13/05/2025'
    valor = '2.456,12'
    
    processo = '659567/2025'
    

    for i in range(int(qtn)):
        id_devedor = random.randint(1,40)
        page.goto("http://localhost:5000/formulario_debitos")

        page.locator("#num_oficio").fill(num_oficio)
        page.locator("#data_oficio").type(data_oficio)
        page.locator("#vencimento").type(vencimento)
        page.locator("#valor").type(valor)
        page.locator("#processo").type(processo)
        page.locator("#saldo_atual").type(valor)
        devedor = True
        while devedor:
            try:
                page.locator("#id_devedor").select_option(str(id_devedor))
                devedor = False
            except:
                id_devedor = random.randint(1,40)

        page.locator("button:has-text('Cadastrar Débito')").click()

        page.wait_for_timeout(7000)


def main():
    url = 'http://localhost:9222/json/version'
        
    try:
        with sync_playwright() as play:
            browser = play.chromium.connect_over_cdp(url)        
        
            default_context = browser.contexts[0]
            pages = default_context.pages    

            target_page = None
            for page in pages:
                if page.url == 'http://localhost:5000/':
                    page.bring_to_front()
                    target_page = page
                    break     
                
            if target_page:
                page = target_page
            else:
                page = default_context.new_page()
                page.goto("http://localhost:5000/")

            op = auto.confirm(text="O que deseja realizar", title="Menu", buttons=['Inserir Devedores','Inserir Débitos'])
            qtn = auto.prompt("Qual quantidade deseja inserir?")
            if op == 'Inserir Devedores':
                inserir_devedores(page,qtn)
            else:
                inserir_debitos(page,qtn)

            auto.alert("Operação concluida.")
            browser.close()
    except:
        auto.alert("Por favor abra o sistema no Chromium que suporta o copiloto.")



main()