# ---------------------------------------------LIBRARIES-------------------------------------------------------------
import psycopg2
import psycopg2.extras

from passlib.hash import sha256_crypt
from datetime import datetime
from datetime import timedelta

# -------------------------------------------VARIÁVEIS------------------------------------------------------------------



# -------------------------------------------Data_Base_conn--------------------------------------------------------------

conn = psycopg2.connect("host=localhost dbname=BD_projeto user=postgres password=Banana1543")
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


# -------------------------------------------------NIVEL 0--------------------------------------------------------------
def nivel0():
    i_0 = int(input('Bem vindo! Deseja 1-Registar-se  2-Fazer Login como cliente  3-Fazer Login como administrador'))

    if i_0 not in [1, 2, 3]:
        print('Erro. Tente novamente.')
        nivel0()
    if i_0 == 1:  # REGISTO
        registo()
    elif i_0 == 2:  # LOGIN CLIENTE
        login_cliente()
    elif i_0 == 3:  #LOGIN ADMIN
        login_admin()


def registo(): #ACABADO
    Nome = input('Qual o seu nome? ')
    email = input('Qual o seu email? ')
    cur.execute("SELECT * FROM pessoa")
    for linha in cur.fetchall():
        maillist = linha['email']

    if email in maillist:
        print('Este email já se encontra registado. Tente novamente ou efetue login.')
        nivel0()  # volta ao nivel 0 para registar ou fazer login

    else:
        Pass = input('Qual a Password? ')
        pass_crypt = sha256_crypt.hash(Pass)
        cur.execute("INSERT INTO pessoa (email, nome, password) values (%s, %s, %s)", (email, Nome, pass_crypt))
        conn.commit()
        cur.execute(f"INSERT INTO cliente (id_clien, saldo, pessoa_email) VALUES (DEFAULT, NULL , (SELECT email FROM pessoa WHERE email = '{email}'))")
        conn.commit()
        print('Conta criada com sucesso! Recebeu um saldo grátis de 20€ para gastar! Só precisa de fazer login :-)')
        nivel0()

def login_cliente(): #ACABADO
    global mail
    mail = input('Email: ')
    aux = input('Password: ')
    cur.execute("SELECT password FROM pessoa WHERE email = %s", [mail])

    if cur.rowcount > 0:
        Pass_crypt, = cur.fetchone()
        if sha256_crypt.verify(aux, Pass_crypt):  # VER O QUE ESTÁ MAL
            print('\nBem vindo!')
            nivel1()
        else:
            print("Palavra passe errada! Volte a tentar fazer login!")
            login_cliente()
    else:
        print("O email inserido não se encontra registado. Por favor faça o registo!")
        nivel0()

# os admin são manualmente adicionados à base de dados
def login_admin(): #ACABADO
    global mail_admin
    mail_admin = input('Email:')
    aux = input('Password:')
    cur.execute("SELECT pessoa_email from admistrador WHERE pessoa_email = %s", [mail_admin])
    if cur.rowcount > 0:
        cur.execute("SELECT password FROM pessoa WHERE email = %s", [mail_admin])
        for linha in cur.fetchall():
            if linha == [aux]:
                print('\nBem vindo!')
                nivel1_admin()
            else:
                print('Password errada! Tente novamente!')
                login_admin()
    else:
        print('O email inserido não é um email associado a um administrador. Tente novamente!')
        login_admin()


# -------------------------------------------------NIVEL 1--------------------------------------------------------------

def logout(): #ACABADO
    print("Obrigado por usar os nossos serviços")
    nivel0()


def listagem(): #ACABADO
    nome()
    cur.execute("SELECT nome, preco, tipo FROM artigo")
    for linha in cur.fetchall():
        titulos = linha['nome']
        preco = linha['preco']
        tipo = linha['tipo']
        print(f'\n Título do filme-{titulos}\n Tipo-{tipo}\n Preço-{preco}€\n')


