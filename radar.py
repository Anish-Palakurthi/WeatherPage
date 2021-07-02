import requests
import json
import time
from datetime import datetime


def zipcodeValidation(code):

    if len(code) == 5:
        try:
            code = int(code)
        except ValueError:
            return False
        if isinstance(code, int):
            return True
        else:
            return False

    else:
        return False


def cleanData(parsedData, topic):
    if topic == "dt":
        return datetime.utcfromtimestamp(parsedData["dt"]).strftime("%Y-%m-%d %H:%M:%S")
    elif topic == "name":
        return parsedData["name"]
    elif topic == "weather":
        return str(((parsedData["weather"])[0])["main"])
    elif topic == "sunrise":
        return datetime.utcfromtimestamp((parsedData["sys"])["sunrise"]).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    elif topic == "sunset":
        return datetime.utcfromtimestamp((parsedData["sys"])["sunset"]).strftime(
            "%Y-%m-%d %H:%M:%S"
        )


def cleanDataSub(parsedData, topic, subtopic):
    if topic == "coord":
        if subtopic == "lon":
            return str((parsedData["coord"])["lon"])
        else:
            return str((parsedData["coord"])["lat"])

    elif topic == "main":
        if subtopic == "temp":
            return str((parsedData["main"])["temp"])
        elif subtopic == "feels_like":
            return str((parsedData["main"])["feels_like"])
        elif subtopic == "temp_min":
            return str((parsedData["main"])["temp_min"])
        elif subtopic == "temp_max":
            return str((parsedData["main"])["temp_max"])
        elif subtopic == "humidity":
            return str((parsedData["main"])["humidity"])

    elif topic == "wind":
        if subtopic == "speed":
            return str((parsedData["wind"])["speed"])


def retrieveData(zipcode):
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


def periodicTimer(period):  # enter period as seconds
    period -= 1
    while period > 0:
        period -= 1
        print(period)
        if period == 0:
            updatePage(zcode)
        time.sleep(1)


def updatePage(zipcode):
    dataDict = retrieveData(zipcode)
    f = open("radarpage.html", "w")
    message = """<html>
    <head><meta http-equiv="refresh" content="0"></head>
    <body> <h1> {time} </h1> <p> City: {city}, Latitude: {latitude}, Longitude: {longitude}</p><p>Weather conditions: {weather}</p> <p>Temperature: {temp} <br> Low: {low}, High: {high}, Feels Like: {feels_like}, Humidity: {humidity} </p></body>
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
    )
    f.write(message)
    f.close()


# main runner
zcode = input("Enter the zipcode which you want information for:")
if zipcodeValidation(zcode) is False:
    print("Invalid zipcode")
    exit()

dTime = int(input("Enter the time delay:"))

refreshNum = input("How many sets of data would you like?")
refreshNum = int(refreshNum) - 1
updatePage(zcode)
for num in range(refreshNum):
    periodicTimer(dTime)
