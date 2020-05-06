import os, datetime, time
import library.db_utils as db_utils
import app.role.service as role_service
import app.team_member.service as team_member_service
import app.project.service as project_service
from bson.objectid import ObjectId

domain = 'Team'

def find(request, space_id):
    admin_projects = project_service.find_admin_projects(space_id, request.user_id)
    if len(admin_projects) > 0:
        data = db_utils.find(space_id, domain, {})
        return (200, {'data': data})
    else:
        member_teams = find_member_teams(space_id, request.user_id)
        admin_teams = find_admin_teams(space_id, request.user_id)
        teamid_list = []
        for item in member_teams:
            if item['teamId'] not in teamid_list:
                teamid_list.append(ObjectId(item['teamId']))
        for item in admin_teams:
            if item['domainId'] not in teamid_list:
                teamid_list.append(ObjectId(item['domainId']))
        teams = db_utils.find(space_id, domain, {'_id': {'$in': teamid_list}})
        return (200, {'data': teams})
    
def update(request, space_id, data):
    isNewRecord = False
    if '_id' not in data:
        isNewRecord = True
    updated_record = db_utils.upsert(space_id, domain, data, request.user_id)
    if isNewRecord:
        role_service.add(space_id, {'type': 'TeamAdministrator', 'userId': request.user_id, 'domainId': updated_record['_id']}, request.user_id)
    return (200, {'data': updated_record})

def delete(request, space_id, id):
    result = db_utils.delete(space_id, domain, {'_id': id}, request.user_id)
    return (200, {'deleted_count': result.deleted_count})

def find_member_teams(space_id, user_id):
    return team_member_service.find(space_id, user_id)

def find_admin_teams(space_id, user_id):
    return role_service.find_admin_teams(space_id, user_id)

def find_by_id(request, space_id, id):
    data = db_utils.find(space_id, domain, {'_id': id})
    return (200, {'data': data})
