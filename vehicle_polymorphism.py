class Vehicle:
    def move(self) -> str:
        raise NotImplementedError("Subclasses must implement move().")

class Car(Vehicle):
    def move(self) -> str:
        return "Driving 🚗"

class Plane(Vehicle):
    def move(self) -> str:
        return "Flying ✈️"

class Boat(Vehicle):
    def move(self) -> str:
        return "Sailing 🚤"

class Bicycle(Vehicle):
    def move(self) -> str:
        return "Pedaling 🚴"

def journey(vehicles):
    for v in vehicles:
        print(v.move())

if __name__ == "__main__":
    fleet = [Car(), Plane(), Boat(), Bicycle()]
    journey(fleet)