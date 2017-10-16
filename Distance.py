#!/usr/bin/env python

# Initial code for SI 601 F15 Hoemwork 4 Part 2

from urllib2 import Request, urlopen, URLError
import json 
import sqlite3 as sqlite


TOWNS_MA=['Abington','Acton','Acushnet','Adams','Agawam','Alford','Amesbury','Amherst','Andover','Aquinnah','Arlington','Ashburnham','Ashby','Ashfield','Ashland','Athol','Attleboro','Auburn','Avon','Ayer','Barnstable','Barre','Becket','Bedford','Belchertown','Bellingham','Belmont','Berkley','Berlin','Bernardston','Beverly','Billerica','Blackstone','Blandford','Bolton','Boston','Bourne','Boxborough','Boxford','Boylston','Braintree','Brewster','Bridgewater','Brimfield','Brockton','Brookfield','Brookline','Buckland','Burlington','Cambridge','Canton','Carlisle','Carver','Charlemont','Charlton','Chatham','Chelmsford','Chelsea','Cheshire','Chester','Chesterfield','Chicopee','Chilmark','Clarksburg','Clinton','Cohasset','Colrain','Concord','Conway','Cummington','Dalton','Danvers','Dartmouth','Dedham','Deerfield','Dennis','Dighton','Douglas','Dover','Dracut','Dudley','Dunstable','Duxbury','East Bridgewater','East Brookfield','East Longmeadow','Eastham','Easthampton','Easton','Edgartown','Egremont','Erving','Essex','Everett','Fairhaven','Fall River','Falmouth','Fitchburg','Florida','Foxborough','Framingham','Franklin','Freetown','Gardner','Georgetown','Gill','Gloucester','Goshen','Gosnold','Grafton','Granby','Granville','Great Barrington','Greenfield','Groton','Groveland','Hadley','Halifax','Hamilton','Hampden','Hancock','Hanover','Hanson','Hardwick','Harvard','Harwich','Hatfield','Haverhill','Hawley','Heath','Hingham','Hinsdale','Holbrook','Holden','Holland','Holliston','Holyoke','Hopedale','Hopkinton','Hubbardston','Hudson','Hull','Huntington','Ipswich','Kingston','Lakeville','Lancaster','Lanesborough','Lawrence','Lee','Leicester','Lenox','Leominster','Leverett','Lexington','Leyden','Lincoln','Littleton','Longmeadow','Lowell','Ludlow','Lunenburg','Lynn','Lynnfield','Malden','Manchester-by-the-Sea','Mansfield','Marblehead','Marion','Marlborough','Marshfield','Mashpee','Mattapoisett','Maynard','Medfield','Medford','Medway','Melrose','Mendon','Merrimac','Methuen','Middleborough','Middlefield','Middleton','Milford','Millbury','Millis','Millville','Milton','Monroe','Monson','Montague','Monterey','Montgomery','Mount Washington','Nahant','Nantucket','Natick','Needham','New Ashford','New Bedford','New Braintree','New Marlborough','New Salem','Newbury','Newburyport','Newton','Norfolk','North Adams','North Andover','North Attleborough','North Brookfield','North Reading','Northampton','Northborough','Northbridge','Northfield','Norton','Norwell','Norwood','Oak Bluffs','Oakham','Orange','Orleans','Otis','Oxford','Palmer','Paxton','Peabody','Pelham','Pembroke','Pepperell','Peru','Petersham','Phillipston','Pittsfield','Plainfield','Plainville','Plymouth','Princeton','Provincetown','Quincy','Randolph','Raynham','Reading','Rehoboth','Revere','Richmond','Rochester','Rockland','Rockport','Rowe','Rowley','Royalston','Russell','Rutland','Salem','Salisbury','Sandisfield','Sandwich','Saugus','Savoy','Scituate','Seekonk','Sharon','Sheffield','Shelburne','Sherborn','Shirley','Shrewsbury','Shutesbury','Somerset','Somerville','South Hadley','Southampton','Southborough','Southbridge','Southwick','Spencer','Springfield','Sterling','Stockbridge','Stoneham','Stoughton','Stow','Sturbridge','Sudbury','Sunderland','Sutton','Swampscott','Swansea','Taunton','Templeton','Tewksbury','Tisbury','Tolland','Topsfield','Townsend','Truro','Tyngsborough','Tyringham','Upton','Uxbridge','Wakefield','Wales','Walpole','Waltham','Ware','Wareham','Warren','Warwick','Washington','Watertown','Wayland','Webster','Wellesley','Wellfleet','Wendell','Wenham','West Boylston','West Bridgewater','West Brookfield','West Newbury','West Springfield','West Stockbridge','West Tisbury','Westborough','Westfield','Westford','Westhampton','Westminster','Weston','Westport','Westwood','Weymouth','Whately','Whitman','Wilbraham','Williamsburg','Williamstown','Wilmington','Winchendon','Winchester','Windsor','Winthrop','Woburn','Worcester','Worthington','Wrentham','Yarmouth']

