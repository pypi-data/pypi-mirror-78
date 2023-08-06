#Python file for searching novels by string and exporting ID
import requests
import sys
import json
from pprint import pprint
class Search:
    def __init__(self):
        self.headers = {'Content-Type': 'application/json'} 
        self.url = "https://www.wlnupdates.com/api" #API link


    def title_search(self, name, similarityNum=0, fullList=False): #similarityNum is the variable for finding how big of a similarity
            payload = '{"title": "'+name+'", "mode": "search-title"}'
            response = requests.request("POST", self.url, headers=self.headers, data=payload)
            json_data = response.json()
            json_data = json_data['data']['results']
            if fullList is True:
                idList = []                
                for results in json_data:
                    if results['match'][0][0] >= similarityNum:
                        idList.append(results)
                
                return idList

            else:
                pprint(json_data)

    def search_advanced(self, name=None, tag_category=None, genre_category=None, chapter_limits=None, series_type=None, sort_mode=None):
        payload = {"mode": "search-advanced"}
        if name:
            payload['title-search-text'] = name
        if series_type:
            payload['series-type'] = series_type
        if tag_category:
            payload['tag-category'] = tag_category
        if genre_category:
            payload['genre-category'] = genre_category
        if chapter_limits:
            payload['chapter-limits'] = chapter_limits

        if sort_mode:
            payload['sort-mode'] = sort_mode
        payload = json.dumps(payload)
        response = requests.request("POST", self.url, headers=self.headers, data=str(payload))
        json_data = response.json()
        return json_data
    

    


