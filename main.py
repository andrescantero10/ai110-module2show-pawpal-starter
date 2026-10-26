from datetime import date
from tabulate import tabulate
from pawpal_system import Task, Pet, Owner, Scheduler

# Emoji mappings
PRIORITY_EMOJI = {"high": "🔴", "medium": "🟡", "low": "🟢"}
SPECIES_EMOJI = {"dog": "🐶", "cat": "🐱", "bird": "🐦", "rabbit": "🐰"}


def status_icon(completed):
    return "✅" if completed else "⏳"


def priority_label(priority):
    return f"{PRIORITY_EMOJI.get(priority, '')} {priority}"


def main():
    # Create owner and pets
    owner = Owner("Andres")
    buddy = Pet(name="Buddy", species="dog", age=3)
    whiskers = Pet(name="Whiskers", species="cat", age=5)
    owner.add_pet(buddy)
    owner.add_pet(whiskers)

    # Add tasks (out of order on purpose)
    buddy.add_task(Task("Evening walk", "17:00", 30, "medium", "daily", date.today()))
    buddy.add_task(Task("Morning walk", "08:00", 30, "high", "daily", date.today()))
    buddy.add_task(Task("Flea medication", "09:00", 5, "high", "once", date.today()))
    whiskers.add_task(Task("Feed breakfast", "07:30", 10, "high", "daily", date.today()))
    whiskers.add_task(Task("Litter box clean", "12:00", 10, "medium", "weekly", date.today()))
    whiskers.add_task(Task("Play session", "09:00", 15, "low", "daily", date.today()))

    scheduler = Scheduler(owner)

    # Today's schedule (sorted by time) as a table
    print(f"\n{'='*60}")
    print(f"  Today's Schedule for {owner.name} ({date.today()})")
    print(f"{'='*60}\n")
    schedule = scheduler.get_todays_schedule()
    table_rows = []
    for task in schedule:
        emoji = SPECIES_EMOJI.get(
            next((p.species for p in owner.pets if p.name == task.pet_name), ""), ""
        )
        table_rows.append([
            task.time,
            task.description,
            f"{emoji} {task.pet_name}",
            f"{task.duration_minutes} min",
            priority_label(task.priority),
            status_icon(task.completed),
        ])
    print(tabulate(table_rows,
                   headers=["Time", "Task", "Pet", "Duration", "Priority", "Status"],
                   tablefmt="rounded_grid"))

    # Filter by pet
    print(f"\n--- Buddy's Tasks ---\n")
    buddy_rows = []
    for task in scheduler.filter_tasks(pet_name="Buddy"):
        buddy_rows.append([task.time, task.description, priority_label(task.priority)])
    print(tabulate(buddy_rows, headers=["Time", "Task", "Priority"], tablefmt="rounded_grid"))

    print(f"\n--- Incomplete Tasks Only ---\n")
    incomplete_rows = []
    for task in scheduler.filter_tasks(completed=False):
        incomplete_rows.append([task.time, task.description, task.pet_name, priority_label(task.priority)])
    print(tabulate(incomplete_rows, headers=["Time", "Task", "Pet", "Priority"], tablefmt="rounded_grid"))

    # Mark a daily task complete and show recurrence
    morning_walk = buddy.get_tasks()[1]  # Morning walk (sorted by add order)
    print(f"\n--- Marking '{morning_walk.description}' as complete ---")
    new_task = scheduler.mark_task_complete(morning_walk)
    print(f"  ✅ Completed: {morning_walk.description} on {morning_walk.due_date}")
    if new_task:
        print(f"  ⏳ Next instance created: {new_task.description} on {new_task.due_date}")

    # Priority-based sorting
    print(f"\n--- Schedule Sorted by Priority ---\n")
    all_tasks = [t for t in owner.get_all_tasks() if not t.completed]
    priority_sorted = scheduler.sort_by_priority_then_time(all_tasks)
    prio_rows = []
    for task in priority_sorted:
        prio_rows.append([priority_label(task.priority), task.time, task.description, task.pet_name])
    print(tabulate(prio_rows, headers=["Priority", "Time", "Task", "Pet"], tablefmt="rounded_grid"))

    # Conflict detection (Buddy's flea med and Whiskers' play session both at 09:00)
    print(f"\n--- Conflict Warnings ---\n")
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            print(f"  ⚠️  {warning}")
    else:
        print("  No conflicts detected.")

    print()


if __name__ == "__main__":
    main()
