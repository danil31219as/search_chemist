from distance import lonlat_distance
from coordinates import get_coor
from scale import set_spn
import requests
from io import BytesIO
from PIL import Image


def set_centr(coor_1, coor_2):
    x1, y1 = map(float, coor_1.split(','))
    x2, y2 = map(float, coor_2.split(','))
    return [str((x1 + x2) / 2), str((y1 + y2) / 2)]


address_ll = ','.join(get_coor(input()).split())
search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'

search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": address_ll,
    "type": "biz"
}
response = requests.get(search_api_server, params=search_params)
if not response:
    pass
json_response = response.json()
organization = json_response["features"][0]
org_name = organization["properties"]["CompanyMetaData"]["name"]
org_address = organization["properties"]["CompanyMetaData"]["address"]
time_of_work = organization["properties"]["CompanyMetaData"]['Hours']['text']
point = organization["geometry"]["coordinates"]
org_point = "{0},{1}".format(point[0], point[1])
map_params = {
    "ll": ','.join(set_centr(address_ll, org_point)),
    "spn": ",".join(set_spn(address_ll, org_point)),
    "l": "map",
    "pt": "{0},pm2dgl~{1},pm2dgl".format(org_point, address_ll)
}
print(org_name, org_address, time_of_work, str(int(lonlat_distance(org_point, address_ll))) + 'м', sep='\n')
map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)
Image.open(BytesIO(
    response.content)).show()
