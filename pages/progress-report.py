import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime

# Load the mock data
@st.cache_data
def load_data():
    return pd.read_csv("mock_data.csv", parse_dates=['datetime'])

df = load_data()
df = df[df["task"].isin(["Brush teeth", "Take meds", "Eat breakfast"])]

# Preprocess
st.title("📊 StepSense: Daily Routine Progress Dashboard")

st.sidebar.header("🔍 Filters")
date_range = st.sidebar.date_input("Select date range", [df["datetime"].min(), df["datetime"].max()])
selected_tasks = st.sidebar.multiselect("Filter by task", df["task"].unique(), default=list(df["task"].unique()))

# Filter data based on selections
filtered_df = df[
    (df["datetime"].dt.date >= date_range[0]) &
    (df["datetime"].dt.date <= date_range[1]) &
    (df["task"].isin(selected_tasks))
]

st.subheader("✅ Task Completion Timeline")
task_order = df['task'].unique().tolist()
task_timeline = alt.Chart(filtered_df).mark_circle(size=100).encode(
    x='datetime:T',
    y=alt.Y('task:N', sort=task_order),
    color=alt.Color('task_completed:N', scale=alt.Scale(domain=[True, False], range=['green', 'red'])),
    tooltip=['datetime', 'task', 'task_completed']
).interactive()
st.altair_chart(task_timeline, use_container_width=True)

st.subheader("📈 Sentiment Over Time")
sentiment_chart = alt.Chart(filtered_df).mark_line(point=True).encode(
    x='datetime:T',
    y=alt.Y('sentiment:N', sort=['Negative', 'Neutral', 'Positive']),
    color='sentiment:N',
    tooltip=['datetime', 'task', 'sentiment']
).interactive()
st.altair_chart(sentiment_chart, use_container_width=True)

st.subheader("🕒 Response Delay Over Time Between Sequential Tasks")

# Ensure data is sorted by datetime
sequential_df = filtered_df.sort_values(by="datetime")

# Map tasks to ensure ordering
task_order_map = {"Brush teeth": 1, "Take meds": 2, "Eat breakfast": 3}
sequential_df["task_order"] = sequential_df["task"].map(task_order_map)

# Calculate delays for each valid sequence
delays = []
for date, group in sequential_df.groupby(sequential_df["datetime"].dt.date):
    group = group.sort_values("task_order")
    for i in range(1, 3):
        task1 = i
        task2 = i + 1
        df1 = group[group["task_order"] == task1]
        df2 = group[group["task_order"] == task2]
        if not df1.empty and not df2.empty:
            t1 = df1.iloc[0]["datetime"]
            t2 = df2.iloc[0]["datetime"]
            delay = (t2 - t1).total_seconds()
            if delay > 0:
                delays.append({
                    "date": t2,
                    "interval": f"{df1.iloc[0]['task']} → {df2.iloc[0]['task']}",
                    "delay_sec": delay
                })

delay_df = pd.DataFrame(delays)
if not delay_df.empty:
    delay_chart = alt.Chart(delay_df).mark_line(point=True).encode(
        x='date:T',
        y='delay_sec:Q',
        color='interval:N',
        tooltip=['date', 'interval', 'delay_sec']
    ).interactive()
    st.altair_chart(delay_chart, use_container_width=True)
else:
    st.info("Not enough data to display delay chart.")

st.subheader("💬 Common User Phrases")
phrase_counts = filtered_df['user_phrase'].value_counts().reset_index()
phrase_counts.columns = ['phrase', 'count']

# Create a bar chart visualization for user phrases
phrase_chart = alt.Chart(phrase_counts).mark_bar().encode(
    x=alt.X('phrase:N', sort='-y', title='User Phrases'),
    y=alt.Y('count:Q', title='Count'),
    tooltip=['phrase:N', 'count:Q']
).properties(
    title='Common User Phrases'
).interactive()

st.altair_chart(phrase_chart, use_container_width=True)

st.subheader("🤖 AI-Generated Insight (Mock)")
st.markdown("""
- You’ve shown the highest engagement with the **'Eat Breakfast'** task.
- Your **morning sentiment** tends to be **positive**, but it dips slightly by late afternoon.
- Consider shifting skipped tasks to your most active time: **7–9am**.
- Great streak on Tuesday and Wednesday — keep it going!
""")