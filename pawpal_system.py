from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional


@dataclass
class Task:
    """Represents a single pet care task with scheduling info."""
    description: str
    time: str  # "HH:MM" format
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    frequency: str = "once"  # "once", "daily", "weekly"
    due_date: date = field(default_factory=date.today)
    completed: bool = False
    pet_name: str = ""

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True


@dataclass
class Pet:
    """Represents a pet with its care tasks."""
    name: str
    species: str
    age: int
    tasks: list = field(default_factory=list)

    def add_task(self, task):
        """Add a task to this pet's task list."""
        task.pet_name = self.name
        self.tasks.append(task)

    def remove_task(self, task):
        """Remove a task from this pet's task list."""
        self.tasks.remove(task)

    def get_tasks(self):
        """Return all tasks for this pet."""
        return list(self.tasks)

    def task_count(self):
        """Return the number of tasks for this pet."""
        return len(self.tasks)


class Owner:
    """Represents a pet owner who manages multiple pets."""

    def __init__(self, name):
        """Initialize an owner with a name and empty pet list."""
        self.name = name
        self.pets = []

    def add_pet(self, pet):
        """Add a pet to the owner's collection."""
        self.pets.append(pet)

    def get_pet(self, name):
        """Find and return a pet by name, or None if not found."""
        for pet in self.pets:
            if pet.name == name:
                return pet
        return None

    def get_all_tasks(self):
        """Gather and return all tasks across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    """Manages scheduling, sorting, filtering, and conflict detection for an owner's pets."""

    def __init__(self, owner):
        """Initialize the scheduler with an owner reference."""
        self.owner = owner

    def get_todays_schedule(self):
        """Return all tasks due today, sorted by time."""
        today = date.today()
        todays_tasks = [t for t in self.owner.get_all_tasks()
                        if t.due_date == today and not t.completed]
        return self.sort_by_time(todays_tasks)

    def sort_by_time(self, tasks):
        """Sort tasks by their scheduled time (HH:MM string parsed to minutes)."""
        def time_to_minutes(t):
            hours, minutes = t.time.split(":")
            return int(hours) * 60 + int(minutes)
        return sorted(tasks, key=time_to_minutes)

    def filter_tasks(self, pet_name=None, completed=None):
        """Filter all tasks by pet name and/or completion status."""
        tasks = self.owner.get_all_tasks()
        if pet_name is not None:
            tasks = [t for t in tasks if t.pet_name == pet_name]
        if completed is not None:
            tasks = [t for t in tasks if t.completed == completed]
        return tasks

    def detect_conflicts(self):
        """Return a list of warning strings for tasks that share the same date and time."""
        warnings = []
        all_tasks = self.owner.get_all_tasks()
        seen = {}
        for task in all_tasks:
            key = (task.due_date, task.time)
            if key in seen:
                other = seen[key]
                warnings.append(
                    f"Conflict: '{task.description}' ({task.pet_name}) and "
                    f"'{other.description}' ({other.pet_name}) are both at "
                    f"{task.time} on {task.due_date}"
                )
            else:
                seen[key] = task
        return warnings

    def mark_task_complete(self, task):
        """Mark a task complete and create the next instance if recurring."""
        task.mark_complete()
        if task.frequency == "once":
            return None
        pet = self.owner.get_pet(task.pet_name)
        if pet is None:
            return None
        if task.frequency == "daily":
            next_date = task.due_date + timedelta(days=1)
        elif task.frequency == "weekly":
            next_date = task.due_date + timedelta(weeks=1)
        else:
            return None
        new_task = Task(
            description=task.description,
            time=task.time,
            duration_minutes=task.duration_minutes,
            priority=task.priority,
            frequency=task.frequency,
            due_date=next_date,
            completed=False,
            pet_name=task.pet_name,
        )
        pet.add_task(new_task)
        return new_task
