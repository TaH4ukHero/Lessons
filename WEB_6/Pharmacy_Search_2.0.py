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


def organization_search(ll, text, spn):
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
    organization = json_response["features"][0]
    org_name = organization["properties"]["CompanyMetaData"]["name"]
    org_address = organization["properties"]["CompanyMetaData"]["address"]
    org_time = organization["properties"]["CompanyMetaData"]["Hours"]["text"]
    org_coords = organization["geometry"]["coordinates"]
    return [org_address, org_name, org_time, org_coords]


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

    org_params = organization_search(','.join([toponym_longitude, toponym_lattitude]), 'Аптека',
                                     delta)
    org_longitude, org_lattitude = org_params[-1][0], org_params[-1][1]

    dots = f"{toponym_longitude},{toponym_lattitude},pm2blm1~{org_longitude},{org_lattitude},pm2blm1"

    map_params = {
        "l": "map",
        "pt": dots
    }
    d = int((((float(toponym_longitude) - org_longitude) ** 2 + (float(toponym_lattitude) -
                                                                 org_lattitude)
              ** 2) ** 0.5) * 111128)
    print(f'Адрес: {org_params[0]}\nНазвание: {org_params[1]}\nРасписание: '
          f'{org_params[2]}\nРасстояние: {d} метров')

    return map_params


def main():
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=scale_map(geocode()))

    Image.open(BytesIO(
        response.content)).show()


if __name__ == '__main__':
    main()
