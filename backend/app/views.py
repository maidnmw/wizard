from app.models import VkUser, Institute
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
        groups = list(map(str, groups[0].split(',')))
        direction = self.detect_direction(groups)
        # remake to return json, not str
        return Response(direction)

    def detect_direction(self, groups: list) -> str:
        return DetectionDetector().predict(groups)


class DirectionsList(APIView):
    def post(self, request):
        candidates = request.POST.get('candidates')
        if not candidates:
            return Response({'detail': 'No candidates provided'}, status=422)
        directions = self.detect_directions(candidates)

        return Response(directions)

    def detect_directions(self, candidates: list) -> list:
        return DetectionDetector().predict_candidates_list(candidates)


class Candidates(APIView):
    def get(self, request):
        age_from = request.GET.get('age_from')
        age_to = request.GET.get('age_to')
        region = request.GET.get('region')
        cities_list = request.GET.get('cities')
        cities = cities_list if cities_list else None

        vk = VkApi()
        vk.get_cities(region_id=region, count=50)
        users = vk.get_users_by_cities(
            cities=cities, age_from=age_from, age_to=age_to)

        return Response(users)


class Regions(APIView):
    def get(self, request):
        country = request.GET.get('country')

        regions = VkApi().get_regions(country_id=country)

        return Response(regions)


class DevCandidates(APIView):
    def get(self, request):
        age_from = request.GET.get('age_from')
        age_to = request.GET.get('age_to')
        region = request.GET.get('region')
        city = request.GET.get('city')

        vk = VkApi()
        # vk.get_cities(region_id=region)
        # print(cities)

        users = vk.get_users_by_cities_dev(age_from, age_to)

        return Response(users)


class DevCities(APIView):
    def get(self, request):
        region_id = request.GET.get('region_id')
        count = request.GET.get('count')

        cities = VkApi().get_cities(region_id=region_id, count=count)

        return Response(cities)


class DevAllCities(APIView):
    def get(self, request):
        region_id = request.GET.get('region_id')

        cities = VkApi().add_all_cities()

        return Response(cities)


class RegionPopulation(APIView):
    def get(self, request):
        age_from = request.GET.get('age_from')
        age_to = request.GET.get('age_to')
        region = request.GET.get('region')

        vk = VkApi()
        vk.get_cities(region_id=region)
        users = vk.population_by_cities(
            cities=None, age_from=age_from, age_to=age_to)

        return Response(users)


class DbCitiesToUsers(APIView):
    def get(self, request):
        vk = VkApi()
        vk.users_to_db(age_from=15, age_to=20)

        return Response({'success': 'db cities to users was successfully ended'})


class DbUsersPredict(APIView):
    def get(self, request):
        users = VkUser.objects()
        for u in users:
            res = DetectionDetector().predict_with_allowed(u.groups)
            inst = Institute.objects(code=res['university_group']).first()
            u.institute = inst
            u.allowedGroups = res['allowed_groups']
            u.successPercentage = res['success_percentage']
            u.save()
