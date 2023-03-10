import pandas as pd

lista_clubes = pd.read_excel('dados/dados.xlsx', sheet_name='Clubes')
lista_estadios = pd.read_excel('dados/dados.xlsx', sheet_name='Estádios')
lista_observacoes = pd.read_excel('dados/dados.xlsx', sheet_name='Observações')
lista_jogadores = pd.read_excel('dados/dados.xlsx', sheet_name='Jogadores')
lista_gols = pd.read_excel('dados/dados.xlsx', sheet_name='Artilharia')
lista_competicoes = pd.read_excel('dados/dados.xlsx', sheet_name='Competições')
lista_competicoesdados = pd.read_excel('dados/dados.xlsx', sheet_name='Competições Dados')
lista_mundanca_clube = pd.read_excel('dados/dados.xlsx', sheet_name='Mudanças')
lista_campeoes = pd.read_excel('dados/dados.xlsx', sheet_name='Campeões')
lista_colocacoes = pd.read_excel('dados/dados.xlsx', sheet_name='Posições')
lista_gruposcruzados = pd.read_excel('dados/dados.xlsx', sheet_name='Grupos Cruzados')
lista_segundoscolocados = pd.read_excel('dados/dados.xlsx', sheet_name='Segundos Colocados')
lista_ajustepts = pd.read_excel('dados/dados.xlsx', sheet_name='Ajustes Pontuação')


def codigo_competicao(_competicao_):
    return lista_competicoes[lista_competicoes['COMPETICAO_ID'] == _competicao_].reset_index().at[0, 'COMPETICAO']


def gol_string(value):
    if pd.isna(value):
        return ''
    elif isinstance(value, float):
        return str(int(value))
    else:
        return value   


def v(row):
    if row['PARTIDA_GOL_M'] > row['PARTIDA_GOL_V']:
        return 1
    else:
        return 0


def e(row):
    if row['PARTIDA_GOL_M'] == row['PARTIDA_GOL_V']:
        return 1
    else:
        return 0


def d(row):
    if row['PARTIDA_GOL_M'] < row['PARTIDA_GOL_V']:
        return 1
    else:
        return 0


def gp_gc(value):
    if pd.isna(value):
        return 0
    elif isinstance(value, float):
        return str(int(value))
    else:
        return value


lista_partidas = pd.read_excel('dados/dados.xlsx', sheet_name='Jogos')
lista_partidas['PARTIDA_DATA'] = lista_partidas['PARTIDA_DATA'].astype(str)
lista_partidas['PARTIDA_HORARIO'] = lista_partidas['PARTIDA_HORARIO'].astype(str)
#lista_partidas['PARTIDA_DATA'] = pd.to_datetime(lista_partidas['PARTIDA_DATA']).dt.date
lista_partidas['PARTIDA_GOL_M_STR'] = lista_partidas['PARTIDA_GOL_M'].apply(gol_string)
lista_partidas['PARTIDA_GOL_V_STR'] = lista_partidas['PARTIDA_GOL_V'].apply(gol_string)
lista_partidas['J'] = 1
lista_partidas['V'] = lista_partidas.apply(v, axis=1)
lista_partidas['E'] = lista_partidas.apply(e, axis=1)
lista_partidas['D'] = lista_partidas.apply(d, axis=1)
lista_partidas['GP'] = lista_partidas['PARTIDA_GOL_M'].apply(gp_gc)
lista_partidas['GC'] = lista_partidas['PARTIDA_GOL_V'].apply(gp_gc)


