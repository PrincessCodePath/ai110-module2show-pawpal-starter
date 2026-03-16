import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value=st.session_state.owner.name)
st.session_state.owner.name = owner_name

pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
if st.button("Add pet"):
    p = Pet(pet_name.strip(), species)
    st.session_state.owner.add_pet(p)
    st.rerun()

pets = st.session_state.owner.get_pets()
if pets:
    st.caption(f"Pets: {', '.join(f'{p.name} ({p.species})' for p in pets)}")

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if pets:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        task_time = st.text_input("Time", value="09:00")
    with col3:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col4:
        priority_label = st.selectbox("Priority", ["high", "medium", "low"], index=0)
    priority_map = {"high": 1, "medium": 2, "low": 3}
    selected_pet = st.selectbox("Pet", options=pets, format_func=lambda p: f"{p.name} ({p.species})")
    if st.button("Add task"):
        task = Task(task_title.strip(), task_time, int(duration), priority_map[priority_label], pet=selected_pet)
        selected_pet.add_task(task)
        st.rerun()

    all_tasks = st.session_state.owner.get_all_tasks()
    if all_tasks:
        st.write("Current tasks:")
        rows = [{"Time": t.time, "Task": t.description, "Pet": t.pet.name if t.pet else "", "Mins": t.duration_mins, "Priority": t.priority} for t in all_tasks]
        st.table(rows)
    else:
        st.info("No tasks yet. Add one above.")
else:
    st.info("Add a pet above first.")

st.divider()

st.subheader("Build Schedule")
scheduler = Scheduler(st.session_state.owner)
if st.button("Generate schedule"):
    plan = scheduler.generate_daily_plan()
    if plan:
        st.write("Today's Schedule")
        for t in plan:
            pet_name = t.pet.name if t.pet else ""
            st.write(f"  {t.time} — {t.description} ({pet_name}) — {t.duration_mins} min")
    else:
        st.info("No tasks to schedule. Add pets and tasks above.")
