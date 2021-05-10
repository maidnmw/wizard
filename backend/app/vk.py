import requests
import time
from typing import List

from app.direction_detector import DetectionDetector


class VkApiMeta(type):
  _instances = {}

  def __init__(self, name, bases, mmbs):
      super(VkApiMeta, self).__init__(name, bases, mmbs)
      self._instance = super(VkApiMeta, self).__call__()

  def __call__(self, *args, **kw):
      return self._instance


class VkApi(metaclass=VkApiMeta):
  """Singleton to VK API class"""

  def __init__(self):
    self.token = '55c2bf56254c2a83be515360d5bdf750bee71b74039ad7317c63c80f750eec3423d1d2b2188644b0cdfe2'
    self.vk_version = '5.130'

  def get_regions(self, country_id=1):
    url = f'https://api.vk.com/method/database.getRegions?v={self.vk_version}&access_token={self.token}&country_id={country_id}'
    res = requests.get(url)
    return res.json()

  def get_cities(self, region_id, country_id=1):
    url = f'https://api.vk.com/method/database.getCities?v={self.vk_version}&access_token={self.token}&country_id={country_id}&region_id={region_id}&need_all=0'
    res = requests.get(url)
    return res.json()
  
  def get_users_by_cities(self, cities, age_from=0, age_to=99):
    cities_result = []

    # VK API max requests count is 5/sec
    for city in cities:
      done = False
      
      while not done:
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


    candidates_groups = self.get_users_predictions(candidates_list)

    for i in candidates_list:
      for j in candidates_groups:
        if i['id'] == j['id']:
          i['prediction'] = j['prediction']
    # print(candidates_groups)
    # arr = self.detect_users_direction(candidates_groups)

    return candidates_list


  def get_users_predictions(self, users: List[dict]):
    result = []

    for candidate in users:
      done = False
      
      while not done:
        url = f'https://api.vk.com/method/groups.get?v={self.vk_version}&access_token={self.token}&user_id={candidate["id"]}'
        res = requests.get(url).json()
        try:
          if len(res['response']['items']) > 0:
            groups = list(map(str, res['response']['items']))
            result.append({
              'id': candidate["id"],
              'prediction': DetectionDetector().predict_with_allowed(groups)
            })
          done = True
        except:
          # Too many requests per second error code 
          if res['error']['error_code'] == 6:
            done = False
          else:
            done = True

    return result

  def detect_users_direction(self, candidates):
    result = []
    for candidate in candidates:
      groups = list(map(str, candidate['groups']))
      result.append({
        'user': candidate['id'],
        'prediction': DetectionDetector().predict_with_allowed(groups)
        })
    return result

  def __clear_close_profiles(self, users: List[dict]):
    profiles_list = []
    for user in users:
      if user['can_access_closed'] == True:
        profiles_list.append(user)
    return profiles_list
