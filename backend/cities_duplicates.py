import mongoengine
from app.models import VkUser, City

mongoengine.connect(db='wizard-admin', host='localhost:27017')

counter = {}
u = City.objects()
for i in u:
    counter[f'{i.vkId}'] = []

for i in u:
    counter[f'{i.vkId}'].append(i)

to_delete = []
c = 0
for key, value in counter.items():
    if len(value) > 1:
        c += 1
        to_delete.append(value)
print(to_delete)

# users = VkUser.objects()
# [print(user.city.vkId) for user in users]

# to_delete[1].delete()
# for i in range(len(to_delete)-1):
#     if i > 0:
#         to_delete[i].delete()
# for i in to_delete:
#     del counter[i]

# for key, value in counter.items():
#     # user = VkUser.objects(city=value[1])
# value[1].delete()
# user.city = value[0]

# city_index = list(City.objects()).index(city)
# print(city_index)
