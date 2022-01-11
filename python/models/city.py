import uuid


class City:

    def __init__(self, id_city: uuid, id_reference: int, ibge_code: int, lat: float, lng: float, capital: bool,
                 state: str, phone_code: int) -> None:
        self.id_city: uuid = id_city
        self.id_reference: int = id_reference
        self.ibge_code: int = ibge_code
        self.lat: float = lat
        self.lng: float = lng
        self.capital: bool = capital
        self.state: str = state
        self.phone_code: int = phone_code
