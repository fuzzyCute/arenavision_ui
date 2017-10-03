from tkinter import *
import main, webbrowser


def todos_jogos():
    lista_jogos.delete(0, END)
    for row in lista_todos_jogos[:-2]:
        lista_jogos.insert(END, main.format_string(row))

def procura_jogo_command():
    lista_jogos.delete(0, END)

    for row in lista_todos_jogos[:-2]:
        if jogo_text.get().upper() in row[4]:
            lista_jogos.insert(END, main.format_string(row))

def get_selected_links(event):
    global links_dos_jogos
    global canais
    canais = []
    lista_jogo_links.delete(0, END)
    index = lista_jogos.curselection()[0]
    jogoSelecionado = lista_todos_jogos[index][5].replace("\n", " ").split()

    if len(jogoSelecionado) is not 0:
        for i in jogoSelecionado:
            if jogoSelecionado.index(i) % 2 is 0:
                if "-" in i:
                    a = i.split("-")
                    for numero in a:
                        lista_jogo_links.insert(END,numero + " - " + jogoSelecionado[jogoSelecionado.index(i) + 1])
                        canais.append(int(numero))
                else:
                    lista_jogo_links.insert(END,i + " - " + jogoSelecionado[jogoSelecionado.index(i) + 1])
                    canais.append(int(i))
    else:
        lista_jogo_links.insert(END, "SEM LINKS PARA O JOGO")


def open_browser_with_link(event):
    global link_para_web
    link_para_web = lista_jogo_links.curselection()[0]



def ligar_jogo():
    # para abrir a aplicacao com o link obtido
    if 1 <= canais[link_para_web] <= 9:
        webbrowser.open_new_tab(main.get_Url("0" + str(canais[link_para_web])))
    else:
        webbrowser.open_new_tab(main.get_Url(canais[link_para_web]))


if __name__ == "__main__":
    lista_todos_jogos = main.get_options_list()
    links_dos_jogos = [] # para os links do jogo, para a segunda lista
    canais = [] # para os canais quando se liga
    link_para_web = ""

    #inicio do gui
    window = Tk()
    window.wm_title("ArenaVison")
    jogo_text=StringVar()
    e1=Entry(window, textvariable=jogo_text)
    e1.grid(row=0, column=0)

    btn_jogo = Button(window, text="Procurar Jogo", width=12, command = procura_jogo_command)
    btn_jogo.grid(row=0, column=1)

    btn_Todosjogos = Button(window, text="Todos Jogos", width=12, command = todos_jogos)
    btn_Todosjogos.grid(row=0, column=2)

    lista_jogos = Listbox(window, height=40, width = 180, exportselection=0)
    lista_jogos.grid(row=1, column = 0, rowspan=3, columnspan=3)

    sb1 = Scrollbar(window)
    sb1.grid(row=1, column=3, rowspan=3)

    lista_jogos.configure(yscrollcommand=sb1.set)
    sb1.configure(command=lista_jogos.yview)

    lista_jogos.bind('<<ListboxSelect>>',get_selected_links)

    lista_jogo_links = Listbox(window, height=10, width = 30, exportselection=0)
    lista_jogo_links.grid(row=1, column = 4)

    lista_jogo_links.bind('<<ListboxSelect>>',open_browser_with_link)

    todos_jogos()

    btn_ligar = Button(window, text="Ligar", width=12, command = ligar_jogo)
    btn_ligar.grid(row=2, column=4)

    window.mainloop()
    #fim do gui
