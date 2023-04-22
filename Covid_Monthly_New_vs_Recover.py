import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np

state = "https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/cases_state.csv"

df_my = pd.read_csv(state)

# convert the 'date' column to a datetime(yyyymm) and to integer
df_my["date"] = pd.to_datetime(df_my["date"]).dt.strftime("%Y%m").astype('int64')
data = df_my.loc[:,["state","date", "cases_new","cases_recovered"]]
data.rename(columns={"state": "State" ,"date": "Month","cases_new": "New_Cases","cases_recovered": "Recover_Cases" },inplace=True)
#df = data.groupby(["State", "Month"]).New_Cases.agg([sum]).sort_values(by=["State","Month"],ascending=True).reset_index()
df = data.groupby(["State", "Month"]).agg({'New_Cases': 'sum', 'Recover_Cases': 'sum'}).sort_values(by=["State","Month"],ascending=True).reset_index()
df["Recover_Cases"] = df["Recover_Cases"] * -1

df.info()
print(df)

fig, ax = plt.subplots(figsize=(15,8))

def animate(month):
    ax.clear()
    filtered = df[df["Month"] == month]
    new_cases = plt.barh(y=filtered["State"], width=filtered["New_Cases"], color="red")
    recover_cases = plt.barh(y=filtered["State"], width=filtered["Recover_Cases"],color="green")
    ax.set_xlim(-300_000, 300_000)
    ax.bar_label(new_cases , padding=3, labels=[f'{(value):,}' for value in filtered['New_Cases']])
    ax.bar_label(recover_cases, padding=3, labels=[f'{-1*(value):,}' for value in filtered['Recover_Cases']])

    for edge in ['top', 'right', 'bottom', 'left']:
        ax.spines[edge].set_visible(False)

    ax.tick_params(left=False)
    ax.get_xaxis().set_visible (False)
    ax.legend ([new_cases,recover_cases ], ["New_Cases","Recover_Cases"])
    #ax.legend([New_Cases, feNew_Cases],["New_Cases","Active_Cases"])
    ax.set_title(f"Monthly New Vs Recover Covid-19 Cases in Malaysia, {month} Month ", size=18,weight="bold")

animation = FuncAnimation(fig, animate, interval=1000, frames=np.array(df['Month']), repeat = False)
plt.show()


