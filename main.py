from pawpal_system import Owner, Pet, Task, Scheduler

owner = Owner("Alex")
dog = Pet("Buddy", "dog")
cat = Pet("Whiskers", "cat")
owner.add_pet(dog)
owner.add_pet(cat)

dog.add_task(Task("Morning walk", "07:00", 30, 1))
dog.add_task(Task("Feed breakfast", "08:00", 15, 2))
cat.add_task(Task("Feed breakfast", "08:30", 10, 2))

scheduler = Scheduler(owner)
plan = scheduler.generate_daily_plan()

print("Today's Schedule")
print("-" * 40)
for t in plan:
    pet_name = t.pet.name if t.pet else "?"
    print(f"  {t.time}  {t.description} ({pet_name}) - {t.duration_mins} min")
print("-" * 40)
