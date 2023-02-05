import sys

import requests


def geocode():
    toponym_to_find = " ".join(sys.argv[1:])

    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json",
    }

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if response:
        json_response = response.json()
    else:
        print(response.reason)
        return
    toponym_coords = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]["Point"]["pos"].replace(' ', ',', 1)
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_coords,
        "format": "json",
        "kind": "district"
    }
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if response:
        json_response = response.json()
    else:
        print(response.reason)
        return
    print(json_response["response"]["GeoObjectCollection"][
              "featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"][
              "Components"][5]["name"])
    return


def main():
    geocode()


if __name__ == '__main__':
    main()
