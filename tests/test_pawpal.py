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
