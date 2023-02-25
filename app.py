from flask import Flask, jsonify, render_template, request
import pandas as pd
import funcoes as pe
import markdown


app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False



@app.route("/")
def index():    
    with open("README.md", "r", encoding='utf-8') as f:
        content = f.read()        
    html = markdown.markdown(content, extensions=['fenced_code'])    
    return render_template("index.html", content=html)



@app.route('/jogos/<_competicao_>/<int:_edicao_>', methods=["GET"])
def r_partidas(_competicao_, _edicao_):
    partidas_ = pe.partidas_1(competicao = pe.codigo_competicao(_competicao_), ano = _edicao_, grupo = 0, fase = 0, rodada = 0, id_jogo = 0)
    return jsonify(partidas_.to_dict('records'))



@app.route('/ficha_jogos/<_competicao_>/<int:_edicao_>', methods=["GET"])
@app.route('/ficha_jogos/<_competicao_>/<int:_edicao_>/<_grupo_>', methods=["GET"])
@app.route('/ficha_jogos/<_competicao_>/<int:_edicao_>/<_grupo_>/<_fase_>/', methods=["GET"])
def r_ficha_jogo(_competicao_, _edicao_, _grupo_ = 0, _fase_ = 0, _rodada_ = 0, _id_jogo_ = 0):
    partidas_ = pe.partidas_1_completo(competicao = pe.codigo_competicao(_competicao_), ano = _edicao_, grupo = _grupo_, fase = _fase_, rodada = _rodada_, id_jogo = _id_jogo_)
    return jsonify(partidas_)



@app.route('/classificacao/<_competicao_>/', methods=["GET"])
@app.route('/classificacao/<_competicao_>/<int:_edicao_>/', methods=["GET"])
@app.route('/classificacao/<_competicao_>/<int:_edicao_>/<_grupo_>/', methods=["GET"])
@app.route('/classificacao/<_competicao_>/<int:_edicao_>/<_grupo_>/<_fase_>', methods=["GET"])
def r_classificacao_grupo(_competicao_, _edicao_ = 0, _grupo_ = 0, _fase_ = 0):
    competicao = pe.codigo_competicao(_competicao_)
    pts_vitoria = pe.pts_competicao(_competicao_, _edicao_).reset_index().at[0, 'COMPETICAO_PTS_VITORIA']
    pts_empate_sem_gols = pe.pts_competicao(_competicao_, _edicao_).reset_index().at[0, 'COMPETICAO_PTS_EMPATE_SEM_GOLS']
    pts_empate_com_gols = pe.pts_competicao(_competicao_, _edicao_).reset_index().at[0, 'COMPETICAO_PTS_EMPATE_COM_GOLS']
    classificacao_ = pe.classificacao(competicao = competicao,
                                      ano = _edicao_, grupo = _grupo_, fase = _fase_, vitoria = pts_vitoria,
                                      empate_sem_gols = pts_empate_sem_gols, empate_com_gols = pts_empate_com_gols, clube = 0)
    return jsonify(classificacao_.to_dict('records'))



@app.route('/participantes/<_competicao_>/', methods=["GET"])
@app.route('/participantes/<_competicao_>/<int:_edicao_>/', methods=["GET"])
def r_clubes_participantes(_competicao_, _edicao_ = 0):
    dados_participacoes_ = pe.participacoes(competicao = pe.codigo_competicao(_competicao_), ano = _edicao_)
    return jsonify(dados_participacoes_.to_dict('records'))



@app.route('/campeoes/<_competicao_>/', methods=["GET"])
@app.route('/campeoes/<_competicao_>/<int:_edicao_>/', methods=["GET"])
def r_campeoes(_competicao_ = 0, _edicao_ = 0):
    campeoes_ = pe.campeoes(competicao = pe.codigo_competicao(_competicao_), ano = _edicao_)
    return jsonify(campeoes_.to_dict('records'))



@app.route('/colocacao/<_competicao_>/<int:_edicao_>/', methods=["GET"])
def r_colocacao(_competicao_ = 0, _edicao_ = 0):
    colocacao_ = pe.colocacao(competicao = pe.codigo_competicao(_competicao_), ano = _edicao_)
    return jsonify(colocacao_.to_dict('records'))



@app.route('/grupos_cruzados/<_competicao_>/<int:_edicao_>/<_grupo_>/', methods=["GET"])
def r_grupos_cruzados(_competicao_ = 0, _edicao_ = 0, _grupo_ = 0):
    grupos_cruzados_ = pe.grupos_cruzados(competicao = pe.codigo_competicao(_competicao_), ano = _edicao_, grupo = _grupo_)
    return jsonify(grupos_cruzados_.to_dict('records'))



@app.route('/segundos_colocados/<_competicao_>/<int:_edicao_>/', methods=["GET"])
def r_segundos_colocados(_competicao_ = 0, _edicao_ = 0, _grupo_ = 0):
    segundos_colocados_ = pe.segundos_colocados(competicao = pe.codigo_competicao(_competicao_), ano = _edicao_)
    return jsonify(segundos_colocados_.to_dict('records'))




@app.route('/clube/<_clube_>/', methods=["GET"])
def r_clube(_clube_):
    clube_ = pe.lista_clubes[pe.lista_clubes['CLUBE_ID'] == _clube_]
    return jsonify(clube_.to_dict('records'))




@app.errorhandler(404)
def page_not_found(error):
    return 'ERRO 404', 404





if __name__ == "__main__":
    app.run(debug=True, port=8080)