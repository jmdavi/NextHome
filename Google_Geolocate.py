#!/usr/bin/env python

"""
Google Distance Matrix API calls
Finds latitude and longitude for different towns in Massachusetts
Then stores data as dictionary file and SQLite table for later reference
"""

from urllib2 import Request, urlopen, URLError
import json 
import sqlite3 as sqlite


TOWNS_MA=['Abington','Acton','Acushnet','Adams','Agawam','Alford','Amesbury','Amherst','Andover','Aquinnah','Arlington','Ashburnham','Ashby','Ashfield','Ashland','Athol','Attleboro','Auburn','Avon','Ayer','Barnstable','Barre','Becket','Bedford','Belchertown','Bellingham','Belmont','Berkley','Berlin','Bernardston','Beverly','Billerica','Blackstone','Blandford','Bolton','Boston','Bourne','Boxborough','Boxford','Boylston','Braintree','Brewster','Bridgewater','Brimfield','Brockton','Brookfield','Brookline','Buckland','Burlington','Cambridge','Canton','Carlisle','Carver','Charlemont','Charlton','Chatham','Chelmsford','Chelsea','Cheshire','Chester','Chesterfield','Chicopee','Chilmark','Clarksburg','Clinton','Cohasset','Colrain','Concord','Conway','Cummington','Dalton','Danvers','Dartmouth','Dedham','Deerfield','Dennis','Dighton','Douglas','Dover','Dracut','Dudley','Dunstable','Duxbury','East Bridgewater','East Brookfield','East Longmeadow','Eastham','Easthampton','Easton','Edgartown','Egremont','Erving','Essex','Everett','Fairhaven','Fall River','Falmouth','Fitchburg','Florida','Foxborough','Framingham','Franklin','Freetown','Gardner','Georgetown','Gill','Gloucester','Goshen','Gosnold','Grafton','Granby','Granville','Great Barrington','Greenfield','Groton','Groveland','Hadley','Halifax','Hamilton','Hampden','Hancock','Hanover','Hanson','Hardwick','Harvard','Harwich','Hatfield','Haverhill','Hawley','Heath','Hingham','Hinsdale','Holbrook','Holden','Holland','Holliston','Holyoke','Hopedale','Hopkinton','Hubbardston','Hudson','Hull','Huntington','Ipswich','Kingston','Lakeville','Lancaster','Lanesborough','Lawrence','Lee','Leicester','Lenox','Leominster','Leverett','Lexington','Leyden','Lincoln','Littleton','Longmeadow','Lowell','Ludlow','Lunenburg','Lynn','Lynnfield','Malden','Manchester-by-the-Sea','Mansfield','Marblehead','Marion','Marlborough','Marshfield','Mashpee','Mattapoisett','Maynard','Medfield','Medford','Medway','Melrose','Mendon','Merrimac','Methuen','Middleborough','Middlefield','Middleton','Milford','Millbury','Millis','Millville','Milton','Monroe','Monson','Montague','Monterey','Montgomery','Mount Washington','Nahant','Nantucket','Natick','Needham','New Ashford','New Bedford','New Braintree','New Marlborough','New Salem','Newbury','Newburyport','Newton','Norfolk','North Adams','North Andover','North Attleborough','North Brookfield','North Reading','Northampton','Northborough','Northbridge','Northfield','Norton','Norwell','Norwood','Oak Bluffs','Oakham','Orange','Orleans','Otis','Oxford','Palmer','Paxton','Peabody','Pelham','Pembroke','Pepperell','Peru','Petersham','Phillipston','Pittsfield','Plainfield','Plainville','Plymouth','Princeton','Provincetown','Quincy','Randolph','Raynham','Reading','Rehoboth','Revere','Richmond','Rochester','Rockland','Rockport','Rowe','Rowley','Royalston','Russell','Rutland','Salem','Salisbury','Sandisfield','Sandwich','Saugus','Savoy','Scituate','Seekonk','Sharon','Sheffield','Shelburne','Sherborn','Shirley','Shrewsbury','Shutesbury','Somerset','Somerville','South Hadley','Southampton','Southborough','Southbridge','Southwick','Spencer','Springfield','Sterling','Stockbridge','Stoneham','Stoughton','Stow','Sturbridge','Sudbury','Sunderland','Sutton','Swampscott','Swansea','Taunton','Templeton','Tewksbury','Tisbury','Tolland','Topsfield','Townsend','Truro','Tyngsborough','Tyringham','Upton','Uxbridge','Wakefield','Wales','Walpole','Waltham','Ware','Wareham','Warren','Warwick','Washington','Watertown','Wayland','Webster','Wellesley','Wellfleet','Wendell','Wenham','West Boylston','West Bridgewater','West Brookfield','West Newbury','West Springfield','West Stockbridge','West Tisbury','Westborough','Westfield','Westford','Westhampton','Westminster','Weston','Westport','Westwood','Weymouth','Whately','Whitman','Wilbraham','Williamsburg','Williamstown','Wilmington','Winchendon','Winchester','Windsor','Winthrop','Woburn','Worcester','Worthington','Wrentham','Yarmouth']


#Google Distance Matrix API: https://developers.google.com/maps/documentation/distance-matrix/start

table_rows=[]
town_dic= {}

for TOWN in TOWNS_MA:
    TOWN_CONC=TOWN.replace(' ','+') #spaces don't work here for the google API, e.g. 'North Adams'
    #makes the API call with modified value
    request = Request('https://maps.googleapis.com/maps/api/geocode/json?address='+TOWN_CONC+',MA&key=AIzaSyCkyES69Lfwk8JrAeBGD0Mlt4u3Rk4P-_Y')
    print TOWN #logging

    try:
        longLatLookup = urlopen(request)
        longLatLookup = json.load(longLatLookup)

        city = TOWN
        latitude= longLatLookup['results'][0]['geometry']['location']['lat']
        longitude= longLatLookup['results'][0]['geometry']['location']['lng']

    except URLError, e:
        print 'No kittez. Got an error code:', e
        city = TOWN
        latitude= 0
        longitude= 0
      
    #save info into list, then into list of lists
    table_row=[city, latitude, longitude]
    table_rows.append(table_row)
    #save info into dictionary
    town_dic[TOWN] = str(latitude)+','+str(longitude)
        
#logging
print table_rows
print town_dic


#export dictionary 
f = open('town_lat_long.txt','w')
f.write(str(town_dic))
f.close()

#print table_rows #logging

#insert into SQLite database
with sqlite.connect('NextHome_database.db') as con: 
    cur = con.cursor()
    #destructive refresh if next two lines are not commented out
    cur.execute("DROP TABLE IF EXISTS town_lat_long")
    cur.execute("CREATE TABLE town_lat_long( city TEXT, latitude REAL, longitude REAL)")
    cur.executemany( "INSERT INTO town_lat_long (city, latitude, longitude) VALUES (?,?,?)", table_rows)


