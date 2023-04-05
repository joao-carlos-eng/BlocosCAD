# -*- coding: utf-8 -*-
"""
Created on Wed Sep 1 15:15:25 2021
@author: joaof

"""
import ezdxf
import time
from tkinter import *
from tkinter import ttk

lis, cnt, erros = [], 0, False
log = 'Acompanhe o programa aqui !!\n'

b = []
executado = False


def up_terminal(text):
    var.set(log + text)


def refresh():
    global var_barra, var
    var_barra.set(0)
    var.set('')
    var.set(log)
    blocos_cad(True)
    janela.update()


def carregar_arquivos():
    global log, var_barra, b, erros

    try:
        doc = ezdxf.readfile("Modelo.dxf")
        msp = doc.modelspace()
        log += "Arquivo \'Modelo.dxf\' carregado com sucesso.\n"
        b = [doc, msp]
        erros = False
    except FileNotFoundError:
        print("Arquivo 'modelo.dxf' não encontrado, verifique o mesmo.\n")
        log += "Arquivo 'modelo.dxf' não encontrado, verifique o mesmo.\n"
        erros = True

    try:
        doc1 = open('pontos.txt', encoding='utf-8')
        log += "Arquivo \'pontos.txt\' carregado com sucesso.\n"
        for i in doc1.readlines():
            co = i.split(',')
            lis.append((float(co[0]), float(co[1])))
        erros = False
    except FileNotFoundError:
        log += 'Arquivo \'pontos.txt\' não encontrado, verifique o mesmo.\n'
        erros = True


def executar():
    global executado
    if executado:
        refresh()
    else:
        executado = True
        blocos_cad()


def blocos_cad(passo=False):
    global lis, cnt, log

    if passo:
        carregar_arquivos()
    else:
        cnt = 0
    if not erros:
        progresso['maximum'] = len(lis)
        while True:
            for point in lis:
                cnt += 1
                var_barra.set(cnt)
                janela.update()
                b[1].add_blockref('PT_E', point)
                up_terminal("\nIniciando o processo de criação de blocos.\n"
                            "Aguarde...\nEstou fazendo o serviço de CORNO para você.\n"
                            f"criando bloco n° {cnt}.".center(50))
            time.sleep(3)
            if cnt == len(lis):
                break

        b[0].saveas("blocos.dxf")
        up_terminal(f'\nForam criados {len(lis)} blocos.\n'
                    f'Concluído, agora abra o novo arquivo.')
    else:
        up_terminal('\n LEIA as instruções e tente novamente\n')


info0 = '>> INSTRUÇÕES <<'.center(120)
info1 = '1    : Salve o Arquivo do CAD como >> .DXF <<'.ljust(99)
info2 = '2    : Salve os postes como lista de cordenadas UTM'.ljust(99)
info3 = '2.1 : As coordenadas devem estar separados por VIRGULA'.ljust(91)
info4 = '2.2 : O arquivo dos postes tem que está salvo como >>pontos.txt<<'.ljust(84)
info5 = '3    : O arquivo de saída é >>blocos.dxf <<'.ljust(106)

janela = Tk()
janela.title("Blocos CAD")

var_barra = DoubleVar(master=janela)
var = StringVar(master=janela)
var.set('Acompanhe o programa aqui !!')

text_info0 = Label(janela, text=info0)
text_info0.grid(column=0, row=0, columnspan=3)

text_info1 = Label(janela, text=info1)
text_info1.grid(column=0, row=1, columnspan=3)

text_info2 = Label(janela, text=info2)
text_info2.grid(column=0, row=2, columnspan=3)

text_info3 = Label(janela, text=info3)
text_info3.grid(column=0, row=3, columnspan=3)

text_info4 = Label(janela, text=info4)
text_info4.grid(column=0, row=4, columnspan=3)

text_info5 = Label(janela, text=info5)
text_info5.grid(column=0, row=5, columnspan=3)

bt_executar = Button(janela, text="Executar", command=executar)
bt_executar.grid(column=0, row=6, padx=1, pady=10, columnspan=1)

bt_repetir = Button(janela, text="Tentar de novo", command=refresh)
bt_repetir.grid(column=1, row=6, padx=1, pady=10)

bt_parar = Button(janela, text="Fechar", command=janela.quit)
bt_parar.grid(column=2, row=6, padx=1, pady=10)

msg = Message(janela, textvariable=var, bg='black', fg='green', width='600')
msg.grid(column=0, row=7, padx=3, pady=3, columnspan=4)

progresso = ttk.Progressbar(janela, variable=var_barra)
progresso.grid(column=0, row=8, padx=5, pady=10, columnspan=4)

janela.mainloop()