#Google Distance Matrix API: https://developers.google.com/maps/documentation/distance-matrix/start?refresh=1&authuser=0

table_rows=[]

for TOWN in TOWNS_MA:
    TOWN=TOWN.replace(' ','+') #spaces don't work here for the google API

    request_car = Request('https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins='+TOWN+',MA&destinations=1325+Boylston+Street,Boston,MA&arrival_time=1508155200&key=AIzaSyDUSjSJ4gqbo2Ymhooebqm5cfDUr_zOXz8')

    request_transit = Request('https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins='+TOWN+',MA&destinations=1325+Boylston+Street,Boston,MA&mode=transit&arrival_time=1508155200&key=AIzaSyDUSjSJ4gqbo2Ymhooebqm5cfDUr_zOXz8')

    try:
        response_car = urlopen(request_car)
        distance_car = json.load(response_car)

        response_transit = urlopen(request_transit)
        distance_transit = json.load(response_transit)
        
        try:
            city = TOWN 
            car_time_text = distance_car['rows'][0]['elements'][0]['duration']['text']
            car_time_sec = distance_car['rows'][0]['elements'][0]['duration']['value']
            car_dis_text = distance_car['rows'][0]['elements'][0]['distance']['text']
            car_dis_meters= distance_car['rows'][0]['elements'][0]['distance']['value']
            car_status=distance_car['status']
        except: 
            car_time_text = 'N/A'
            car_time_sec = 969969
            car_dis_text = 'N/A'
            car_dis_meters= 969969
            car_status='N/A'


        try:
            transit_time_text = distance_transit['rows'][0]['elements'][0]['duration']['text']
            transit_time_sec = distance_transit['rows'][0]['elements'][0]['duration']['value']
            transit_dis_text = distance_transit['rows'][0]['elements'][0]['distance']['text']
            transit_dis_meters= distance_transit['rows'][0]['elements'][0]['distance']['value']
            transit_status=distance_transit['status']
        except: 
            transit_time_text = 'N/A'
            transit_time_sec = 969969
            transit_dis_text = 'N/A'
            transit_dis_meters= 969969
            transit_status='N/A'

        table_row= [city,car_time_text,car_time_sec,car_dis_text,car_dis_meters,car_status,transit_time_text,transit_time_sec,transit_dis_text,transit_dis_meters,transit_status]
        table_rows.append(table_row)

        print city,car_time_text,car_time_sec,car_dis_text,car_dis_meters,car_status,transit_time_text,transit_time_sec,transit_dis_text,transit_dis_meters,transit_status

    except URLError, e:
        print 'No kittez. Got an error code:', e
        city=TOWN
        car_time_text = 'N/A'
        car_time_sec = 969969
        car_dis_text = 'N/A'
        car_dis_meters= 969969
        car_status='N/A'
        transit_time_text = 'N/A'
        transit_time_sec = 969969
        transit_dis_text = 'N/A'
        transit_dis_meters= 969969
        transit_status='N/A'
        table_row= [city,car_time_text,car_time_sec,car_dis_text,car_dis_meters,car_status,transit_time_text,transit_time_sec,transit_dis_text,transit_dis_meters,transit_status]
        table_rows.append(table_row)



#print table_rows

with sqlite.connect('yelp_database.db') as con: 
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS travel_times")
    cur.execute("CREATE TABLE travel_times(city TEXT,car_time_text TEXT,car_time_sec REAL,car_dis_text TEXT,car_dis_meters REAL,car_status TEXT ,transit_time_text TEXT,transit_time_sec REAL ,transit_dis_text TEXT ,transit_dis_meters REAL ,transit_status TEXT )")
    cur.executemany( "INSERT INTO travel_times (city,car_time_text,car_time_sec,car_dis_text,car_dis_meters,car_status,transit_time_text,transit_time_sec,transit_dis_text,transit_dis_meters,transit_status) VALUES (?,?,?,?,?,?,?,?,?,?,?)", table_rows)


