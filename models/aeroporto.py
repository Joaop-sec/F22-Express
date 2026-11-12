class Aeroporto:
    def __init__(self, id, ident, iata_code, type, name, municipality,
                 iso_country, latitude, longitude, elevation_ft):
        self.id = id
        self.ident = ident
        self.iata_code = iata_code
        self.type = type
        self.name = name
        self.municipality = municipality
        self.iso_country = iso_country
        self.latitude = latitude
        self.longitude = longitude
        self.elevation_ft = elevation_ft