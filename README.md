# NextHome

## Overview
This codebase is being used to gather and analyze data for places we might like to live around Boston, MA. Essentially, we use Python and several API's including Yelp and Google to collect information into a SQLite database, where further analysis can be done. For the sake of this project, we will provide the finished product of the database file (NextHome_database.db) in addition to the Python scripts interacting with the API's.

Documentation and links to various helpful components:

[Yelp Fusion API documentation](https://www.yelp.com/developers/documentation/v3)

[Yelp Fusion examples - Github](https://www.???)

[Google Maps - Distance Matrix API documentation](https://developers.google.com/maps/documentation/distance-matrix/start)

[Google Maps - Places API Web Service documentation](https://developers.google.com/places/web-service/intro)

[MA 2016 Presidential Voting Data By City](http://www.wbur.org/politicker/2016/11/08/massachusetts-election-map)

## Using SQLite for analysis

As mentioned, we will try to keep the database up-to-date with some of the latest info. We'll include queries that can be run on the data in a file called report1.sql. Also, we recommend installing the program DB Browser for SQLite to see into NextHome_database.db.

# How-to

## Gathering from Yelp Fusion
Before doing anything else, run the following to install the dependencies:
`pip install -r requirements.txt`.

To run the code without specifying any arguments (thereby utilizing the DEFAULT values we altered):
`python sample.py`. Alternatively, run the code sample by specifying the optional arguments:
`python sample.py --term="bars" --location="San Francisco, CA"`

Specifically, we've used the following files to pull information `python yelp_api_to_json.py` with optional parameters.
Then to get into SQLite database use `python yelptosql.py`.

## Gathering from Google Distance Matrix API
The first API calls we made were to determine how long morning commutes would be, via the Distance Matrix API. Just run `python Google_Distance_Matrix_API.py` to compile for all towns in MA against the target destination (Boston) to arrive by 8 a.m. It would definitely be possible to generalize the code and accept command-line inputs.

