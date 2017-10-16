# -*- coding: utf-8 -*-
"""
Yelp Fusion API code sample.

This program demonstrates the capability of the Yelp Fusion API
by using the Search API to query for businesses by a search term and location,
and the Business API to query additional information about the top result
from the search query.

Please refer to http://www.yelp.com/developers/v3/documentation for the API
documentation.

This program requires the Python requests library, which you can install via:
`pip install -r requirements.txt`.

Sample usage of the program:
`python sample.py --term="bars" --location="San Francisco, CA"`
"""
from __future__ import print_function

import argparse
import json
import pprint
import requests
import sys
import urllib
import re
import csv 
import urllib2
from bs4 import BeautifulSoup


# This client code can run on Python 2.x or 3.x.  Your imports can be
# simpler if you only need one of those.
try:
    # For Python 3.0 and later
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2 and urllib
    from urllib2 import HTTPError
    from urllib import quote
    from urllib import urlencode


# OAuth credential placeholders that must be filled in by users.
# You can find them on
# https://www.yelp.com/developers/v3/manage_app
CLIENT_ID = '3-P7Vz57L7f4_vIJv5mr6Q'
CLIENT_SECRET = 'pZr70wDzEgfsrOl75CmbzUBhhXbjleT5sWRooEKxu6eJkr7sWXy0MI224f5ZRNDg'


# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.
TOKEN_PATH = '/oauth2/token'
GRANT_TYPE = 'client_credentials'


#towns in MA
TOWNS_MA=['Abington','Acton','Acushnet','Adams','Agawam','Alford','Amesbury','Amherst','Andover','Aquinnah','Arlington','Ashburnham','Ashby','Ashfield','Ashland','Athol','Attleboro','Auburn','Avon','Ayer','Barnstable','Barre','Becket','Bedford','Belchertown', 'Bellingham','Belmont','Berkley','Berlin','Bernardston','Beverly','Billerica','Blackstone','Blandford','Bolton','Boston', 'Bourne', 'Boxborough','Boxford','Boylston','Braintree','Brewster','Bridgewater','Brimfield','Brockton','Brookfield','Brookline','Buckland','Burlington','Cambridge','Canton','Carlisle', 'Carver','Charlemont','Charlton','Chatham','Chelmsford','Chelsea','Cheshire','Chester','Chesterfield','Chicopee','Chilmark','Clarksburg','Clinton','Cohasset','Colrain','Concord','Conway','Cummington','Dalton','Danvers','Dartmouth','Dedham','Deerfield','Dennis','Dighton','Douglas','Dover','Dracut','Dudley','Dunstable','Duxbury','East Bridgewater','East Brookfield','East Longmeadow','Eastham','Easthampton','Easton','Edgartown','Egremont','Erving','Essex','Everett','Fairhaven','Fall River','Falmouth','Fitchburg','Florida','Foxborough','Framingham','Franklin','Freetown','Gardner','Georgetown','Gill','Gloucester','Goshen','Gosnold','Grafton','Granby','Granville','Great Barrington','Greenfield','Groton','Groveland','Hadley','Halifax','Hamilton','Hampden','Hancock','Hanover','Hanson','Hardwick','Harvard','Harwich','Hatfield','Haverhill','Hawley','Heath','Hingham','Hinsdale','Holbrook','Holden','Holland','Holliston','Holyoke','Hopedale','Hopkinton','Hubbardston','Hudson','Hull','Huntington','Ipswich','Kingston','Lakeville','Lancaster','Lanesborough','Lawrence','Lee','Leicester','Lenox','Leominster','Leverett','Lexington','Leyden','Lincoln','Littleton','Longmeadow','Lowell','Ludlow','Lunenburg','Lynn','Lynnfield','Malden','Manchester-by-the-Sea','Mansfield','Marblehead','Marion','Marlborough','Marshfield','Mashpee','Mattapoisett','Maynard','Medfield','Medford','Medway','Melrose','Mendon','Merrimac','Methuen','Middleborough','Middlefield','Middleton','Milford','Millbury','Millis','Millville','Milton','Monroe','Monson','Montague','Monterey','Montgomery','Mount Washington','Nahant','Nantucket','Natick','Needham','New Ashford','New Bedford','New Braintree','New Marlborough','New Salem','Newbury','Newburyport','Newton','Norfolk','North Adams','North Andover','North Attleborough','North Brookfield','North Reading','Northampton','Northborough','Northbridge','Northfield','Norton','Norwell','Norwood','Oak Bluffs','Oakham','Orange','Orleans','Otis','Oxford','Palmer','Paxton','Peabody','Pelham','Pembroke','Pepperell','Peru','Petersham','Phillipston','Pittsfield','Plainfield','Plainville','Plymouth','Princeton','Provincetown','Quincy','Randolph','Raynham','Reading','Rehoboth','Revere','Richmond','Rochester','Rockland','Rockport','Rowe','Rowley','Royalston','Russell','Rutland','Salem','Salisbury','Sandisfield','Sandwich','Saugus','Savoy','Scituate','Seekonk','Sharon','Sheffield','Shelburne','Sherborn','Shirley','Shrewsbury','Shutesbury','Somerset','Somerville','South Hadley','Southampton','Southborough','Southbridge','Southwick','Spencer','Springfield','Sterling','Stockbridge','Stoneham','Stoughton','Stow','Sturbridge','Sudbury','Sunderland','Sutton','Swampscott','Swansea','Taunton','Templeton','Tewksbury','Tisbury','Tolland','Topsfield','Townsend','Truro','Tyngsborough','Tyringham','Upton','Uxbridge','Wakefield','Wales','Walpole','Waltham','Ware','Wareham','Warren','Warwick','Washington','Watertown','Wayland','Webster','Wellesley','Wellfleet','Wendell','Wenham','West Boylston','West Bridgewater','West Brookfield','West Newbury','West Springfield ','West Stockbridge','West Tisbury','Westborough','Westfield','Westford','Westhampton','Westminster','Weston','Westport','Westwood','Weymouth','Whately','Whitman','Wilbraham ','Williamsburg','Williamstown','Wilmington','Winchendon','Winchester','Windsor','Winthrop','Woburn','Worcester','Worthington','Wrentham','Yarmouth']



