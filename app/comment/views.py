from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from django.core import serializers
import app.comment.service as service

@api_view(['PUT'])
def update_comment(request, space):
    if request.method == 'PUT':
        response = service.update(request, space_id, request.body)
        return JsonResponse(response[1], status=response[0])
    
@api_view(['DELETE'])
def delete_comment(request,space_id,id):
    if request.method == 'DELETE':
        response = service.delete(request, space_id, id)
        return JsonResponse(response[1], status=response[0])

@api_view(['GET'])
def get_by_task_id(request, space, task_id):
    if request.method == 'GET':
        response = service.find_by_taskid(request, space, task_id)
        return JsonResponse(response[1], status=response[0])