from dataclasses import dataclass, field


@dataclass
class Task:
    description: str
    time: str
    duration_mins: int
    priority: int
    frequency: str = "daily"
    completed: bool = False
    pet: "Pet" = field(default=None, repr=False)

    def mark_complete(self) -> None:
        """Set this task as completed."""
        self.completed = True


@dataclass
class Pet:
    name: str
    species: str
    owner: "Owner" = field(default=None, repr=False)
    tasks: list[Task] = field(default_factory=list, repr=False)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's list."""
        task.pet = self
        self.tasks.append(task)


class Owner:
    def __init__(self, name: str):
        self.name = name
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Register a pet to this owner."""
        pet.owner = self
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner."""
        if pet in self.pets:
            self.pets.remove(pet)
            pet.owner = None

    def get_pets(self) -> list[Pet]:
        """Return all pets for this owner."""
        return self.pets

    def get_all_tasks(self) -> list[Task]:
        """Return all tasks across all of this owner's pets."""
        out = []
        for p in self.pets:
            out.extend(p.tasks)
        return out


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def get_tasks(self) -> list[Task]:
        """Retrieve all tasks from the owner's pets."""
        return self.owner.get_all_tasks()

    def add_task(self, task: Task) -> None:
        """Add a task to its assigned pet's list."""
        if task.pet is not None and task not in task.pet.tasks:
            task.pet.add_task(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from its pet's list."""
        if task.pet is not None and task in task.pet.tasks:
            task.pet.tasks.remove(task)
            task.pet = None

    def generate_daily_plan(self) -> list[Task]:
        """Return today's tasks sorted by time."""
        tasks = self.get_tasks()
        return sorted(tasks, key=lambda t: t.time)
