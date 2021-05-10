import logging

from rest_framework.views import APIView
from rest_framework.response import Response

from app.direction_detector import DetectionDetector
from app.vk import VkApi


log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
log.addHandler(handler)


class Direction(APIView):
    def get(self, request, format=None):
        log.info(f'GET [Direction]: {request}')
        groups = request.GET.getlist('groups')
        if not groups:
            return Response({'detail': 'No groups provided'}, status=422)
        print('bb', groups)
        groups = list(map(str, groups[0].split(',')))
        print('aa', groups)
        direction = self.detect_direction(groups)
        # remake to return json, not str
        return Response(direction)

    def detect_direction(self, groups: list) -> str:
        return DetectionDetector().predict(groups)


class Candidates(APIView):
    def get(self, request):
        age_from = request.GET.get('age_from')
        age_to = request.GET.get('age_to')
        region = request.GET.get('region')
        city = request.GET.get('city')

        cities = VkApi().get_cities(region_id=region)
        cities = cities['response']['items']
        # print(cities)
        # cities_ids = [city['id'] for city in cities['response']['items']]
        users = VkApi().get_users_by_cities(cities, age_from, age_to)
        # print(users)
        # print(age, region, city)
        return Response(users)

class Regions(APIView):
    def get(self, request):
        country = request.GET.get('country')

        regions = VkApi().get_regions(country_id=country)

        return Response(regions)