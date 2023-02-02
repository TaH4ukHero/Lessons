import sys
from io import BytesIO

import requests
from PIL import Image


def geocode():
    toponym_to_find = " ".join(sys.argv[1:])

    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if response:
        json_response = response.json()
    else:
        print(response.reason)
        return
    return json_response


def scale_map(response):
    toponym = response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    toponym_upperCorner, toponym_lowerCorner = toponym["boundedBy"]["Envelope"]["upperCorner"].split(
        ' '), \
                                               toponym["boundedBy"]["Envelope"]["lowerCorner"].split(
                                                   ' ')

    delta_longitude = float(toponym_upperCorner[0]) - float(toponym_lowerCorner[0])
    delta_lattitude = float(toponym_upperCorner[1]) - float(toponym_lowerCorner[1])

    delta = f"{delta_longitude},{delta_lattitude}"

    dot = f"{toponym_longitude},{toponym_lattitude},pm2blm1"

    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": delta,
        "l": "map",
        "pt": dot
    }

    return map_params


def main():
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=scale_map(geocode()))

    Image.open(BytesIO(
        response.content)).show()


if __name__ == '__main__':
    main()
