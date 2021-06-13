import logging
import requests
import time
from math import ceil
from typing import List

import app.helpers.mongo_service as mongo_service
from app.direction_detector import DetectionDetector
from app.helpers.response import res_error_parser
from app.models import City, VkUser

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
s_handler = logging.StreamHandler()
s_handler.setLevel(logging.INFO)

f_handler = logging.FileHandler(filename='logs/error-logs.log')
f_handler.setLevel(logging.ERROR)
log.addHandler(s_handler)
log.addHandler(f_handler)


# class VkApiMeta(type):
#   _instances = {}

#   def __init__(self, name, bases, mmbs):
#     super(VkApiMeta, self).__init__(name, bases, mmbs)
#     self._instance = super(VkApiMeta, self).__call__()

#   def __call__(self, *args, **kw):
#     return self._instance


class VkApi():
    """Singleton to VK API class"""

    def __init__(self):
        """
            GET TOKEN
            https://oauth.vk.com/authorize?client_id=7864484&scope=327680&display=page&redirect_uri=https://oauth.vk.com/blank.html&response_type=token&v=5.130
        """
        self.token = '4e0572514e524b3b76f702169db701e9dfebffd85c1707a6e5ca58f3b08608bcd7aec1f611b81b76b3c70'
        self.vk_version = '5.130'

    def get_regions(self, country_id=1):
        log.info(f'Get regions by [country_id: {country_id}]')
        url = f'https://api.vk.com/method/database.getRegions?v={self.vk_version}&access_token={self.token}&country_id={country_id}'
        res = requests.get(url).json()

        mongo_service.add_regions_list(res['response']['items'])
        return res

    def get_cities(self, region_id, country_id=1, count=None):
        log.info(
            f'Get cities by [country_id: {country_id}], [region_id: {region_id}] [offset_from: 0], [offset_to: 1000]')

        url = f'https://api.vk.com/method/database.getCities?v={self.vk_version}&access_token={self.token}&country_id={country_id}&region_id={region_id}&need_all=0&count={count if count else 1000}'
        res = requests.get(url).json()

        if (res.get('error')):
            log.error(res)
            return res

        self.cities = res.get('response', {}).get('items')
        self.cities_count = res.get('response', {}).get('count')

        if count:
            return self.cities

        log.info(
            f'Cities [count is {self.cities_count}] in [region_id: {region_id}]')

        # Vk api getCities max count is 1000
        for i in range(1, ceil(self.cities_count/1000)):
            while True:
                log.info(
                    f'Get cities in [region_id: {region_id}], [offset_from: {(i)*1000}], [offset_to: {(i+1)*1000}]')

                url = f'https://api.vk.com/method/database.getCities?v={self.vk_version}&access_token={self.token}&country_id={country_id}&region_id={region_id}&need_all=1&offset={1000*i}&count=1000'
                res = requests.get(url).json()

                res_error_parser(
                    res, f'FAILED get cities in [region_id: {region_id}], [offset_from: {(i)*1000}], [offset_to: {(i+1)*1000}]')

                res_cities = res.get('response', {}).get('items')
                if res_cities:
                    self.cities = self.cities + res_cities
                    break

        log.info(
            f'Final cities [count: {len(self.cities)}] in [region_id: {region_id}]')

        mongo_service.add_cities_list(self.cities, region_id)

        return self.cities

    def users_to_db(self, age_from=0, age_to=99):
        # cities = City.objects()[1892:]
        cities = City.objects(vkId=2236)

        for city in cities:
            while True:
                log.info(
                    f'Get users in [city_id: {city["vkId"]}], [city_title: {city["title"]}], [age_from: {age_from}], [age_to: {age_to}]')
                url = f'https://api.vk.com/method/users.search?v={self.vk_version}&access_token={self.token}&city={city["vkId"]}&age_from={age_from}&age_to={age_to}&fields=bdate&count=1000'
                res = requests.get(url).json()

                error = res_error_parser(
                    res, f'FAILED get users in [city_id: {city["vkId"]}], [city_title: {city["title"]}, [age_from: {age_from}], [age_to: {age_to}]')

                if error:
                    continue

                res_citizens = res.get('response', {}).get('items')
                # We cant access user groups on close profiles
                res_citizens = self.__clear_close_profiles(res_citizens)

                for user in res_citizens:
                    u = VkUser.objects(vkId=user.get('id')).first()
                    if u == None:
                        groups = self.get_user_groups(user)
                        if groups:
                            mongo_service.add_user(
                                user, city['vkId'], groups)
                            print(f'user {user["id"]} added')
                    else:
                        print(f'user {u.vkId} already existed')
                break

    def get_users_by_cities(self, cities=None, age_from=0, age_to=99):
        log.info(
            f'Get users by cities [age_from: {age_from}], [age_to: {age_to}]')
        cities = self.cities if cities == None else cities
        citizens = []

        # VK API max requests count is 5/sec
        for city in cities:
            while True:
                log.info(
                    f'Get users in [city_id: {city["id"]}], [city_title: {city["title"]}], [age_from: {age_from}], [age_to: {age_to}]')
                url = f'https://api.vk.com/method/users.search?v={self.vk_version}&access_token={self.token}&city={city["id"]}&age_from={age_from}&age_to={age_to}&fields=bdate'
                res = requests.get(url).json()

                error = res_error_parser(
                    res, f'FAILED get users in [city_id: {city["id"]}], [city_title: {city["title"]}, [age_from: {age_from}], [age_to: {age_to}]')

                if error:
                    continue

                res_citizens = res.get('response', {}).get('items')
                # We cant access user groups on close profiles
                res_citizens = self.__clear_close_profiles(res_citizens)
                for user in res_citizens:
                    citizens.append({
                        'id': user.get('id'),
                        'first_name': user.get('first_name'),
                        'last_name': user.get('last_name'),
                        'bdate': user.get('bdate'),
                        'city': city.get('title'),
                        'groups': self.get_user_groups(user)
                    })
                break

        # candidates_groups = self.get_users_predictions(citizens)

        # for i in citizens:
        #     for j in candidates_groups:
        #         if i['id'] == j['id']:
        #             i['prediction'] = j['prediction']
        candidates = self.detect_users_direction(citizens)

        return candidates

    def get_user_groups(self, user):
        res_groups = None
        while True:
            url = f'https://api.vk.com/method/groups.get?v={self.vk_version}&access_token={self.token}&user_id={user["id"]}'
            res = requests.get(url).json()

            error = res_error_parser(
                res, f'FAILED get user groups [id: {user["id"]}]')

            if error and error.get('error_code') == 6:
                continue
            elif error and error.get('error_code') == 7:
                break

            res_groups = res.get('response', {}).get('items')
            break

        return res_groups

    # def get_users_predictions(self, users: List[dict]):
    #     result = []

    #     for candidate in users:
    #         done = False

    #         while not done:
    #             url = f'https://api.vk.com/method/groups.get?v={self.vk_version}&access_token={self.token}&user_id={candidate["id"]}'
    #             res = requests.get(url).json()
    #             try:
    #                 if len(res['response']['items']) > 0:
    #                     groups = list(map(str, res['response']['items']))
    #                     result.append({
    #                         'id': candidate["id"],
    #                         'prediction': DetectionDetector().predict_with_allowed(groups)
    #                     })
    #                 done = True
    #             except:
    #                 # Too many requests per second error code
    #                 if res['error']['error_code'] == 6:
    #                     done = False
    #                 else:
    #                     done = True

    #     return result

    def detect_users_direction(self, candidates):
        # result = []
        for candidate in candidates:
            groups = list(map(str, candidate['groups']))
            candidate['prediction'] = DetectionDetector(
            ).predict_with_allowed(groups)

        return candidates

    def __clear_close_profiles(self, users: List[dict]):
        profiles_list = []
        for user in users:
            if user['can_access_closed'] == True:
                profiles_list.append(user)
        return profiles_list

    def get_users_by_cities_dev(self, age_from=0, age_to=99):
        cities_result = []

        # for city in cities:
        done = False

        while not done:
            url = f'https://api.vk.com/method/users.search?v={self.vk_version}&access_token={self.token}&city=49&birth_day=12&birth_month=1&birth_year=1998'
            res = requests.get(url).json()
            print(res)
            try:
                if len(res['response']['items']) > 0:
                    cities_result.append({
                        'city': city['title'],
                        'users': self.__clear_close_profiles(res['response']['items'])
                    })
                done = True
            except:
                done = False

        return cities_result

    def get_users_count(self, city_id, age_from=0, age_to=99):
        cities_result = []

        # for city in cities:
        done = False

        while not done:
            url = f'https://api.vk.com/method/users.search?v={self.vk_version}&access_token={self.token}&country=1&age_from=16&age_to=19'
            res = requests.get(url).json()
            print(res)
            try:
                if len(res['response']['items']) > 0:
                    cities_result.append({
                        'city': city['title'],
                        'users': self.__clear_close_profiles(res['response']['items'])
                    })
                done = True
            except:
                done = False

        return cities_result

    def population_by_cities(self, cities=None, age_from=0, age_to=99):
        log.info(
            f'Get population by cities [age_from: {age_from}], [age_to: {age_to}]')
        cities = self.cities if cities == None else cities
        cities_result = []

        # VK API max requests count is 5/sec
        for city in cities:
            done = False

            while not done:
                log.info(
                    f'Try get population in [city_id: {city["id"]}], [city_title: {city["title"]}], [age_from: {age_from}], [age_to: {age_to}]')
                url = f'https://api.vk.com/method/users.search?v={self.vk_version}&access_token={self.token}&city={city["id"]}&age_from={age_from}&age_to={age_to}'
                res = requests.get(url).json()
                try:
                    if len(res['response']['items']) > 0:
                        cities_result.append({
                            'city': city['title'],
                            'users': self.__clear_close_profiles(res['response']['items'])
                        })
                    done = True
                except:
                    log.info(
                        f'FAILED try get population in [city_id: {city["id"]}], [city_title: {city["title"]}, [age_from: {age_from}], [age_to: {age_to}]')
                    done = False

        candidates_list = []
        for city in cities_result:
            for user in city['users']:
                candidates_list.append({
                    'id': user['id'],
                    'first_name': user['first_name'],
                    'last_name': user['last_name'],
                    'city': city['city'],
                })

        return {
            'count': len(candidates_list),
            'candidates': candidates_list
        }

    def add_all_cities(self, country_id=1):
        url = f'https://api.vk.com/method/database.getRegions?v={self.vk_version}&access_token={self.token}&country_id={country_id}'
        res = requests.get(url).json()

        regions = res.get('response', {}).get('items')

        cities = []
        for region in regions:
            cities = cities + self.get_cities(region_id=region.get('id'))

        mongo_service.add_cities_list(cities)
        return {}
