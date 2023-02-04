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
