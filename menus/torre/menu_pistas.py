from services.pista_service import PistaService
from services.torre_service import verificar_ocupacao_pista

PISTAS_RESERVADAS = set()


def exibir_menu_pistas(aeroporto_ativo=None):
    cabecalho = (
        f"PISTAS - {aeroporto_ativo.ident} ({aeroporto_ativo.name})"
        if aeroporto_ativo
        else "GERENCIAMENTO DE PISTAS"
    )
    opcao = input(f"""
=========================================
  {cabecalho}
=========================================

1 - Ver pistas disponíveis
2 - Reservar pista
3 - Liberar pista
4 - Ver fila de aeronaves
5 - Ver pistas ocupadas

0 - Voltar

=========================================
Escolha uma opção: """).strip()
    return opcao


def _obter_pistas_alvo(service, aeroporto_ativo=None):
    if aeroporto_ativo is not None:
        return service.buscar_por_aeroporto(aeroporto_ativo.ident), aeroporto_ativo.ident

    icao = input("Código ICAO do aeroporto (ex: SBGR): ").strip().upper()
    if not icao:
        return [], None
    return service.buscar_por_aeroporto(icao), icao


def visualizar_pistas_disponiveis(aeroporto_ativo=None):

    service = PistaService()
    pistas, icao = _obter_pistas_alvo(service, aeroporto_ativo)
    if not pistas:
        print(f"\nNenhuma pista cadastrada para {icao or 'o aeroporto informado'}.")
        return

    print(f"\n--- PISTAS EM {icao} ---")
    for p in pistas:
        if p.closed:
            status = "Fechada"
        elif p.id in PISTAS_RESERVADAS:
            status = "Reservada"
        else:
            status = "Aberta"
        print(f"  ID: {p.id} | {p.ident} | {p.length_ft}ft | {p.surface} | {status}")


def reservar_pista():

    try:
        id_pista = int(input("ID da pista a reservar: "))
    except ValueError:
        print("ID inválido.")
        return

    service = PistaService()
    pista = service.buscar_por_id(id_pista)
    if not pista:
        print("Pista não encontrada.")
        return
    if pista.closed:
        print(f"A pista {pista.ident} ({pista.airport_ident}) está fechada e não pode ser reservada.")
        return
    if id_pista in PISTAS_RESERVADAS:
        print(f"A pista {pista.ident} ({pista.airport_ident}) já está reservada.")
        return

    PISTAS_RESERVADAS.add(id_pista)
    print(f"Pista {pista.ident} ({pista.airport_ident}) reservada com sucesso.")


def liberar_pista():

    try:
        id_pista = int(input("ID da pista a liberar: "))
    except ValueError:
        print("ID inválido.")
        return

    service = PistaService()
    pista = service.buscar_por_id(id_pista)
    if not pista:
        print("Pista não encontrada.")
        return

    PISTAS_RESERVADAS.discard(id_pista)
    print(f"Pista {pista.ident} ({pista.airport_ident}) liberada.")


def visualizar_fila_aeronaves():

    print("\nFuncionalidade em desenvolvimento...")


def visualizar_pistas_ocupadas(aeroporto_ativo=None):

    service = PistaService()
    pistas, icao = _obter_pistas_alvo(service, aeroporto_ativo)
    if not pistas:
        print(f"\nNenhuma pista cadastrada para {icao or 'o aeroporto informado'}.")
        return

    print(f"\n--- STATUS DAS PISTAS EM {icao} (TEMPO REAL) ---")
    for p in pistas:
        ocupantes, erro = verificar_ocupacao_pista(p.le_lat, p.le_lon)
        if erro:
            print(f"  Pista {p.ident}: erro ao verificar - {erro}")
        elif ocupantes is None:
            print(f"  Pista {p.ident}: sem dados")
        elif not ocupantes:
            print(f"  Pista {p.ident}: livre")
        else:
            print(f"  Pista {p.ident}: ocupada por {len(ocupantes)} aeronave(s)")
            for v in ocupantes:
                print(f"    - {v['callsign']} a {v['dist']:.2f} km, alt {v['baro_altitude']} m")


def gerenciar_pistas(aeroporto_ativo=None):

    while True:
        opcao = exibir_menu_pistas(aeroporto_ativo)
        if opcao == '1':
            visualizar_pistas_disponiveis(aeroporto_ativo)
        elif opcao == '2':
            reservar_pista()
        elif opcao == '3':
            liberar_pista()
        elif opcao == '4':
            visualizar_fila_aeronaves()
        elif opcao == '5':
            visualizar_pistas_ocupadas(aeroporto_ativo)
        elif opcao == '0':
            break
        else:
            print("\nOpção inválida.")
        input("\nPressione Enter para continuar...")