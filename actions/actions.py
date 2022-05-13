# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals


from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker,ValidationAction, FormValidationAction
from rasa_sdk.events import SlotSet, AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher
from sqlalchemy import union
from weather import Weather
from rasa_sdk.forms import FormValidationAction
from dotenv import dotenv_values
import requests
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pandas as pd
from word2number import w2n

import requests
import json
from random import randint
import datetime
import os
import pafy
import vlc
import time
import random
import re, requests, subprocess, urllib.parse, urllib.request

from database_connectivity import DataUpdate


from rasa_sdk import Action
from rasa_sdk.events import SlotSet, AllSlotsReset
import requests
import json
from random import randint
import datetime
import os
import yaml


class ActionPlaySong(Action):
    def name(self) -> Text:
        return 'action_play_song'
        

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        current_song = next(tracker.get_latest_entity_values("song"),None)
        query_string = urllib.parse.urlencode({"search_query":current_song})
        formatUrl = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)
        search_results = re.findall(r"watch\?v=(\S{11})", formatUrl.read().decode())
        clip2 = "https://www.youtube.com/watch?v=" + "{}".format(search_results[0])
        video = pafy.new(clip2) 	
        videolink = video.getbest()
        media = vlc.MediaPlayer(videolink.url)  
        media.play()
        time.sleep(30)
        media.stop()
        return []



class ActionWeather(Action):

    def name(self) -> Text:
        return "action_weather_api"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    
        current_city=next(tracker.get_latest_entity_values("city"),None)
        temp = Weather(current_city)
    
        dispatcher.utter_message(f"It's {temp} degrees celsius in {current_city} right now")

        return []

from database_connectivity import DataUpdate
class ActionFirstName(Action):
    def name(self) -> Text: 
        """Unique identifier of the form"""
        return "action_last_name"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]: 
        dispatcher.utter_message(response="utter_ask_lastN") 

        return [SlotSet('firstN',tracker.latest_message['text'])]
class ActionFeedback(Action): 
    def name(self) -> Text: 
        """Unique identifier of the form""" 
        return "action_feedback"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]: 
        dispatcher.utter_message(response="utter_ask_feedback")   
        return [SlotSet('lastN',tracker.latest_message['text'])]


class ActionSubmit(Action): 
    def name(self) -> Text: 
        """Unique identifier of the form""" 
        return "action_submit"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]: 
        SlotSet('feedback',tracker.latest_message['text'])
        DataUpdate(tracker.get_slot("firstN"),tracker.get_slot("lastN"),tracker.get_slot("feedback"))
        dispatcher.utter_message("Thanks for the valuable feedback.") 
        return []

class ActionFormInfo(FormValidationAction): 
    def name(self) -> Text: 
        """Unique identifier of the form""" 
        return "form_info"

    @staticmethod 
    def required_slots(tracker: Tracker) -> List[Text]: 
        """A list of required slots that the form has to fill""" 
        return ["firstN", "lastN","feedback"] 
    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]: 
        """A dictionary to map required slots to - an extracted entity - intent: value pairs - a whole message or a list of them, where a first match will be picked """ 
        return {"firstN": [ self.from_entity( entity="firstN",    
                                         intent="FirstName"), ], 
                                          "lastN": [self.from_text()], 
                                           "feedback": [self.from_text()], }
    def submit( self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any], ) -> List[Dict]: 
        """Define what the form has to do after all required slots are filled""" # utter submit template

        dispatcher.utter_message(template="utter_submit",   
        Fname=tracker.get_slot("firstN"), 
        Lname=tracker.get_slot("lastN"), 
        fdbk=tracker.get_slot("feedback")) 
        return []




geolocator = Nominatim(user_agent="rasa_chat")
reverse = RateLimiter(geolocator.reverse, min_delay_seconds=0.1)
API_KEY = dotenv_values()["API_KEY"]

class ActionBeginningSearch(Action):
    def name(self) -> Text:
        return "action_beginning_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Utter message before making search
        dispatcher.utter_message(text=f'Looking for {tracker.get_slot("place_type")} in \
            {", ".join(tracker.get_slot("address"))} with a search radius of {tracker.get_slot("radius")} km')
        return []


