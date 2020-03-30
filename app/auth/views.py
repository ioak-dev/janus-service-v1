from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from app.auth.service import generate_keys, get_keys, do_signup, do_signin, do_jwttest, do_signin_via_jwt
from django.core import serializers
import json

@api_view(['GET'])
def keys(request, spaceId):
    response = generate_keys()
    return JsonResponse(response[1], status=response[0])

@api_view(['POST'])
def signup(request, spaceId):
    response = do_signup(spaceId, request.body)
    return JsonResponse(response[1], status=response[0])

@api_view(['GET'])
def getKeys(request, spaceId, email):
    response = get_keys(spaceId, email)
    return HttpResponse(response[1].get('problem'), status=response[0])

@api_view(['POST'])
def signin(request, spaceId):
    response = do_signin(spaceId, request.body)
    return JsonResponse(response[1], status=response[0])

@api_view(['GET'])
def jwtTest(request, spaceId):
    response = do_jwttest(spaceId)
    return HttpResponse(response[1], status=response[0])

@api_view(['POST'])
def signin_jwt(request, spaceId):
    response = do_signin_via_jwt(spaceId, request.body)
    return JsonResponse(response[1], status=response[0])