def procura_todos(): #ACABADO
    nome()
    global lista_filmes
    pesquisa = int(input('Como deseja pesquisar? 1- Nome 2- Género 3- Realizador 4-Ator'))
    if pesquisa not in [1, 2, 3, 4]:
        print('Erro. Tente novamente.')
        procura_todos()

    elif pesquisa == 1:
        nome_artigo = input('Qual o nome do artigo?')
        cur.execute("SELECT * FROM artigo WHERE artigo.nome = %s", [nome_artigo])  # COMO FAZER PARA VERIFICAR SE HA
        lista_filmes = []
        for linha in cur.fetchall():
            titulo_filme = linha['nome']
            tipo = linha['tipo']
            preco = linha['preco']
            tempo_disp = linha['tempo_disp']
            descricao = linha['descricao']
            lista_filmes.append(titulo_filme)
            print(f'\n Título do filme-{titulo_filme}\n Tipo-{tipo}\n Preço-{preco}€\n Tempo disponível-{tempo_disp}dias\n Descrição-{descricao}\n')

        escolha = int(input('Pretende alugar um filme? 1-Sim 2-Não'))
        if escolha == 1:
            alugar()
        elif escolha ==2:
            nivel1()

    elif pesquisa == 2:
        genero = input('Qual o género de filme?')
        cur.execute("SELECT * FROM artigo WHERE artigo.tipo = %s", [genero])
        lista_filmes = []
        for linha in cur.fetchall():
            titulo_filme = linha['nome']
            tipo = linha['tipo']
            preco = linha['preco']
            tempo_disp = linha['tempo_disp']
            descricao = linha['descricao']
            lista_filmes.append(titulo_filme)
            print(f'\n Título do filme-{titulo_filme}\n Tipo-{tipo}\n Preço-{preco}€\n Tempo disponível-{tempo_disp}dias\n Descrição-{descricao}\n')
        escolha = int(input('Pretende alugar um filme? 1-Sim 2-Não'))
        if escolha == 1:
            alugar()
        elif escolha == 2:
            nivel1()

    elif pesquisa in [3, 4]:
        participante = input('Qual o interveniente que pretende pesquisar?')
        cur.execute("SELECT * FROM artigo WHERE id_arti IN (SELECT artigo_id_arti FROM artigo_participante WHERE participante_id_pess IN (SELECT id_pess FROM participante WHERE nome = %s))", [participante])
        lista_filmes = []
        for linha in cur.fetchall():
            titulo_filme = linha['nome']
            tipo = linha['tipo']
            preco = linha['preco']
            tempo_disp = linha['tempo_disp']
            descricao = linha['descricao']
            lista_filmes.append(titulo_filme)
            print(f'\n Título do filme-{titulo_filme}\n Tipo-{tipo}\n Preço-{preco}€\n Tempo disponível-{tempo_disp}dias\n Descrição-{descricao}\n')
        escolha = int(input('Pretende alugar um filme? 1-Sim 2-Não'))
        if escolha == 1:
            alugar()
        elif escolha == 2:
            nivel1()

def procura_alugados(): #mudar algumas coisas #ACABADO
    nome()
    now = datetime.now()
    procura = int(input('Como deseja pesquisar? 1- Nome 2- Género 3- Realizador 4-Ator'))
    if procura not in [1, 2, 3, 4]:
        print('Erro. Tente novamente.')
        procura_alugados()

    elif procura == 1:
        try:
            Nome_artigo = input('Qual o nome do artigo?')
            cur.execute(f"SELECT * FROM aluguer WHERE nome = '{Nome_artigo}' AND cliente_pessoa_email = '{mail}'")
            for linha in cur.fetchall():
                tempofinal = linha['tempo_final']
                if tempofinal < now:
                    cur.execute(f"UPDATE aluguer SET expirado = TRUE WHERE nome = '{Nome_artigo}' AND cliente_pessoa_email = '{mail}'")
                    conn.commit()
                    print('O artigo selecionado encontra-se expirado')
                    procura_alugados()
                else:
                    titulo_filme = linha['nome']
                    tipo = linha['tipo']
                    preco = linha['preco']
                    print(f'\n Título do filme-{titulo_filme}\n Tipo-{tipo}\n Preço-{preco}€\n Pode ver o filme!')
        except:
            print('Erro. Pode não ter alugado artigos com esse nome')
            conn.rollback()

    elif procura == 2:
        try:
            genero = input('Qual o género de filme?')
            cur.execute(f"SELECT * FROM aluguer WHERE tipo = '{genero}' AND cliente_pessoa_email = '{mail}'")
            for linha in cur.fetchall():
                nome_filme = linha['nome']
                tempofinal = linha['tempo_final']
                if tempofinal < now:
                    cur.execute(f"UPDATE aluguer SET expirado = TRUE WHERE nome = '{nome_filme}' AND cliente_pessoa_email = '{mail}'")
                    conn.commit()
                    print(f'O artigo de nome {nome_filme} encontra-se expirado')
                else:
                    titulo_filme = linha['nome']
                    tipo = linha['tipo']
                    preco = linha['preco']
                    print(f'\n Título do filme-{titulo_filme}\n Tipo-{tipo}\n Preço-{preco}€\n Pode ver o filme!')
        except:
            print('Erro. Pode não ter alugado artigos desse tipo')
            conn.rollback()

    elif procura in [3, 4]:
        try:
            participante = input('Qual o interveniente que pretende pesquisar?')
            cur.execute(f"SELECT * FROM aluguer WHERE cliente_pessoa_email = '{mail}' AND aluguer.artigo_id_arti IN (SELECT artigo_id_arti FROM artigo_participante WHERE participante_id_pess IN (SELECT id_pess FROM participante WHERE nome = %s))", [participante])
            for linha in cur.fetchall():
                nome_filme = linha['nome']
                tempofinal = linha['tempo_final']
                if tempofinal < now:
                    cur.execute(f"UPDATE aluguer SET expirado = TRUE WHERE nome = '{nome_filme}' AND cliente_pessoa_email = '{mail}'")
                    conn.commit()
                    print(f'O artigo de nome {nome_filme} encontra-se expirado')
                else:
                    titulo_filme = linha['nome']
                    tipo = linha['tipo']
                    preco = linha['preco']
                    print(f'\n Título do filme-{titulo_filme}\n Tipo-{tipo}\n Preço-{preco}€\n Pode ver o filme!')
        except:
            print('Erro. Pode não ter alugado artigos com esse interveniente')
            conn.rollback()

