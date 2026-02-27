import sqlite3

conn = sqlite3.connect("conversas.db")
c = conn.cursor()

c.execute("SELECT * FROM mensagens")
dados = c.fetchall()

for linha in dados:
    print(linha)

conn.close()