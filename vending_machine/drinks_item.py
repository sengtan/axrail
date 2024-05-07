from vending_machine.vending_item import VendingItem
from vending_machine.vending_exceptions import InvalidItemDataError

class DrinksItem(VendingItem):
    valid_temperature = ('Hot', 'Cold')

    def __init__(self, 
            name: str, 
            price: int,
            quantity: int,
            numbering: int,
            category: str = "Drinks",   # could be others, eg. Soda, Coffee etc
            temperature: str = "Cold",
        ):

        super().__init__(
            name=name,
            price=price,
            quantity=quantity,
            numbering=numbering,
            category=category,
        )

        self.set_temperature(temperature=temperature)

    @property
    def temperature(self) -> str:
        return self.__temperature
    
    def set_temperature(self, temperature: str = "Cold"):
        if temperature not in self.valid_temperature:
            raise InvalidItemDataError(
                message=f"Invalid drink temperature entered: '{temperature}', only {'/'.join(self.valid_temperature)} allowed"
            )
        
        self.__temperature = temperature

    # Information printout
    def print_info(self):
        super().print_info()
        print(f"""
        Temperature: {self.temperature}
        """.rstrip("\n").rstrip(), end="")

    