import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np

#data = "https://github.com/MoH-Malaysia/covid19-public/blob/main/epidemic/cases_malaysia.csv"
#my = "https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/cases_malaysia.csv"
state = "https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/cases_state.csv"


df_my = pd.read_csv(state)
#df_my['date'] = pd.to_datetime(df_my['date'])
df_my["date"] = pd.to_datetime(df_my["date"]).dt.strftime("%Y%m%d").astype('int64')
print(df_my.dtypes)
df_my.info()

# convert the 'date' column to a datetime object

#df_my['day'] =df_my.date.dt.day
#df_my['month'] =df_my.date.dt.month
#df_my['year'] =df_my.date.dt.year
df0 = df_my.loc[:,["state","date", "cases_new","cases_active"]]
print(df0)
df0.rename(columns={"state": "Age Group" ,"date": "Year","cases_new": "New_Cases","cases_active": "Active_Case" },inplace=True)
df = df0.sort_values(by=["Age Group","Year"],ascending=True)
#df = df0.groupby(["Age Group", "Year"]).New_Cases.agg([sum]).sort_values(by=["Age Group","Year"],ascending=True).reset_index()

print(df.to_string())


#df["Year"] = df["Year"].astype('int64')



fig, ax = plt.subplots(figsize=(15,8))

def animate(year):
    ax.clear()
    filtered = df[df["Year"] == year]
    active_case = plt.barh(y=filtered["Age Group"], width=filtered["Active_Case"], color="red")
    #feNew_Cases = plt.barh(y=filtered["Age Group"], width=filtered["FeNew_Cases"],color="green")
    ax.set_xlim(-10, 105_000)
    ax.bar_label(active_case, padding=3, labels=[f'{value}' for value in filtered['Active_Case']])
    #ax.bar_label(feNew_Cases, padding=3, labels=[f'{-1*round(value,-3):,}' for value in filtered['FeNew_Cases']])

    for edge in ['top', 'right', 'bottom', 'left']:
        ax.spines[edge].set_visible(True)

    ax.tick_params(left=False)
    ax.get_xaxis().set_visible (True)
    ax.legend ([active_case], ["Active_Case"])
    #ax.legend([New_Cases, feNew_Cases],["New_Cases","FeNew_Cases"])
    ax.set_title(f"Daily Active Covid-19 Cases in Malaysia dated {year} ", size=18,weight="bold")

animation = FuncAnimation(fig, animate,interval=50, frames=np.array(df.Year),repeat=False)
#animation.save(r"c:\users\t520\downloads\covid19_animate.gif", dpi=300, writer=PillowWriter(fps=5))

plt.show()




