from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from django.core import serializers
import app.attachment.service as service

@api_view(['POST'])
def add_attachment(request, space_id):
    if request.method == 'POST':
        response = service.add(request, space_id, request.POST.get('taskId'), request.FILES.get('attachment'))
        return HttpResponse(response[1], status=response[0])
        # content_type='application/octet-stream', 

@api_view(['GET'])
def get_by_task_id(request, space_id, task_id):
    if request.method == 'GET':
        response = service.find_by_taskid(request, space_id, task_id)
        return JsonResponse(response[1], status=response[0])

@api_view(['GET', 'DELETE'])
def download_delete_attachment(request, space_id, attachment_id):
    if request.method == 'GET':
        response = service.download_attachment(request, space_id, attachment_id)
        return HttpResponse(response[1], status=response[0])
    elif request.method == 'DELETE':
        response = service.delete(request, space_id, attachment_id)
        return JsonResponse(response[1], status=response[0])