def alugar(): #ACABADO
    global selecao
    selecao = input('Selecione o nome do(a) filme/série que pretende alugar')
    x = datesum()
    if selecao in lista_filmes: #Resolver isto
        rent = int(input('Tem a certeza que quer alugar o filme/série? 1-Sim 2-Não'))
        if rent not in [1, 2]:
            print('Opção não disponível, tente novamente')
            alugar()
        elif rent == 1:
            cur.execute("SELECT saldo FROM cliente WHERE pessoa_email = %s", [mail])
            saldo = cur.fetchone()[0]
            cur.execute("SELECT preco FROM artigo WHERE nome = %s", [selecao])
            preco_arti = cur.fetchone()[0]
            if saldo < preco_arti:
                print('Saldo insuficiente')
                nivel1()
            else:
                cur.execute("SELECT * FROM artigo WHERE nome = %s", [selecao])
                for linha in cur.fetchall():
                    nome = linha['nome']
                    tipo = linha['tipo']
                    preco = linha['preco']
                    tempo_disp = linha['tempo_disp']
                cur.execute(f"INSERT INTO aluguer (id_aluguer, nome, tipo, preco, expirado, cliente_pessoa_email, artigo_id_arti, tempo_disp, tempo_final)"
                            f"VALUES (DEFAULT,'{nome}','{tipo}',{preco},FALSE,'{mail}',(SELECT id_arti FROM artigo WHERE nome = '{selecao}'),{tempo_disp},TIMESTAMP'{x}')")
                conn.commit()
                novo_saldo = saldo - preco_arti
                cur.execute(f"UPDATE cliente SET saldo = {novo_saldo} WHERE pessoa_email = '{mail}'")
                conn.commit()
                print('Transação efetuada!')
    else:
        print('Erro. Tente novamente')
        alugar()

def mensagem(): #ACABADO
    nome()
    status = int(input('1-mensagens não lidas 2-mensagens lidas'))
    if status not in [1, 2]:
        print('opção não disponivel. Tente novamente.')
        mensagem()

    if status == 1:
        cur.execute("SELECT * FROM mensagens WHERE estado = FALSE AND id_mens IN (SELECT mensagens_id_mens FROM cliente_mensagens WHERE cliente_pessoa_email IN (SELECT pessoa_email FROM cliente WHERE pessoa_email = %s))", [mail])
        for linha in cur.fetchall():
            texto = linha['texto']
            print(f'\nMensagem: {texto}')
        cur.execute("UPDATE mensagens SET estado = TRUE WHERE estado = FALSE AND id_mens IN (SELECT mensagens_id_mens FROM cliente_mensagens WHERE cliente_pessoa_email = %s)", [mail]) #não lidas passam a estar lidas
        conn.commit()

    elif status == 2:
        cur.execute("SELECT * FROM mensagens WHERE estado = TRUE AND id_mens IN (SELECT mensagens_id_mens FROM cliente_mensagens WHERE cliente_pessoa_email IN (SELECT pessoa_email FROM cliente WHERE pessoa_email = %s))", [mail])  # mudar esta linha
        for linha in cur.fetchall():
            texto = linha['texto']
            print(f'\nMensagem: {texto}')


