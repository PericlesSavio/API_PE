import pandas as pd

lista_jogos = pd.read_excel('dados/dados.xlsx', sheet_name='Jogos')
lista_jogos['data'] = pd.to_datetime(lista_jogos['data']).dt.date
lista_clubes = pd.read_excel('dados/dados.xlsx', sheet_name='Clubes')
lista_campeoes = pd.read_excel('dados/dados.xlsx', sheet_name='Campeões')
#lista_artilharia = pd.read_excel('dados/dados.xlsx', sheet_name='Artilharia')
lista_jogadores = pd.read_excel('dados/dados.xlsx', sheet_name='Jogadores')
lista_gols = pd.read_excel('dados/dados.xlsx', sheet_name='Artilharia')
lista_estadios = pd.read_excel('dados/dados.xlsx', sheet_name='Estádios')
lista_observacoes = pd.read_excel('dados/dados.xlsx', sheet_name='Observações')
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
    if row['gol_m'] > row['gol_v']:
        return 1
    else:
        return 0

def e(row):
    if row['gol_m'] == row['gol_v']:
        return 1
    else:
        return 0

def d(row):
    if row['gol_m'] < row['gol_v']:
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

lista_jogos['gol_m_str'] = lista_jogos['gol_m'].apply(gol_string)
lista_jogos['gol_v_str'] = lista_jogos['gol_v'].apply(gol_string)
lista_jogos['j'] = 1
lista_jogos['v'] = lista_jogos.apply(v, axis=1)
lista_jogos['e'] = lista_jogos.apply(e, axis=1)
lista_jogos['d'] = lista_jogos.apply(d, axis=1)
lista_jogos['gp'] = lista_jogos['gol_m'].apply(gp_gc)
lista_jogos['gc'] = lista_jogos['gol_v'].apply(gp_gc)



def partidas_1(competicao = 0, ano = 0, grupo = 0, fase = 0, rodada = 0, id_jogo = 0):
    partidas = pd.merge(left=lista_jogos, right=lista_estadios, left_on='local', right_on='estadio', how='left')
    partidas = partidas.drop(['gol_m', 'gol_v', 'j', 'v', 'e', 'd', 'gp', 'gc', 'completo', 'estadio', 'capacidade', 'cidade', 'estado',
                              'data_inauguracao', 'partida_inauguracao', ], axis=1)

    partidas = partidas[partidas['competicao'] == competicao] if competicao != 0 else partidas
    partidas = partidas[partidas['ano'] == ano] if ano != 0 else partidas    
    partidas = partidas[partidas['grupo'] == grupo] if grupo != 0 else partidas
    partidas = partidas[partidas['fase'] == fase] if fase != 0 else partidas
    partidas = partidas[partidas['id_jogo'].str.contains(id_jogo)] if id_jogo != 0 else partidas
    partidas = partidas[partidas['rodada'] == rodada] if rodada != 0 else partidas    

    partidas = pd.merge(left=partidas, right=lista_clubes, left_on='mandante', right_on='clube', how='left')
    partidas = partidas.drop(['completo', 'clube', 'fundacao', 'cidade', 'estado'], axis=1)
    partidas = pd.merge(left=partidas, right=lista_clubes, left_on='visitante', right_on='clube', how='left')
    partidas = partidas.drop(['completo', 'clube', 'fundacao', 'cidade', 'estado'], axis=1)

    partidas = partidas.rename(columns={"slug_clube_x": "slug_clube_m", "slug_clube_y": "slug_clube_v"})
    partidas = partidas.where(pd.notnull(partidas), '')    
    partidas = partidas[['id_jogo', 'ano', 'competicao', 'data', 'horario', 'grupo', 'fase', 'rodada', 'mandante', 'gol_m_str', 'gol_v_str',
                         'visitante', 'local', 'confronto1', 'confronto2', 'slug_estadio', 'slug_clube_m', 'slug_clube_v']]

    return partidas

