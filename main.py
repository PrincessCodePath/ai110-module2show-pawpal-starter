from pawpal_system import Owner, Pet, Task, Scheduler

owner = Owner("Alex")
dog = Pet("Buddy", "dog")
cat = Pet("Whiskers", "cat")
owner.add_pet(dog)
owner.add_pet(cat)

dog.add_task(Task("Evening walk", "18:00", 30, 1))
dog.add_task(Task("Feed breakfast", "08:00", 15, 2))
cat.add_task(Task("Feed breakfast", "08:30", 10, 2))
dog.add_task(Task("Medication", "08:00", 5, 1))

scheduler = Scheduler(owner)

warnings = scheduler.check_conflicts()
for w in warnings:
    print(f"Warning: {w}")

print("Today's Schedule (sorted by time)")
print("-" * 40)
plan = scheduler.sort_by_time()
for t in plan:
    pet_name = t.pet.name if t.pet else "?"
    print(f"  {t.time}  {t.description} ({pet_name}) - {t.duration_mins} min")
print("-" * 40)

print("Tasks for Buddy only")
print("-" * 40)
for t in scheduler.filter_tasks(pet_name="Buddy"):
    print(f"  {t.time}  {t.description}")
print("-" * 40)

print("Incomplete tasks only")
print("-" * 40)
for t in scheduler.filter_tasks(completed=False):
    pet_name = t.pet.name if t.pet else "?"
    print(f"  {t.time}  {t.description} ({pet_name})")
print("-" * 40)

recurring = Task("Daily brush", "09:00", 10, 2, frequency="daily", pet=dog)
dog.add_task(recurring)
print("Before mark_complete: Buddy has", len(dog.tasks), "tasks")
recurring.mark_complete()
print("After mark_complete (daily): Buddy has", len(dog.tasks), "tasks")
