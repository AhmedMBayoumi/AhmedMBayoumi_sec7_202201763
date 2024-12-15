from abc import ABC, abstractmethod

class InventoryManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InventoryManager, cls).__new__(cls)
            cls._instance._inventory = {"Margherita": 100,"Pepperoni": 100,"Cheese": 100,"Olives": 100,"Mushrooms": 100,}
        return cls._instance

    def check_and_decrement(self, item: str):
        if self._inventory.get(item, 0) > 0:
            self._inventory[item] -= 1
            return True
        return False

    def get_inventory(self):
        return self._inventory

class Pizza(ABC):
    @abstractmethod
    def get_description(self):
        pass

    @abstractmethod
    def get_cost(self):
        pass

class Margherita(Pizza):
    def get_description(self):
        return "Margherita"

    def get_cost(self):
        return 10

class Pepperoni(Pizza):
    def get_description(self):
        return "Pepperoni"

    def get_cost(self):
        return 15

class ToppingDecorator(Pizza):
    def __init__(self, pizza: Pizza):
        self._pizza = pizza

    @abstractmethod
    def get_description(self):
        pass

    @abstractmethod
    def get_cost(self):
        pass

class Cheese(ToppingDecorator):
    def get_description(self):
        return f"{self._pizza.get_description()} + Cheese"

    def get_cost(self):
        return self._pizza.get_cost() + 1

class Olives(ToppingDecorator):
    def get_description(self):
        return f"{self._pizza.get_description()} + Olives"

    def get_cost(self):
        return self._pizza.get_cost() + 1.5

class Mushrooms(ToppingDecorator):
    def get_description(self):
        return f"{self._pizza.get_description()} + Mushrooms"

    def get_cost(self):
        return self._pizza.get_cost() + 2

class PizzaFactory:
    @staticmethod
    def create_pizza(pizza_type: str):
        if pizza_type == "1":
            return Margherita()
        elif pizza_type == "2":
            return Pepperoni()
        else:
            raise ValueError("Invalid pizza type")

class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount: float):
        pass

class PayPalPayment(PaymentMethod):
    def pay(self, amount: float):
        print(f"Paid ${amount:.2f} using PayPal. Payment Successful!")

class CreditCardPayment(PaymentMethod):
    def pay(self, amount: float):
        print(f"Paid ${amount:.2f} using Credit Card. Payment Successful!")

def main():
    inventory_manager = InventoryManager()
    total_cost = 0
    full_description = []

    print("Welcome to the Pizza Restaurant!")

    while True:
        print("\nChoose your pizza:")
        print("1. Margherita ($10)")
        print("2. Pepperoni ($15)")
        print("0 => to finish order")
        pizza_choice = input("Enter a number: ")

        if pizza_choice == '0':
            break

        try:
            pizza = PizzaFactory.create_pizza(pizza_choice)
        except ValueError as e:
            print(e)
            continue

        while True:
            print("\nAvailable toppings:")
            print("1. Cheese ($1.0)")
            print("2. Olives ($1.5)")
            print("3. Mushrooms ($2.0)")
            print("4. Finish adding toppings")
            topping_choice = input("Enter a number: ")

            if topping_choice == "1" and inventory_manager.check_and_decrement("Cheese"):
                pizza = Cheese(pizza)
            elif topping_choice == "2" and inventory_manager.check_and_decrement("Olives"):
                pizza = Olives(pizza)
            elif topping_choice == "3" and inventory_manager.check_and_decrement("Mushrooms"):
                pizza = Mushrooms(pizza)
            elif topping_choice == "4":
                break
            else:
                print("Topping unavailable or out of stock")

        total_cost += pizza.get_cost()
        full_description.append(pizza.get_description())

    print("\nYour full order:")
    print(f"Description: {', '.join(full_description)}")
    print(f"Total cost: ${total_cost:.2f}")

    print("\nChoose a payment method:")
    print("1. PayPal")
    print("2. Credit Card")
    payment_choice = input("Enter the number of your choice: ")
    if payment_choice == "1":
        payment = PayPalPayment()
    elif payment_choice == "2":
        payment = CreditCardPayment()
    else:
        print("Invalid payment method. Order canceled.")
        return

    payment.pay(total_cost)

    print("\nRemaining Inventory:")
    print(inventory_manager.get_inventory())

if __name__ == "__main__":
    main()
