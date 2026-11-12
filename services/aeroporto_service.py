import sqlite3
from models.aeroporto import Aeroporto


class AeroportoService:
    def __init__(self, db_path="data/bank.bd"):
        self.db_path = db_path

    def _conectar(self):
        return sqlite3.connect(self.db_path)

    def _row_to_aeroporto(self, row):
        return Aeroporto(
            id=row[0],
            ident=row[1],
            iata_code=row[2],
            type=row[3],
            name=row[4],
            municipality=row[5],
            iso_country=row[6],
            latitude=row[7],
            longitude=row[8],
            elevation_ft=row[9],
        )

    def buscar_por_codigo(self, codigo: str):
        codigo = codigo.strip().upper()
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM aeroportos WHERE ident = ? OR iata_code = ? LIMIT 1",
            (codigo, codigo),
        )
        row = cursor.fetchone()
        conn.close()
        return self._row_to_aeroporto(row) if row else None

    def buscar_por_termo(self, termo: str, limite: int = 15):
        padrao = f"%{termo.strip()}%"
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM aeroportos
            WHERE ident LIKE ? OR iata_code LIKE ? OR name LIKE ? OR municipality LIKE ?
            ORDER BY CASE type
                WHEN 'large_airport' THEN 1
                WHEN 'medium_airport' THEN 2
                ELSE 3
            END
            LIMIT ?
            """,
            (padrao, padrao, padrao, padrao, limite),
        )
        rows = cursor.fetchall()
        conn.close()
        return [self._row_to_aeroporto(r) for r in rows]

    def listar_destaques_brasil(self):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM aeroportos
            WHERE iso_country = 'BR' AND type = 'large_airport'
            ORDER BY municipality
            """
        )
        rows = cursor.fetchall()
        conn.close()
        return [self._row_to_aeroporto(r) for r in rows]