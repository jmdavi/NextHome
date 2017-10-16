import sqlite3 as sqlite
import json, sys

#takes JSON output from Yelp API and inserts into SQLite database

#below assumes one list, but you may have a list of lists of JSON data
#therefore, you may need to alter the JSON file by replacing the string '][' with a comma ','
#(untested)
#with open('output_yelp.json') as f:
#    newText=f.read().replace('][', ',')
#with open('output_yelp.json', "w") as f:
#    f.write(newText)


table_rows=[]

with open('output_yelp.json') as json_data:
    listOfJSON = json.load(json_data)
    for shop in listOfJSON:
    	#print shop
    	name= shop['name']
    	rating= shop['rating']
    	review_count= shop['review_count']
    	try: #we find that sometimes this field doesn't exist. Should be dollar signs, e.g., '$$'
    		price= shop['price']
    	except: price='N/A'
    	latitude= shop['coordinates']['latitude']
    	longitude= shop['coordinates']['longitude']
    	address= shop['location']['display_address']
    	address=', '.join(address)
    	city= shop['location']['city']
    	categories= shop['categories']
    	aliases=[]
    	for x in categories:
    		aliases.append(x['alias'])
    	aliases=', '.join(aliases)
    	table_row=[name,rating,review_count,price,latitude,longitude,address,city,aliases]
    	table_rows.append(table_row)
    	#print table_row
    	#print table_rows



with sqlite.connect('yelp_database.db') as con: 
	cur = con.cursor()
	#Uncomment next lines if you want to do destructive refreshes of Yelp data
	#cur.execute("DROP TABLE IF EXISTS shops")
	#cur.execute("CREATE TABLE shops(name TEXT, rating REAL, review_count INTEGER, price TEXT, latitude REAL, longitude REAL, address TEXT, city TEXT, categories TEXT )")
	cur.executemany( "INSERT INTO shops (name, rating, review_count, price,latitude,longitude,address,city,categories) VALUES (?,?,?,?,?,?,?,?,?)", table_rows)


#SQL code to dedupe JSON afterwards (almost certainly necessary)
#CREATE TABLE shops_distinct AS
#SELECT DISTINCT * FROM shops

	
