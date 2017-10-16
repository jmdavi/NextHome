import sqlite3 as sqlite
import json, sys

#input = open('output_bookssharon2.json', 'rU')

table_rows=[]

with open('output_booksMA.json') as json_data:
    listOfJSON = json.load(json_data)
    for shop in listOfJSON:
    	#print shop
    	name= shop['name']
    	rating= shop['rating']
    	review_count= shop['review_count']
    	try: #we find that sometimes this field doesn't exist
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

	#Genre Table
	cur.execute("DROP TABLE IF EXISTS shops")
	cur.execute("CREATE TABLE shops(name TEXT, rating REAL, review_count INTEGER, price TEXT, latitude REAL, longitude REAL, address TEXT, city TEXT, categories TEXT )")
	cur.executemany( "INSERT INTO shops (name, rating, review_count, price,latitude,longitude,address,city,categories) VALUES (?,?,?,?,?,?,?,?,?)", table_rows)


#SQLITE code to be run afterwards
#CREATE TABLE shops_distinct AS
#SELECT DISTINCT * FROM shops

#SELECT City, count(name), GROUP_CONCAT(name,','),review_count, avg(rating)
#FROM shops_distinct
#GROUP BY City
#ORDER BY avg(rating) DESC, count(name)DESC, review_count DESC





	