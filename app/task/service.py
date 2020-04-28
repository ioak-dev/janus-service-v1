import os, datetime, time, pymongo
import library.db_utils as db_utils
from app.sequence.service import nextval, reset_sequence
import app.log.service as log_service

domain = 'Task'
domain_attachment = 'Task.Attachment'
domain_comment = 'Task.Comment'
domain_checklistitem = 'Task.checklistitem'

def find(request, space_id, project_id):
    data = db_utils.find(space_id, domain, {'projectId': project_id}, [('order', pymongo.DESCENDING)])
    return (200, {'data': data})

def update(request, space_id, project_id, data):
    project = db_utils.find(space_id, 'Project', {'_id': project_id})[0]
    data['projectId'] = project_id
    snapshot = []
    if '_id' not in data:
        data['taskId'] = project['name'][:4].lower() + '-' + str(nextval(space_id, 'taskId', project_id))
        data['order'] = nextval(space_id, 'taskOrder', project_id)
    else:
        snapshot = db_utils.find(space_id, domain, {'_id': data['_id']})
    updated_record = db_utils.upsert(space_id, domain, data, request.user_id)
    if '_id' in data and len(snapshot) == 1:
        log_service.add(space_id, domain, snapshot[0], updated_record, ['type', 'title', 'description', 'assignedTo', 'parentTaskId', 'priority'], request.user_id)
    return (200, {'data': updated_record})

def delete(request, space_id, id):
    result = delete_by_id(space_id, id, request.user_id)
    return (200, result)

def delete_by_id(space_id, id, user_id):
    task_result = db_utils.delete(space_id, domain, {'_id': id}, user_id)
    attachment_result = db_utils.delete(space_id, domain_attachment, {'taskId': id}, user_id)
    comment_result = db_utils.delete(space_id, domain_comment, {'taskId': id}, user_id)
    checklist_result = db_utils.delete(space_id, domain_checklistitem, {'taskId': id}, user_id)
    return {'tasks_deleted': task_result.deleted_count, 'attachments_deleted': attachment_result.deleted_count, 'comments_deleted': comment_result.deleted_count, 'checklists_deleted': checklist_result.deleted_count}

def find_by_id(request, space_id, project_id, id):
    data = db_utils.find(space_id, domain, {'_id': id})
    return (200, {'data': data})

def move_task(request, space_id, project_id, data):
    moveTask = db_utils.find(space_id, domain, {'_id': data['moveTaskId']})[0]
    afterTask = db_utils.find(space_id, domain, {'_id': data['afterTaskId']})[0]
    inc = afterTask['order'] + 1
    if moveTask['order'] != inc:
        print(moveTask['order'], afterTask['order'], inc)
        recompute_order(space_id, project_id, afterTask['order'])
        moveTask['order'] = inc
    else:
        sub = afterTask['order']
        afterTask['order'] = moveTask['order']
        moveTask['order'] = sub
        updated_record = db_utils.upsert(space_id, domain, afterTask, request.user_id)

    moveTask['stageId'] = afterTask['stageId']
    updated_record = db_utils.upsert(space_id, domain, moveTask, request.user_id)
    return (200, {'data': updated_record})

def recompute_order(space_id, project_id, order):
    tasks = db_utils.find(space_id, domain, {'$and': [{'projectId': project_id}, {'order': {'$gt': order}}]}, [('order', pymongo.ASCENDING)])
    for task in tasks:
        task['order'] = nextval(space_id, 'taskOrder', project_id)
        db_utils.upsert(space_id, domain, task)
