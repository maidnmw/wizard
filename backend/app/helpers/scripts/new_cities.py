import app.helpers.mongo_service as mongo_service
import json
import mongoengine
from app.models import City, CityNew, Region

mongoengine.connect(db='wizard-admin', host='localhost:27017')

with open("cities.json", "r") as f:
    file = f.read()

new_cities = json.loads(file)

cities = []

# for new_city in new_cities:
#     city = City.objects(title=new_city['label'])
#     for i in city:
#         if new_city['region'] == i['region']['title']:
#             CityNew(vkId=i['vkId'], title=i['title'],
#                     area=i['area'], region=i['region']).save()
#             print(i['title'], i['region']['title'], i['area'], i['vkId'])

# print(len(cities))

# sad = City.objects(title='Мирный')
# for i in sad:
#     print(i['title'], i['region']['title'], i['area'], i['vkId'])

# mongo_service.add_newcities_list(cities)
