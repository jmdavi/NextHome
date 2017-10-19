#!/usr/bin/env python

"""
Work-in-progress
Google Maps API - Place Search
Uses dictionary of Town_MA latitudes and longitudes created by Google_Geolocate.py file to define starting location
Finds Places within radius of lat,long values
Stores in memory before insert into SQLite database
Could return GB's of JSON for long list of towns/locations, be wary of running too many at once

To use:
1) insert a valid API key into the variable key below
2) uncomment the block
3) replace variable types with different types of places you are interested in from the longer list we commented out
"""

from urllib2 import Request, urlopen, URLError
import json
import sqlite3 as sqlite

#WARNING: you must add your own Google API key below, manage at https://console.cloud.google.com
key='insert+here'

#dictionary of Massachusetts towns within 1 hour of Boston (longitude, latitude)
locations= {"Freetown":"41.7619708,-71.014118","Dighton":"41.843859,-71.1567344","Lakeville":"41.8459169,-70.9495226","Berkley":"41.8459347,-71.0828222","Middleborough":"41.8929942,-70.9107708","Taunton":"41.900101,-71.0897674","Attleboro":"41.9445441,-71.2856082","Raynham":"41.9487077,-71.0731162","Plymouth":"41.9584457,-70.6672621","Norton":"41.9667703,-71.1869963","North Attleborough":"41.9695516,-71.3565439","Bridgewater":"41.9903519,-70.9750541","Halifax":"41.991213,-70.861985","Kingston":"41.9932752,-70.7284785","Plainville":"42.0042655,-71.3328331","West Bridgewater":"42.0189894,-71.0078215","Easton":"42.0245442,-71.1286594","East Bridgewater":"42.0334341,-70.9592096","Mansfield":"42.0334565,-71.2190578","Duxbury":"42.0417525,-70.6722767","Foxborough":"42.0653812,-71.2478251","Wrentham":"42.0667652,-71.3281114","Pembroke":"42.0714925,-70.8092","Hanson":"42.0751892,-70.8800187","Whitman":"42.0806564,-70.935599","Franklin":"42.0834313,-71.396725","Brockton":"42.0834335,-71.0183787","Bellingham":"42.0867608,-71.4745881","Marshfield":"42.0917453,-70.7055871","Abington":"42.1048228,-70.9453218","Mendon":"42.1056525,-71.5522859","Hanover":"42.1162217,-70.8476708","Oxford":"42.1167606,-71.8647577","Norfolk":"42.1195426,-71.3250563","Stoughton":"42.1229099,-71.1092012","Sharon":"42.1236499,-71.1786237","Hopedale":"42.1306357,-71.5412077","Avon":"42.1306554,-71.0411582","Rockland":"42.1306563,-70.9161551","Milford":"42.1398577,-71.5163049","Walpole":"42.1417442,-71.2495096","Medway":"42.1417641,-71.3967256","Holbrook":"42.144846,-71.014118","Sutton":"42.1500353,-71.7632878","Northbridge":"42.1516323,-71.6494407","Canton":"42.1584324,-71.1447732","Norwell":"42.1615157,-70.7927832","Randolph":"42.1619739,-71.042551","Millis":"42.1669661,-71.351738","Upton":"42.1744878,-71.6022583","Medfield":"42.1875826,-71.3064597","Millbury":"42.1920719,-71.761522","Norwood":"42.1943909,-71.1989695","Auburn":"42.1945385,-71.8356271","Scituate":"42.195929,-70.7258633","Holliston":"42.2000966,-71.4245049","Grafton":"42.2070391,-71.6856236","Braintree":"42.2079017,-71.0040013","Westwood":"42.2139873,-71.2244987","Weymouth":"42.2180724,-70.9410356","Hopkinton":"42.2286954,-71.5225646","Sherborn":"42.2389857,-71.3697813","Cohasset":"42.2417675,-70.8036544","Hingham":"42.2418172,-70.889759","Dedham":"42.2436085,-71.1676536","Dover":"42.2458749,-71.2828719","Milton":"42.2495321,-71.0661653","Quincy":"42.2528772,-71.0022705","Ashland":"42.2612067,-71.4633956","Worcester":"42.2625932,-71.8022934","Westborough":"42.2695216,-71.6161294","Natick":"42.2775281,-71.3468091","Framingham":"42.279286,-71.4161565","Needham":"42.2809285,-71.2377548","Shrewsbury":"42.2959267,-71.7128471","Wellesley":"42.296797,-71.2923877","Hull":"42.3020647,-70.9078346","Southborough":"42.3056501,-71.5245087","Northborough":"42.3195556,-71.6411997","Brookline":"42.3317642,-71.1211635","Newton":"42.3370413,-71.2092214","Marlborough":"42.3459271,-71.5522874","Boston":"42.3600825,-71.0588801","Wayland":"42.3625953,-71.3614484","West Boylston":"42.3667589,-71.785627","Weston":"42.3667625,-71.3031132","Watertown":"42.3709299,-71.1828321","Cambridge":"42.3736158,-71.1097335","Waltham":"42.3764852,-71.2356113","Winthrop":"42.3778173,-70.9811334","Berlin":"42.3812039,-71.6370121","Sudbury":"42.3834278,-71.4161725","Somerville":"42.3875968,-71.0994968","Boylston":"42.3889953,-71.6908142","Hudson":"42.391736,-71.566139","Chelsea":"42.3917638,-71.0328284","Belmont":"42.3956405,-71.1776114","Everett":"42.40843,-71.0536625","Revere":"42.4084302,-71.0119948","Arlington":"42.4153925,-71.1564729","Clinton":"42.4167635,-71.6829081","Medford":"42.4184296,-71.1061639","Malden":"42.4250964,-71.066163","Lincoln":"42.4259283,-71.3039469","Nahant":"42.4265633,-70.922279","Bolton":"42.4334258,-71.6078449","Maynard":"42.4334903,-71.4495058","Stow":"42.4370374,-71.5056199","Lexington":"42.4430372,-71.2289641","Winchester":"42.452303,-71.1369959","Lancaster":"42.4556452,-71.6731242","Melrose":"42.4584292,-71.0661633","Concord":"42.4603719,-71.3489484","Saugus":"42.4651421,-71.0110473","Lynn":"42.466763,-70.9494938","Swampscott":"42.4709437,-70.9175562","Woburn":"42.4792618,-71.1522765","Stoneham":"42.4802469,-71.0999719","Boxborough":"42.4834197,-71.5167139","Acton":"42.4850931,-71.43284","Bedford":"42.4906231,-71.2760089","Marblehead":"42.4999582,-70.8578024","Harvard":"42.5000919,-71.5828444","Wakefield":"42.5039395,-71.0723391","Burlington":"42.5047161,-71.1956205","Salem":"42.51954,-70.8967155","Reading":"42.5256563,-71.0952891","Peabody":"42.5278731,-70.9286609","Carlisle":"42.5292597,-71.3495046","Littleton":"42.5372893,-71.5128022","Lynnfield":"42.53869,-71.0465638","Shirley":"42.5437035,-71.6495176","Wilmington":"42.5481714,-71.1724467","Billerica":"42.5584218,-71.2689461","Beverly":"42.5584283,-70.880049","Ayer":"42.5611947,-71.5899054","Danvers":"42.5750009,-70.932122","North Reading":"42.5750939,-71.0786653","Manchester-by-the-Sea":"42.577834,-70.7675967","Westford":"42.5792583,-71.4378411","Middleton":"42.5950939,-71.0161643","Chelmsford":"42.5998139,-71.3672838","Wenham":"42.604261,-70.8911612","Tewksbury":"42.6106478,-71.2342248","Groton":"42.6112018,-71.5745152","Gloucester":"42.6159285,-70.6619888","Essex":"42.6319582,-70.7829315","Lowell":"42.6334247,-71.3161718","Hamilton":"42.6362052,-70.8431049","Topsfield":"42.6375941,-70.9495053","Rockport":"42.6556505,-70.620363","Andover":"42.6583356,-71.1367953","Boxford":"42.6611604,-70.996726","Pepperell":"42.6659232,-71.5884363","Dracut":"42.6703687,-71.3020052","Dunstable":"42.6750898,-71.4828433","Tyngsborough":"42.6766696,-71.4244224","Ipswich":"42.6791832,-70.8411558","Lawrence":"42.7070354,-71.1631137","Rowley":"42.7167483,-70.8787277","Georgetown":"42.7250918,-70.9911659","Methuen":"42.7262016,-71.1908924","Groveland":"42.7603688,-71.0314451","Newbury":"42.7649497,-70.8714528","Newburyport":"42.8125913,-70.8772751","Merrimac":"42.8340582,-71.0005509","Salisbury":"42.841723,-70.8605982","Amesbury":"42.8583925,-70.9300376"}

