import os, datetime, time
import library.db_utils as db_utils
import app.sequence.service as sequence_service
import app.team_member.service as team_member_service
import app.role.service as role_service
import app.project_team.service as project_team_service
from bson.objectid import ObjectId

domain = 'Project'

def find(request, space_id):
    member_projects = find_member_projects(space_id, request.user_id)
    admin_projects = find_admin_projects(space_id, request.user_id)
    projectid_list = []
    for item in member_projects:
        if item['projectId'] not in projectid_list:
            projectid_list.append(ObjectId(item['projectId']))
    for item in admin_projects:
        if item['domainId'] not in projectid_list:
            projectid_list.append(ObjectId(item['domainId']))

    projects = db_utils.find(space_id, domain, {'_id': {'$in': projectid_list}})
    
    return (200, {'data': projects})

def update(request, space_id, data):
    new_record = False
    if '_id' not in data:
        new_record = True
    updated_record = db_utils.upsert(space_id, domain, data, request.user_id)
    if new_record:
        sequence_service.create_sequence(space_id, 'taskOrder', updated_record['_id'], 1)
        sequence_service.create_sequence(space_id, 'stageOrder', updated_record['_id'], 1)
        sequence_service.create_sequence(space_id, 'taskId', updated_record['_id'], 1)
    return (200, {'data': updated_record})

def delete(request, space_id, id):
    result = db_utils.delete(space_id, domain, {'_id': id}, request.user_id)
    return (200, {'deleted_count': result.deleted_count})

def find_member_projects(space_id, user_id):
    team_members = team_member_service.find(space_id, user_id)
    teams = []
    for item in team_members:
        teams.append(item['teamId'])
    return project_team_service.find_by_teams(space_id, teams)

def find_admin_projects(space_id, user_id):
    return role_service.find_admin_projects(space_id, user_id)


def find_by_id(request, space_id, id):
    data = db_utils.find(space_id, domain, {'_id': id})
    return (200, {'data': data})

# TBD deprecated should be removed
def find_all_projects(space_id):
    return db_utils.find(space_id, domain, {})