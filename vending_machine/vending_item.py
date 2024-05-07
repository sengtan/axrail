from vending_machine.vending_exceptions import InvalidItemNameError, InvalidItemPriceError, InvalidItemQuantityError, InvalidItemDataError

class VendingItem():
    __name = "VendingItem"
    __price = 0
    __quantity = 0
    __numbering = 0
    __category = "General"
    __total_sold = 0

    def __init__(self, 
            name: str, 
            price: int,
            quantity: int,
            numbering: int,
            category: str = "General",
        ):

        # Initialize the data
        # Note: no true private variables in Python, but we can still make access to it hard
        self.set_name(name=name)
        self.set_price(price=price)
        self.set_quantity(quantity=quantity)
        self.set_numbering(numbering=numbering)
        self.set_category(category=category)
        self.set_total_sold(total_sold=0)

    # Getters using @property, possible to just use method instead
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def price(self) -> int:
        return self.__price
    
    @property
    def quantity(self) -> int:
        return self.__quantity
    
    @property
    def numbering(self) -> int:
        return self.__numbering
    
    @property
    def category(self) -> str:
        return self.__category
    
    @property
    def total_sold(self) -> int:
        return self.__total_sold
    
    # Setters with checks to ensure valid data is entered
    # Note: assert not used here as assert could be removed when packaging into a module (option)
    def set_name(self, name: str):
        if name == "":
            raise InvalidItemNameError(
                message=f"Invalid item name entered: '{name}'"
            )

        self.__name = name

    def set_price(self, price: int):
        if price < 0:
            raise InvalidItemPriceError(
                message=f"Invalid item price entered: '{price}'"
            )
        
        self.__price = price
        
    def set_quantity(self, quantity: int):
        if quantity < 0:
            raise InvalidItemQuantityError(
                message=f"Invalid item quantity entered: '{quantity}'"
            )

        self.__quantity = quantity

    def set_numbering(self, numbering: int):
        if numbering <= 0:
            raise InvalidItemDataError(
                message=f"Invalid item numbering entered: '{numbering}'"
            )

        self.__numbering= numbering

    def set_category(self, category: str = "General"):
        if category == "":
            raise InvalidItemDataError(
                message=f"Invalid item category entered: '{category}'"
            )
        
        self.__category = category

    def set_total_sold(self, total_sold: int):
        if total_sold < 0:
            raise InvalidItemQuantityError(
                message=f"Invalid item sold quantity entered: '{total_sold}'"
            )

        self.__total_sold = total_sold

    # Helper methods to increment/decrement quantity, dispense operation
    def inc_quantity(self):
        self.set_quantity(self.quantity + 1)
    
    def dec_quantity(self):
        self.set_quantity(self.quantity - 1)

    def dispense_one(self):
        self.dec_quantity()
        self.set_total_sold(self.total_sold + 1)

    # Information printout
    def print_info(self):
        print(f"""
        Product Information
        -------------------
        Name:       {self.name}
        Price:      {self.price}
        Quantity:   {self.quantity}
        Category:   {self.category}
        Numbering:  {self.numbering}
        Total Sold: {self.total_sold}
        Total Sales:{self.total_sold*self.quantity}
        """.strip("\n").rstrip(), end="")