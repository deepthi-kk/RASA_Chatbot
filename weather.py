import requests

def Weather(city):
    api_address="http://api.openweathermap.org/data/2.5/weather?q=city&appid=c5ec0648cd942b88dd37affb4dc0ddb9"
    # city = input('Enter the City Name :')
    json_data = requests.get(api_address).json()
    format_add = json_data['main']

        
    return int(format_add['temp']-273)