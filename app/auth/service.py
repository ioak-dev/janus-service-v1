import os, datetime, time, requests
from pymongo import MongoClient
import secrets, jwt, time
import library.db_utils as db_utils
import library.jwt_utils as jwt_utils
import app.user.service as user_service

DATABASE_URI = os.environ.get('DATABASE_URI')

self_space_id = 'janus'
domain="user"

def do_jwttest(space_id):
    space = db_utils.find(self_space_id, domain, {'name': space_id})[0]
    jwtPassword = space.get('jwtPassword')
    return (200, jwt.encode({
            'userId': '4587439657496t',
            'name': 'test user display name',
            'email': 'q1@1.com',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        }, jwtPassword, algorithm='HS256').decode('utf-8'))

def do_signin_via_jwt(space_id, data):
    spaceData=db_utils.find(self_space_id, domain, {'name': space_id})
    #spaceData = db_utils.find(space, domain, {'name': space})
    jwtPassword = spaceData.get('jwtPassword')
    jwtToken = data.get('jwtToken')
    tokenData = jwt.decode(jwtToken, jwtPassword, algorithm='HS256')
    user = db_utils.find(space_id, domain, {'email': tokenData.get('email')})
    #user = db_utils.find(space, domain,{'email': tokenData.get('email')})
    if user is None:
        db_utils.upsert(space_id, domain, {
            'name': tokenData.get('name'),
            'email': tokenData.get('email'),
            'type': 'JWT_USER'
        })
    else:
        db_utils.upsert(space_id, domain, {
            {'_id': user.get('_id')},
            {
                'name': tokenData.get('name'),
                'email': tokenData.get('email'),
                'type': 'JWT_USER'
            }
        })
    
    user = db_utils.find(space_id, domain, {'email': tokenData.get('email')})
    return (200, {
        'name': user.get('name'),
        'email': user.get('email'),
        'token': jwt.encode({
                'name': str(user.get('_id')),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8)
            }, jwtPassword, algorithm='HS256').decode('utf-8'),
        'space_id': space_id,
        'secret': 'none'
    })

def get_session(space_id, auth_key):
    start_time = int(round(time.time() * 1000))
    response = requests.get('http://127.0.0.1:8020/auth/' + space_id + '/session/' + auth_key)
    oa_time = int(round(time.time() * 1000))
    if response.status_code != 200:
        return (response.status_code, response.json())
    oa_response = jwt_utils.decode(response.json()['token'])
    existing_user_data = user_service.find_by_user_id(space_id, oa_response['userId'])
    if len(existing_user_data) == 1:
        existing_user_data[0]['token'] = response.json()['token']
        res_time = int(round(time.time() * 1000))
        print(start_time, oa_time, res_time)
        return (200, {'data': existing_user_data[0]})
    else:
        new_data = user_service.insert_user(space_id, {
            '_id': oa_response['userId'],
            'name': oa_response['name'],
            'email': oa_response['email']
        })
        new_data['token'] = response.json()['token']
        return (200, {'data': new_data})
