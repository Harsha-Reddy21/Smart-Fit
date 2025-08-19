import streamlit as st
import requests
import os 
from datetime import date as dt_date
from dotenv import load_dotenv
load_dotenv()

API_BASE = os.getenv("API_BASE") or os.getenv("api_base", "http://127.0.0.1:8000")

st.set_page_config(page_title="SmartFit Chat")

if "session" not in st.session_state:
    st.session_state.session = None

st.title("SmartFit – Minimal")

with st.sidebar:
    st.subheader("Auth")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    email = st.text_input("Email (for register)")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            try:
                resp = requests.post(f"{API_BASE}/auth/login", json={"username": username, "password": password})
                resp.raise_for_status()
                st.session_state.session = resp.json()
                st.success("Logged in")
            except Exception as e:
                st.error(f"Login failed: {e}")
    with col2:
        if st.button("Register"):
            try:
                payload = {
                    "username": username,
                    "email": email or f"{username}@example.com",
                    "password": password,
                }
                resp = requests.post(f"{API_BASE}/auth/register", json=payload)
                resp.raise_for_status()
                st.success("Registered. Click Login.")
            except Exception as e:
                st.error(f"Register failed: {e}")

st.divider()

if st.session_state.session:
    user_id = st.session_state.session.get("user_id")
    st.caption(f"Logged in as {st.session_state.session.get('username')} (id={user_id})")
    st.subheader("Chat")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    question = st.text_input("Ask about workouts, nutrition, recovery…")
    if st.button("Ask") and question:
        try:
            resp = requests.post(f"{API_BASE}/chat/ask", params={"user_id": user_id, "question": question})
            resp.raise_for_status()
            answer = resp.json()["answer"]
            st.session_state.chat.insert(0, {"q": question, "a": answer})
        except Exception as e:
            st.error(f"Ask failed: {e}")

    for idx, item in enumerate(st.session_state.chat):
        with st.expander(f"Q: {item['q']}", expanded=(idx == 0)):
            st.write(item["a"])

    st.subheader("Recent Messages")
    try:
        resp = requests.get(f"{API_BASE}/chat/history/{user_id}")
        resp.raise_for_status()
        history = resp.json()
        for msg in history[:10]:
            st.markdown(f"- {msg['created_at']}: {msg['question']}")
    except Exception:
        pass

    st.divider()

    st.subheader("Workouts")
    workouts = []
    try:
        w_resp = requests.get(f"{API_BASE}/workouts")
        w_resp.raise_for_status()
        workouts = w_resp.json() or []
    except Exception as e:
        st.warning(f"Could not load workouts: {e}")

    selected_workout = None
    if workouts:
        selected_workout = st.selectbox(
            "Select a workout plan (optional)",
            workouts,
            format_func=lambda w: f"{w['plan_name']} (#{w['id']})"
        )
        with st.expander("Selected workout details", expanded=False):
            st.json({k: v for k, v in selected_workout.items() if k != "id"})
    else:
        st.info("No workouts available yet.")

    st.subheader("Log a Workout")
    with st.form("log_workout_form"):
        log_date = st.date_input("Date", value=dt_date.today())
        exercises_completed = st.text_area("Exercises completed (comma-separated)")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            sets = st.number_input("Sets", min_value=0, step=1, value=0)
        with col_b:
            reps = st.number_input("Reps", min_value=0, step=1, value=0)
        with col_c:
            duration = st.number_input("Duration (min)", min_value=0, step=1, value=0)
        weights = st.text_input("Weights (e.g., 20kg, 25kg)")
        calories_burned = st.number_input("Calories burned", min_value=0, step=10, value=0)
        submit_log = st.form_submit_button("Add to Progress")
    if submit_log:
        payload = {
            "user_id": user_id,
            "workout_id": selected_workout["id"] if isinstance(selected_workout, dict) else None,
            "date": log_date.isoformat(),
            "exercises_completed": exercises_completed or None,
            "sets": int(sets) if sets else None,
            "reps": int(reps) if reps else None,
            "weights": weights or None,
            "duration": int(duration) if duration else None,
            "calories_burned": int(calories_burned) if calories_burned else None,
        }
        try:
            pr = requests.post(f"{API_BASE}/progress", json=payload)
            pr.raise_for_status()
            st.success("Workout logged to your progress.")
        except Exception as e:
            st.error(f"Failed to log workout: {e}")

    st.subheader("Your Progress")
    try:
        p_resp = requests.get(f"{API_BASE}/progress", params={"user_id": user_id})
        p_resp.raise_for_status()
        progress_items = p_resp.json() or []
        if progress_items:
            # Show a compact table
            import pandas as pd
            df = pd.DataFrame(progress_items)
            df = df[[
                "date",
                "workout_id",
                "exercises_completed",
                "sets",
                "reps",
                "weights",
                "duration",
                "calories_burned",
            ]]
            st.dataframe(df.sort_values(by="date", ascending=False), use_container_width=True)
        else:
            st.info("No progress logged yet. Use the form above to add your first entry.")
    except Exception as e:
        st.error(f"Failed to load progress: {e}")
else:
    st.info("Use the sidebar to register or log in.")


