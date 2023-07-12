import requests
from datetime import datetime

def get_upcoming_launches():
    url = "https://api.spacexdata.com/v4/launches/upcoming"
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception if request fails

    launches = response.json()
    return launches

def display_launch_details(launch):
    flight_number = launch['flight_number']
    mission_name = launch['name']
    launch_date_unix = launch['date_unix']
    launch_date = datetime.fromtimestamp(launch_date_unix)
    rocket_type = launch['rocket']
    payloads = launch['payloads']
    articles = launch['links']['article']
    videos = launch['links']['webcast']

    print("Flight Number:", flight_number)
    print("Mission Name:", mission_name)
    print("Launch Date:", launch_date)
    print("Rocket Type:", rocket_type)
    print("Payloads:", payloads)
    print("Articles:", articles)
    print("Videos:", videos)
    print("--------------------------------------")

try:
    upcoming_launches = get_upcoming_launches()
    for launch in upcoming_launches:
        display_launch_details(launch)
except requests.exceptions.HTTPError as err:
    print("HTTP Error:", err)
except requests.exceptions.RequestException as err:
    print("Error:", err)
