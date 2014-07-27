'''
Created on Jun 21, 2014

@author: Allwinleoprakash
'''

__author__ = "Allwinleoprakash"

import requests
import sys

#variable for the api key
FLICKR_API_KEY = ""

#base url for activity requests to FLICKR 
BASE_URL_FLICKR = "https://api.flickr.com/services/rest/"

def setApiKey():
    """It loads the API key from flickr_api.txt"""
    global FLICKR_API_KEY
    try:
        #reads the api key from the flickr_api.txt file
        fp = open("flickr_api.txt")
        FLICKR_API_KEY = fp.readline()
        if FLICKR_API_KEY == "":
            print("The flickr_api.txt file appears to be blank")
            print("If you do not have an API Key from FLICKR, please register for one at: https://www.flickr.com/services/api/misc.api_keys.html")
            sys.exit(0)
                
        fp.close()
    except IOError:
        print('API Key not found! Please create and fill up flickr_api.txt file in the same directory which contains the FLICKR module')
        print('If you do not have an API Key from FLICKR, please register for one at: https://www.flickr.com/services/api/misc.api_keys.html')
        sys.exit(0)
    except Exception as e:
        print(e)

def defaultSearch(baseUrl,params):
    """function for searching the activities
    
    INPUT -> 
        baseUrl : base url for getting google plus activities
        params : a dictionary of GET request parameters
    
    OUTPUT -> 
        response : returns the response returned by the google server as a python dictionary object
    """
    global API_REQUEST_COUNT 
    try:
        #GET request sent to Flickr
        r = requests.get(baseUrl,params=params)
       
        #response in json format converted into a dictionary
        response = eval(r.text)
        return response

    except Exception as e:
        print("Error for URL: ", r.url)
        print(e)
        return { 'status':'ERROR', 'statusInfo':r.status_code }

def fullSearch():
    """function for iterating through the entire set of activites for a particular query through all the pages. 
    
    INPUT ->
        q : the search query
        options : a dictionary of options as provided by the google plus api .Please check here
                    https://www.flickr.com/services/api/flickr.photos.getRecent.html
                    for the details of the various options available.
                    
    
    OUTPUT -> 
        response : returns activity 
    """
    
    #dictionary for containing the GET query parameters.
    params = {}
    params["format"] = 'json'
    #setting the query parameter
    params["method"] = 'flickr.photos.getRecent'
    #setting the FLICKR  api key
    params["api_key"] = FLICKR_API_KEY
    #setting the parameter for the number of returned results to 20
    params["time_frame"] = '5d'
    #setting the order of the returned results to recent.
    params["nojsoncallback"] = 1
    
    resp = defaultSearch(BASE_URL_FLICKR, params)
    # Get the content within tag "photos"
    photos = resp["photos"]
    # Get the number of pages into a variable
    pages = photos["pages"]
    # Iterate through the pages to retrieve activities
    for x in range(1,pages+1):
        params["page"] = x
        resp = defaultSearch(BASE_URL_FLICKR, params)
        photos = resp["photos"]
        for item in photos["photo"]:
            print item
