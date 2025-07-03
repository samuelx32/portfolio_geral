def valida_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))

    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    def calcula_digito(d, peso):
        soma = 0
        for i, v in enumerate(d):
            soma += int(v) * peso[i]
        resto = soma % 11
        return (11 - resto) if resto > 1 else 0

    # Pesos para o primeiro e segundo dígitos verificadores
    peso1 = [10, 9, 8, 7, 6, 5, 4, 3, 2]
    peso2 = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]

    digito1 = calcula_digito(cpf[:-2], peso1)
    if digito1 != int(cpf[-2]):
        return False

    digito2 = calcula_digito(cpf[:-1], peso2)
    if digito2 != int(cpf[-1]):
        return False

    return True

def valida_cnpj(cnpj):
    cnpj = ''.join(filter(str.isdigit, cnpj))

    # Verifica se tem 14 dígitos e se todos os dígitos não são iguais
    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        return False

    def calcula_digito(d, peso):
        soma = 0
        for i, v in enumerate(d):
            soma += int(v) * peso[i]
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    # Pesos para o primeiro e segundo dígitos verificadores
    peso1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    peso2 = [6] + peso1  # Adiciona um peso extra no início para o segundo dígito

    digito1 = calcula_digito(cnpj[:-2], peso1)
    if digito1 != int(cnpj[-2]):
        return False

    digito2 = calcula_digito(cnpj[:-1], peso2)
    if digito2 != int(cnpj[-1]):
        return False

    return True


def valida_conta_bb(sConta):
    try:
        s = ""
        for x in range(len(sConta) - 1):
            if sConta[x].isdigit():
                s += sConta[x]
        if len(s) > 11:
            return False
        iResult = 0
        for x in range(len(s[:11])):
            factor = 9 - x
            if factor in range(10):
                iResult += int(s[len(s[:11]) - x - 1]) * factor
            else:
                iResult += int(s[len(s[:11]) - x - 1]) * 9
        sTotal = int(iResult / 11)
        sTotal = int(sTotal * 11)
        sTotal = int(iResult - sTotal)
        if sTotal == 10:
            sTotal = "X"
        if sConta[-1] == str(sTotal):
            return True
        else:
            return False
    except Exception as e:
        print("Erro:", e)
        return False