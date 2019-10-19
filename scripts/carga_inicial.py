import sqlite3

conn = sqlite3.connect('analiseSentimento.db')

conn.execute('''CREATE TABLE Modulo
         (Frase           TEXT    NOT NULL,
         Sentimento            INT     NOT NULL
        );''')

conn.execute('''CREATE TABLE Config
         (IsTreinado           INT    NOT NULL
        );''')

with open("dataset.txt", "r") as arquivo_texto:
        for linha in arquivo_texto:
            dados = linha.split(';')
            dados[1] = dados[1].rstrip()
            conn.execute("INSERT INTO Modulo (Frase,Sentimento)VALUES (?,?)",dados);
            
conn.execute("INSERT INTO Config (IsTreinado)VALUES (1)");
conn.commit()
conn.close()