from datetime import date
from pawpal_system import Task, Pet, Owner, Scheduler


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

    # Today's schedule (sorted by time)
    print(f"=== Today's Schedule for {owner.name} ({date.today()}) ===\n")
    schedule = scheduler.get_todays_schedule()
    for task in schedule:
        status = "Done" if task.completed else "Pending"
        print(f"  {task.time} - {task.description} ({task.pet_name}, "
              f"{task.duration_minutes} min) [priority: {task.priority}] [{status}]")

    # Filter by pet
    print(f"\n=== Buddy's Tasks ===\n")
    for task in scheduler.filter_tasks(pet_name="Buddy"):
        print(f"  {task.time} - {task.description} [{task.priority}]")

    print(f"\n=== Incomplete Tasks Only ===\n")
    for task in scheduler.filter_tasks(completed=False):
        print(f"  {task.time} - {task.description} ({task.pet_name}) [{task.priority}]")

    # Mark a daily task complete and show recurrence
    morning_walk = buddy.get_tasks()[1]  # Morning walk (sorted by add order)
    print(f"\n=== Marking '{morning_walk.description}' as complete ===")
    new_task = scheduler.mark_task_complete(morning_walk)
    print(f"  Completed: {morning_walk.description} on {morning_walk.due_date}")
    if new_task:
        print(f"  Next instance created: {new_task.description} on {new_task.due_date}")

    # Priority-based sorting
    print(f"\n=== Schedule Sorted by Priority ===\n")
    all_tasks = [t for t in owner.get_all_tasks() if not t.completed]
    priority_sorted = scheduler.sort_by_priority_then_time(all_tasks)
    for task in priority_sorted:
        print(f"  [{task.priority.upper()}] {task.time} - {task.description} ({task.pet_name})")

    # Conflict detection (Buddy's flea med and Whiskers' play session both at 09:00)
    print(f"\n=== Conflict Warnings ===\n")
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            print(f"  ⚠ {warning}")
    else:
        print("  No conflicts detected.")

    print()


if __name__ == "__main__":
    main()
