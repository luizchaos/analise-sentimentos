from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import BernoulliNB
from flask import Flask, render_template, jsonify, json, abort
from sklearn.externals import joblib
import sqlite3
app = Flask(__name__, template_folder='view',static_url_path='/static')

def recupera_flag():
    conn = sqlite3.connect('analiseSentimento.db')
    cursor = conn.execute("SELECT IsTreinado from Config")
    for row in cursor:
        return row[0]

def atualiza_config_flag(flag):
    conn = sqlite3.connect('analiseSentimento.db')
    conn.execute("UPDATE Config set IsTreinado = ?",[flag])
    conn.commit

def recebe_feedback(frase, valor,feedback):
    atualiza_config_flag(0)
    conn = sqlite3.connect('analiseSentimento.db')
    if feedback=="1":
        print(" kkkk")
        conn.execute("INSERT INTO Modulo (Frase,Sentimento)VALUES (?,?)",[frase, valor]);
        conn.commit()
    else:
        print(" llll")
        valor_reverso = 0 if valor == "1" else 1
        print(valor)
        print(valor_reverso)
        conn.execute("INSERT INTO Modulo (Frase,Sentimento)VALUES (?,?)",[frase, valor_reverso]);
        conn.commit()
    
    atualiza_config_flag(1)

def exibir_resultado(valor):
    frase, resultado = valor
    resultado = "Frase positiva" if resultado[0] == 1 else "Frase negativa"
    return(frase,resultado)

def analisar_frase(classificador, vetorizador, frase):
    return frase, classificador.predict(vetorizador.transform([frase]))


def obter_dados_das_fontes():
    conn = sqlite3.connect('analiseSentimento.db')
    cursor = conn.execute("SELECT Frase, Sentimento from Modulo")
    dados = []
    for row in cursor:
        dados.append(row)
    return dados

def pre_processamento():
    dados = obter_dados_das_fontes()

    return (dados)


def realizar_treinamento(registros_de_treino, vetorizador):
    treino_comentarios = [registro_treino[0] for registro_treino in registros_de_treino]
    treino_respostas = [registro_treino[1] for registro_treino in registros_de_treino]

    treino_comentarios = vetorizador.fit_transform(treino_comentarios)
    atualiza_config_flag(1)
    return BernoulliNB().fit(treino_comentarios, treino_respostas)

registros_de_treino = pre_processamento()
vetorizador = CountVectorizer(binary = 'true')
classificador = realizar_treinamento(registros_de_treino, vetorizador)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calcularsentimento/<frase>')
def calcularsentimento(frase):
    if(recupera_flag() == 1):
        retorno = exibir_resultado( analisar_frase(classificador, vetorizador, frase))
        return jsonify(
            resultado=retorno,
        )
    else:
        abort(404)

@app.route('/feedback/<frase>/<valor>/<feedback>')
def feedback(frase, valor,feedback):
    recebe_feedback(frase, valor,feedback)
    global classificador
    classificador = realizar_treinamento(registros_de_treino, vetorizador)
    return "ok"

app.run(debug=True, port=8080, host="0.0.0.0")
# exibir_resultado( analisar_frase(classificador, vetorizador,"eu amo"))