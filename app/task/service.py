import os, datetime, time
from library.db_connection_factory import get_collection
import library.db_utils as db_utils

domain = 'Task'

def find(request, space, project_id):
    data = db_utils.find(space, domain, {'projectId': project_id})
    return (200, {'data': data})

def update(request, space, project_id, data):
    data['projectId'] = project_id
    updated_record = db_utils.upsert(space, domain, data, request.user_id)
    return (200, {'data': updated_record})

def delete(request, space, project_id, id):
    result = db_utils.delete(space, domain, {'_id': id}, request.user_id)
    return (200, {'deleted_count': result.deleted_count})

def find_by_id(request, space, project_id, id):
    data = db_utils.find(space, domain, {'_id': id})
    return (200, {'data': data})

def move_task(request, space, project_id, data):
    moveTask = db_utils.find(space, domain, {'_id': data['moveTaskId']})[0]
    afterTask = db_utils.find(space, domain, {'_id': data['afterTaskId']})[0]
    # inc = afterTask['order'] + 1
    # if inc not ending in 0, moveTask['order'] = inc
    moveTask['stageId'] = afterTask['stageId']
    updated_record = db_utils.upsert(space, domain, moveTask, request.user_id)
    return (200, {'data': updated_record})
