import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime

#data = "https://github.com/MoH-Malaysia/covid19-public/blob/main/epidemic/cases_malaysia.csv"
my = "https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/cases_malaysia.csv"
state = "https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/cases_state.csv"


df_my = pd.read_csv(my)
df= pd.read_csv(state)
#df.to_csv("c:\\users\\DT\\DROPBOX\\WFH\\python\\covid_state.csv", index=False)# source file created


#pd.options.display.max_columns = None
df['date'] = pd.to_datetime(df['date'])


#df.info()
def check(df):
    l=[]
    columns=df.columns
    for col in columns:
        dtypes=df[col].dtypes
        nunique=df[col].nunique()
        sum_null=df[col].isnull().sum()
        l.append([col,dtypes,nunique,sum_null])
    df_check=pd.DataFrame(l)
    df_check.columns=['column','dtypes','nunique','sum_null']
    return df_check
print(check(df))


#DEFINE VARIABLE
state_list = df.state.unique().tolist()
n = np.array(df.state.nunique())
r = np.arange(n)

data = df.groupby(["state",(df['date'].dt.year)])["cases_new"].sum().unstack()
print(data)

#PLOT LINE CHART
data.plot(figsize=(14,7), marker="o")
plt.ticklabel_format(style="plain", axis='y')
plt.xticks(r,state_list)
plt.xlim(-1,16)
plt.xticks(rotation=35 , horizontalalignment="right",fontsize=10)
plt.title("TOTAL NEW COVID-19 CASES BY STATE FROM YEAR 2020 - 2023 ", fontsize=15)
plt.ylabel("Number of Cases", fontsize=15)
plt.xlabel("State", fontsize=15)
plt.legend(title ="YEARS:")
plt.grid()
plt.show()

#PLOT BAR CHART
data.plot(kind ="bar",figsize=(14,7),stacked=False)
plt.title("TOTAL NEW COVID-19 CASES BY STATE FROM YEAR 2020 - 2023 ", fontsize=15)
plt.ylabel("Number of Cases", fontsize=15)
plt.xlabel("State", fontsize=15)
plt.ticklabel_format(style="plain", axis='y')
plt.xticks(rotation=25)
plt.legend(title ="YEARS:")
plt.grid()
plt.show()


#DEFINE VARIABLE
df1 = df.copy()
df1 =df1.sort_values(by=["state","date"],ascending=True)
y1 =df1.cases_new
y2 =df1.cases_recovered * -1
x = df1.date

#PLOT LINE CHART FOR DUAL DATA
plt.figure(figsize=(13,7))
plt.title("OVERVIEW COVID-19 NEW CASES VS RECOVERY CASES",fontsize=15)
plt.plot(x,y1, color='red', linewidth = 2,  label = 'NEW_CASES')
plt.plot(x,y2, color='blue', linewidth = 2,  label = 'RECOVERY_CASES')
plt.ylabel("CASES")
plt.xlabel("DATE")
plt.ticklabel_format(style="plain",axis='y')
plt.xticks(rotation=35)
plt.grid()
plt.legend(title ="NEW CASES VS RECOVERY CASES:")
plt.show()



# DISPLAY LATEST RESULT
print(df.loc[:,["date","state", "cases_new"]].tail(16))
#print(df.groupby(["state",(df['date'].dt.year),(df['date'].dt.month),(df['date'].dt.day)])["cases_new"].sum().unstack())


# DISPLAY LAST 7 DAY TOTAL RESULT
date_7_days_ago = datetime.datetime.today() - datetime.timedelta(days=10)
# Filter the dataframe to only include rows for the last 7 days
df_last_7_days = df[df['date'] >= date_7_days_ago]
# Group the data by date and calculate the sum of new cases for each day
df_new_cases_last_7_days = df_last_7_days.groupby(["state"]).agg({'cases_new': 'sum'}).reset_index()
# Print the resulting dataframe
print(df_new_cases_last_7_days)


# DISPLAY LAST 7 DAY RESULT
pd.options.display.max_columns = None
print(df_last_7_days.groupby(['state',df['date'].dt.date])["cases_new"].sum().unstack())
df2 = df_last_7_days.groupby(['state',df['date'].dt.date])["cases_new"].sum().unstack()
#print(df2.date)
df2.plot(figsize=(14,7), marker="X")
plt.xticks(r,state_list,rotation=25)
plt.ticklabel_format(style="plain",axis='y')
plt.title("LAST 7 DAYS NEW COVID-19 CASES BREAKDOWN BY STATE ", fontsize=15)
plt.ylabel("Number of  New Cases", fontsize=15)
plt.xlabel("State", fontsize=15)
plt.legend(title ="LAST 7 DAYS:")
plt.grid()
plt.show()

