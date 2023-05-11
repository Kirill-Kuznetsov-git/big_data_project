"""Module providing dashboard."""
import streamlit as st
import altair as alt

import pandas as pd

TRIPS = pd.read_csv("data/trips.tsv", sep="\t")
TRIPS_PRPROC = pd.read_csv("output/trips_preprocessed.csv")

Q1 = pd.read_csv("output/q1.csv")
Q2 = pd.read_csv("output/q2.csv")
Q3 = pd.read_csv("output/q3.csv")
Q4 = pd.read_csv("output/q4.csv")
Q5 = pd.read_csv("output/q5.csv")
Q6 = pd.read_csv("output/q6.csv")
Q7 = pd.read_csv("output/q7.csv")

EVALS = pd.read_csv("output/evaluation.csv")
LR = pd.read_csv("output/lr.csv")
RF = pd.read_csv("output/rf.csv")

st.write("# Big Data Project  \n _Estimated travel time for a taxi ride_  \n", "*Year*: **2023**")
st.write("")

# Display the descriptive information of the dataframe

TRIP_DESCRIPTION = TRIPS.describe()
st.write(TRIP_DESCRIPTION)

# hour by call type by trip time sec
st.write("## Hour of day of start trip and Call type and Trip time sec")
st.write("Here we show the dependence of trip time"
         " in seconds, call type and hour of start of trip:")

C = alt.Chart(TRIPS_PRPROC).mark_circle().encode(
    x='hour', y='call_type', size='trip_time_sec', color='trip_time_sec',
    tooltip=['hour', 'call_type', 'trip_time_sec']).properties(height=300, width=500)
st.write(C)

# ---------

# q1 - Missing values
st.write("## Missing values")
st.write("Here we can see the number of missing values for each column."
         "ORIGIN_CALL and ORIGIN_STAND have too many missing data."
         " This tells us that we cannot rely on these columns for our predictions:")
st.write(Q1)

# ---------

# q2 - Day of week
st.write("## Day of week and average trip time")
Q2['day_of_week'] = Q2['day_of_week'].astype('int')
Q2['avg_trip_time'] = Q2['avg_trip_time'].astype('int')
st.write("Here we show the distribution of average time trip for different days of week."
         " We can see that values are difference, "
         "so we can use this feature for out prediction of trip time:")
# countplot / horizontal
CHART_Q2 = alt.Chart(Q2).mark_bar().encode(
    x="day_of_week:O",
    y="avg_trip_time:Q").properties(height=300, width=500)

st.write(CHART_Q2)

st.write("Fifth day of the week has the most number of taxi trips by total time."
         " This higher demand may be correlated with "
         "increased traffic that day which can increase the trip duration.")

# ---------

# q3 - Hours
st.write("## Hour of start trip start and average trip time")
Q3['hour'] = Q3['hour'].astype('int')
Q3['avg_trip_time'] = Q3['avg_trip_time'].astype('int')
st.write("Here we show the distribution of average time trip for different hours of day."
         " We can see that values are difference, "
         "so we can use this feature for out prediction of trip time:")
# countplot / horizontal
CHART_Q3 = alt.Chart(Q3).mark_bar().encode(
    x="hour:O",
    y="avg_trip_time:Q").properties(height=300, width=500)
st.write(CHART_Q3)
st.write("We can see that the peak hours for taxi are the most busy hours of the day "
         "- when people go to work and when people return from work. "
         "This could mean that the city is "
         "experiencing higher traffic which leads to longer trip time.")

# ---------

# q4 - call type (avg)
st.write("## Call type and average trip time with trip's count")
Q4['avg_trip_time'] = Q4['avg_trip_time'].astype('int')
st.write("Here we show the distributions of average time trip for"
         " different call types and cout of trips for difference call types."
         " We can see that values are difference, "
         "so we can use this feature for out prediction of trip time:")
# countplot / horizontal
CHART_Q4 = alt.Chart(Q4).mark_bar().encode(
    x="call_type:O",
    y="avg_trip_time:Q").properties(height=300, width=500)
st.write(CHART_Q4)

Q5['count_trip_time'] = Q5['count_trip_time'].astype('int')
CHART_Q5 = alt.Chart(Q5).mark_bar().encode(
    x="call_type:O",
    y="count_trip_time:Q").properties(height=300, width=500)
st.write(CHART_Q5)
# ---------

# q7 - day type
st.write("## Distribution of day types")
st.write("Here we show distribution of trips for difference day type:"
         "B-holiday or any special day,"
         "C-day before holiday, "
         "A-any other normal day."
         "In distribution we can see that all trips was in normal day,"
         " so we don't need to use this feature in trip time prediction:")
Q7['count'] = Q7['count'].astype('int')
CHART_Q7 = alt.Chart(Q7).mark_bar().encode(
    x="day_type:O",
    y="count:Q").properties(height=300, width=500)
st.write(CHART_Q7)
# ---------

# model 1 - lr
st.write("## Result of linear regression on test dataset")
st.write("Linear regression predicts the data perfectly."
         " This could mean that the label is linearly dependent on the features:")
RF = RF.sample(10, random_state=42)
st.write(RF)

# ---------

# model 2 - rf
st.write("## Result of random forest on test dataset")
st.write("Random forest tree regression does not show such good results as linear regression:")
RF = RF.sample(10, random_state=42)
st.write(RF)

# ---------

# evaluations
st.write("## Final evaluation")
st.write("Final metric's evaluation for random forent tree"
         " and linear regression and comparing of these two methods:")
EVALS = EVALS.drop(columns=['gbt'])
st.write(EVALS)

# ---------

# result
st.write("# Results")
st.write("We make all stages: move data PG->HDFS->HIVE, then extract 6-th insights from"
         "features for next step prediction. From this insights we got that only some "
         "of the features are useful and only call type, day of week of trip start, hour of trip"
         " start and polyline length are impactful for prediction. We analyzed a dataset and found"
         " that one of its labels had a linear correlation with some of its features. To predict"
         " this label, we used two algorithms: Linear Regression and Random Forest Regression."
         " Our results showed that Linear Regression performed better with an R2 score of 1 and"
         " an RMSE of 1.7, indicating that this algorithm can accurately predict the label using"
         " linear equations. In contrast, Random Forest Regression had an R2 score of 0.6 and an"
         " RMSE of 436.3, showing that this algorithm is less accurate for this dataset and may"
         " not be the best choice for predicting the label. Overall, our findings suggest that"
         " Linear Regression is a more suitable algorithm for predicting"
         " the label in this dataset.")
# ---------