def historico():  # dinheiro gasto no site e artigos alugados ACABADO
    try:
        nome()
        lista_preco = []
        cur.execute("SELECT nome, preco, expirado FROM aluguer WHERE cliente_pessoa_email = %s", [mail])
        for linha in cur.fetchall():
            Nome = linha['nome']
            preco = linha['preco']
            expirado = linha['expirado']
            lista_preco.append(preco)
            if expirado == True:
                exp = 'artigo expirado'
            else:
                exp = 'artigo ativo'
        total = sum(lista_preco)
        print(f'Nome do artigo: {Nome}\nPreço do artigo: {preco}\n-> {exp}')
        print(f"O total gasto em filmes/séries é de {total}€")
    except:
        print('Erro. Pode nunca ter alugado um artigo')
        conn.rollback()



def saldo(): #ACABADO
    nome()
    cur.execute("SELECT saldo FROM cliente WHERE pessoa_email = %s", [mail])
    for linha in cur.fetchall():
        dinheiro = linha['saldo']
        print(f"Tem {dinheiro}€ disponíveis para gastar")

def nome(): #ACABADO
    cur.execute("SELECT nome FROM pessoa WHERE email = %s", [mail])
    nome_cliente = cur.fetchone()[0]
    print(f"\n                                                                          Conta de {nome_cliente}\n")

def nome_admin(): #ACABADO
    cur.execute("SELECT nome FROM pessoa WHERE email = %s", [mail_admin])
    nome_cliente = cur.fetchone()[0]
    print(f"\n                                                                          Conta de {nome_cliente}\n")

def datesum(): #ACABADO
    cur.execute("SELECT tempo_disp FROM artigo WHERE nome = %s", [selecao])
    delta = cur.fetchone()[0]
    data_now = datetime.now()
    soma = (data_now + timedelta(days = delta))
    return soma



"""

Funções do admin

"""


def enviar_mensagem(): #ACABADO
    nome_admin()
    option = int(input("Seleccione se quer mandar mensagem a 1-clientes específicos ou 2-todos os clientes"))

    if option not in [1,2]:
        print("Opção invalida tente novamente")
        enviar_mensagem()


    elif option ==1:
        n_pessoas= int(input('Quer mandar mensagem a quantas pessoas?'))
        i = 1
        lista_mails = []
        while i <= n_pessoas:
            mails = input(f"mail da {i}ª pessoa:")
            lista_mails.append(mails)
            i = i+1
        lista_mails.sort()

        sendingtext = input("Escreva a mensagem a enviar: ")

        lista_pessoas=[]
        cur.execute("SELECT email FROM pessoa")                 #mails existentes
        for linha in cur.fetchall():
            lista_pessoas.append(linha)
        lista_pessoas.sort()
        if lista_mails not in lista_pessoas:
            print('Erro, um ou mais mails errados. Tente novamente.')
            enviar_mensagem()
        else:
            cur.execute(f"INSERT INTO mensagens (id_mens, estado, texto, admistrador_pessoa_email) VALUES (DEFAULT, FALSE, '{sendingtext}', '{mail_admin}')")
            conn.commit()

            for j in lista_mails:
                cur.execute(f"INSERT INTO cliente_mensagens (cliente_pessoa_email, mensagens_id_mens) VALUES ('{j}', (SELECT id_mens FROM mensagens WHERE texto = '{sendingtext}'))")
                conn.commit()
            print('Mensagem enviada!')
    elif option == 2:

        texto = input("escreva a mensagem a enviar: ")
        cur.execute("SELECT pessoa_email FROM cliente")
        for linha in cur.fetchall():
            cur.execute(f"INSERT INTO mensagens (id_mens, texto, estado, admistrador_pessoa_email) VALUES (DEFAULT, '{texto}', FALSE, '{mail_admin}')")
            conn.commit()
            mails = linha['pessoa_email']
            cur.execute(f"INSERT INTO cliente_mensagens (cliente_pessoa_email, mensagens_id_mens) VALUES ('{mails}', (SELECT MAX(id_mens) FROM mensagens))") #ver se isto resulta com o MAX
            conn.commit()
        print('Mensagem enviada!')

