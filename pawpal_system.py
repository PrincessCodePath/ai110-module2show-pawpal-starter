from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass
class Task:
    description: str
    time: str
    duration_mins: int
    priority: int
    frequency: str = "daily"
    completed: bool = False
    pet: "Pet" = field(default=None, repr=False)
    due_date: date | None = field(default=None, repr=False)

    def mark_complete(self) -> None:
        """Set this task as completed; create next occurrence if daily or weekly."""
        self.completed = True
        if not self.pet or self.frequency not in ("daily", "weekly"):
            return
        base = self.due_date or date.today()
        delta = timedelta(days=1) if self.frequency == "daily" else timedelta(days=7)
        next_task = Task(
            self.description,
            self.time,
            self.duration_mins,
            self.priority,
            self.frequency,
            False,
            self.pet,
            base + delta,
        )
        self.pet.add_task(next_task)


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

    def sort_by_time(self) -> list[Task]:
        """Return all tasks sorted by time (HH:MM)."""
        return sorted(self.get_tasks(), key=lambda t: t.time)

    def filter_tasks(
        self,
        completed: bool | None = None,
        pet_name: str | None = None,
    ) -> list[Task]:
        """Return tasks filtered by completion status and/or pet name."""
        tasks = self.get_tasks()
        if completed is not None:
            tasks = [t for t in tasks if t.completed == completed]
        if pet_name is not None:
            tasks = [t for t in tasks if t.pet and t.pet.name == pet_name]
        return tasks

    def check_conflicts(self) -> list[str]:
        """Return warning messages for tasks scheduled at the same time."""
        by_time: dict[str, list[Task]] = {}
        for t in self.get_tasks():
            by_time.setdefault(t.time, []).append(t)
        warnings = []
        for tm, group in by_time.items():
            if len(group) > 1:
                names = ", ".join(f"{t.description} ({t.pet.name})" if t.pet else t.description for t in group)
                warnings.append(f"Conflict at {tm}: {names}")
        return warnings

    def generate_daily_plan(self) -> list[Task]:
        """Return today's tasks sorted by time."""
        return self.sort_by_time()
