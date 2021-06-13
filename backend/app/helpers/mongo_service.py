from app.models import Region, City, VkUser


def add_region(region):
    vkId = int(region.get('id', None))
    title = region.get('title', None)

    if Region.objects(vkId=vkId).first() == None:
        print('Region added: ', region)
        Region(vkId=vkId, title=title).save()
    return


def add_regions_list(regions):
    for region in regions:
        add_region(region)


def add_city(city, region_vk_id):
    vkId = int(city.get('id', None))
    title = city.get('title', None)
    area = city.get('area', None)
    region = Region.objects(vkId=region_vk_id).first()

    if not region:
        return

    if City.objects(vkId=vkId).first() == None:
        # print('City added: ', city)
        City(vkId=vkId, title=title, area=area, region=region).save()
    return


def add_cities_list(cities, region_vk_id):
    for city in cities:
        add_city(city, region_vk_id)


def add_user(user, city_vk_id, groups):
    vkId = int(user.get('id', None))
    firstName = user.get('first_name', None)
    lastName = user.get('last_name', None)
    bdate = user.get('bdate')
    city = City.objects(vkId=city_vk_id).first()
    groups = list(map(str, groups))
    totalGroups = len(groups)

    if VkUser.objects(vkId=vkId).first() == None:
        # print('City added: ', city)
        VkUser(vkId=vkId, firstName=firstName, lastName=lastName, bdate=bdate,
               city=city, groups=groups, totalGroups=totalGroups).save()
