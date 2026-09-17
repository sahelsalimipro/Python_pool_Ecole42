class Plant:
    # nested statistic class
    class Stats:
        def __init__(self):
            self.nb_show = 0
            self.nb_age = 0
            self.nb_grow = 0

        def record_grow(self):
            self.nb_grow += 1

        def record_age(self):
            self.nb_age += 1

        def record_show(self):
            self.nb_show += 1

        def show_stat(self):
            print(
                f"Stats : {self.nb_grow} grow, "
                f"{self.nb_age} age, "
                f"{self.nb_show} show")

    # Plant
    def __init__(self, name: str, height: float, age: int) -> None:
        self.name = name
        self._height = 0.0
        self._age = 0

        self.set_height(height)
        self.set_age(age)
        self._stats = Plant.Stats()

    def get_height(self) -> float:
        return self._height

    def get_age(self) -> int:
        return self._age

    def set_height(self, height: float) -> bool:
        if height < 0:
            print(f"{self.name}: Error, height can't be negative")
            return False
        else:
            self._height = height
            return True

    def display_stats(self) -> None:
        self._stats.show_stat()

    def set_age(self, age: int) -> bool:
        if age < 0:
            print(f"{self.name}: Error, age can't be negative")
            return False
        else:
            self._age = age
            return True

    def grow(self, day):
        self._height += day
        self._stats.record_grow()

    def age(self, day):
        self._age += day
        self._stats.record_age()

    def show(self) -> None:
        print(
            f"{self.name}: {round(self._height, 1)}cm,", end=" ")
        print(f"{self._age} days old")
        self._stats.record_show()

    @staticmethod
    def is_older_than_year(age: int) -> bool:
        return age > 365

    @classmethod
    def create_anonymous(cls):
        return cls("Unknown plant", 0.0, 0)


class Flower(Plant):
    def __init__(self, name: str, height: float, age: int, color: str):
        super().__init__(name, height, age)
        self.color = color
        self.bloomed = False

    def show(self):
        super().show()
        print(f"Color: {self.color}")
        if self.bloomed is False:
            print(f"{self.name} has not bloomed yet")
        else:
            print(f"{self.name} is blooming beautifully!")

    def bloom(self):
        self.bloomed = True


class Seed(Flower):
    def __init__(self, name: str, height: float, age: int, color: str):
        super().__init__(name, height, age, color)
        self.seeds = 0

    def bloom(self, seeds):
        super().bloom()
        self.seeds = seeds

    def show(self):
        super().show()
        print(f"Seeds: {self.seeds}")


class Tree(Plant):
    def __init__(self, name: str, height: float, age: int, trunk: float):
        super().__init__(name, height, age)
        self.trunk = trunk
        self._shade = 0

    def show(self):
        super().show()
        print(f"Trunk diameter: {self.trunk}cm")

    def produce_shade(self):
        self._shade += 1
        print(
            f"Tree {self.name} now produces a shade of ", end=" ")
        print(f"{round(self._height, 1)}cm long", end=" ")
        print(f"and {round(self.trunk, 1)}cm wide.")

    def display_shade(self):
        print(f"{self._shade} shade")


class Vegetable(Plant):
    def __init__(self, name: str, height: float, age: int, Harvest: str):
        super().__init__(name, height, age)
        self.Harvest = Harvest
        self.Nutritional = 0

    def show(self):
        super().show()
        print(f"Harvest season: {self.Harvest}")
        print(f"Nutritional value: {self.Nutritional}")

    def grow(self, day):
        super().grow(day)
        self.Nutritional += day


def display_plant_statistics(plant):
    print(f"[statistics for {plant.name}]")
    plant._stats.show_stat()


if __name__ == "__main__":
    print("=== Garden statistics ===")
    print("=== Check year-old")
    print(f"Is 30 days more than a year? -> {Plant.is_older_than_year(30)}")
    print(f"Is 400 days more than a year? -> {Plant.is_older_than_year(400)}")

    print("=== Flower")
    rose = Flower("Rose", 15.0, 10, "Red")
    rose.show()
    rose.bloom()
    display_plant_statistics(rose)
    print("[asking the rose to grow and bloom]")
    rose.grow(8.0)
    rose.bloom()
    rose.show()
    display_plant_statistics(rose)

    print()
    print("=== Tree")
    oak = Tree("Oak", 200.0, 365, 5.0)
    oak.show()
    display_plant_statistics(oak)
    oak.display_shade()
    print("[asking the oak to produce shade]")
    oak.produce_shade()

    display_plant_statistics(oak)
    oak.display_shade()

    print()
    print("=== Seed")
    sunflower = Seed("sunflower", 80.0, 45, "yellow")
    sunflower.show()
    print("[make sunflower grow, age and bloom]")
    sunflower.age(20)
    sunflower.grow(30)
    sunflower.bloom(42)
    sunflower.show()
    display_plant_statistics(sunflower)

    print("\n==== Anonymous")
    anonymous = Plant.create_anonymous()
    anonymous.show()
    print("[statistics for Unknown plant]")
    anonymous._stats.show_stat()
