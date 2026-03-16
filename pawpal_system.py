from dataclasses import dataclass, field


@dataclass
class Pet:
    name: str
    species: str
    owner: "Owner" = field(default=None, repr=False)


@dataclass
class Task:
    name: str
    duration_mins: int
    priority: int
    task_type: str
    recurring: bool = False
    pet: Pet = field(default=None, repr=False)


class Owner:
    def __init__(self, name: str):
        self.name = str(name)
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, pet: Pet) -> None:
        pass

    def get_pets(self) -> list[Pet]:
        pass


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task: Task) -> None:
        pass

    def generate_daily_plan(self):
        pass
