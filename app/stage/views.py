from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from django.core import serializers
import app.stage.service as service

@api_view(['GET', 'PUT'])
def get_update_stage(request, space_id):
    if request.method == 'GET':
        response = service.find(request, space_id)
        return JsonResponse(response[1], status=response[0])
    if request.method == 'PUT':
        response = service.update(request, space_id, request.body)
        return JsonResponse(response[1], status=response[0])

@api_view(['GET', 'DELETE'])
def by_id(request, space_id, id):
    if request.method == 'GET':
        response = service.find_by_id(request, space_id, id)
        return JsonResponse(response[1], status=response[0])
    if request.method == 'DELETE':
        response = service.delete(request, space_id, id)
        print(response[1])
        return JsonResponse(response[1], status=response[0])

@api_view(['POST'])
def move_stage(request, space_id, project_id):
    print('**************')
    if request.method == 'POST':
        response = service.move_stage(request, space_id, project_id, request.body)
        return JsonResponse(response[1], status=response[0])