# Defaults for our simple example.
DEFAULT_TERM = 'restaurant'
DEFAULT_LOCATION = 'Sharon, MA'
SEARCH_LIMIT = 45 #default=20, max=50
DEFAULT_CATEGORIES = 'vegetarian'
RADIUS= 0






def obtain_bearer_token(host, path):
    """Given a bearer token, send a GET request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        str: OAuth bearer token, obtained using client_id and client_secret.

    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    assert CLIENT_ID, "Please supply your client_id."
    assert CLIENT_SECRET, "Please supply your client_secret."
    data = urlencode({
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': GRANT_TYPE,
    })
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
    }
    response = requests.request('POST', url, data=data, headers=headers)
    bearer_token = response.json()['access_token']
    return bearer_token


def request(host, path, bearer_token, url_params=None):
    """Given a bearer token, send a GET request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        bearer_token (str): OAuth bearer token, obtained using client_id and client_secret.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % bearer_token,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search(bearer_token, term, location, categories, radius):
    """Query the Search API by a search term and location.

    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.

    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'categories': categories.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, bearer_token, url_params=url_params)


def get_business(bearer_token, business_id):
    """Query the Business API by a business ID.

    Args:
        business_id (str): The ID of the business to query.

    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path, bearer_token)


def query_api(term, location, categories, radius):
    """Queries the API by the input values from the user.

    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    bearer_token = obtain_bearer_token(API_HOST, TOKEN_PATH)

    response = search(bearer_token, term, location, categories, radius)

    businesses = response.get('businesses')
    #print(businesses)

    if not businesses:
        print(u'No businesses for {0} in {1} found.'.format(term, location))
        return

    with open('output_vegRestMA.json', 'a') as outfile:
        json.dump(businesses, outfile)

    # business_id = businesses[0]['id']

    # print(u'{0} businesses found, querying business info ' \
    #     'for the top result "{1}" ...'.format(
    #         len(businesses), business_id))
    # response = get_business(bearer_token, business_id)

    # print(u'Result for business "{0}" found:'.format(business_id))
    # pprint.pprint(response, indent=2)
    
        

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM,
                        type=str, help='Search term (default: %(default)s)')
    parser.add_argument('-l', '--location', dest='location',
                        default=DEFAULT_LOCATION, type=str,
                        help='Search location (default: %(default)s)')
    parser.add_argument('-c', '--categories', dest='categories',
                        default=DEFAULT_CATEGORIES, type=str,
                        help='Search category (default: %(default)s)')
    parser.add_argument('-r', '--radius', dest='radius',
                        default=RADIUS, type=str,
                        help='Search radius (default: %(default)s)')
 

    input_values = parser.parse_args()
    
    for x in TOWNS_MA:
        location=x+', MA'
        print(location)
        try:
            query_api(input_values.term, location, input_values.categories, input_values.radius)
        except HTTPError as error:
            sys.exit(
                'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                    error.code,
                    error.url,
                    error.read(),
                )
            )


if __name__ == '__main__':
    main()
