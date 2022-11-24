from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response

class repair(APIView):
    def post(self, request, format=None):
        return Response(request.body)