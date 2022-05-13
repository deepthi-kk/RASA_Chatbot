# RASA_Chatbot (RASA 3.1.0)

* **This chatbot can be used during driving. This chatbot gives information about the restraunts nearby, plays a song and answers queries about the weather in a specific city.**
* **This is a voice based chatbot which recieves voice commands responds verbally too.**


## Activating OpenWeatherMap API

The below needs to be modified in and a valid API key should be inserted in weather.py. API key is available from https://openweathermap.org/
```
api_address="http://api.openweathermap.org/data/2.5/weather?q=city&appid=YOUR_APIKEY"
```
## Activating Youtube api

The YouTube API is an application programming interface that allows you to embed videos, curate playlists, and offer other YouTube functionalities on your website.

You can log in to Google Developers Console using your Google account, create an Youtube API key and paste the key in action.py.

```
API_KEY = dotenv_values()["YOUR_APIKEY"]
```
## Activating Places Search API

To use any the FOURSQUARE APIs, first we need to make a developer’s account on FOURSQUARE. Then we create a new project and generate a new API key. We can find the procedure on the FOURSQUARE website.

We need to keep the API key secret, so a common practice is to retrieve it as an environment variable. To do this we make a file with the name ‘.env’ in the project’s root directory. The contents of the .env file will be similar to that shown below.
```
API_KEY=replace_this_with_your_api_key
```
## Running the Chatbot

### Install the required Libraries
```
pip install requirements.txt
```

### Train the Model

```
rasa train
```
To start the rasa chatbot in backend now add the following lines of code to send the received text (from step 1) to rasa chatbot externally and to get the corresponding out for it.
```
rasa run -m models --endpoints endpoints.yml --port 5002 --credentials credentials.yml
```
Now to see your voice bot in action run the Voice_bot.py file and also run the action server using

```
rasa run actions
```
**Give voice commands for the bot to respond**

There you go! Happy coding.
