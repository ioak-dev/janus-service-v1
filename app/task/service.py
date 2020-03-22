import os, datetime, time, pymongo
from library.db_connection_factory import get_collection
import library.db_utils as db_utils
from app.sequence.service import nextval, reset_sequence

domain = 'Task'

def find(request, space, project_id):
    data = db_utils.find(space, domain, {'projectId': project_id}, [('order', pymongo.ASCENDING)])
    return (200, {'data': data})

def update(request, space, project_id, data):
    data['projectId'] = project_id
    if 'order' not in data:
        data['order'] = nextval(space, 'taskOrder', project_id)
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
    inc = afterTask['order'] + 1
    if inc % 10 != 1:
        moveTask['order'] = afterTask['order'] + 1
    else:
        moveTask['order'] = afterTask['order'] + 1
        recompute_order(space, project_id)

    moveTask['stageId'] = afterTask['stageId']
    updated_record = db_utils.upsert(space, domain, moveTask, request.user_id)
    return (200, {'data': updated_record})

def recompute_order(space, project_id):
    reset_sequence(space, 'taskOrder', project_id)
    tasks = db_utils.find(space, domain, {'projectId': project_id}, [('order', pymongo.ASCENDING)])
    for task in tasks:
        task['order'] = nextval(space, 'taskOrder', project_id)
        db_utils.upsert(space, domain, task)
