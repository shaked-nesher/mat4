# -*- coding: utf-8 -*-
"""
Created on Thu May 13 17:28:01 2021

@author: shaked nesher
"""

import json
import requests
import pprint

apikey =input('please enter your API key:')
destinations = open("dests.txt", encoding='utf-8')
destinations_ls = []
response2data_ls = []


# take the second element for sort
def take_first(elem):
    dist = elem[0].split("km")[0]
    if "," in dist:
        dist = dist.replace(",", "").strip()
    return float(dist)


for i in destinations:
    i = i.strip()
    destinations_ls.append(i)
try:
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins=תל אביב&destinations=%s|%s|%s|%s|%s&key=%s' % (destinations_ls[0], destinations_ls[1], destinations_ls[2], destinations_ls[3], destinations_ls[4], apikey)
    response = requests.get(url).json()
    for place in destinations_ls:
        url2 = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s' % (place, apikey)
        response2data_ls.append(requests.get(url2).json())
    index = 0
    distance = {}
    x_km_ls = []
    for city in response["destination_addresses"]:
        distance_data = response["rows"][0]["elements"][index]["distance"]["text"]
        duration_data = response["rows"][0]["elements"][index]["duration"]["text"]
        if "day" in duration_data or "days" in duration_data:
            try:
                hours = int(duration_data.split("day")[0]) * 24
                try:
                    total_hours = int(duration_data.split("hours")[0].split("day")[1]) + hours
                except:
                    try:
                        total_hours = int(duration_data.split("hours")[0].split("days")[1]) + hours
                    except:
                        None
                duration_str = "{0} hours, {1} min".format(total_hours, 0)
            except:
                None
        else:
            duration_str = duration_data
        lat_data = response2data_ls[index]["results"][0]["geometry"]["location"]["lat"]
        lng_data = response2data_ls[index]["results"][0]["geometry"]["location"]["lng"]
        distance[city] = (distance_data, duration_str,"lat: "+str(lat_data),"lng: "+ str(lng_data))
        duration_str = ""
        x_km_ls.append((distance_data, city))
        index = index + 1
        
    pprint.pprint(distance,width=60,depth=3,indent=1)
    
    sort_x_km_ls = sorted(x_km_ls, key=take_first)
    sort_x_km_ls = sort_x_km_ls[2:]
    print("the 3 furthest cities from tel aviv are:\n" + str(sort_x_km_ls))


except:
    print("There is a problem with the file")

