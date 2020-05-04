import os, datetime, time
import library.db_utils as db_utils

domain = 'project.team'

def find(request, space_id):
    data = db_utils.find(space_id, domain, {})
    return (200, {'data': data})

def add(request, space_id, project_id, team_id):
    existing_list = db_utils.find(space_id, domain, {'projectId': project_id, 'teamId': team_id})
    if len(existing_list) == 0:
        inserted_record = db_utils.upsert(space_id, domain, {'projectId': project_id, 'teamId': team_id}, request.user_id)
        return (200, {'data': inserted_record})
    else:
        return (200, {'data': existing_list[0]})

def delete(request, space_id, project_id, team_id):
    result = db_utils.delete(space_id, domain, {'projectId': project_id, 'teamId': team_id}, request.user_id)
    return (200, {'deleted_count': result.deleted_count})

def delete_by_id(request, space_id, id):
    result = db_utils.delete(space_id, domain, {'_id': id}, request.user_id)
    return (200, {'deleted_count': result.deleted_count})
