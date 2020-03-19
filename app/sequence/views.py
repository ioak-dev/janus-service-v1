from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
import app.sequence.service as service

@api_view(['GET', 'PUT'])
def get_update_sequence(request, space):
    if request.method == 'GET':
        response = service.find(request, space)
        return JsonResponse(response[1], status=response[0])
    if request.method == 'PUT':
        response = service.update(request, space, request.body)
        return JsonResponse(response[1], status=response[0])
    
@api_view(['DELETE'])
def delete_sequence(request,space,id):
    if request.method == 'DELETE':
        response = service.delete(request, space, id)
        return JsonResponse(response[1], status=response[0])

@api_view(['GET'])
def get_by_id(request, space, id):
    if request.method == 'GET':
        response = service.find_by_id(request, space, id)
        return JsonResponse(response[1], status=response[0])

@api_view(['GET'])
def get_sequence(request, space, field, context):
    if request.method == 'GET':
        response = service.next_sequence(request, space, field, context)
        return JsonResponse(response[1], status=response[0])