def partidas_1(competicao = 0, ano = 0, grupo = 0, fase = 0, rodada = 0, id_jogo = 0):
    partidas = pd.merge(left=lista_partidas, right=lista_estadios[['ESTADIO', 'ESTADIO_ID']], left_on='PARTIDA_LOCAL', right_on='ESTADIO', how='left')
    partidas = partidas.drop(['ESTADIO'], axis=1)

    partidas = partidas[partidas['PARTIDA_COMPETICAO'] == competicao] if competicao != 0 else partidas
    partidas = partidas[partidas['PARTIDA_ANO'] == ano] if ano != 0 else partidas    
    partidas = partidas[partidas['PARTIDA_GRUPO'] == grupo] if grupo != 0 else partidas
    partidas = partidas[partidas['PARTIDA_FASE'] == fase] if fase != 0 else partidas
    partidas = partidas[partidas['PARTIDA_ID'].str.contains(id_jogo)] if id_jogo != 0 else partidas
    partidas = partidas[partidas['PARTIDA_RODADA'] == rodada] if rodada != 0 else partidas 

    partidas = pd.merge(left=partidas, right=lista_clubes[['CLUBE', 'CLUBE_ID']], left_on='PARTIDA_MANDANTE', right_on='CLUBE', how='left')
    partidas = partidas.drop(['CLUBE'], axis=1)
    partidas = pd.merge(left=partidas, right=lista_clubes[['CLUBE', 'CLUBE_ID']], left_on='PARTIDA_VISITANTE', right_on='CLUBE', how='left')
    partidas = partidas.drop(['CLUBE'], axis=1)
    partidas = partidas.rename(columns={'CLUBE_ID_x': 'CLUBE_MANDANTE_ID', 'CLUBE_ID_y': 'CLUBE_VISITANTE_ID'})
    partidas = pd.merge(left=partidas, right=lista_observacoes, on='PARTIDA_ID', how='left')

    partidas = partidas.where(pd.notnull(partidas), '')

    partidas = partidas[['PARTIDA_ID', 'PARTIDA_ANO', 'PARTIDA_COMPETICAO', 'PARTIDA_DATA', 'PARTIDA_HORARIO', 'PARTIDA_GRUPO', 'PARTIDA_FASE', 'PARTIDA_RODADA',
                        'PARTIDA_MANDANTE', 'PARTIDA_GOL_M_STR', 'PARTIDA_GOL_V_STR', 'PARTIDA_VISITANTE', 'PARTIDA_LOCAL', 'PARTIDA_CONFRONTO1', 'PARTIDA_CONFRONTO2',
                        'ESTADIO_ID', 'CLUBE_MANDANTE_ID', 'CLUBE_VISITANTE_ID', 'PARTIDA_OBS']]
    
    partidas = partidas.rename(columns={'PARTIDA_GOL_M_STR': 'PARTIDA_MANDANTE_GOL', 'PARTIDA_GOL_V_STR': 'PARTIDA_VISITANTE_GOL'})

    return partidas



def partidas_1_completo(competicao = 0, ano = 0, grupo = 0, fase = 0, rodada = 0, id_jogo = 0):
    partidas = partidas_1(competicao, ano, grupo, fase, rodada, id_jogo).astype(str).to_dict('records')
    dados_gols = pd.merge(left=lista_gols, right=lista_jogadores, on='JOGADOR_ID', how='left')
    dados_gols = dados_gols.where(pd.notnull(dados_gols), '')
    dados_gols = dados_gols[['PARTIDA_ID', 'JOGADOR_ID', 'JOGADOR_ALCUNHA', 'JOGADOR_CLUBE', 'JOGADOR_GOL_TEMPO', 'JOGADOR_GOL_MIN', 'JOGADOR_GOL_TIPO']]

    for i in range(0, len(partidas)):
        partidas[i]['PARTIDA_DADOS'] = dados_gols[dados_gols['PARTIDA_ID'] == partidas[i]['PARTIDA_ID']].to_dict('records')
    return partidas



