from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from django.core import serializers
import app.stage.service as service

@api_view(['GET', 'PUT'])
def get_update_stage(request, spaceId):
    if request.method == 'GET':
        response = service.find(request, spaceId)
        return JsonResponse(response[1], status=response[0])
    if request.method == 'PUT':
        response = service.update(request, spaceId, request.body)
        return JsonResponse(response[1], status=response[0])

@api_view(['GET', 'DELETE'])
def by_id(request, spaceId, project_id, id):
    if request.method == 'GET':
        response = service.find_by_id(request, spaceId, project_id, id)
        return JsonResponse(response[1], status=response[0])
    if request.method == 'DELETE':
        response = service.delete(request, spaceId, project_id, id)
        return JsonResponse(response[1], status=response[0])