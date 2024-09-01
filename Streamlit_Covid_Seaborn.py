import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import datetime, timedelta

# Load data
state = "https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/cases_state.csv"
df = pd.read_csv(state)

# Data processing
df['date'] = pd.to_datetime(df['date'])
df = df.apply(lambda x: x.replace({'W.P. Kuala Lumpur': 'Kuala Lumpur',
                                   'W.P. Labuan': 'Labuan',
                                   'W.P. Putrajaya': 'Putrajaya '}))

seven_days_ago = df['date'].max() - timedelta(days=7)
df_last_7_days = df[df['date'] > seven_days_ago]

df1 = df_last_7_days.groupby(["state"]).agg({'cases_new': 'sum'}).reset_index()
df_7_day_average = df_last_7_days.groupby(["state"]).agg({'cases_new': 'mean'}).reset_index().round({'cases_new': 0})

total_7days_average = df_7_day_average.cases_new.sum().astype("int64")
total_7days = df1.cases_new.sum()

df2 = df_last_7_days.groupby(['state', df['date'].dt.date])["cases_new"].sum().unstack().reset_index()

# Display data in Streamlit
st.write("COVID-19 Data for the Last 7 Days:")
st.write(df1)
st.write("7-Day Averages by State:")
st.write(df_7_day_average)
st.write(f"Total 7-day average: {total_7days_average}")
st.write(f"Total cases in the last 7 days: {total_7days}")
st.write(df2)

# PLOT GRAPH
fig, axs = plt.subplots(3, 1, figsize=(19.20, 10.80))

# First plot (total cases)
sns.barplot(x=df1["state"], y=df1["cases_new"], color='lightgreen', ax=axs[0])
axs[0].set_title(f"TOTAL LAST 7 DAYS NEW COVID-19 CASES BY STATE: {total_7days}", fontsize=15)
axs[0].set_ylabel("Number of New Cases", fontsize=12)
axs[0].set_xlabel("State", fontsize=12)
axs[0].grid()

# Annotate bars
for i, value in enumerate(df1["cases_new"]):
    axs[0].text(i, value + 5, f'{value:.0f}', ha='center', va='bottom')

# Second plot (average cases)
sns.barplot(x=df_7_day_average["state"], y=df_7_day_average["cases_new"], color='lightgreen', ax=axs[1])
axs[1].set_title(f"7-DAY AVERAGE COVID-19 CASES BY STATE: {total_7days_average}", fontsize=15)
axs[1].set_ylabel("Number of New Cases", fontsize=12)
axs[1].set_xlabel("State", fontsize=12)
axs[1].grid()

# Annotate bars
for i, value in enumerate(df_7_day_average["cases_new"]):
    axs[1].text(i, value + 5, f'{value:.0f}', ha='center', va='bottom')

# Third plot (daily breakdown)
df_melted = pd.melt(df2, id_vars='state', var_name='date', value_name='cases_new')
sns.barplot(x='state', y='cases_new', hue='date', data=df_melted, palette='viridis', ax=axs[2])
axs[2].set_title("LAST 7 DAYS NEW COVID-19 CASES BY STATE", fontsize=15)
axs[2].set_ylabel("Number of New Cases", fontsize=12)
axs[2].set_xlabel("State", fontsize=12)
axs[2].grid()

# Tight layout
plt.tight_layout()

# Display the plots in Streamlit
st.pyplot(fig)
