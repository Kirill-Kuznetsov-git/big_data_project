import streamlit as st

import pandas as pd

trips = pd.read_csv("data/trips.tsv", sep="\t")
trips_prproc = pd.read_csv("output/trips_preprocessed.csv")

# q1 = pd.read_csv("output/q1.csv")
# q2 = pd.read_csv("output/q2.csv")
# q3 = pd.read_csv("output/q3.csv")
# q4 = pd.read_csv("output/q4.csv")
# q5 = pd.read_csv("output/q5.csv")
# q6 = pd.read_csv("output/q6.csv")
# q7 = pd.read_csv("output/q7.csv")

# evals = pd.read_csv("output/evaluations.csv")
# lr = pd.read_csv("output/lr.csv")
# rf = pd.read_csv("output/rf.csv")
# gbt = pd.read_csv("output/gbt.csv")


# TODO: add project name
st.write("# Big Data Project  \n _Employee Salary_$^{Prediction}$ :sunglasses:  \n", "*Year*: **2023**")


# Display the descriptive information of the dataframe
trip_description = trips.describe()
st.write(trip_description)


# hour by call type by trip time sec
import altair as alt
c = alt.Chart(trips_prproc).mark_circle().encode(
    x='hour', y='call_type', size='trip_time_sec', color='sal', tooltip=['ename', 'deptno', 'trip_time_sec'])
st.write(c)



# q1 - Missing values

# trip_description = trips.describe()
# st.write(trip_description)

# q2 - Day of week

# q3 - Hours

# q4 - call type (avg)

# q5 - call type (count)

# q6 - avg, max, min trip time

# q7 - day type

# model 1 - lr

# model 2 - rf

# model 3 - gbt

# evaluations

