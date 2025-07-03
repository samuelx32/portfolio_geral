
def converter_valor(valor):
    if type(valor) == str:
        valor = float(valor.replace("R$","").replace(",","-").replace(".","").replace("-","."))
        return valor
    else:
        valor = f"{valor:02}".replace(".",",")
        valor = valor.split(",")
        valor_c_pontos = ""
        x = len(valor[0])
        for i in range(len(valor[0])):
            

            if len(valor[0]) > 3 and x % 3 == 0 and x > 0:
                valor_c_pontos = valor_c_pontos+"."
            
            valor_c_pontos = valor_c_pontos + valor[0][i]
           
            x -= 1
            
        if valor_c_pontos[0] == ".":
            valor_c_pontos = valor_c_pontos.replace(".","",1)
            
        valor = "R$ "+valor_c_pontos+","+valor[1]

        return valor

