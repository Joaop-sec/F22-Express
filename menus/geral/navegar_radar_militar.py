from menus.torre.menu_radar_militar import exibir_menu_radar_militar
from services.radar_militar_service import RadarMilitarService


def _imprimir_tabela_tatica(df, aeroporto_ativo=None):
    if df.empty:
        print("\n[RADAR] Nenhum alvo militar ou alerta identificado no setor.")
        return

    print(f"\n[RADAR] Alvos detectados: {len(df)}")
    print("-" * 95)

    colunas = ["callsign", "icao24", "origin_country", "altitude_ft", "velocidade_kt", "classificacao"]
    if aeroporto_ativo is not None and "dist_km" in df.columns:
        colunas = ["callsign", "dist_km", "rumo", "altitude_ft", "velocidade_kt", "origin_country", "classificacao"]

    colunas_validas = [c for c in colunas if c in df.columns]
    print(df[colunas_validas].to_string(index=False))
    print("-" * 95)


def navegar_radar_militar(aeroporto_ativo=None):
    radar = RadarMilitarService()

    while True:
        opcao = exibir_menu_radar_militar(aeroporto_ativo)

        if opcao == '1':
            df, erro = radar.varredura_militar(aeroporto=aeroporto_ativo)
            if erro:
                print(f"\nErro no radar: {erro}")
            else:
                _imprimir_tabela_tatica(df, aeroporto_ativo)

        elif opcao == '2':
            if aeroporto_ativo is None:
                print("\nSelecione um aeroporto na Torre de Controle antes de usar o radar de proximidade.")
            else:
                try:
                    raio = float(input("Raio de varredura em km (ex: 300): ").strip())
                except ValueError:
                    print("Raio inválido.")
                    continue
                df, erro = radar.varredura_militar(aeroporto=aeroporto_ativo, raio_km=raio)
                if erro:
                    print(f"\nErro no radar: {erro}")
                else:
                    print(f"\nVarredura num raio de {raio:.0f} km de {aeroporto_ativo.ident}:")
                    _imprimir_tabela_tatica(df, aeroporto_ativo)

        elif opcao == '3':
            pais = input("Digite o país em inglês (ex: Brazil, United States): ").strip()
            df, erro = radar.varredura_militar(aeroporto=aeroporto_ativo)
            if erro:
                print(f"\nErro no radar: {erro}")
            elif not df.empty:
                filtrado = df[df["origin_country"].str.contains(pais, case=False, na=False)]
                _imprimir_tabela_tatica(filtrado, aeroporto_ativo)

        elif opcao == '4':
            df, erro = radar.varredura_militar(aeroporto=aeroporto_ativo)
            if erro:
                print(f"\nErro no radar: {erro}")
            elif not df.empty:
                alertas = df[df["classificacao"].str.startswith("SQUAWK", na=False)]
                _imprimir_tabela_tatica(alertas, aeroporto_ativo)

        elif opcao == '5':
            termo = input("Digite o Callsign ou ICAO24 do alvo: ").strip().upper()
            df, erro = radar.varredura_militar(aeroporto=aeroporto_ativo)
            if erro:
                print(f"\nErro no radar: {erro}")
            elif not df.empty:
                alvo = df[
                    (df["callsign"].astype(str).str.strip().str.upper() == termo)
                    | (df["icao24"].astype(str).str.strip().str.upper() == termo)
                ]
                if alvo.empty:
                    print(f"\nAlvo '{termo}' não encontrado no radar militar.")
                else:
                    for _, r in alvo.iterrows():
                        print("\n--- FICHA TELEMÉTRICA DO ALVO ---")
                        print(f"Callsign     : {str(r['callsign']).strip()}")
                        print(f"ICAO24       : {r['icao24']}")
                        print(f"País         : {r['origin_country']}")
                        print(f"Classificação: {r['classificacao']}")
                        print(f"Posição      : Lat {r['latitude']}, Lon {r['longitude']}")
                        print(f"Altitude     : {r['altitude_ft']} ft ({r['baro_altitude']} m)")
                        print(f"Velocidade   : {r['velocidade_kt']} kt")
                        print(f"Rumo aeronave: {r['heading']}°")
                        print(f"Em solo      : {'Sim' if r['on_ground'] else 'Não'}")
                        if aeroporto_ativo is not None and "dist_km" in r:
                            print(f"Distância    : {r['dist_km']} km de {aeroporto_ativo.ident} (Marcação {r['rumo']})")

        elif opcao == '0':
            break

        else:
            print("Opção inválida!")

        input("\nPressione Enter para continuar...")