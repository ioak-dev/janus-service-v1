from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from django.core import serializers
import app.project_team.service as service

@api_view(['POST','DELETE'])
def post_delete(request, space_id, project_id, team_id):
    if request.method == 'POST':
        response = service.add(request, space_id, project_id, team_id)
        return JsonResponse(response[1], status=response[0])
    if request.method == 'DELETE':
        response = service.delete(request, space_id, project_id, team_id)
        return JsonResponse(response[1], status=response[0])


@api_view(['DELETE'])
def delete_by_id(request, space_id, id):
    if request.method == 'DELETE':
        response = service.delete_by_id(request, space_id, id)
        return JsonResponse(response[1], status=response[0])

@api_view(['GET'])
def get(request, space_id):
    if request.method == 'GET':
        response = service.find(request, space_id)
        return JsonResponse(response[1], status=response[0])
