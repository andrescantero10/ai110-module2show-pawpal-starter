from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional


@dataclass
class Task:
    description: str
    time: str  # "HH:MM" format
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    frequency: str = "once"  # "once", "daily", "weekly"
    due_date: date = field(default_factory=date.today)
    completed: bool = False
    pet_name: str = ""

    def mark_complete(self):
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: list = field(default_factory=list)

    def add_task(self, task):
        pass

    def remove_task(self, task):
        pass

    def get_tasks(self):
        pass

    def task_count(self):
        pass


class Owner:
    def __init__(self, name):
        self.name = name
        self.pets = []

    def add_pet(self, pet):
        pass

    def get_pet(self, name):
        pass

    def get_all_tasks(self):
        pass


class Scheduler:
    def __init__(self, owner):
        self.owner = owner

    def get_todays_schedule(self):
        pass

    def sort_by_time(self, tasks):
        pass

    def filter_tasks(self, pet_name=None, completed=None):
        pass

    def detect_conflicts(self):
        pass

    def mark_task_complete(self, task):
        pass
