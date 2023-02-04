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


def organizations_search(ll, text, spn):
    search_params = {
        "ll": ll,
        "text": text,
        "spn": spn,
        "lang": "ru_RU",
        "apikey": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
    }
    search_api_server = "https://search-maps.yandex.ru/v1/"
    response = requests.get(search_api_server, params=search_params)
    json_response = response.json()
    organizations = json_response["features"]
    dots = []
    for i in organizations:
        org_coords = i["geometry"]["coordinates"]
        if i["properties"]["CompanyMetaData"]["Hours"]["Availabilities"]:
            if 'круглосуточно' in i["properties"]["CompanyMetaData"]["Hours"]["text"]:
                color = 'gn'
            else:
                color = 'bl'
        else:
            color = 'gr'
        dots.append(f'{org_coords[0]},{org_coords[1]},pm2{color}m1')

    return '~'.join(dots)


def scale_map(response):
    toponym = response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    dots = organizations_search(','.join([toponym_longitude, toponym_lattitude]), 'Аптека',
                                '0.005, 0.005')

    map_params = {
        "l": "map",
        "pt": dots
    }

    return map_params


def main():
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=scale_map(geocode()))

    Image.open(BytesIO(
        response.content)).show()


if __name__ == '__main__':
    main()
