from vending_machine.vending_machine import VendingMachine

def main():
    vending_machine = VendingMachine("drinks.csv")
    vending_machine.operate()

if __name__ == "__main__":
    main()