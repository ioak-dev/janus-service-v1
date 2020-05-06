import os, datetime, time
import library.db_utils as db_utils
import app.role.service as role_service

domain = 'project.team'

def find(request, space_id):
    data = db_utils.find(space_id, domain, {})
    return (200, {'data': data})

def find_by_teams(space_id, team_list):
    return db_utils.find(space_id, domain, {'teamId': {'$in': team_list}})

def add(request, space_id, project_id, team_id):
    if role_service.is_project_admin(space_id, request.user_id, project_id):
        existing_list = db_utils.find(space_id, domain, {'projectId': project_id, 'teamId': team_id})
        if len(existing_list) == 0:
            inserted_record = db_utils.upsert(space_id, domain, {'projectId': project_id, 'teamId': team_id}, request.user_id)
            return (200, {'data': inserted_record})
        else:
            return (200, {'data': existing_list[0]})
    else:
        return (401, {'data': 'unauthorized'})

def delete(request, space_id, project_id, team_id):
    if role_service.is_project_admin(space_id, request.user_id, project_id):
        result = db_utils.delete(space_id, domain, {'projectId': project_id, 'teamId': team_id}, request.user_id)
        return (200, {'deleted_count': result.deleted_count})
    else:
        return (401, {'data': 'unauthorized'})

def delete_by_id(request, space_id, id):
    existing_record = db_utils.find(space_id, domain, {'_id': id})
    if len(existing_record) == 1:
        if role_service.is_project_admin(space_id, request.user_id, existing_record[0]['projectId']):    
            result = db_utils.delete(space_id, domain, {'_id': id}, request.user_id)
            return (200, {'deleted_count': result.deleted_count})
        else:
            return (401, {'data': 'unauthorized'})
    else:
        return (404, {'data': 'no matching role to remove'})
