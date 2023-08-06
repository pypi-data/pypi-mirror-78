import requests
from pprint import pprint

class Wrapper:
    def __init__(self):
        self.headers = {'Content-Type': 'application/json'} 
        self.url = "https://www.wlnupdates.com/api" #API link


    def get_series_data(self, id):
        payload = '{"id":'+ id +', "mode": "get-series-id"}'
        response = requests.request("POST", self.url, headers=self.headers, data=payload)
        json_data = response.json()
        if json_data['error'] is True:
            message = 'Error! '+json_data['message']
            return message
        else:
            return json_data

    def get_watches(self, id):
        payload = '{"id":'+ id +', "mode": "get-tag-id"}'
        response = requests.request("POST", self.url, headers=self.headers, data=payload)
        try:
            json_data = response.json()
        except:
            return f"ID: {id} does not exist"
        if json_data['error'] is True:
            message = 'Error! '+json_data['message']
            return message
        else:
            return json_data

    def get_publisher_data(self, id):
        payload = '{"id":'+ id +', "mode": "get-publisher-id"}'
        response = requests.request("POST", self.url, headers=self.headers, data=payload)
        try:
            json_data = response.json()
        except:
            return f"ID: {id} does not exist"
        if json_data['error'] is True:
            message = 'Error! '+json_data['message']
            return message
        else:
            return json_data

    def get_group_data(self, id):
        payload = '{"id":'+ id +', "mode": "get-group-id"}'
        response = requests.request("POST", self.url, headers=self.headers, data=payload)
        try:
            json_data = response.json()
        except:
            return f"ID: {id} does not exist"
        if json_data['error'] is True:
            message = 'Error! '+json_data['message']
            return message
        else:
            return json_data

    def get_artist_data(self, id):
        payload = '{"id":'+ id +', "mode": "get-artist-id"}'
        response = requests.request("POST", self.url, headers=self.headers, data=payload)
        try:
            json_data = response.json()
        except:
            return f"ID: {id} does not exist"
        if json_data['error'] is True:
            message = 'Error! '+json_data['message']
            return message
        else:
            return json_data

    def get_author_data(self, id):
        payload = '{"id":'+ id +', "mode": "get-author-id"}'
        response = requests.request("POST", self.url, headers=self.headers, data=payload)
        try:
            json_data = response.json()
        except:
            return f"ID: {id} does not exist"
        if json_data['error'] is True:
            message = 'Error! '+json_data['message']
            return message
        else:
            return json_data

    def get_genre_data(self, id):
        payload = '{"id":'+ id +', "mode": "get-genre-id"}'
        response = requests.request("POST", self.url, headers=self.headers, data=payload)
        try:
            json_data = response.json()
        except:
            return f"ID: {id} does not exist"
        if json_data['error'] is True:
            message = 'Error! '+json_data['message']
            return message
        else:
            return json_data

