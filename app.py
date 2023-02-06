from flask import Flask, jsonify
import pandas as pd
import funcoes as pe


dados_partidas = pe.lista_jogos.astype(str)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route("/", methods=["GET"])
def get_data():
    return jsonify(partidas.to_dict('records'))



@app.route('/competicoes/<edicao>', methods=["GET"])
def partidas(edicao):
    partidas_ = pe.partidas_1(competicao = 0, ano = 0, grupo = 0, fase = 0, rodada = 0, id_jogo = 0)
    return jsonify(partidas_.astype(str).to_dict('records'))






if __name__ == "__main__":
    app.run(debug=True)