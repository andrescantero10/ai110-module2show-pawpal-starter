# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked Claude Code to add a `find_next_available_slot(date, duration_minutes, start, end)` method to the Scheduler class. The method should scan all existing tasks on a given date and find the first gap that fits the requested duration, within a configurable window (default 08:00 to 21:00).

**What did the agent do?**

- **Files modified:** `pawpal_system.py` (added the method), `tests/test_pawpal.py` (added 3 tests)
- The agent added the method to `Scheduler` in `pawpal_system.py`. It converts "HH:MM" times to minutes, builds a sorted list of occupied intervals from existing tasks, then walks through the day looking for the first gap that fits the duration.
- It wrote three tests: one for finding a slot between two tasks, one for a fully booked day returning `None`, and one for an empty day returning the start time.
- It ran `python -m pytest -v` to confirm all 16 tests pass.

**What did you have to verify or fix manually?**

The implementation was correct on the first pass. I verified the logic by checking the basic test case: with a 30-min walk at 08:00 and a 15-min feed at 09:00, a 20-min slot should fit at 08:30 (right after the walk ends). The test confirmed this. No manual fixes were needed for this feature.

---

## Prompt Comparison (SF11)

> Comparing Claude Code vs another model on the recurring-task rescheduling logic.

| | Option A (Claude Code) | Option B |
|-|------------------------|----------|
| **Model / tool used** | Claude Opus 4.6 (Claude Code agent mode) | <!-- ANDRES: run this prompt in ChatGPT or Gemini and fill in the model name --> |
| **Prompt** | "Implement `mark_task_complete(task)` in the Scheduler class. When a task is marked complete: set completed=True. If frequency is 'daily', create a new Task with due_date + 1 day on the same pet. If 'weekly', due_date + 7 days. If 'once', do nothing extra. Return the new task or None." | <!-- ANDRES: use the same prompt above in ChatGPT/Gemini and paste the exact prompt you used --> |
| **Response summary** | Claude implemented it in one pass: calls `task.mark_complete()`, checks frequency, uses `timedelta(days=1)` or `timedelta(weeks=1)`, creates a new Task dataclass instance with all the same fields except due_date and completed=False, and calls `pet.add_task()` to attach it to the right pet. Returns the new task or None. | <!-- ANDRES: summarize what the other model generated --> |
| **What was useful** | The implementation correctly looked up the pet via `owner.get_pet(task.pet_name)` so it could call `pet.add_task()` on the right pet. It also returned the new task so the caller can display it. | <!-- ANDRES: what was useful about the other model's response --> |
| **Problems noticed** | None. The code worked on the first try and all recurrence tests passed. | <!-- ANDRES: any issues with the other model's response --> |
| **Decision** | Used Claude's implementation as-is. | <!-- ANDRES: which one did you prefer and why --> |

**Which approach did you use in your final implementation and why?**

I used Claude Code's implementation because it worked correctly on the first pass and handled the pet lookup cleanly through the Owner object. <!-- ANDRES: after running the prompt in the other model, update this conclusion with your comparison -->
