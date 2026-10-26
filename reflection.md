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

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
