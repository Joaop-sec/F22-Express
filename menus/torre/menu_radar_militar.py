def exibir_menu_radar_militar(aeroporto_ativo=None):
    ref_texto = (
        f"{aeroporto_ativo.ident} ({aeroporto_ativo.municipality})"
        if aeroporto_ativo
        else "GLOBAL (Sem aeroporto base)"
    )

    opcao = input(f"""
==================================================
        ÁREA DE RADAR MILITAR & DEFESA AÉREA
        Referência: {ref_texto}
==================================================
1 - Varredura global de aeronaves militares
2 - Radar de proximidade (raio ao redor do aeroporto)
3 - Filtrar alvos por país de origem
4 - Monitorar alertas Squawk (7500 / 7600 / 7700 / 7777)
5 - Inspecionar alvo específico (Callsign ou ICAO24)
0 - Voltar
==================================================

Escolha uma opção: """).strip()
    return opcao