def partidas_2(competicao = 0, ano = 0, grupo = 0, fase = 0, clube = 0):
    jogos = pd.merge(left = lista_jogos, right = lista_observacoes, left_on='id_jogo', right_on='id_jogo', how='left')

    jogos = pd.DataFrame({
        'id': jogos['id_jogo'],
        'competição': jogos['competicao'],
        'ano': jogos['ano'],
        'data': jogos['data'],
        'horário': jogos['horario'],
        'grupo': jogos['grupo'],
        'fase': jogos['fase'],
        'rodada': jogos['rodada'],
        'mandante': jogos['mandante'],
        'placar': jogos['gol_m_str'] + '-' + jogos['gol_v_str'],
        'visitante': jogos['visitante'],
        'local': jogos['local'],
        'obs': jogos['obs'],
        'confronto1': jogos['confronto1'],
        'confronto2': jogos['confronto2']
    })    

    jogos = pd.merge(left=jogos, right=lista_estadios, left_on='local', right_on='estadio', how='left').drop(['completo', 'estadio', 'capacidade', 'cidade', 'estado', 'data_inauguracao', 'partida_inauguracao'], axis=1)

    jogos = jogos[jogos['competição'] == competicao] if competicao != 0 else jogos
    jogos = jogos[jogos['ano'] == ano] if ano != 0 else jogos    
    jogos = jogos[jogos['grupo'] == grupo] if grupo != 0 else jogos
    jogos = jogos[jogos['fase'] == fase] if fase != 0 else jogos
    jogos = jogos[jogos['id'].str.contains(clube)] if clube != 0 else jogos
    jogos = jogos.sort_values(['data'], ascending = [False]) if clube != 0 else jogos.sort_values(['data'], ascending = [True])

    mata_mata = pd.merge(left = jogos, right = jogos, left_on='confronto1', right_on='confronto2')
    mata_mata = mata_mata[mata_mata['rodada_x'] == 'Ida']
    mata_mata = mata_mata.where(pd.notnull(mata_mata), '')

    mata_mata2 = pd.DataFrame({
        'competição': mata_mata['competição_x'],
        'ano': mata_mata['ano_x'],
        'grupo': mata_mata['grupo_x'],
        'fase': mata_mata['fase_x'],

        'id_ida': mata_mata['id_x'],        
        'data_ida': mata_mata['data_x'],
        'horário_ida': mata_mata['horário_x'],        
        'rodada_ida': mata_mata['rodada_x'],
        'mandante_ida': mata_mata['mandante_x'],
        'placar_ida': mata_mata['placar_x'],
        'visitante_ida': mata_mata['visitante_x'],
        'local_ida': mata_mata['local_x'],
        'slug_local_ida': mata_mata['slug_estadio_x'],
        'obs_ida': mata_mata['obs_x'],

        'id_volta': mata_mata['id_y'],
        'data_volta': mata_mata['data_y'],
        'horário_volta': mata_mata['horário_y'],
        'rodada_volta': mata_mata['rodada_y'],
        'mandante_volta': mata_mata['mandante_y'],
        'placar_volta': mata_mata['placar_y'],
        'visitante_volta': mata_mata['visitante_y'],
        'local_volta': mata_mata['local_y'],
        'slug_local_volta': mata_mata['slug_estadio_y'],
        'obs_volta': mata_mata['obs_y']
    })    

    return mata_mata2

def classificacao(competicao = 0, ano = 0, grupo = 0, fase = 0, vitoria = 3, empate_sem_gols = 1, empate_com_gols = 1, clube = 0):
    clasf1 = pd.DataFrame({
        'id_jogo': lista_jogos['id_jogo'],
        'ano': lista_jogos['ano'],
        'competicao': lista_jogos['competicao'],
        'grupo': lista_jogos['grupo'],
        'fase': lista_jogos['fase'],
        'estadio': lista_jogos['local'],
        'clube': lista_jogos['mandante'],
        'pts': 0,
        'j': lista_jogos['j'].astype(int),
        'v': lista_jogos['v'].astype(int),
        'e': lista_jogos['e'].astype(int),
        'd': lista_jogos['d'].astype(int),
        'gp': lista_jogos['gp'].astype(int),
        'gc': lista_jogos['gc'].astype(int),
        'saldo': lista_jogos['gp'].astype(int) - lista_jogos['gc'].astype(int),
    })
    clasf2 = pd.DataFrame({
        'id_jogo': lista_jogos['id_jogo'],
        'ano': lista_jogos['ano'],
        'competicao': lista_jogos['competicao'],
        'grupo': lista_jogos['grupo'],
        'fase': lista_jogos['fase'],
        'estadio': lista_jogos['local'],
        'clube': lista_jogos['visitante'],
        'pts': 0,
        'j': lista_jogos['j'].astype(int),
        'v': lista_jogos['v'].astype(int),
        'e': lista_jogos['e'].astype(int),
        'd': lista_jogos['d'].astype(int),
        'gp': lista_jogos['gc'].astype(int),
        'gc': lista_jogos['gp'].astype(int),
        'saldo': lista_jogos['gc'].astype(int) - lista_jogos['gp'].astype(int),
    }) 

    classificacao = pd.concat([clasf1, clasf2])
    
    classificacao.loc[classificacao['gp'] > classificacao['gc'], 'pts'] = vitoria
    classificacao.loc[classificacao['gp'] < classificacao['gc'], 'pts'] = 0
    classificacao.loc[(classificacao['gp'] == classificacao['gc']) & (classificacao['gp'] + classificacao['gc'] == 0), 'pts'] = empate_sem_gols
    classificacao.loc[(classificacao['gp'] == classificacao['gc']) & (classificacao['gp'] + classificacao['gc'] > 0), 'pts'] = empate_com_gols
    
    classificacao = classificacao[classificacao['competicao'] == competicao] if competicao != 0 else classificacao
    classificacao = classificacao[classificacao['ano'] == ano] if ano != 0 else classificacao
    classificacao = classificacao[classificacao['grupo'] == grupo] if grupo != 0 else classificacao
    classificacao = classificacao[classificacao['fase'] == fase] if fase != 0 else classificacao
    classificacao = classificacao[classificacao['clube'].str.contains(clube)] if clube != 0 else classificacao
    classificacao = classificacao.sort_values(['pts', 'saldo'], ascending = [False, False])
    classificacao = classificacao.groupby(['clube']).sum().reset_index().sort_values(['pts', 'v', 'saldo', 'gp'], ascending = [False, False, False, False])
    classificacao = classificacao.drop(columns=['ano']).reset_index().drop('index', axis=1)
    
    classificacao.insert(0, 'pos', classificacao.index + 1)
    classificacao = pd.merge(left=classificacao, right=lista_clubes, left_on='clube', right_on='clube', how='left').drop(['completo', 'fundacao', 'cidade', 'estado'], axis=1)

    return classificacao




