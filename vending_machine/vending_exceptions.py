class InvalidItemNameError(Exception):
    def __init__(self, message="Invalid item name entered"):
        self.message = message
        super().__init__(self.message)

class InvalidItemPriceError(Exception):
    def __init__(self, message="Invalid item price entered"):
        self.message = message
        super().__init__(self.message)

class InvalidItemQuantityError(Exception):
    def __init__(self, message="Invalid item quantity entered"):
        self.message = message
        super().__init__(self.message)

class InvalidItemDataError(Exception):
    def __init__(self, message="Invalid item data entered"):
        self.message = message
        super().__init__(self.message)