def mudar_preco(): #ACABADO
    nome_admin()
    now = datetime.now()
    artigo= input("Qual o artigo a alterar? Digite o nome do item:  ")
    novopreco= float(input("Qual o novo preço? "))

    itemlist = []
    cur.execute("SELECT * FROM artigo")
    for linha in cur.fetchall():
       itemlist.append(linha['nome'])

    if artigo not in itemlist:
        print("O artigo que selecionou não está disponivel")
        mudar_preco()
    else:
        cur.execute("SELECT preco FROM artigo WHERE nome =%s", [artigo])
        for linha in cur.fetchall():
            preco_ant = linha['preco']

            cur.execute(f"UPDATE artigo SET preco = {novopreco} WHERE nome = '{artigo}'")
            cur.execute(f"INSERT INTO historico_arti (novo_pre, preco_anti, data_alteracao, artigo_id_arti) VALUES ({novopreco}, {preco_ant}, TIMESTAMP '{now}', (SELECT id_arti FROM artigo WHERE nome = '{artigo}'))")
            conn.commit()
            print('Alterações efetuadas!')


def stats(): #ACABADO
    nome_admin()
    cur.execute("SELECT count(pessoa_email) FROM cliente")
    ans = cur.fetchone()[0]
    print(f"Há {ans} cliente(s) \n")

    cur.execute("SELECT count(nome) FROM artigo")
    ans = cur.fetchone()[0]
    print(f"Há {ans} artigo(s) diferente(s) para selecionar \n")

    cur.execute("SELECT sum(preco) FROM aluguer")
    ans = cur.fetchone()[0]
    print(f"Valor total gasto pelos clientes: {ans}€ \n")

    cur.execute("SELECT sum(preco) FROM aluguer where expirado = FALSE")
    ans = cur.fetchone()[0]
    print(f"Valor gasto em alugueres ainda disponiveis: {ans}€ \n")

    cur.execute("SELECT DISTINCT tipo FROM artigo")
    for linha in cur.fetchall():
        cur.execute("SELECT count(nome) FROM artigo WHERE tipo = %s", linha)
        ans = cur.fetchone()[0]
        tipo = linha[0]
        print(f"Total de artigos (por tipo):\n{tipo}: {str(ans)} artigo(s) \n")

#falta mais uma escolher alguma que seja facil de implementar ou qual o cliente que gastou mais dinheiro
#Visualizar todos os artigos disponíveis (incluindo preço e condições de aluguer).


def remover_artigo(): # ACABADO
    nome_admin()
    lista_alugados = []
    cur.execute("SELECT * FROM aluguer")    #dizer aqui que é so os que n estão alugados
    for linha in cur.fetchall():
        lista_alugados.append(linha["nome"])
    lista_todos_artigos=[]
    cur.execute("SELECT * FROM artigo")
    for linha in cur.fetchall():
        lista_todos_artigos.append(linha["nome"])

    escolha = input("Elimine apenas um item de cada vez. Introduza o nome do item que pretende eliminar: ")
    if escolha in lista_alugados or escolha not in lista_todos_artigos:
        print("Opção inválida: item não existente ou item alugado por algum cliente")
        remover_artigo()
    else:
        cur.execute("SELECT participante_id_pess FROM artigo_participante WHERE artigo_id_arti IN (SELECT id_arti FROM artigo WHERE nome = %s)", [escolha])
        for linha in cur.fetchall():
            idsave = linha[0]
        cur.execute("DELETE FROM artigo_participante WHERE artigo_id_arti IN (SELECT id_arti FROM artigo WHERE nome = %s)", [escolha])
        cur.execute("DELETE FROM artigo WHERE nome = %s", [escolha])
        cur.execute(f"DELETE FROM participante WHERE id_pess = {idsave}")
        conn.commit()
    print('Alterações efetuadas!')


