# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
=== Today's Schedule for Andres (2026-10-25) ===

  07:30 - Feed breakfast (Whiskers, 10 min) [priority: high] [Pending]
  08:00 - Morning walk (Buddy, 30 min) [priority: high] [Pending]
  09:00 - Flea medication (Buddy, 5 min) [priority: high] [Pending]
  09:00 - Play session (Whiskers, 15 min) [priority: low] [Pending]
  12:00 - Litter box clean (Whiskers, 10 min) [priority: medium] [Pending]
  17:00 - Evening walk (Buddy, 30 min) [priority: medium] [Pending]

=== Buddy's Tasks ===

  17:00 - Evening walk [medium]
  08:00 - Morning walk [high]
  09:00 - Flea medication [high]

=== Incomplete Tasks Only ===

  17:00 - Evening walk (Buddy) [medium]
  08:00 - Morning walk (Buddy) [high]
  09:00 - Flea medication (Buddy) [high]
  07:30 - Feed breakfast (Whiskers) [high]
  12:00 - Litter box clean (Whiskers) [medium]
  09:00 - Play session (Whiskers) [low]

=== Marking 'Morning walk' as complete ===
  Completed: Morning walk on 2026-10-25
  Next instance created: Morning walk on 2026-10-26

=== Conflict Warnings ===

  ⚠ Conflict: 'Play session' (Whiskers) and 'Flea medication' (Buddy) are both at 09:00 on 2026-10-25
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts tasks chronologically by parsing "HH:MM" into total minutes for comparison. |
| Filtering | `Scheduler.filter_tasks()` | Filters tasks by pet name and/or completion status across all pets. |
| Conflict handling | `Scheduler.detect_conflicts()` | Flags tasks that share the same date and time, even across different pets. |
| Recurring tasks | `Scheduler.mark_task_complete()` | Marks a task done and auto-creates the next instance for daily (+1 day) or weekly (+7 days) tasks. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
