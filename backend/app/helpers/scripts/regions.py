import json
from app.models import Region
import mongoengine

mongoengine.connect(db='wizard-admin', host='localhost:27017')

with open('cities.json', 'r') as f:
    data = f.read()

cities = json.loads(data)

regions = []
for i in cities:
    regions.append(i['region'])

regions = list(dict.fromkeys(regions))

region_counter = 0


not_included_regions = []

db_regions = [i['title'] for i in Region.objects()]
for reg in regions:
    if not(reg in db_regions):
        not_included_regions.append(reg)

print(not_included_regions)
