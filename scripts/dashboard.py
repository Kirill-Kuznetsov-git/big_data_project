import streamlit as st

import pandas as pd

# trips = pd.read_csv("data/trips.tsv", sep="\t")
trips_prproc = pd.read_csv("output/trips_preprocessed.csv")

# q1 = pd.read_csv("output/q1.csv")
q2 = pd.read_csv("output/q2.csv")
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
st.write("# Big Data Project  \n _Estimated travel time for a taxi ride_  \n", "*Year*: **2023**")


# # Display the descriptive information of the dataframe
# trip_description = trips.describe()
# st.write(trip_description)


# hour by call type by trip time sec
import altair as alt
c = alt.Chart(trips_prproc).mark_circle().encode(
    x='hour', y='call_type', size='trip_time_sec', color='trip_time_sec', tooltip=['hour', 'call_type', 'trip_time_sec'])
st.write(c)

# ---------

# q1 - Missing values

# Here we can see that origin_ and origin_ have too many missing data. This tells us that we cannot rely on these tables for our predictions

# trip_description = trips.describe()
# st.write(trip_description)

# ---------

# q2 - Day of week
q2['day_of_week'] = q2['day_of_week'].astype('int')
q2['avg_trip_time'] = q2['avg_trip_time'].astype('int')

# q2 = q2['trip_time_sec'].astype('int')
# countplot / horizontal
chart = alt.Chart(q2).mark_bar().encode(
    x=alt.X("day_of_week:Q", title="Day of week"),
    y=alt.Y("avg_trip_time:Q"), title="Trip time in seconds").properties(height=alt.Step(20))

st.write(chart)

# Fifth day of the week has the most number of taxi trips by total time. This higher demand may be correlated with increased traffic that day which can increase the trip duration

# ---------

# q3 - Hours

# countplot / horizontal
# We can see that the peak hours for taxi are the most busy hours of the day - when people go to work and when people return from work. This could mean that the city is experiencing higher traffic which leads to longer trip time

# ---------

# q4 - call type (avg)

# countplot
# Придумай сам

# ---------

# q5 - call type (count)

# countplot
# придумай сам

# ---------

# q6 - avg, max, min trip time

# count plot 

# ---------

# q7 - day type

# ---------

# model 1 - lr

# Linear regression predicts the data perfectly. This could mean that the label is linearly dependant on the features 

# cart with 20 columns

# ---------

# model 2 - rf

# почему rf плохо подошел

# ---------

# evaluations

