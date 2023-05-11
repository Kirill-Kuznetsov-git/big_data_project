import streamlit as st

import pandas as pd

# trips = pd.read_csv("data/trips.tsv", sep="\t")
trips_prproc = pd.read_csv("output/trips_preprocessed.csv")

q1 = pd.read_csv("output/q1.csv")
q2 = pd.read_csv("output/q2.csv")
q3 = pd.read_csv("output/q3.csv")
q4 = pd.read_csv("output/q4.csv")
q5 = pd.read_csv("output/q5.csv")
q6 = pd.read_csv("output/q6.csv")
q7 = pd.read_csv("output/q7.csv")

evals = pd.read_csv("output/evaluation.csv")
lr = pd.read_csv("output/lr.csv")
rf = pd.read_csv("output/rf.csv")


st.write("# Big Data Project  \n _Estimated travel time for a taxi ride_  \n", "*Year*: **2023**")
st.write("")

# # Display the descriptive information of the dataframe
# trip_description = trips.describe()
# st.write(trip_description)

# hour by call type by trip time sec
st.write("## Hour of day of start trip and Call type and Trip time sec")
st.write("Here we show the dependence of trip time in seconds, call type and hour of start of trip:")
import altair as alt
c = alt.Chart(trips_prproc).mark_circle().encode(
    x='hour', y='call_type', size='trip_time_sec', color='trip_time_sec', tooltip=['hour', 'call_type', 'trip_time_sec']).properties(height=300, width=500)
st.write(c)

# ---------

# q1 - Missing values
st.write("## Missing values")
st.write("Here we can see the number of missing values for each column."
          " ORIGIN_CALL and ORIGIN_STAND have too many missing data."
          " This tells us that we cannot rely on these columns for our predictions:")
st.write(q1)

# ---------

# q2 - Day of week
st.write("## Day of week and average trip time")
q2['day_of_week'] = q2['day_of_week'].astype('int')
q2['avg_trip_time'] = q2['avg_trip_time'].astype('int')
st.write("Here we show the distribution of average time trip for different days of week."
         " We can see that values are difference, "
         "so we can use this feature for out prediction of trip time:")
# countplot / horizontal
chart_q2 = alt.Chart(q2).mark_bar().encode(
    x="day_of_week:O",
    y="avg_trip_time:Q").properties(height=300, width=500)

st.write(chart_q2)

st.write("Fifth day of the week has the most number of taxi trips by total time."
         " This higher demand may be correlated with increased traffic that day which can increase the trip duration.")

# ---------

# q3 - Hours
st.write("## Hour of start trip start and average trip time")
q3['hour'] = q3['hour'].astype('int')
q3['avg_trip_time'] = q3['avg_trip_time'].astype('int')
st.write("Here we show the distribution of average time trip for different hours of day."
         " We can see that values are difference, "
         "so we can use this feature for out prediction of trip time:")
# countplot / horizontal
chart_q3 = alt.Chart(q3).mark_bar().encode(
    x="hour:O",
    y="avg_trip_time:Q").properties(height=300, width=500)
st.write(chart_q3)
st.write("We can see that the peak hours for taxi are the most busy hours of the day "
         "- when people go to work and when people return from work. "
         "This could mean that the city is experiencing higher traffic which leads to longer trip time.")

# ---------

# q4 - call type (avg)
st.write("## Call type and average trip time with trip's count")
q4['avg_trip_time'] = q4['avg_trip_time'].astype('int')
st.write("Here we show the distributions of average time trip for"
         " different call types and cout of trips for difference call types."
         " We can see that values are difference, "
         "so we can use this feature for out prediction of trip time:")
# countplot / horizontal
chart_q4 = alt.Chart(q4).mark_bar().encode(
    x="call_type:O",
    y="avg_trip_time:Q").properties(height=300, width=500)
st.write(chart_q4)

q5['count_trip_time'] = q5['count_trip_time'].astype('int')
chart_q5 = alt.Chart(q5).mark_bar().encode(
    x="call_type:O",
    y="count_trip_time:Q").properties(height=300, width=500)
st.write(chart_q5)
# ---------

# q7 - day type
st.write("## Distribution of day types")
st.write("Here we show distribution of trips for difference day type:"
         "B-holiday or any special day,"
         "C-day before holiday, "
         "A-any other normal day."
         "In distribution we can see that all trips was in normal day,"
         " so we don't need to use this feature in trip time prediction:")
q7['count'] = q7['count'].astype('int')
chart_q7 = alt.Chart(q7).mark_bar().encode(
    x="day_type:O",
    y="count:Q").properties(height=300, width=500)
st.write(chart_q7)
# ---------

# model 1 - lr
st.write("## Result of linear regression on test dataset")
st.write("Linear regression predicts the data perfectly."
         " This could mean that the label is linearly dependent on the features:")
lr = lr.sample(10, random_state=42)
st.write(lr)

# ---------

# model 2 - rf
st.write("## Result of random forest on test dataset")
st.write("Random forest tree regression does not show such good results as linear regression:")
rf = rf.sample(10, random_state=42)
st.write(rf)

# ---------

# evaluations
st.write("## Final evaluation")
st.write("Final metric's evaluation for random forent tree and linear regression and comparing of these two methods:")
evals = evals.drop(columns=['gbt'])
st.write(evals)

# ---------

# result
st.write("# Results")
st.write()
# ---------
