from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from django.core import serializers
import app.log.service as service

@api_view(['GET'])
def find_logs(request, space, domain_name, reference):
    if request.method == 'GET':
        response = service.find_logs(request, space, domain_name, reference)
        return JsonResponse(response[1], status=response[0])
