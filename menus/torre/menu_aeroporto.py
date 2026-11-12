def exibir_menu_aeroporto():
    opcao = input("""
=========================================
        SELEÇÃO DE AEROPORTO (TORRE)
=========================================
1 - Buscar por código ICAO ou IATA (ex: SBGR, GRU)
2 - Buscar por nome ou cidade
3 - Listar principais aeroportos do Brasil
0 - Voltar
=========================================

Escolha uma opção: """).strip()
    return opcao