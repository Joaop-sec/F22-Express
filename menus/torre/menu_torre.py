from menus.geral.navegar_aeroporto import navegar_selecionar_aeroporto
from menus.torre.monitoramento import exibir_submenu_monitoramento
from menus.torre.menu_pistas import gerenciar_pistas
from menus.geral.navegar_radar_militar import navegar_radar_militar


def exibir_menu_torre(aeroporto_ativo=None):
    cabecalho_aero = (
        f"{aeroporto_ativo.ident} - {aeroporto_ativo.name}"
        if aeroporto_ativo
        else "Nenhum selecionado"
    )

    opcao = input(f"""
========================================
TORRE DE CONTROLE
Aeroporto: {cabecalho_aero}
========================================
1 - Selecionar aeroporto
2 - Monitorar voos
3 - Gerenciar pistas
4 - Área de radar militar
0 - Voltar
========================================

Escolha uma opção: """)
    return opcao


def selecionar_aeroporto():
    return navegar_selecionar_aeroporto()


def monitorar_voos():
    exibir_submenu_monitoramento()


def rastrear_militares(aeroporto_ativo=None):
    navegar_radar_militar(aeroporto_ativo)