def classificacao(competicao = 0, ano = 0, grupo = 0, fase = 0, vitoria = 3, empate_sem_gols = 1, empate_com_gols = 1, clube = 0):
        clasf1 = pd.DataFrame({
            'PARTIDA_ID': lista_partidas['PARTIDA_ID'],
            'PARTIDA_ANO': lista_partidas['PARTIDA_ANO'],
            'PARTIDA_COMPETICAO': lista_partidas['PARTIDA_COMPETICAO'],
            'PARTIDA_GRUPO': lista_partidas['PARTIDA_GRUPO'],
            'PARTIDA_FASE': lista_partidas['PARTIDA_FASE'],
            'PARTIDA_ESTADIO': lista_partidas['PARTIDA_LOCAL'],
            'CLUBE': lista_partidas['PARTIDA_MANDANTE'],
            'PTS': 0,
            'J': lista_partidas['J'].astype(int),
            'V': lista_partidas['V'].astype(int),
            'E': lista_partidas['E'].astype(int),
            'D': lista_partidas['D'].astype(int),
            'GP': lista_partidas['GP'].astype(int),
            'GC': lista_partidas['GC'].astype(int),
            'SALDO': lista_partidas['GP'].astype(int) - lista_partidas['GC'].astype(int),
    })
        clasf2 = pd.DataFrame({
            'PARTIDA_ID': lista_partidas['PARTIDA_ID'],
            'PARTIDA_ANO': lista_partidas['PARTIDA_ANO'],
            'PARTIDA_COMPETICAO': lista_partidas['PARTIDA_COMPETICAO'],
            'PARTIDA_GRUPO': lista_partidas['PARTIDA_GRUPO'],
            'PARTIDA_FASE': lista_partidas['PARTIDA_FASE'],
            'PARTIDA_ESTADIO': lista_partidas['PARTIDA_LOCAL'],
            'CLUBE': lista_partidas['PARTIDA_VISITANTE'],
            'PTS': 0,
            'J': lista_partidas['J'].astype(int),
            'V': lista_partidas['D'].astype(int),
            'E': lista_partidas['E'].astype(int),
            'D': lista_partidas['V'].astype(int),
            'GP': lista_partidas['GC'].astype(int),
            'GC': lista_partidas['GP'].astype(int),
            'SALDO': lista_partidas['GC'].astype(int) - lista_partidas['GP'].astype(int),
    }) 

        classificacao = pd.concat([clasf1, clasf2])    
    
        for i in lista_ajustepts['AJUSTE_ID_PARTIDA']:
                for j in range(0,2):
                        clube_ajt = clube_ajuste(i, j).at[0, 'AJUSTE_CLUBE']
                        classificacao.loc[(classificacao['PARTIDA_ID'] == i) & (classificacao['CLUBE'] == clube_ajt), 'V'] = clube_ajuste(i, j).at[0, 'AJUSTE_VITORIA']
                        classificacao.loc[(classificacao['PARTIDA_ID'] == i) & (classificacao['CLUBE'] == clube_ajt), 'E'] = clube_ajuste(i, j).at[0, 'AJUSTE_EMPATE']
                        classificacao.loc[(classificacao['PARTIDA_ID'] == i) & (classificacao['CLUBE'] == clube_ajt), 'D'] = clube_ajuste(i, j).at[0, 'AJUSTE_DERROTA']
                        classificacao.loc[(classificacao['PARTIDA_ID'] == i) & (classificacao['CLUBE'] == clube_ajt), 'PTS'] = clube_ajuste(i, j).at[0, 'AJUSTE_PONTOS']
    
        classificacao.loc[classificacao['V'] == 1, 'PTS'] = vitoria + classificacao.loc[classificacao['V'] == 1, 'PTS']
        classificacao.loc[classificacao['D'] == 1, 'PTS'] = 0 + classificacao.loc[classificacao['D'] == 1, 'PTS']
        classificacao.loc[(classificacao['E'] == 1) & (classificacao['GP'] + classificacao['GC'] == 0), 'PTS'] = empate_sem_gols + classificacao.loc[(classificacao['E'] == 1) & (classificacao['GP'] + classificacao['GC'] == 0), 'PTS']
        classificacao.loc[(classificacao['E'] == 1) & (classificacao['GP'] + classificacao['GC'] > 0), 'PTS'] = empate_com_gols + classificacao.loc[(classificacao['E'] == 1) & (classificacao['GP'] + classificacao['GC'] > 0), 'PTS']

        classificacao = classificacao[classificacao['PARTIDA_COMPETICAO'] == competicao] if competicao != 0 else classificacao
        classificacao = classificacao[classificacao['PARTIDA_ANO'] == ano] if ano != 0 else classificacao
        classificacao = classificacao[classificacao['PARTIDA_GRUPO'] == grupo] if grupo != 0 else classificacao
        classificacao = classificacao[classificacao['PARTIDA_FASE'] == fase] if fase != 0 else classificacao
        classificacao = classificacao[classificacao['CLUBE'].str.contains(clube)] if clube != 0 else classificacao
        classificacao = classificacao.sort_values(['PTS', 'SALDO'], ascending = [False, False])
        classificacao = classificacao.groupby(['CLUBE']).sum(numeric_only=True).reset_index().sort_values(['PTS', 'V', 'SALDO', 'GP'], ascending = [False, False, False, False])
        classificacao = classificacao.drop(columns=['PARTIDA_ANO']).reset_index().drop('index', axis=1)
        classificacao.insert(0, 'POS', classificacao.index + 1)
        classificacao = pd.merge(left=classificacao, right=lista_clubes[['CLUBE', 'CLUBE_ID']], left_on='CLUBE', right_on='CLUBE', how='left') #.drop(['completo', 'fundacao', 'ESTADIO_CIDADE', 'ESTADIO_ESTADO'], axis=1)

        return classificacao