#because there are limits on the API calls, it is strongly recommended not to run all types that you want at once
#types=['book_store', 'bakery', 'cafe', 'meal_delivery' , 'meal_takeaway', 'museum', 'park', 'restaurant', 'synagogue' , 'train_station', 'transit_station' , 'movie_theater', art_gallery]
types=['book_store', 'bakery']

#this will be a list of lists regarding what to insert into sqlite table
table_rows=[]

'''uncomment to create the SQLite table the first time or to perform a destructive refresh whenever'''
#with sqlite.connect('yelp_database.db') as con:
#    cur = con.cursor()
#    cur.execute("DROP TABLE IF EXISTS google_places")
#    cur.execute("CREATE TABLE google_places(name TEXT, rating REAL, formatted_address TEXT, store_types TEXT, city TEXT, place_id INTEGER, town_org TEXT)")

town_count=0

for town in locations:
    town_count+=1
    location= locations[town]
    #print location
    for place_type in types:
        print town,town_count, place_type
        #first API call request gathers list of places of interest from Google based on the town's latitude and longitude, with hardcoded radius and variable for place_type, e.g. bookstores
        request1 = Request('https://maps.googleapis.com/maps/api/place/radarsearch/json?location='+location+'&radius=8046.72&type='+place_type+'&key='+key)
        try:
            placeSearch=urlopen(request1)
            placeSearch=json.load(placeSearch)
            #print 'placeSearch'
            #print placeSearch
            place_count=0
            for x in placeSearch['results']:
                table_row=[]
                place_id = placeSearch['results'][place_count]['place_id']
                #print 'place_id'
                #print place_id
                #series of secondary API requests for details on each place identified per town and place_type above
                detail_request= Request('https://maps.googleapis.com/maps/api/place/details/json?placeid='+place_id+'&key='+key)
                
                #provide values based on request JSON
                try:
                    detailSearch=urlopen(detail_request)
                    detailSearch=json.load(detailSearch)
                    #print 'detailSearch'
                    #print detailSearch
                    
                    #grabbing pieces we need for the SQLite table into variables
                    name= detailSearch['result']['name']
                    try:
                        rating= detailSearch['result']['rating']
                    except:
                        rating= None #for SQLite null value, set in Python to None
                    formatted_address= detailSearch['result']['formatted_address']
                    try:
                        store_types= detailSearch['result']['types']
                        store_types=', '.join(store_types)
                    except:
                        store_types=None
                    for x in detailSearch['result']['address_components']:
                        if 'locality' in x['types']:
                            #print x['types']
                            #print x['long_name']
                            city= x['long_name']
                except:
                    print 'Failed at getting any specific details about whatever from placeid. Got an error code:', e
                    name='N/A'
                    rating= None
                    formatted_address= 'N/A'
                    store_types= 'N/A'
                    city= 'N/A'

                #put what values you can into the table_rows list
                table_row=[name, rating, formatted_address, store_types, city, place_id,town]
                #print 'table_row'
                #print table_row
                table_rows.append(table_row)
                place_count+=1

        except URLError:
            print 'Failed at getting any results for Town/City. Got an error code'

        #you will update the SQLite table per each town and place_type loop
        #this runs awhile, so regular inserts gaurd against errors or the thing 
        with sqlite.connect('NextHome_database.db') as con:
            cur = con.cursor()
            cur.executemany( "INSERT INTO google_places(name, rating, formatted_address, store_types, city, place_id) VALUES (?,?,?,?,?,?)", table_rows)
            table_rows=[] #clear it out after inserts
            #print 'empty table_rows', table_rows
