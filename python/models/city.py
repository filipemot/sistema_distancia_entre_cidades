import uuid


class City:

    def __init__(self, name: str, id_reference: int, ibge_code: int, lat: float, lng: float, capital: bool,
                 state: str, phone_code: int) -> None:
        self.id_city: str = str(uuid.uuid4())
        self.name = name
        self.id_reference: int = id_reference
        self.ibge_code: int = ibge_code
        self.lat: float = lat
        self.lng: float = lng
        self.capital: bool = capital
        self.state: str = state
        self.phone_code: int = phone_code
