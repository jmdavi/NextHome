#!/usr/bin/env python

"""
Work-in-progress
Google Maps API - Place Search
Uses dictionary of Town_MA latitudes and longitudes created by Google_Geolocate.py file to define starting location
Finds Places within radius of lat,long values
Stores in memory before insert into SQLite database
Could return GB's of JSON for long list of towns/locations, be wary of running too many at once
"""

from urllib2 import Request, urlopen, URLError
import json
import sqlite3 as sqlite




locations= {"North Adams":"42.700915,-73.1087148"}

types=['book_store']

table_rows=[]

for town in locations:
    location= locations[town]
    print location
    for place_type in types:
        print 'place_type'
        print place_type
        request1 = Request('https://maps.googleapis.com/maps/api/place/radarsearch/json?location='+location+'&radius=12874.8&type='+place_type+'&key=AIzaSyDhPqPZfb9Ixo_44lr30i8IaFMKJ080YEE')
        try:
            placeSearch=urlopen(request1)
            placeSearch=json.load(placeSearch)
            print 'placeSearch'
            print placeSearch
            count=0
            for x in placeSearch['results']:
                table_row=[]
                place_id = placeSearch['results'][count]['place_id']
                print 'place_id'
                print place_id
                detail_request= Request('https://maps.googleapis.com/maps/api/place/details/json?placeid='+place_id+'&key=AIzaSyDhPqPZfb9Ixo_44lr30i8IaFMKJ080YEE')
                try:
                    detailSearch=urlopen(detail_request)
                    detailSearch=json.load(detailSearch)
                    print 'detailSearch'
                    print detailSearch
                    
                    #grabbing pieces we need for the SQLite table into variables
                    name= detailSearch['result']['name']
                    try:
                        rating= detailSearch['result']['rating']
                    except:
                        rating= 'null'
                    formatted_address= detailSearch['result']['formatted_address']
                    try:
                        store_types= detailSearch['result']['types']
                        store_types=', '.join(store_types)
                    except:
                        store_types='null'
                    city= detailSearch['result']['address_components'][2]['long_name']
                except:
                    print 'Failed at getting any specific details about whatever from placeid. Got an error code:', e
                    name='N/A'
                    rating= 'null'
                    formatted_address= 'N/A'
                    store_types= 'N/A'
                    city= 'N/A'

                #put what you can into the table_rows list
                table_row=[name, rating, formatted_address, store_types, city, place_id]
                print 'table_row'
                print table_row
                table_rows.append(table_row)
                count+=1

        except URLError, e:
            print 'Failed at getting any results for Town/City. Got an error code:', e

with sqlite.connect('NextHome_database.db') as con:
    cur = con.cursor()
    #Destructive refresh if the next two lines are not commented out
    cur.execute("DROP TABLE IF EXISTS google_places")
    cur.execute("CREATE TABLE google_places(name TEXT, rating REAL, formatted_address TEXT, store_types TEXT, city TEXT, place_id INTEGER)")
    cur.executemany( "INSERT INTO google_places(name, rating, formatted_address, store_types, city, place_id) VALUES (?,?,?,?,?,?)", table_rows)
