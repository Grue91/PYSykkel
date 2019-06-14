#!/usr/bin/python3

import requests
import json
import time

#We`ll send a header identifying the application as pr the owners request
header = {'Client-Name' : 'Grue91-PySykkel'}

#URLs
stationsEndpoint = "https://gbfs.urbansharing.com/oslobysykkel.no/station_information.json"
statusEndpoint = "https://gbfs.urbansharing.com/oslobysykkel.no/station_status.json"

def bike(stationName):
    stationsRequest = requests.get(stationsEndpoint, headers=header)
    statusRequest = requests.get(statusEndpoint, headers=header)

    #Figure out what stationID to get status for
    stationRequestsJSON = stationsRequest.json()['data']['stations']

    station = None

    for i in stationRequestsJSON:
        if stationName in i['name']:
            station = i

    if station == None:
        print("Could not match the name", stationName, "to a station.")
        return

    #Get status for specified station
    stationsList = statusRequest.json()['data']['stations']
    for i in stationsList:
        if station['station_id'] in i['station_id']:
            stationDetails = i

    #Generate a Google Maps Link to the stations location
    mapsLink = "https://www.google.com/maps/place/" + str(station["lat"]) +"," + str(station["lon"])

    #convert timestamps
    timestamp = time.localtime(stationDetails['last_reported'])
    reportTime = time.strftime("%d-%m-%Y %H:%M:%S", timestamp)

    #Print the info
    print("Bysykkel status for station: ",station['name'])
    print("Status last updated: ", reportTime)
    print("Bikes Available:", stationDetails['num_bikes_available'])
    print("Locks Available: ", stationDetails['num_docks_available'])
    print("Total station capacity: ", station['capacity'])
    print("Location in Maps: ", mapsLink)


def AllStations(fullDetails=False):

    stationsRequest = requests.get(stationsEndpoint, headers=header)
    stationRequestsJSON = stationsRequest.json()['data']['stations']

    if fullDetails:
        print ("{:<8} {:<25} {:<30} {:<20} {:<20} {:<8}".format('StationID','Name','Address','lat', 'lon', 'Capacity'))
        for i in stationRequestsJSON:
            print ("{:<8} {:<25} {:<30} {:<20} {:<20} {:<8}".format(i['station_id'], i['name'], i['address'], i['lat'], i['lon'], i['capacity']))

    else: 
        for i in stationRequestsJSON:
            print(i['name'])

def options():
    print("###################################")
    print("Enter the name of a station to check its status")
    print("Enter \"all\" to see a list of all stations, \"all+\" to get verbose stationinfo, or \"q\" to quit")
    print("###################################")

options()

while 1>0:
    UserChoice = input()

    if UserChoice == "q":
        exit()
    elif UserChoice == "all+":
        AllStations(fullDetails=True)
    elif UserChoice == "all":
        AllStations()
    else:
        bike(UserChoice)
    print ("")
    options()
