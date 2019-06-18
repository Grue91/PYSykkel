#!/usr/bin/python3
import pandas as pd 
import plotly.graph_objs as go
import plotly

#Choose your dataset
dataSet = pd.read_json("https://data.urbansharing.com/oslobysykkel.no/trips/v1/2019/05.json", convert_dates=True)

#Trim columns we won't use
del dataSet['end_station_description']
del dataSet['start_station_description']

#Make sure data is sorted by trip start time
dataSet = dataSet.sort_values(by="started_at")

#total trips in period
tot_trips = dataSet.count()[0]

####Trip duration####
#Longest trip in the dataset (duration)
longestTripDuration = dataSet["duration"].max()
#Shortest trip in the dataset (duration)
shortestTripDuration = dataSet["duration"].min()
#Average duration of trips in the dataset
avg_Duration = dataSet.loc[:,"duration"].mean()

####Msot popular start and end stations###
pop_startStation = dataSet["start_station_name"].value_counts().nlargest(1) #.keys()[0]
pop_endStation = dataSet["end_station_name"].value_counts().nlargest(1)

def printme():
    print("Statistics:")
    print("Total trips in selected timeperiod:", tot_trips)
    print("Longest duration of trip in the dataset:", longestTripDuration, "seconds")
    print("Shortest duration of trip in the dataset:", shortestTripDuration, "seconds")
    print("Average duration of trip in the dataset:", avg_Duration, "seconds")
    print("Most popular starting station for trip:", pop_startStation.keys()[0], "(", pop_startStation[0], "trips )" )
    print("Most popular end station for trip:", pop_endStation.keys()[0], "(", pop_endStation[0], "trips )" )

printme()

#Group and count events by day
countByDay = dataSet.groupby(pd.DatetimeIndex(dataSet['started_at']).normalize()).count()

#Graph it!
#Plot: count rentals pr day
data = [go.Scatter(x=countByDay.started_at.index.date, y=countByDay.started_at)]
plotly.offline.plot(data, image_filename="File", image="jpeg")