import streamlit as st
from datetime import date
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.markdown("A pet care planning assistant that helps you schedule and manage tasks for your pets.")

# Initialize session state
if "owner" not in st.session_state:
    st.session_state.owner = Owner("My Owner")

owner = st.session_state.owner
scheduler = Scheduler(owner)

# Owner name
owner_name = st.text_input("Owner name", value=owner.name)
owner.name = owner_name

st.divider()

# Add Pet section
st.subheader("🐶 Add a Pet")
col1, col2, col3 = st.columns(3)
with col1:
    new_pet_name = st.text_input("Pet name", value="")
with col2:
    new_pet_species = st.selectbox("Species", ["dog", "cat", "bird", "rabbit", "other"])
with col3:
    new_pet_age = st.number_input("Age", min_value=0, max_value=30, value=1)

if st.button("Add Pet"):
    if new_pet_name.strip():
        if owner.get_pet(new_pet_name.strip()) is None:
            owner.add_pet(Pet(name=new_pet_name.strip(), species=new_pet_species, age=new_pet_age))
            st.success(f"Added {new_pet_name}!")
            st.rerun()
        else:
            st.warning(f"A pet named '{new_pet_name}' already exists.")
    else:
        st.warning("Please enter a pet name.")

# Show current pets
if owner.pets:
    st.markdown("**Your Pets:** " + ", ".join(f"{p.name} ({p.species}, age {p.age})" for p in owner.pets))
else:
    st.info("No pets yet. Add one above.")

st.divider()

# Add Task section
if owner.pets:
    st.subheader("📋 Add a Task")
    pet_names = [p.name for p in owner.pets]

    col1, col2 = st.columns(2)
    with col1:
        task_pet = st.selectbox("For which pet?", pet_names)
        task_desc = st.text_input("Task description", value="Morning walk")
        task_priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col2:
        task_time = st.text_input("Time (HH:MM)", value="08:00")
        task_duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        task_frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

    if st.button("Add Task"):
        if task_desc.strip() and task_time.strip():
            pet = owner.get_pet(task_pet)
            new_task = Task(
                description=task_desc.strip(),
                time=task_time.strip(),
                duration_minutes=int(task_duration),
                priority=task_priority,
                frequency=task_frequency,
                due_date=date.today(),
            )
            pet.add_task(new_task)
            st.success(f"Added '{task_desc}' for {task_pet}!")
            st.rerun()

    st.divider()

    # Today's Schedule
    st.subheader("📅 Today's Schedule")

    # Filters
    filter_col1, filter_col2 = st.columns(2)
    with filter_col1:
        filter_pet = st.selectbox("Filter by pet", ["All"] + pet_names)
    with filter_col2:
        filter_status = st.selectbox("Filter by status", ["All", "Pending", "Completed"])

    # Build filtered task list
    pet_filter = None if filter_pet == "All" else filter_pet
    completed_filter = None
    if filter_status == "Pending":
        completed_filter = False
    elif filter_status == "Completed":
        completed_filter = True

    filtered = scheduler.filter_tasks(pet_name=pet_filter, completed=completed_filter)
    sorted_tasks = scheduler.sort_by_time(filtered)

    if sorted_tasks:
        table_data = []
        for t in sorted_tasks:
            status = "✅" if t.completed else "⏳"
            table_data.append({
                "Time": t.time,
                "Task": t.description,
                "Pet": t.pet_name,
                "Duration": f"{t.duration_minutes} min",
                "Priority": t.priority,
                "Frequency": t.frequency,
                "Status": status,
            })
        st.table(table_data)

        # Mark complete
        st.subheader("✔️ Mark Task Complete")
        incomplete = [t for t in sorted_tasks if not t.completed]
        if incomplete:
            task_options = {f"{t.time} - {t.description} ({t.pet_name})": t for t in incomplete}
            selected_label = st.selectbox("Select a task to complete", list(task_options.keys()))
            if st.button("Mark Complete"):
                selected_task = task_options[selected_label]
                new_task = scheduler.mark_task_complete(selected_task)
                st.success(f"Marked '{selected_task.description}' as complete!")
                if new_task:
                    st.info(f"Recurring task: next '{new_task.description}' scheduled for {new_task.due_date}")
                st.rerun()
        else:
            st.success("All tasks are complete!")
    else:
        st.info("No tasks match the current filters.")

    # Conflict warnings
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            st.warning(f"⚠️ {warning}")
