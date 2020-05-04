import os, datetime, time
import library.db_utils as db_utils

domain = 'team.member'

def find(request, space_id):
    data = db_utils.find(space_id, domain, {})
    return (200, {'data': data})

def add(request, space_id, team_id, user_id):
    existing_list = db_utils.find(space_id, domain, {'teamId': team_id, 'userId': user_id})
    if len(existing_list) == 0:
        inserted_record = db_utils.upsert(space_id, domain, {'teamId': team_id, 'userId': user_id}, request.user_id)
        return (200, {'data': inserted_record})
    else:
        return (200, {'data': existing_list[0]})

def delete(request, space_id, team_id, user_id):
    result = db_utils.delete(space_id, domain, {'teamId': team_id, 'userId': user_id}, request.user_id)
    return (200, {'deleted_count': result.deleted_count})

def delete_by_id(request, space_id, id):
    print(space_id)
    print(domain)
    print(id)
    result = db_utils.delete(space_id, domain, {'_id': id}, request.user_id)
    return (200, {'deleted_count': result.deleted_count})
