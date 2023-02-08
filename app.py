from flask import Flask, jsonify
import pandas as pd
import funcoes as pe


#dados_partidas = pe.lista_jogos.astype(str)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False


@app.route("/", methods=["GET"])
def get_data():
    return 'API em desenvolvimento'



@app.route('/jogos/<_competicao_>/<_edicao_>', methods=["GET"])
def r_partidas(_competicao_, _edicao_):
    partidas_ = pe.partidas_1(competicao = pe.lista_competicoes[pe.lista_competicoes['codigo'] == _competicao_].reset_index().at[0, 'competicao'],
                              ano = int(_edicao_),
                              grupo = 0, fase = 0, rodada = 0, id_jogo = 0)  
      
    return jsonify(partidas_.astype(str).to_dict('records'))


@app.route('/classificacao/<_competicao_>/', methods=["GET"])
def r_classificacao_geral(_competicao_):
    classificacao_ = pe.classificacao(competicao = pe.lista_competicoes[pe.lista_competicoes['codigo'] == _competicao_].reset_index().at[0, 'competicao'],
                                      ano = 0, grupo = 0, fase = 0, vitoria = 3, empate_sem_gols = 1, empate_com_gols = 1, clube = 0)    
    
    return jsonify(classificacao_.astype(str).to_dict('records'))


@app.route('/classificacao/<_competicao_>/<_edicao_>', methods=["GET"])
def r_classificacao_geral_ano(_competicao_, _edicao_):

    classificacao_ = pe.classificacao(competicao = pe.lista_competicoes[pe.lista_competicoes['codigo'] == _competicao_].reset_index().at[0, 'competicao'],
                                      ano = int(_edicao_),
                                      grupo = 0, fase = 0, vitoria = 3, empate_sem_gols = 1, empate_com_gols = 1, clube = 0)    
    
    return jsonify(classificacao_.astype(str).to_dict('records'))









@app.route('/classificacao/<_competicao_>/<_edicao_>/<_grupo_>', methods=["GET"])
def r_classificacao(_competicao_, _edicao_, _grupo_):

    classificacao_ = pe.classificacao(competicao = pe.lista_competicoes[pe.lista_competicoes['codigo'] == _competicao_].reset_index().at[0, 'competicao'],
                                      ano = int(_edicao_),
                                      grupo = _grupo_, fase = 0, vitoria = 3, empate_sem_gols = 1, empate_com_gols = 1, clube = 0)    
    
    return jsonify(classificacao_.astype(str).to_dict('records'))






if __name__ == "__main__":
    app.run(debug=True)