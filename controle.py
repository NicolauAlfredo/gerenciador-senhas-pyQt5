from PyQt5 import uic, QtWidgets
import sqlite3
from reportlab.pdfgen import canvas

MASTER_PASSWORD = '123456'

conn = sqlite3.connect('passwords.db')


def verificar_senha():
    senha_master = login.txt_login.text()
    if senha_master != MASTER_PASSWORD:
        print('Senha inválida!')
        exit()
    else:
        login.close()
        registo.show()


cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    service TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);
''') 


def inserir_senha():
    service = registo.txt_servico.text()
    username = registo.txt_nome.text()
    password = registo.txt_senha.text()

    print(f'Service: {service}')
    print(f'Username: {username}')
    print(f'Password: {password}')

    # Inserir dados ao banco
    cursor.execute(f'''
    INSERT INTO users (service, username, password) VALUES ('{service}', '{username}', '{password}')
    ''')
    conn.commit() 

    # Limpar os campos do formulário
    registo.txt_servico.setText("")
    registo.txt_nome.setText("")
    registo.txt_senha.setText("")


def listar_servicos():
    lista.show()

    cursor.execute('''
    SELECT * FROM users;
    ''')
    dados_lidos = cursor.fetchall()

    lista.tbl_servicos.setRowCount(len(dados_lidos))
    lista.tbl_servicos.setColumnCount(3)

    for linha in range(0, len(dados_lidos)):
        for coluna in range(0, 3):
            lista.tbl_servicos.setItem(linha, coluna, QtWidgets.QTableWidgetItem(str(dados_lidos[linha][coluna])))


def gerar_pdf(): 
    cursor.execute('''SELECT * FROM users''')
    dados_lidos = cursor.fetchall()

    y = 0
    pdf = canvas.Canvas('Gerenciador de senhas.pdf')
    pdf.setFont('Times-Bold', 25)
    pdf.drawString(200, 800, 'Gerenciador de Senhas')
    pdf.setFont('Times-Bold', 18)

    pdf.drawString(10, 750, 'Serviço')
    pdf.drawString(110, 750, 'Username')
    pdf.drawString(210, 750, 'Password') 

    for c in range(0, len(dados_lidos)):
        y = y + 50
        pdf.drawString(10, 750 - y, str(dados_lidos[c][0]))
        pdf.drawString(110, 750 - y, str(dados_lidos[c][1]))
        pdf.drawString(210, 750 - y, str(dados_lidos[c][2])) 

    pdf.save()
    print('PDF FOI GERADO COM SUCESSO!')


def excluir_servico():
    linha = lista.tbl_servicos.currentRow()
    lista.tbl_servicos.removeRow(linha)

    cursor.execute('SELECT service FROM users')
    dados_lidos = cursor.fetchall()

    valor_servico = dados_lidos[linha][0]
    cursor.execute(f"DELETE FROM users WHERE service = '{valor_servico}'")


app = QtWidgets.QApplication([])

login = uic.loadUi("login.ui")
registo = uic.loadUi("registo.ui")
lista = uic.loadUi("lista.ui")

# Apresentar as páginas
login.btnGo.clicked.connect(verificar_senha)

registo.btn_guardar.clicked.connect(inserir_senha)
registo.btn_listar.clicked.connect(listar_servicos)

lista.btn_pdf.clicked.connect(gerar_pdf)
lista.btn_excluir.clicked.connect(excluir_servico)

login.show()
app.exec()
