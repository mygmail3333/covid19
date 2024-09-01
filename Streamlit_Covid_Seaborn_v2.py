import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np
import streamlit as st
import tempfile

# Load the dataset
state = "https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/cases_state.csv"
df_my = pd.read_csv(state)

# Convert the 'date' column to a datetime object and format it
df_my["date"] = pd.to_datetime(df_my["date"]).dt.strftime("%Y%m%d").astype('int64')

# Filter and rename columns
df0 = df_my.loc[:, ["state", "date", "cases_new", "cases_active"]]
df0.rename(columns={"state": "Age Group", "date": "Year", "cases_new": "New_Cases", "cases_active": "Active_Case"}, inplace=True)
df = df0.sort_values(by=["Age Group", "Year"], ascending=True)

# Create the figure for animation
fig, ax = plt.subplots(figsize=(15, 8))

def animate(year):
    ax.clear()
    filtered = df[df["Year"] == year]
    active_case = plt.barh(y=filtered["Age Group"], width=filtered["Active_Case"], color="red")
    ax.set_xlim(-10, 105_000)
    ax.bar_label(active_case, padding=3, labels=[f'{value}' for value in filtered['Active_Case']])

    for edge in ['top', 'right', 'bottom', 'left']:
        ax.spines[edge].set_visible(True)

    ax.tick_params(left=False)
    ax.get_xaxis().set_visible(True)
    ax.legend([active_case], ["Active_Case"])
    ax.set_title(f"Daily Active Covid-19 Cases in Malaysia dated {year} ", size=18, weight="bold")

# Generate the animation
animation = FuncAnimation(fig, animate, interval=50, frames=np.array(df.Year.unique()), repeat=False)

# Save the animation as a GIF using a temporary file
with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as tmpfile:
    animation.save(tmpfile.name, dpi=80, writer=PillowWriter(fps=5))

# Display the GIF in Streamlit
st.title("Daily Active COVID-19 Cases in Malaysia")
st.image(tmpfile.name)
