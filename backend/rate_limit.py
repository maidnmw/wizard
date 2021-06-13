import mongoengine
from app.models import VkUser, City

mongoengine.connect(db='wizard-admin', host='localhost:27017')


u = VkUser.objects()[len(VkUser.objects())-1]
print(u['firstName'])

print(u.successPercentage)
city = u.city
print(city.title)
city_index = list(City.objects()).index(city)
print(city_index)
