import requests
import json
import time
from datetime import datetime

# import statements allow us to request the JSON data, interpret the JSON, and track datetime


def zipcodeValidation(
    code,
):  # zipcode validator is a preventative measure to stop invalid zipcodes from being sent to the API that would call an error

    if len(code) == 5:  # must be 5 characters
        try:
            code = int(code)
        except ValueError:
            return False
        if isinstance(code, int):  # must be all numbers
            return True
        else:
            return False

    else:
        return False


# cleanData and cleanDataSub are both crucial for retrieving and storing our JSON data into python variables for us to manipulate and then present to the client
def cleanData(parsedData, topic):
    if (
        topic == "dt"
    ):  # parses JSON key value pairs and then converts the UTC time to standard time
        return datetime.utcfromtimestamp(parsedData["dt"]).strftime("%Y-%m-%d %H:%M:%S")
    elif topic == "name":
        return parsedData["name"]
    elif topic == "weather":
        return str(((parsedData["weather"])[0])["main"])
    elif topic == "sunrise":
        temp = datetime.utcfromtimestamp((parsedData["sys"])["sunrise"]).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        temp2 = temp.split(" ")
        temp = temp2[1]
        return temp
    elif topic == "sunset":
        temp = datetime.utcfromtimestamp((parsedData["sys"])["sunset"]).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        temp2 = temp.split(" ")
        temp = temp2[1]
        return temp


def cleanDataSub(
    parsedData, topic, subtopic
):  # some JSON data is compartmentalized into subgroups, so a new function is required to access those subtopics
    if topic == "coord":
        if subtopic == "lon":
            return str((parsedData["coord"])["lon"])
        else:
            return str((parsedData["coord"])["lat"])

    elif topic == "main":
        if subtopic == "temp":
            return str(
                round(((((parsedData["main"])["temp"]) - 273.15) * 9 / 5 + 32), 2)
            )
        elif subtopic == "feels_like":
            return str(
                round(((((parsedData["main"])["feels_like"]) - 273.15) * 9 / 5 + 32), 2)
            )
        elif subtopic == "temp_min":
            return str(
                round(((((parsedData["main"])["temp_min"]) - 273.15) * 9 / 5 + 32), 2)
            )
        elif subtopic == "temp_max":
            return str(
                round(((((parsedData["main"])["temp_max"]) - 273.15) * 9 / 5 + 32), 2)
            )
        elif subtopic == "humidity":
            return str((parsedData["main"])["humidity"])

    elif topic == "wind":
        if subtopic == "speed":
            return str((parsedData["wind"])["speed"])


def retrieveData(
    zipcode,
):  # retrieveData is the core API caller of the function and is responsible for accessing the API and then returning a parsed form of the raw JSON
    if zipcodeValidation(zipcode) is True:
        try:
            test_API = requests.get(
                (
                    "https://api.openweathermap.org/data/2.5/weather?zip={},us&appid=1f32df32063a31f7b1a4b4fd9adeefd7".format(
                        zipcode
                    )
                )  # https://api.openweathermap.org/data/2.5/weather?zip=78746,us&appid=1f32df32063a31f7b1a4b4fd9adeefd7
            )
        except:
            print("City not found")

        data = test_API.text
        json.loads(data)
        parse_json = json.loads(data)

        time = parse_json["dt"]
        print(parse_json)
        time = datetime.utcfromtimestamp(time).strftime("%Y-%m-%d %H:%M:%S")
        print(time)
        dataAndTime = data + time
        return parse_json

    else:
        print("Please enter a numeric 5-digit zipcode")


def periodicTimer(
    period,
):  # our time import is used here to set a time interval for the API to be refreshed at depending on the user's requirements
    period -= 1
    while period > 0:
        period -= 1
        print(period)
        if period == 0:
            updatePage(zcode)
        time.sleep(1)


def updatePage(
    zipcode,
):  # updatePage is what opens and rewrites the contents of the HTML file after using cleanData to access fresh data from the API
    dataDict = retrieveData(zipcode)
    if cleanData(dataDict, "weather") == "Clouds":
        weatherBackground = "cloudy"
        tempColor = "currentTempC"
    elif cleanData(dataDict, "weather") == "Sunny":
        weatherBackground = "sunny"
        tempColor = "currentTempS"
    else:
        weatherBackground = ""
        tempColor = ""

    f = open("radarpage.html", "w")  # opens html page under the handle
    message = """<html>
    <head><meta http-equiv="refresh" content="0"> <link rel="stylesheet" href="radarpage.css"></head>
    <body id = "{backgroundID}"> <p id = "{tempID}"> {temp} <span>&#8457;</span> </p> <p>{low}<span>&#8457;</span> {high}<span>&#8457;</span> </p> <p> Feels Like: {feels_like}<span>&#8457;</span>, Humidity: {humidity} </p> <p id = "footer"> {time} <br> City: {city}, Latitude: {latitude}, Longitude: {longitude}</p> <p> Windspeed: {windspeed} MPH </p> <p> Sunrise: {sunrise} Sunset: {sunset}</body>
    </html>""".format(
        city=cleanData(dataDict, "name"),
        latitude=cleanDataSub(dataDict, "coord", "lat"),
        longitude=cleanDataSub(dataDict, "coord", "lon"),
        weather=cleanData(dataDict, "weather"),
        temp=cleanDataSub(dataDict, "main", "temp"),
        low=cleanDataSub(dataDict, "main", "temp_min"),
        high=cleanDataSub(dataDict, "main", "temp_max"),
        feels_like=cleanDataSub(dataDict, "main", "feels_like"),
        humidity=cleanDataSub(dataDict, "main", "humidity"),
        windspeed=cleanDataSub(dataDict, "wind", "speed"),
        time=cleanData(dataDict, "dt"),
        sunrise=cleanData(dataDict, "sunrise"),
        sunset=cleanData(dataDict, "sunset"),
        backgroundID=weatherBackground,
        tempID=tempColor,
    )  # by using .format, I can replace the interim variables in the message variable with the newly updated data retrieved from the API without having to couple the order of the words or deal with lengthy parantheses
    f.write(message)
    f.close()


# main runner below

zcode = input(
    "Enter the zipcode which you want information for:"
)  # user inputs zipcode they want information for
if zipcodeValidation(zcode) is False:
    print("Invalid zipcode")
    exit()  # if the zipcode is invalid, the program will immediately stop

dTime = int(
    input("Enter the time delay:")
)  # entered as seconds, the user specifies how long they want to wait for fresh data

refreshNum = input(
    "How many sets of data would you like?"
)  # for testing purposes mainly and wouldn't be included in a real product where it would simply be constant
refreshNum = int(refreshNum) - 1
updatePage(zcode)
for num in range(refreshNum):
    periodicTimer(dTime)
