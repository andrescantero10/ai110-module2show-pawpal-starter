from datetime import date, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


def test_mark_complete_flips_status():
    task = Task("Walk", "08:00", 30, "high")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_count():
    pet = Pet("Buddy", "dog", 3)
    assert pet.task_count() == 0
    pet.add_task(Task("Walk", "08:00", 30, "high"))
    assert pet.task_count() == 1
    pet.add_task(Task("Feed", "09:00", 10, "medium"))
    assert pet.task_count() == 2


def test_sort_by_time_chronological():
    owner = Owner("Test")
    pet = Pet("Dog", "dog", 2)
    owner.add_pet(pet)
    pet.add_task(Task("Late", "17:00", 30, "low", due_date=date.today()))
    pet.add_task(Task("Early", "07:00", 15, "high", due_date=date.today()))
    pet.add_task(Task("Mid", "12:00", 20, "medium", due_date=date.today()))
    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time(owner.get_all_tasks())
    times = [t.time for t in sorted_tasks]
    assert times == ["07:00", "12:00", "17:00"]


def test_recurrence_daily_creates_next_day():
    owner = Owner("Test")
    pet = Pet("Dog", "dog", 2)
    owner.add_pet(pet)
    today = date.today()
    task = Task("Walk", "08:00", 30, "high", frequency="daily", due_date=today)
    pet.add_task(task)
    scheduler = Scheduler(owner)
    new_task = scheduler.mark_task_complete(task)
    assert task.completed is True
    assert new_task is not None
    assert new_task.due_date == today + timedelta(days=1)
    assert new_task.completed is False
    assert pet.task_count() == 2


def test_recurrence_weekly_creates_next_week():
    owner = Owner("Test")
    pet = Pet("Cat", "cat", 3)
    owner.add_pet(pet)
    today = date.today()
    task = Task("Grooming", "10:00", 20, "medium", frequency="weekly", due_date=today)
    pet.add_task(task)
    scheduler = Scheduler(owner)
    new_task = scheduler.mark_task_complete(task)
    assert new_task is not None
    assert new_task.due_date == today + timedelta(weeks=1)


def test_recurrence_once_does_not_recur():
    owner = Owner("Test")
    pet = Pet("Dog", "dog", 2)
    owner.add_pet(pet)
    task = Task("Vet visit", "14:00", 60, "high", frequency="once")
    pet.add_task(task)
    scheduler = Scheduler(owner)
    result = scheduler.mark_task_complete(task)
    assert result is None
    assert pet.task_count() == 1


def test_conflict_detection_same_time():
    owner = Owner("Test")
    pet1 = Pet("Dog", "dog", 2)
    pet2 = Pet("Cat", "cat", 3)
    owner.add_pet(pet1)
    owner.add_pet(pet2)
    today = date.today()
    pet1.add_task(Task("Walk", "09:00", 30, "high", due_date=today))
    pet2.add_task(Task("Feed", "09:00", 10, "high", due_date=today))
    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) == 1
    assert "09:00" in conflicts[0]


def test_conflict_detection_no_false_positive():
    owner = Owner("Test")
    pet = Pet("Dog", "dog", 2)
    owner.add_pet(pet)
    today = date.today()
    pet.add_task(Task("Walk", "08:00", 30, "high", due_date=today))
    pet.add_task(Task("Feed", "09:00", 10, "high", due_date=today))
    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) == 0


def test_filter_by_pet():
    owner = Owner("Test")
    dog = Pet("Dog", "dog", 2)
    cat = Pet("Cat", "cat", 3)
    owner.add_pet(dog)
    owner.add_pet(cat)
    dog.add_task(Task("Walk", "08:00", 30, "high"))
    cat.add_task(Task("Feed", "09:00", 10, "high"))
    scheduler = Scheduler(owner)
    dog_tasks = scheduler.filter_tasks(pet_name="Dog")
    assert len(dog_tasks) == 1
    assert dog_tasks[0].description == "Walk"


def test_filter_by_status():
    owner = Owner("Test")
    pet = Pet("Dog", "dog", 2)
    owner.add_pet(pet)
    t1 = Task("Walk", "08:00", 30, "high")
    t2 = Task("Feed", "09:00", 10, "high")
    pet.add_task(t1)
    pet.add_task(t2)
    t1.mark_complete()
    scheduler = Scheduler(owner)
    pending = scheduler.filter_tasks(completed=False)
    assert len(pending) == 1
    assert pending[0].description == "Feed"


def test_pet_with_no_tasks():
    pet = Pet("Empty", "fish", 1)
    assert pet.task_count() == 0
    assert pet.get_tasks() == []


def test_owner_with_no_pets():
    owner = Owner("Lonely")
    assert owner.get_all_tasks() == []
    assert owner.get_pet("Nobody") is None


def test_find_next_available_slot_basic():
    owner = Owner("Test")
    pet = Pet("Dog", "dog", 2)
    owner.add_pet(pet)
    today = date.today()
    pet.add_task(Task("Walk", "08:00", 30, "high", due_date=today))
    pet.add_task(Task("Feed", "09:00", 15, "high", due_date=today))
    scheduler = Scheduler(owner)
    slot = scheduler.find_next_available_slot(today, 20)
    assert slot == "08:30"  # After the 08:00-08:30 walk, before 09:00 feed


def test_find_next_available_slot_no_room():
    owner = Owner("Test")
    pet = Pet("Dog", "dog", 2)
    owner.add_pet(pet)
    today = date.today()
    # Fill the entire day
    pet.add_task(Task("Long task", "08:00", 780, "high", due_date=today))  # 08:00-21:00
    scheduler = Scheduler(owner)
    slot = scheduler.find_next_available_slot(today, 30)
    assert slot is None


def test_find_next_available_slot_empty_day():
    owner = Owner("Test")
    pet = Pet("Dog", "dog", 2)
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    slot = scheduler.find_next_available_slot(date.today(), 30)
    assert slot == "08:00"


def test_sort_by_priority_then_time():
    owner = Owner("Test")
    pet = Pet("Dog", "dog", 2)
    owner.add_pet(pet)
    today = date.today()
    pet.add_task(Task("Low early", "07:00", 10, "low", due_date=today))
    pet.add_task(Task("High late", "17:00", 30, "high", due_date=today))
    pet.add_task(Task("Medium mid", "12:00", 20, "medium", due_date=today))
    pet.add_task(Task("High early", "08:00", 15, "high", due_date=today))
    scheduler = Scheduler(owner)
    result = scheduler.sort_by_priority_then_time(owner.get_all_tasks())
    descriptions = [t.description for t in result]
    assert descriptions == ["High early", "High late", "Medium mid", "Low early"]


def test_json_round_trip(tmp_path):
    owner = Owner("Andres")
    pet = Pet("Buddy", "dog", 3)
    owner.add_pet(pet)
    today = date.today()
    pet.add_task(Task("Walk", "08:00", 30, "high", "daily", today))
    path = str(tmp_path / "test_data.json")
    owner.save_to_json(path)
    loaded = Owner.load_from_json(path)
    assert loaded.name == "Andres"
    assert len(loaded.pets) == 1
    assert loaded.pets[0].name == "Buddy"
    assert loaded.pets[0].task_count() == 1
    task = loaded.pets[0].get_tasks()[0]
    assert task.description == "Walk"
    assert task.due_date == today
    assert task.frequency == "daily"


def test_empty_schedule():
    owner = Owner("Test")
    scheduler = Scheduler(owner)
    assert scheduler.get_todays_schedule() == []
    assert scheduler.detect_conflicts() == []
    assert scheduler.filter_tasks() == []
