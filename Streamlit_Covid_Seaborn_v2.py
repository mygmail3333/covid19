import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np
import tempfile

# Sample data for testing
data = {
    'Age Group': ['Selangor', 'Penang', 'Johor'],
    'Year': [20230101, 20230101, 20230101],
    'Active_Case': [1000, 1500, 1200]
}

df = pd.DataFrame(data)

# Create the figure for animation
fig, ax = plt.subplots(figsize=(8, 4))

def animate(year):
    ax.clear()
    filtered = df[df["Year"] == year]
    active_case = ax.barh(filtered["Age Group"], filtered["Active_Case"], color="red")
    ax.set_xlim(-10, 2000)
    ax.set_title(f"Active COVID-19 Cases in Malaysia - Year {year}")

animation = FuncAnimation(fig, animate, frames=[20230101], repeat=False)

# Save the animation as a GIF
with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as tmpfile:
    animation.save(tmpfile.name, writer=PillowWriter(fps=2))

# Display the GIF in Streamlit
st.image(tmpfile.name)
