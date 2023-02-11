import pandas as pd

lista_partidas = pd.read_excel('dados/dados.xlsx', sheet_name='Jogos')
lista_partidas['PARTIDA_DATA'] = pd.to_datetime(lista_partidas['PARTIDA_DATA']).dt.date
lista_clubes = pd.read_excel('dados/dados.xlsx', sheet_name='Clubes')
lista_estadios = pd.read_excel('dados/dados.xlsx', sheet_name='Estádios')
lista_observacoes = pd.read_excel('dados/dados.xlsx', sheet_name='Observações')
lista_jogadores = pd.read_excel('dados/dados.xlsx', sheet_name='Jogadores')
lista_gols = pd.read_excel('dados/dados.xlsx', sheet_name='Artilharia')


lista_campeoes = pd.read_excel('dados/dados.xlsx', sheet_name='Campeões')
lista_colocacoes = pd.read_excel('dados/dados.xlsx', sheet_name='Posições')
lista_mundanca_clube = pd.read_excel('dados/dados.xlsx', sheet_name='Mudanças')
lista_competicoes = pd.read_excel('dados/dados.xlsx', sheet_name='Competições')


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

def gp(value):
    if pd.isna(value):
        return 0
    elif isinstance(value, float):
        return str(int(value))
    else:
        return value

def gp_gc(value):
    if pd.isna(value):
        return 0
    elif isinstance(value, float):
        return str(int(value))
    else:
        return value

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
            'V': lista_partidas['V'].astype(int),
            'E': lista_partidas['E'].astype(int),
            'D': lista_partidas['D'].astype(int),
            'GP': lista_partidas['GC'].astype(int),
            'GC': lista_partidas['GP'].astype(int),
            'SALDO': lista_partidas['GC'].astype(int) - lista_partidas['GP'].astype(int),
    }) 

    classificacao = pd.concat([clasf1, clasf2])

    classificacao.loc[classificacao['GP'] > classificacao['GC'], 'PTS'] = vitoria
    classificacao.loc[classificacao['GP'] < classificacao['GC'], 'PTS'] = 0
    classificacao.loc[(classificacao['GP'] == classificacao['GC']) & (classificacao['GP'] + classificacao['GC'] == 0), 'PTS'] = empate_sem_gols
    classificacao.loc[(classificacao['GP'] == classificacao['GC']) & (classificacao['GP'] + classificacao['GC'] > 0), 'PTS'] = empate_com_gols

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


def participacoes(ano, competicao):

    lista_mandantes = lista_partidas[['PARTIDA_MANDANTE', 'PARTIDA_ANO', 'PARTIDA_COMPETICAO']].groupby(['PARTIDA_MANDANTE', 'PARTIDA_ANO', 'PARTIDA_COMPETICAO']).sum().reset_index()
    lista_mandantes.columns = ['CLUBE', 'ANO', 'COMPETICAO']
    lista_visitantes = lista_partidas[['PARTIDA_VISITANTE', 'PARTIDA_ANO', 'PARTIDA_COMPETICAO']].groupby(['PARTIDA_VISITANTE', 'PARTIDA_ANO', 'PARTIDA_COMPETICAO']).sum().reset_index()
    lista_visitantes.columns = ['CLUBE', 'ANO', 'COMPETICAO']
    participacoes = pd.concat([lista_mandantes, lista_visitantes])
    participacoes = participacoes[participacoes['COMPETICAO'] == competicao].groupby(['CLUBE', 'ANO']).sum(numeric_only=True).reset_index()
    clubes_participacoes = participacoes[participacoes['ANO'] <= ano]

    n_participacoes = pd.DataFrame(clubes_participacoes['CLUBE'].value_counts()).reset_index()
    n_participacoes.columns = ['CLUBE', 'PARTICIPACOES']

    participantes = pd.merge(left=clubes_participacoes, right=n_participacoes, on='CLUBE', how='left')
    participantes = participantes[participantes['ANO'] == ano]
    participantes = participantes[['CLUBE', 'PARTICIPACOES', 'ANO']]

    participantes = pd.merge(left=participantes, right=lista_clubes, on='CLUBE', how='left').sort_values(['CLUBE'])
    participantes = pd.merge(left=participantes, right=lista_mundanca_clube, left_on='CLUBE_NOME_COMPLETO', right_on='MUDANCA_NOME_ATUAL', how='left').fillna('')


    return participantes








