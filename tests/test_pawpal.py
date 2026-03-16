from datetime import date, timedelta

from pawpal_system import Owner, Pet, Task, Scheduler


def test_task_mark_complete_changes_status():
    task = Task("Walk", "09:00", 20, 1)
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_adding_task_to_pet_increases_task_count():
    owner = Owner("Test")
    pet = Pet("Dog", "dog")
    owner.add_pet(pet)
    assert len(pet.tasks) == 0
    pet.add_task(Task("Feed", "08:00", 10, 1))
    assert len(pet.tasks) == 1
    pet.add_task(Task("Walk", "12:00", 30, 2))
    assert len(pet.tasks) == 2


def test_sort_by_time_returns_chronological_order():
    owner = Owner("Test")
    pet = Pet("Dog", "dog")
    owner.add_pet(pet)
    pet.add_task(Task("Late", "18:00", 10, 1))
    pet.add_task(Task("Early", "07:00", 10, 1))
    pet.add_task(Task("Mid", "12:00", 10, 1))
    scheduler = Scheduler(owner)
    ordered = scheduler.sort_by_time()
    assert [t.time for t in ordered] == ["07:00", "12:00", "18:00"]


def test_marking_daily_task_complete_creates_next_day_task():
    owner = Owner("Test")
    pet = Pet("Dog", "dog")
    owner.add_pet(pet)
    today = date.today()
    task = Task("Brush", "09:00", 10, 1, "daily", False, pet, today)
    pet.add_task(task)
    assert len(pet.tasks) == 1
    task.mark_complete()
    assert len(pet.tasks) == 2
    next_task = pet.tasks[1]
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task.completed is False


def test_check_conflicts_flags_duplicate_times():
    owner = Owner("Test")
    pet = Pet("Dog", "dog")
    owner.add_pet(pet)
    pet.add_task(Task("Feed", "08:00", 15, 1))
    pet.add_task(Task("Meds", "08:00", 5, 2))
    scheduler = Scheduler(owner)
    warnings = scheduler.check_conflicts()
    assert len(warnings) == 1
    assert "08:00" in warnings[0]


def test_pet_with_no_tasks_returns_empty_schedule():
    owner = Owner("Test")
    pet = Pet("Dog", "dog")
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    assert scheduler.sort_by_time() == []
    assert scheduler.check_conflicts() == []
