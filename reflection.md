# PawPal+ Project Reflection

## 1. System Design

**Three core user actions:**
1. Add a pet with basic info (name, species, age)
2. Schedule a care task for a pet (description, time, duration, priority, frequency)
3. View today's sorted schedule with conflict warnings and filtering

**a. Initial design**

I started with four classes mapped out in a Mermaid UML diagram:

- **Task** (dataclass): holds everything about a single care task -- description, time, duration, priority, frequency, due date, completion status, and pet name. Has a `mark_complete()` method.
- **Pet** (dataclass): stores the pet's name, species, age, and a list of tasks. Methods to add, remove, list, and count tasks.
- **Owner**: the top-level container with a name and list of pets. Methods to add a pet, look one up by name, and gather all tasks across all pets.
- **Scheduler**: takes an Owner reference and does the algorithmic work -- sorting by time, filtering, conflict detection, and handling task completion with recurrence.

The relationships are: Owner owns many Pets, each Pet has many Tasks, and Scheduler works through the Owner to reach everything.

**b. Design changes**

Yes. My original Task class did not have a `pet_name` field. I added it during skeleton design because conflict detection and filtering need to know which pet a task belongs to without walking back up the object graph. This keeps the Scheduler methods simpler -- they can work with flat lists of tasks and still produce messages like "Conflict: Buddy and Whiskers both have tasks at 09:00". I also added `due_date` to Task so recurring tasks can generate their next instance on the correct future date.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers time (tasks have a specific HH:MM slot), priority (high/medium/low), frequency (once/daily/weekly), and pet assignment. Time is the primary sort key because a pet owner's day revolves around when things happen, not just what's important. Priority matters for deciding what to do first when two tasks land at the same time, but the base sorting is chronological so the schedule reads like a timeline.

I decided time mattered most because the whole point is a daily plan you can follow in order. Priority becomes a tiebreaker and a filter, not the primary axis.

**b. Tradeoffs**

Conflict detection uses exact time matching (same HH:MM on same date) rather than full duration overlap checking. Two tasks at 08:00 and 08:15 would not be flagged even if the first one is 30 minutes long. I chose this because it keeps the logic simple and easy to reason about. For a pet care app, most conflicts are "I accidentally scheduled two things at the exact same time," not subtle overlaps. A full interval-overlap check would add complexity without much practical benefit for this use case. If I had more time I would upgrade to duration-aware overlap detection.

---

## 3. AI Collaboration

**a. How you used AI**

I used Claude Code (agent mode) for pretty much the entire build. I gave it the full project spec and let it work through each phase: UML design, class skeletons, full implementation, Streamlit UI, tests, and docs. The most useful part was having it run terminal commands directly. It wrote the code, ran `python main.py` to check output, ran `pytest` to catch failures, and pasted real terminal output into the README. That loop of write-run-fix inside one tool saved a ton of time.

The most helpful prompts were the ones that gave clear structure: "implement these four classes with these methods" rather than "build me a pet scheduler." Breaking the work into phases kept things focused.

Honestly, speed was the most noticeable advantage. Watching it write code, run it, fix it, and move on in seconds made the whole project feel way more productive than doing it all manually.

**b. Judgment and verification**

One thing I changed: Claude initially built the conflict detector to only check tasks within the same pet. I caught that the spec said "same pet or different pets" and had it update `detect_conflicts()` to look across all pets via `owner.get_all_tasks()`. The original version would have missed the Buddy/Whiskers 09:00 conflict that is the main demo scenario.

I verified by running the test suite after every change and checking that `main.py` output matched what I expected. If the conflict warning did not show up, I knew something was wrong.

There were also moments where I had to stop and read the generated code twice before accepting it. For example, I was not sure the conflict detection was actually working right at first. I had to trace through the logic myself to make sure it was catching conflicts across different pets and not just within one pet's tasks.

---

## 4. Testing and Verification

**a. What you tested**

I wrote 13 tests covering: mark_complete flipping a task's status, add_task increasing the count, chronological sorting of out-of-order tasks, daily recurrence creating a next-day task, weekly recurrence creating a next-week task, "once" tasks not recurring, conflict detection catching same-time tasks across different pets, no false positives when times differ, filtering by pet name, filtering by completion status, a pet with zero tasks, an owner with zero pets, and an empty schedule returning empty lists.

These tests matter because each one targets a specific behavior the scheduler promises. Without them, a small change to sorting or recurrence could silently break the whole daily plan.

**b. Confidence**

I'm fairly confident (4 out of 5) that the scheduler works correctly for the scenarios it handles. The main gap is duration-based overlap. Right now, two tasks at 08:00 and 08:15 would not be flagged as conflicting even if the first one runs 30 minutes. If I had more time I would also test tasks spanning midnight and tasks with invalid time formats.

---

## 5. Reflection

**a. What went well**

I am most satisfied with how the Scheduler class turned out. It pulls tasks across all pets through the Owner, so every algorithm (sorting, filtering, conflicts, recurrence) works at the whole-household level, not just one pet at a time. The test suite also came together well. Having 13 tests that cover the core behaviors and edge cases gives me real confidence that the logic is correct.

The thing I like most is how the Scheduler pulls tasks across all pets. It feels like the right design. One method call and you get every task for every pet, sorted and ready to go.

**b. What you would improve**

If I had another iteration I would upgrade conflict detection to check duration overlap instead of just exact time matches. I would also add a way to edit or delete tasks in the Streamlit UI (right now you can only add and complete). Persistence would be nice too so you don't lose everything on a page refresh.

I would also add a calendar view so you can see the whole week laid out instead of just today's list. That would make it feel more like a real planner.

**c. Key takeaway**

The biggest thing I learned is that being the "lead architect" with AI means you still have to understand the design. Claude Code wrote the code fast but I had to catch things like the cross-pet conflict check and make sure the class relationships actually made sense. The AI is a fast builder but not a substitute for thinking through the system design yourself. Breaking the project into phases (UML first, then skeletons, then implementation, then tests) kept things from getting messy.

Using AI is the smartest way to code right now. You learn faster than ever and you deploy faster than ever. But you still have to know what you're looking at. The speed only helps if you can tell when something is wrong.
