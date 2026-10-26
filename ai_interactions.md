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

> Compare two different prompts (or two different models) on the same task.

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | | |
| **Prompt** | | |
| **Response summary** | | |
| **What was useful** | | |
| **Problems noticed** | | |
| **Decision** | | |

**Which approach did you use in your final implementation and why?**

<!-- Your conclusion -->
