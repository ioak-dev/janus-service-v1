import os, datetime, time, pymongo
from library.db_connection_factory import get_collection
import library.db_utils as db_utils
from app.sequence.service import nextval, reset_sequence

domain = 'Task'

def find(request, spaceId, project_id):
    data = db_utils.find(spaceId, domain, {'projectId': project_id}, [('order', pymongo.DESCENDING)])
    return (200, {'data': data})

def update(request, spaceId, project_id, data):
    project = db_utils.find(spaceId, 'Project', {'_id': project_id})[0]
    data['projectId'] = project_id
    if '_id' not in data:
        data['taskId'] = project['name'][:4].upper() + '-' + str(nextval(spaceId, 'taskId', project_id))
        data['order'] = nextval(spaceId, 'taskOrder', project_id)
    updated_record = db_utils.upsert(spaceId, domain, data, request.user_id)
    return (200, {'data': updated_record})

def delete(request, spaceId, project_id, id):
    result = db_utils.delete(spaceId, domain, {'_id': id}, request.user_id)
    return (200, {'deleted_count': result.deleted_count})

def find_by_id(request, spaceId, project_id, id):
    data = db_utils.find(spaceId, domain, {'_id': id})
    return (200, {'data': data})

def move_task(request, spaceId, project_id, data):
    moveTask = db_utils.find(spaceId, domain, {'_id': data['moveTaskId']})[0]
    afterTask = db_utils.find(spaceId, domain, {'_id': data['afterTaskId']})[0]
    inc = afterTask['order'] + 1
    if moveTask['order'] != inc:
        print(moveTask['order'], afterTask['order'], inc)
        recompute_order(spaceId, project_id, afterTask['order'])
        moveTask['order'] = inc
    else:
        sub = afterTask['order']
        afterTask['order'] = moveTask['order']
        moveTask['order'] = sub
        updated_record = db_utils.upsert(spaceId, domain, afterTask, request.user_id)

    moveTask['stageId'] = afterTask['stageId']
    updated_record = db_utils.upsert(spaceId, domain, moveTask, request.user_id)
    return (200, {'data': updated_record})

def recompute_order(spaceId, project_id, order):
    tasks = db_utils.find(spaceId, domain, {'$and': [{'projectId': project_id}, {'order': {'$gt': order}}]}, [('order', pymongo.ASCENDING)])
    for task in tasks:
        task['order'] = nextval(spaceId, 'taskOrder', project_id)
        db_utils.upsert(spaceId, domain, task)
