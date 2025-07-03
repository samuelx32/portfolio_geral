from playwright.sync_api import sync_playwright

def entrar_no_siafi(page, cpf, senha):
    page.goto("https://siafi.tesouro.gov.br/senha/public/pages/security/login.jsf")
    page.fill('#j_username', cpf)
    page.fill('#j_password', senha)
    page.click('#submitNormal')
    page.wait_for_selector('#frmTemplateAcesso\\:_btnSelecionarFuncionalidade', state='visible', timeout=120000)
    page.click('#frmTemplateAcesso\\:_btnSelecionarFuncionalidade')
    page.wait_for_load_state('networkidle', timeout=60000)

def entrar_gercomp(page):
    page.fill('#frmMenu\\:acessoRapido', "")
    page.fill('#frmMenu\\:acessoRapido', "GERCOMP")
    page.click('#frmMenu\\:botaoAcessoRapidoVerificaTipoTransacao')
    page.wait_for_load_state('networkidle', timeout=60000)

def consultar_np(page):
    page.fill('#formComp\\:tipoDocHabil_input', "")
    page.fill('#formComp\\:tipoDocHabil_input', "NP")
    page.fill('#formComp\\:dataInicialPagamento_calendarInputDate', "")
    page.fill('#formComp\\:dataInicialPagamento_calendarInputDate', "01/01/2024")
    page.fill('#formComp\\:dataFinalPagamento_calendarInputDate', "")
    page.fill('#formComp\\:dataFinalPagamento_calendarInputDate', "31/12/2024")
    page.select_option('#formComp\\:combo_agrupamento', 'DOCUMENTO_HABIL')
    page.select_option('#formComp\\:combo_documentoRealizacao', 'OB')
    page.click('#formComp\\:botao_pesquisar')
    page.wait_for_load_state('networkidle', timeout=60000)

def sair_do_siafi(page):
    input("Por favor, pressione Enter para sair...")
    page.click('a.exit[title="Sair do sistema"]')

def run_playwright(action=None):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False, args=['--start-maximized'])
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()

        cpf = "72278110187"
        senha = "AP$206"

        # Entrar no SIAFI
        entrar_no_siafi(page, cpf, senha)

        if action == "gercomp":
            entrar_gercomp(page)
            consultar_np(page)
        elif action == "sair":
            sair_do_siafi(page)

        browser.close()
