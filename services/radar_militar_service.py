import math
import pandas as pd
from services.opensky_service import OpenSkyService
from services.torre_service import haversine

PREFIXOS_MILITARES = (
    "FAB", "FORCA", "RCH", "REACH", "AF1", "AF2", "SAM",
    "NAVY", "ARMY", "CNV", "PAT", "GAF", "RFR", "RRR",
    "ASY", "CFC", "IAM", "NATO", "LAGR",
)

SQUAWKS_ESPECIAIS = {
    "7500": "INTERFERÊNCIA ILÍCITA (SEQUESTRO)",
    "7600": "FALHA DE COMUNICAÇÃO",
    "7700": "EMERGÊNCIA GERAL",
    "7777": "OPERAÇÃO MILITAR / INTERCEPTAÇÃO",
}


def calcular_rumo(lat1: float, lon1: float, lat2: float, lon2: float) -> tuple[float, str]:
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dlon = math.radians(lon2 - lon1)

    y = math.sin(dlon) * math.cos(phi2)
    x = math.cos(phi1) * math.sin(phi2) - math.sin(phi1) * math.cos(phi2) * math.cos(dlon)
    graus = (math.degrees(math.atan2(y, x)) + 360) % 360

    setores = ["N", "NE", "L", "SE", "S", "SO", "O", "NO"]
    indice = round(graus / 45) % 8
    return graus, setores[indice]


class RadarMilitarService:
    def _classificar_alvo(self, row) -> str | None:
        callsign = str(row.get("callsign") or "").strip().upper()
        squawk = str(row.get("squawk") or "").strip()

        if squawk in SQUAWKS_ESPECIAIS:
            return f"SQUAWK {squawk} ({SQUAWKS_ESPECIAIS[squawk]})"

        if any(callsign.startswith(pref) for pref in PREFIXOS_MILITARES):
            return "INDICATIVO MILITAR"

        return None

    def varredura_militar(self, aeroporto=None, raio_km: float | None = None):
        with OpenSkyService() as service:
            resultado = service.buscar_voos()

        if not resultado.success:
            return None, resultado.error

        df = resultado.data
        if df.empty:
            return pd.DataFrame(), None

        df = df.copy()
        df["classificacao"] = df.apply(self._classificar_alvo, axis=1)
        df_mil = df[df["classificacao"].notna()].copy()

        if df_mil.empty:
            return df_mil, None

        df_mil["altitude_ft"] = df_mil["baro_altitude"].apply(
            lambda m: round(m * 3.28084) if pd.notna(m) else None
        )
        df_mil["velocidade_kt"] = df_mil["velocity"].apply(
            lambda v: round(v * 1.94384) if pd.notna(v) else None
        )

        if aeroporto is not None:
            distancias = []
            direcoes = []
            for _, row in df_mil.iterrows():
                if pd.notna(row["latitude"]) and pd.notna(row["longitude"]):
                    d = haversine(
                        aeroporto.latitude,
                        aeroporto.longitude,
                        row["latitude"],
                        row["longitude"],
                    )
                    graus, cardeal = calcular_rumo(
                        aeroporto.latitude,
                        aeroporto.longitude,
                        row["latitude"],
                        row["longitude"],
                    )
                    distancias.append(round(d, 1))
                    direcoes.append(f"{int(graus):03d}° ({cardeal})")
                else:
                    distancias.append(None)
                    direcoes.append("-")

            df_mil["dist_km"] = distancias
            df_mil["rumo"] = direcoes

            if raio_km is not None:
                df_mil = df_mil[df_mil["dist_km"].notna() & (df_mil["dist_km"] <= raio_km)]

            df_mil = df_mil.sort_values(by="dist_km", na_position="last")

        return df_mil, None