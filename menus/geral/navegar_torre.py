from menus.torre.menu_torre import (
    exibir_menu_torre,
    selecionar_aeroporto,
    monitorar_voos,
    gerenciar_pistas,
    rastrear_militares,
)


def navegar_torre():
    aeroporto_ativo = None

    while True:
        opcao = exibir_menu_torre(aeroporto_ativo)

        if opcao == '1':
            novo = selecionar_aeroporto()
            if novo is not None:
                aeroporto_ativo = novo

        elif opcao == '2':
            monitorar_voos()

        elif opcao == '3':
            gerenciar_pistas(aeroporto_ativo)

        elif opcao == '4':
            rastrear_militares(aeroporto_ativo)

        elif opcao == '0':
            break

        else:
            print("Opção inválida!")