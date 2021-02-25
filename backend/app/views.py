from rest_framework.views import APIView
from rest_framework.response import Response


class Direction(APIView):
    def get(self, request, format=None):
        queryList = request.GET.getlist('groups')
        groups = []

        if len(queryList) > 0:
            groups = queryList[0].split(',')

        groups = list(map(int, groups))

        # Добавить вызов функции для определения направления
        direction = "Прикладная информатика"

        return Response(direction)