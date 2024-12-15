# Below is the Relation Between SOLID Principles and Design Patterns in my system:
## 1. Factory Method (Creational Pattern):

SOLID Principle: Open/Closed Principle (OCP), Single Responsibility Principle (SRP)

OCP: The PizzaFactory can be extended to support new pizza types without modifying existing code.

SRP: The PizzaFactory class encapsulates the creation logic for pizzas, separating it from other functions.

Using a factory ensures that the pizza creation process is modular and easily extendable, adhering to OCP.

```python
class PizzaFactory:
    @staticmethod
    def create_pizza(pizza_type: str) -> Pizza:
        if pizza_type == "1":
            return Margherita()
        elif pizza_type == "2":
            return Pepperoni()
        else:
            raise ValueError("Invalid pizza type")
```
## 2. Observer (Behavioral Pattern)

SOLID Principles: Single Responsibility Principle (SRP), Dependency Inversion Principle (DIP)

SRP: Observers focus solely on responding to changes in the subject.

DIP: Observers depend on abstractions.

By implementing an observer pattern, the system can notify multiple dependent objects of state changes, improving modularity and scalability.

Code Snippet:
```python
class InventoryObserver:
    def update_inventory(self, item: str):
        inventory_manager = InventoryManager()
        inventory_manager.check_and_decrement(item)
```
# Another example:
```python
class Cheese(ToppingDecorator):
    def __init__(self, pizza: Pizza):
        super().__init__(pizza)
        self.update_inventory("Cheese")
```

## 3. Adapter (Structural Pattern)
SOLID Principles: Open/Closed Principle (OCP), Single Responsibility Principle (SRP)

OCP: The adapter allows new incompatible interfaces to be integrated without altering existing code.

SRP: The adapter class serves the sole purpose of converting one interface into another.

Implementation: An adapter ensures that components with incompatible interfaces (e.g., legacy payment systems or third-party libraries) can seamlessly work together without modifying their internal logic.

```python
class PaymentAdapter(PaymentMethod):
    def __init__(self, payment_gateway):
        self.payment_gateway = payment_gateway

    def pay(self, amount: float):
        self.payment_gateway.process_payment(amount)

# Usage
class StripeGateway:
    def process_payment(self, amount: float):
        print(f"Paid ${amount:.2f} using Stripe. Payment Successful!")
```
# Overengineering
### Overengineering occurs when a system is designed with excessive complexity, including unnecessary features or patterns that complicate the implementation without adding significant value.
### Example:
```python
class Dough:
    def __init__(self):
        self.type = "Regular"

    def __str__(self):
        return self.type


class Sauce:
    def __init__(self):
        self.type = "Tomato"

    def __str__(self):
        return self.type


class Topping:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Pizza:
    def __init__(self, name):
        self.name = name
        self.dough = Dough()
        self.sauce = Sauce()
        self.toppings = []

    def add_topping(self, topping):
        self.toppings.append(Topping(topping))

    def __str__(self):
        toppings = ", ".join(str(t) for t in self.toppings)
        return (
            f"Pizza: {self.name}\n"
            f"Dough: {self.dough}\n"
            f"Sauce: {self.sauce}\n"
            f"Toppings: {toppings if toppings else 'None'}"
        )
```
the above code is over-engineered because it uses a lot of unnecessary classes and methods that can be simplified into only 1 or 2 classes.
