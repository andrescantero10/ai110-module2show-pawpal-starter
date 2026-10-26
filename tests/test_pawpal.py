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
