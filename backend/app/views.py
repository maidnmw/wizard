import logging

from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.throttling import AnonRateThrottle

from app.direction_detector import DetectionDetector

# log = logging.getLogger(__name__)
# log.setLevel(logging.INFO)
# handler = logging.StreamHandler()
# handler.setLevel(logging.INFO)
# log.addHandler(handler)


class Direction(APIView):
    throttle_scope = 'anon'

    def get(self, request, format=None):
        groups = request.GET.getlist('groups')
        if not groups:
            return Response({'detail': 'No groups provided'}, status=422)

        groups = list(map(str, groups[0].split(',')))
        direction = self.detect_direction(groups)
        # remake to return json, not str
        return Response(direction)

    def detect_direction(self, groups: list) -> str:
        return DetectionDetector().predict(groups)
