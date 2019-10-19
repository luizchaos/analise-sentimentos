import sqlite3

conn = sqlite3.connect('analiseSentimento.db')


cursor = conn.execute("SELECT Frase, Sentimento from Modulo")

for row in cursor:
    print(row)