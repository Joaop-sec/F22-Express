from menus.torre.menu_pistas import exibir_menu_pistas
from services.pista_service import PistaService
from services.torre_service import verificar_ocupacao_pista


def gerenciar_pistas(aeroporto_ativo=None):
    service = PistaService()

    while True:
        opcao = exibir_menu_pistas(aeroporto_ativo)

        if opcao == '1':
            icao = (
                aeroporto_ativo.ident
                if aeroporto_ativo is not None
                else input("Código ICAO do aeroporto (ex: SBGR): ").strip().upper()
            )
            pistas = service.buscar_por_aeroporto(icao)
            if not pistas:
                print("Nenhuma pista encontrada para esse aeroporto.")
            else:
                print(f"\nPistas em {icao}:")
                for p in pistas:
                    status = "Fechada" if p.closed else "Aberta"
                    print(f"  ID: {p.id} | {p.ident} | {p.length_ft}ft | {p.surface} | {status}")

        elif opcao == '2':
            try:
                id_pista = int(input("ID da pista: "))
            except ValueError:
                print("ID inválido.")
                continue

            pista = service.buscar_por_id(id_pista)
            if not pista:
                print("Pista não encontrada.")
                continue

            ocupantes, erro = verificar_ocupacao_pista(pista.le_lat, pista.le_lon)
            if erro:
                print(f"Erro: {erro}")
            elif ocupantes is None:
                print("Não foi possível verificar a ocupação.")
            elif not ocupantes:
                print(f"Pista {pista.ident} ({pista.airport_ident}) livre.")
            else:
                print(f"\nPista {pista.ident} ocupada por {len(ocupantes)} aeronave(s):")
                for v in ocupantes:
                    print(f"  {v['callsign']} | dist: {v['dist']:.2f} km | alt: {v['baro_altitude']} m | solo: {v['on_ground']}")

        elif opcao == '3':
            if aeroporto_ativo is None:
                print("Selecione um aeroporto primeiro na Torre de Controle.")
                continue

            pistas = service.buscar_por_aeroporto(aeroporto_ativo.ident)
            if not pistas:
                print("Nenhuma pista encontrada para esse aeroporto.")
                continue

            print(f"\n--- STATUS DAS PISTAS EM {aeroporto_ativo.ident} ---")
            for p in pistas:
                ocupantes, erro = verificar_ocupacao_pista(p.le_lat, p.le_lon)
                if erro:
                    print(f"  Pista {p.ident}: erro - {erro}")
                elif ocupantes is None:
                    print(f"  Pista {p.ident}: sem dados")
                elif not ocupantes:
                    print(f"  Pista {p.ident}: LIVRE")
                else:
                    print(f"  Pista {p.ident}: OCUPADA por {len(ocupantes)} aeronave(s)")
                    for v in ocupantes:
                        print(f"    - {v['callsign']} | dist: {v['dist']:.2f} km | alt: {v['baro_altitude']} m | solo: {v['on_ground']}")

        elif opcao == '0':
            break

        else:
            print("Opção inválida!")