def participacoes(competicao = 0, ano = 0):
    lista_mandantes = lista_partidas[['PARTIDA_MANDANTE', 'PARTIDA_ANO', 'PARTIDA_COMPETICAO']].groupby(['PARTIDA_MANDANTE', 'PARTIDA_ANO', 'PARTIDA_COMPETICAO']).sum().reset_index()
    lista_mandantes.columns = ['CLUBE', 'ANO', 'COMPETICAO']
    lista_visitantes = lista_partidas[['PARTIDA_VISITANTE', 'PARTIDA_ANO', 'PARTIDA_COMPETICAO']].groupby(['PARTIDA_VISITANTE', 'PARTIDA_ANO', 'PARTIDA_COMPETICAO']).sum().reset_index()
    lista_visitantes.columns = ['CLUBE', 'ANO', 'COMPETICAO']
    participacoes = pd.concat([lista_mandantes, lista_visitantes])
    participacoes = participacoes[participacoes['COMPETICAO'] == competicao].groupby(['CLUBE', 'ANO']).sum(numeric_only=True).reset_index()

    clubes_participacoes = participacoes[participacoes['ANO'] <= ano] if ano != 0 else participacoes
    n_participacoes = pd.DataFrame(clubes_participacoes['CLUBE'].value_counts()).reset_index()
    n_participacoes.columns = ['CLUBE', 'PARTICIPACOES']

    participantes = pd.merge(left=clubes_participacoes, right=n_participacoes, on='CLUBE', how='left')
    participantes = participantes[participantes['ANO'] == ano] if ano != 0 else participantes
    participantes = participantes[['CLUBE', 'PARTICIPACOES', 'ANO']]
    participantes = pd.merge(left=participantes, right=lista_clubes, on='CLUBE', how='left').sort_values(['CLUBE'])
    participantes = pd.merge(left=participantes, right=lista_mundanca_clube, left_on='CLUBE_NOME_COMPLETO', right_on='MUDANCA_NOME_ATUAL', how='left').fillna('')

    if ano == 0:
        participantes = participantes.drop(columns=['ANO']).drop_duplicates()
    return participantes



def campeoes(competicao = 0, ano = 0):
    campeoes = lista_campeoes[lista_campeoes['COMPETICAO'] == competicao] if competicao != 0 else lista_campeoes
    campeoes = campeoes[campeoes['COMPETICAO_ANO'] == ano] if ano != 0 else campeoes
    return campeoes



def colocacao(competicao = 0, ano = 0):
    colocacoes = lista_colocacoes[lista_colocacoes['POSICAO_COMPETICAO'] == competicao] if competicao != 0 else lista_colocacoes
    colocacoes = lista_colocacoes[lista_colocacoes['POSICAO_ANO'] == ano] if ano != 0 else colocacoes
    return colocacoes



def grupos_cruzados(competicao = 0, ano = 0, grupo = 0):
    grupos_cruzados = lista_gruposcruzados[lista_gruposcruzados['GRUPOS-CRUZADOS_COMPETICAO'] == competicao] if competicao != 0 else lista_gruposcruzados
    grupos_cruzados = grupos_cruzados[grupos_cruzados['GRUPOS-CRUZADOS_ANO'] == ano] if ano != 0 else grupos_cruzados
    grupos_cruzados = grupos_cruzados[grupos_cruzados['GRUPOS-CRUZADOS_GRUPO'] == grupo]# if grupo != 0 else grupos_cruzados
    return grupos_cruzados



def segundos_colocados(competicao, ano):
    segundos_colocados = lista_segundoscolocados[lista_segundoscolocados['SEGUNDOS-COLOCADOS_COMPETICAO'] == competicao]
    segundos_colocados = segundos_colocados[segundos_colocados['SEGUNDOS-COLOCADOS_ANO'] == ano]
    return segundos_colocados



def pts_competicao(competicao, ano):
    competicoes_dados = lista_competicoesdados[lista_competicoesdados['COMPETICAO_ID'] == competicao]
    competicoes_dados = competicoes_dados[competicoes_dados['COMPETICAO_ANO'] == ano]
    return competicoes_dados



def clube_ajuste(id_jogo, indice):
        ajuste_pts = lista_ajustepts[lista_ajustepts['AJUSTE_ID_PARTIDA'] == id_jogo]
        ajuste_pts = ajuste_pts.iloc[[indice]]
        return ajuste_pts.reset_index().drop(['index'], axis=1)



