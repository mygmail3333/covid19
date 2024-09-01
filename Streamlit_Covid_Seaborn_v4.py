import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np
import streamlit as st
import tempfile

# Load the dataset
state = "https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/cases_state.csv"
df_my = pd.read_csv(state)

# Convert the 'date' column to a datetime object and format it as YYYYMM
df_my["date"] = pd.to_datetime(df_my["date"]).dt.strftime("%Y%m").astype('int64')

# Prepare the data
data = df_my.loc[:, ["state", "date", "cases_new", "cases_recovered"]]
data.rename(columns={"state": "State", "date": "Month", "cases_new": "New_Cases", "cases_recovered": "Recover_Cases"}, inplace=True)
df = data.groupby(["State", "Month"]).agg({'New_Cases': 'sum', 'Recover_Cases': 'sum'}).sort_values(by=["State", "Month"], ascending=True).reset_index()
df["Recover_Cases"] = df["Recover_Cases"] * -1

# Create the figure for animation
fig, ax = plt.subplots(figsize=(10, 6))

def animate(month):
    ax.clear()
    filtered = df[df["Month"] == month]
    new_cases = ax.barh(y=filtered["State"], width=filtered["New_Cases"], color="red")
    recover_cases = ax.barh(y=filtered["State"], width=filtered["Recover_Cases"], color="green")
    ax.set_xlim(-300_000, 300_000)
    ax.bar_label(new_cases, padding=3, labels=[f'{value:,}' for value in filtered['New_Cases']])
    ax.bar_label(recover_cases, padding=3, labels=[f'{-1*value:,}' for value in filtered['Recover_Cases']])

    for edge in ['top', 'right', 'bottom', 'left']:
        ax.spines[edge].set_visible(False)

    ax.tick_params(left=False)
    ax.get_xaxis().set_visible(False)
    ax.legend([new_cases, recover_cases], ["New_Cases", "Recover_Cases"])
    ax.set_title(f"Monthly New Vs Recover Covid-19 Cases in Malaysia, {month} Month", size=14, weight="bold")

# Generate the animation
animation = FuncAnimation(fig, animate, interval=1000, frames=np.array(df['Month'].unique()), repeat=False)

# Save the animation as a GIF using a temporary file
with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as tmpfile:
    animation.save(tmpfile.name, dpi=80, writer=PillowWriter(fps=1))

# Display the GIF in Streamlit
st.title("Monthly New and Recovered COVID-19 Cases in Malaysia")
st.image(tmpfile.name)