class ActionPlacesSearch(Action):
    def __init__(self) -> None:
        # Defining dictionary for mapping to category ids
        self.code_dict = {'restaurants':'13065', 'coffee houses':'13032', 'both restaurants and coffee houses':'13065,13032'}
    
    def name(self) -> Text:
        return "action_places_search"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Getting parameter values from slots
        categories = self.code_dict[tracker.get_slot('place_type')]
        location = tracker.get_slot('lat_lon')
        radius = int(float(tracker.get_slot('radius'))*1000)
        
        # Setting headers to pass to the API call
        headers = {
            "Accept": "application/json",
            "Authorization": API_KEY
        }
        
        params = {'ll':location, 'radius':radius, 'categories':categories}
        url = 'https://api.foursquare.com/v3/places/search'
        
        try:
            # Making the API call
            r = requests.get(url, params=params, headers=headers)
            
            # Parsing the returned json to get desired values
            results = {'name':[], 'lat':[], 'lon':[], 'distance':[]}
            
            for result in r.json()['results']:
                results['name'].append(result['name'])
                results['lat'].append(result['geocodes']['main']['latitude'])
                results['lon'].append(result['geocodes']['main']['longitude'])
                results['distance'].append(result['distance'] / 1000)
            
            df = pd.DataFrame(results)
            
            # We get the latitude and values from the FOURSQUARE API, and we convert them to addresses by reverse geocoding using geopy Nominatim
            df['address'] = df.apply(lambda x: reverse((x['lat'], x['lon']) ).address , axis=1)
            
            # Format the dataframe to bot response
            bot_response = '\n\n'.join(df.apply(lambda x: f"Name: {x['name']} | Address: {x['address']} | Distance: {x['distance']} km", axis=1))
        except:
            # In case we run into an error we return this response
            bot_response = 'No results returned. Try with a different location or larger radius.'
        
        dispatcher.utter_message(text = bot_response)
        return []


class ValidatePredefinedSlots(ValidationAction):
    def validate_address(
        self,
        slot_value: List,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        
        try:
            # Get the latitude and longitude of the address by geocoding using geopy Nominatim
            location = geolocator.geocode(', '.join(slot_value))
            
            if location is None:
                # If the location isn't recognized by geopy Nominatim we return the following message and set the slot value to none
                dispatcher.utter_message(template="utter_wrong_address")
                return {"address": None}
            else:
                # If all is right we keep the address slot value as is. We also set the value of the lat_lon slot using the latitude and longitude value of the current address
                return {"address": slot_value, 'lat_lon': f'{location.latitude},{location.longitude}'}
        except:
            # In case we run into an error we return the following message
            dispatcher.utter_message(text='Facing server issues. Please try again later')

    def validate_radius(
        self,
        slot_value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        
        try:
            # if the user gave a valid number as input we should be able to convert to numeric form
            number =  w2n.word_to_num(slot_value)
            
            # The radius should be between 0 to 100 km. However we don't want to search with radius less that 0.1 km
            if number > 100:
                dispatcher.utter_message(text='Maximum radius is 100 km. Setting radius to 100 km.')
                return {'radius': str(100)}
            elif number < 0.1:
                dispatcher.utter_message(text='Minimum radius is 0.1 km. Setting radius to 0.1 km.')
                return {'radius': str(0.1)}
            else:
                return {'radius': str(number)}
        except:
            # if user gave input that cannot be converted into a number, then we return the following messsage
            dispatcher.utter_message(template="utter_wrong_radius")
            return {"radius": None}

class ValidatePlacesSearchForm(FormValidationAction):
    def name(self) -> Text:
        return 'validate_places_search_form'
    
    def validate_address(
        self,
        slot_value: List,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        
        try:
            # Get the latitude and longitude of the address by geocoding using geopy Nominatim
            location = geolocator.geocode(', '.join(slot_value))
            
            if location is None:
                # If the location isn't recognized by geopy Nominatim we return the following message and set the slot value to none
                dispatcher.utter_message(template="utter_wrong_address")
                return {"address": None}
            else:
                # If all is right we keep the address slot value as is. We also set the value of the lat_lon slot using the latitude and longitude value of the current address
                return {"address": slot_value, 'lat_lon': f'{location.latitude},{location.longitude}'}
        except:
            # In case we run into an error we return the following message
            dispatcher.utter_message(text='Facing server issues. Please try again later')
    
    def validate_radius(
        self,
        slot_value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        
        try:
            # if the user gave a valid number as input we should be able to convert to numeric form
            number =  w2n.word_to_num(slot_value)
            
            # The radius should be between 0 to 100 km. However we don't want to search with radius less that 0.1 km
            if number > 100:
                dispatcher.utter_message(text='Maximum radius is 100 km. Setting radius to 100 km.')
                return {'radius': str(100)}
            elif number < 0.1:
                dispatcher.utter_message(text='Minimum radius is 0.1 km. Setting radius to 0.1 km.')
                return {'radius': str(0.1)}
            else:
                return {'radius': str(number)}
        except:
            # if user gave input that cannot be converted into a number, then we return the following messsage
            dispatcher.utter_message(template="utter_wrong_radius")
            return {"radius": None}
