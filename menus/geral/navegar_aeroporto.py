from menus.torre.menu_aeroporto import exibir_menu_aeroporto
from services.aeroporto_service import AeroportoService


def navegar_selecionar_aeroporto():
    service = AeroportoService()

    while True:
        opcao = exibir_menu_aeroporto()

        if opcao == '1':
            codigo = input("Digite o código ICAO ou IATA: ").strip()
            aeroporto = service.buscar_por_codigo(codigo)
            if aeroporto:
                print(f"\nAeroporto selecionado: {aeroporto.ident} ({aeroporto.iata_code or '-'}) - {aeroporto.name}")
                return aeroporto
            print("\nAeroporto não encontrado.")

        elif opcao == '2':
            termo = input("Digite o nome ou cidade: ").strip()
            resultados = service.buscar_por_termo(termo)
            if not resultados:
                print("\nNenhum aeroporto encontrado.")
                continue

            print("\n--- RESULTADOS ---")
            for idx, a in enumerate(resultados, start=1):
                iata = f" / {a.iata_code}" if a.iata_code else ""
                print(f"{idx} - [{a.ident}{iata}] {a.name} ({a.municipality} - {a.iso_country})")

            try:
                escolha = int(input("\nEscolha o número do aeroporto (0 para cancelar): "))
                if 1 <= escolha <= len(resultados):
                    selecionado = resultados[escolha - 1]
                    print(f"\nAeroporto selecionado: {selecionado.ident} - {selecionado.name}")
                    return selecionado
            except ValueError:
                print("Entrada inválida.")

        elif opcao == '3':
            principais = service.listar_destaques_brasil()
            if not principais:
                print("\nNenhum aeroporto brasileiro encontrado no banco.")
                continue

            print("\n--- PRINCIPAIS AEROPORTOS (BRASIL) ---")
            for idx, a in enumerate(principais, start=1):
                iata = f" / {a.iata_code}" if a.iata_code else ""
                print(f"{idx} - [{a.ident}{iata}] {a.name} ({a.municipality})")

            try:
                escolha = int(input("\nEscolha o número do aeroporto (0 para cancelar): "))
                if 1 <= escolha <= len(principais):
                    selecionado = principais[escolha - 1]
                    print(f"\nAeroporto selecionado: {selecionado.ident} - {selecionado.name}")
                    return selecionado
            except ValueError:
                print("Entrada inválida.")

        elif opcao == '0':
            return None

        else:
            print("\nOpção inválida!")