def adicionar_artigo(): #ACABADO
    nome_admin()
    titulo = input('Título do artigo: ')
    preco = input('Preco do artigo: ')
    tipo = input('Tipo do artigo: ')
    tempo = input('Tempo disponivel após aluguer do artigo: ')
    descricao = input('Sinopse do filme/série: ')
    cur.execute("SELECT nome FROM artigo")
    lista_titulos = []
    for linha in cur.fetchall():
        lista_titulos.append(linha)

    if titulo in lista_titulos:
        print('O artigo que pretende adicionar já existe. Volte a tentar!')
        adicionar_artigo()
    else:
        cur.execute(f"INSERT INTO artigo (id_arti, nome, preco, tempo_disp, descricao, tipo, admistrador_pessoa_email) VALUES (DEFAULT, '{titulo}', {preco}, {tempo}, '{descricao}', '{tipo}', '{mail_admin}')")

    n_participantes = int(input('Introduzir os participantes do filme/série. Quantos participantes quer adicionar?'))
    j = 1
    while j <= n_participantes:
        nome_p = input(f'Introduza o nome do {j}º participante')
        funcao_p = input('Qual o papel do participante? (se é ator, realizador,...)')
        idade_p = input('Qual a idade do participante?')
        nacionalidade_p = input('Qual a nacionalidade do participante?')
        cur.execute(f"INSERT INTO participante (id_pess, funcao, nome, nacionalidade, idade) VALUES (DEFAULT, '{funcao_p}', '{nome_p}', '{nacionalidade_p}', {idade_p})")
        cur.execute("INSERT INTO artigo_participante (artigo_id_arti, participante_id_pess) VALUES ((SELECT MAX(id_arti) FROM artigo), (SELECT MAX(id_pess) FROM participante))")
        j = j+1
    conn.commit()
    print('Alterações efetuadas!')



def alterar_saldo(): #ACABADO
    nome_admin()
    try:
        aux = input("Introduza o email do cliente de quem quer alterar o saldo: ")
        newbalance = int(input("Qual o novo saldo? "))
        maillist = []
        cur.execute("SELECT * FROM cliente WHERE pessoa_email = %s", [aux])
        for linha in cur.fetchall():
            maillist.append(linha['pessoa_email'])

        if aux not in maillist:
            print("A pessoa que selecionou não está registada. Tente novamente!")
            alterar_saldo()
        else:
            cur.execute(f"UPDATE cliente SET saldo = {newbalance} WHERE pessoa_email = '{aux}'")
            conn.commit()
            print("Operação concluída com sucesso!")
    except psycopg2.DatabaseError as erro:
        print('Ocorreu um erro! Operação anulada.')
        print(erro)
        conn.rollback()
    except:
        print('Ocorreu um erro! Operação anulada.')
        conn.rollback()



#-----------------------------------------------------------------------------------------------------------------------------------------------


# OPCOES: 1-Listar os artigos 2-Procurar artigos 3-C0mprar 4- Ver historico 5-Ver mensagens 6- saldo 7-Logout
def nivel1():
    nome()
    i_1 = int(input('1-Todos os artigos disponíveis para alugar\n2-Procurar artigos novos\n3-Procurar artigos alugados\n4-Ver historico\n5-Ver mensagens\n6- Consultar saldo\n7-Logout'))

    if i_1 == 1:  # LISTAGEM
        listagem()
        nivel1()

    elif i_1 == 2:  # PROCURA
        procura_todos()
        nivel1()

    elif i_1 == 3:  # PROCURA ALUGADOS
        procura_alugados()
        nivel1()

    elif i_1 == 4:  # HISTORICO
        historico()
        nivel1()

    elif i_1 == 5:  # MENSAGENS
        mensagem()
        nivel1()

    elif i_1 == 6:  # SALDO
        saldo()
        nivel1()

    elif i_1 == 7:  # LOGOUT
        logout()

    else:
        print('Opção inválida. Tente novamente')
        nivel1()

def nivel1_admin():
    nome_admin()
    i_1 = int(input('1-Enviar mensagem\n2-Alterar preço de um artigo\n3-Remover um artigo\n4-Adicionar um artigo\n5-Alterar o saldo de um cliente\n6-Estatísticas\n7-Logout'))

    if i_1 == 1:
        enviar_mensagem()
        nivel1_admin()

    elif i_1 == 2:
        mudar_preco()
        nivel1_admin()

    elif i_1 == 3:
        remover_artigo()
        nivel1_admin()

    elif i_1 == 4:
        adicionar_artigo()
        nivel1_admin()

    elif i_1 == 5:
        alterar_saldo()
        nivel1_admin()

    elif i_1 == 6:
        stats()
        nivel1_admin()

    elif i_1 == 7:  # LOGOUT
        logout()

    else:
        print('Opção inválida. Tente novamente')
        nivel1_admin()





# -------------------------------------------interação_entre_níveis------------------------------------------------------

# pip install pyfiglet
import pyfiglet
ascii_banner = pyfiglet.figlet_format("NETFLOX")
print(ascii_banner)

nivel0()
#datesum()
#nivel1()
#login_admin()
#mensagem()
#saldo()
#historico()
#procura_todos()
#mensagem()


# --------------------------------------------------close_conn-----------------------------------------------------------

cur.close()
conn.close()


# ---------------------------------------------correções--------------------------------------

'''


'''





