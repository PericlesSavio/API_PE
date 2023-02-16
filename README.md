# API_PE
API com os dados históricos do futebol pernambucano.

### Endpoints

* [/jogos/<_competicao_>/<_edicao_>](/jogos/ne/1994)
* [/ficha_jogos/<_competicao_>/<_edicao_>](/ficha_jogos/ne/1994)
* [/classificacao/<_competicao_>](/classificacao/ne)
* [/classificacao/<_competicao_>/<_edicao_>](/classificacao/ne/1994)
* [/classificacao/<_competicao_>/<_edicao_>/<_grupo_>](/classificacao/ne/1994/A)
* [/participantes/<_competicao_>/<_edicao_>](/participantes/ne/1994)

```json
{
    "PARTIDA_ID": "2014-04-02_sport-pe_ceara-ce",
    "PARTIDA_ANO": "2014",
    "PARTIDA_COMPETICAO": "Copa do Nordeste",
    "PARTIDA_DATA": "2014-04-02",
    "PARTIDA_HORARIO": "22:00",
    "PARTIDA_GRUPO": "",
    "PARTIDA_FASE": "Final",
    "PARTIDA_RODADA": "Ida",
    "PARTIDA_MANDANTE": "Sport-PE",
    "PARTIDA_MANDANTE_GOL": "2",
    "PARTIDA_VISITANTE_GOL": "0",
    "PARTIDA_VISITANTE": "Ceará-CE",
    "PARTIDA_LOCAL": "Ilha do Retiro",
    "PARTIDA_CONFRONTO1": "Sport-PE_Ceará-CE",
    "PARTIDA_CONFRONTO2": "Ceará-CE_Sport-PE",
    "ESTADIO_ID": "ilhadoretiro",
    "CLUBE_MANDANTE_ID": "sport-pe",
    "CLUBE_VISITANTE_ID": "ceara-ce",
    "PARTIDA_DADOS": [
      {
        "PARTIDA_ID": "2014-04-02_sport-pe_ceara-ce",
        "JOGADOR_ID": "neto-baiano_1982-09-17",
        "JOGADOR_ALCUNHA": "Neto Baiano",
        "JOGADOR_CLUBE": "Sport-PE",
        "JOGADOR_GOL_TEMPO": "1T",
        "JOGADOR_GOL_MIN": "11min",
        "JOGADOR_GOL_TIPO": "Gol"
      },
      {
        "PARTIDA_ID": "2014-04-02_sport-pe_ceara-ce",
        "JOGADOR_ID": "danilo-barcelos_1991-08-17",
        "JOGADOR_ALCUNHA": "Danilo Barcelos",
        "JOGADOR_CLUBE": "Sport-PE",
        "JOGADOR_GOL_TEMPO": "2T",
        "JOGADOR_GOL_MIN": "41min",
        "JOGADOR_GOL_TIPO": "Gol"
      }
    ]
  }
```
