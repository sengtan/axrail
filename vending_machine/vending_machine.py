from vending_machine.vending_item import VendingItem
from vending_machine.drinks_item import DrinksItem
from typing import Dict, List
import csv

class VendingMachine():
    __category_item_map: Dict[str, List[VendingItem]] = {}
    __number_item_map: Dict[int, VendingItem] = {}
    __total_sales: int = 0
    __acceptable_notes: List = (1, 5, 10, 50, 100)

    def __init__(
            self,
            item_csv_file_path: str
        ):

        # Initialize data
        self.__total_sales = 0

        # Load up item information from provided csv
        self.read_csv_load_items(item_csv_file_path)

    @property
    def category_item_map(self) -> Dict[str, List[VendingItem]]:
        return self.__category_item_map.copy()
    
    @property
    def number_item_map(self) -> Dict[int, VendingItem]:
        return self.__number_item_map.copy()
    
    @property
    def total_sales(self) -> int:
        return self.__total_sales
    
    @property
    def acceptable_notes(self) -> tuple:
        return self.__acceptable_notes
    
    def set_total_sales(self, total_sales: int):
        if total_sales < 0:
            raise ValueError(f"Invalid total_sales value entered: {total_sales}")
        self.__total_sales = total_sales

    def clear_category_item_map(self):
        self.__category_item_map = {}

    def add_items(self, item: VendingItem):
        if item.category not in self.category_item_map.keys():
            self.__category_item_map[item.category] = []

        self.__category_item_map[item.category].append(item)
        self.__number_item_map[item.numbering] = item

    def read_csv_load_items(self, item_csv_file_path: str):
        self.clear_category_item_map()
        numbering = 1
        with open(item_csv_file_path, 'r') as f:
            reader = csv.DictReader(f)
            for drinks_data in reader:
                self.add_items(
                    item=DrinksItem(
                        name=drinks_data["Name"],
                        price=int(drinks_data["Price"]),
                        quantity=int(drinks_data["Quantity"]),
                        numbering=numbering,
                        temperature=drinks_data["Temperature"]
                    )
                )
                numbering += 1

    def shutdown(self):
        print("Seng's Vending Machine shutting down...")
        exit()

    def display_menu(self):
        print("\nWelcome to Seng's Vending Machine")
        for category, items in self.category_item_map.items():
            print(category)
            print(f"{'_'*20}")
            print(f"{'No':<3}{'Name':<15}Price")
            for item in items:
                print(f"{item.numbering:<3}{item.name:<15}RM{item.price:<10}{'SOLD OUT' if item.quantity <=0 else ''}")
            print(f"{'_'*20}")
    
    def await_selection(self):
        numbering = 0
        while numbering not in self.number_item_map.keys():
            self.display_menu()
            numbering = input("Please enter the numbering of the drink you want (-1 to shutdown): ")

            # Allow user/owner to shutdown (in real-life case, we wouldn't allow user to enter -1 like that)
            if numbering == "-1":
                numbering = input("Type 'shutdown' to confirm: ")
                if numbering == "shutdown":
                    self.shutdown()
                else:
                    continue
            
            # Check if the number entered is valid
            else:
                # Ensure selection is an integer value
                try:
                    numbering = int(numbering)
                except ValueError:
                    print(f"Invalid input: {numbering}, please try again.")
                    continue

                if numbering not in self.number_item_map.keys() or self.number_item_map[numbering].quantity <=0:
                    print(f"Item {numbering} is not available, please pick another one.")

        return self.number_item_map[numbering].price
    
    def release_change(self, total_amount_received:int, total_amount_required: int):
        dispensable_notes = list(self.acceptable_notes)
        dispensable_notes.sort(reverse = True)
        notes_to_release = {key: 0 for key in dispensable_notes}
        
        change = total_amount_received - total_amount_required

        # Checks if change is valid value
        if change == 0:
            print("No change required")
            return
        elif change <0:
            raise ValueError(f"Invalid change value: {change}, please contact Admin at +60184724702")

        # Calculates minimum notes to release as change
        amount = 0
        for note in dispensable_notes:
            num_of_note = int((change-amount)/note)
            
            if num_of_note:
                amount += note*num_of_note
                notes_to_release[note] = num_of_note
            
            if amount == change:
                print(f"Releasing your change (RM{amount}):")
                print(f"{'Note':<7}{'Pcs':>4}")
                for note, count in notes_to_release.items():
                    if count > 0:
                        print(f"RM{note:>4}:{count:>4}")
                return
        
        if amount != change:
            print(f"Error: Machine does not have sufficient denominations to release exact change. Change releasable:{amount}")
            raise ValueError(f"Unable to release exact change, please contact Admin at +60184724702")

        return
    
    def await_payment(self, total_amount_required: int):
        total_amount_received = 0
        
        received_note = 0
        while total_amount_received < total_amount_required:
            print(f"Amount Paid: {total_amount_received}/{total_amount_required}")
            received_note = input(f"Please insert note {self.acceptable_notes} or type 'x' to cancel: ")

            # Allow user to cancel purchase, in which case will release change
            if received_note == 'x':
                self.release_change(total_amount_received, 0)
                return 0

            # Ensure note inserted is an integer value
            value = 0
            try:
                value = int(received_note)
            except ValueError:
                print(f"Invalid input: {received_note}, please try again.")
                continue
            
            # Ensure the note inserted is acceptable by the machine
            if value not in self.acceptable_notes:
                print(f"The machine is unable to accept the inserted note: {value}")
            else:
                total_amount_received += value
        
        print(f"Dispensing... Enjoy your drink! Thank you, come again!")
        self.set_total_sales(self.total_sales + total_amount_required)
        self.release_change(total_amount_received, total_amount_required)

    def operate(self):
        while 1:
            amount_required = self.await_selection()
            self.await_payment(amount_required)