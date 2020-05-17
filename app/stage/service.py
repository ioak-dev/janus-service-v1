import os, datetime, time, pymongo
import library.db_utils as db_utils
from app.sequence.service import nextval, reset_sequence
import app.task.service as task_service

domain = 'Stage'
domain_task = 'Task'

def find(request, space_id):
    data = db_utils.find(space_id, domain, {}, [('order', pymongo.ASCENDING)])
    return (200, {'data': data})

def get_last_stage(space_id, project_id):
    data = db_utils.find(space_id, domain, {'projectId': project_id}, [('order', pymongo.DESCENDING)])
    if len(data) > 0:
        return data[0]
    else:
        return ''

def update(request, space_id, data):
    if '_id' not in data:
        data['order'] = nextval(space_id, 'stageOrder', data['projectId'])
    updated_record = db_utils.upsert(space_id, domain, data, request.user_id)
    return (200, {'data': updated_record})

def delete(request, space_id, id):
    tasks = db_utils.find(space_id, domain_task, {'stageId': id})
    task_deleted_count = 0
    task_attachment_deleted_count = 0
    task_checklist_deleted_count = 0
    task_comment_deleted_count = 0
    for task in tasks:
        result = task_service.delete_by_id(space_id, task['_id'], request.user_id)
        task_attachment_deleted_count += result['attachments_deleted']
        task_checklist_deleted_count += result['checklists_deleted']
        task_comment_deleted_count += result['comments_deleted']
        task_deleted_count += result['tasks_deleted']
    stage_result = db_utils.delete(space_id, domain, {'_id': id}, request.user_id)
    return (200, {'task_deleted_count': task_deleted_count, 'task_attachment_deleted_count': task_attachment_deleted_count, 'task_checklist_deleted_count': task_checklist_deleted_count, 'task_comment_deleted_count': task_comment_deleted_count, 'stages_deleted': stage_result.deleted_count})

def find_by_id(request, space_id, id):
    data = db_utils.find(space_id, domain, {'_id': id})
    return (200, {'data': data})


def move_stage(request, space_id, project_id, data):
    moveStage = db_utils.find(space_id, domain, {'_id': data['moveStageId']})[0]
    afterStage = db_utils.find(space_id, domain, {'_id': data['afterStageId']})[0]
    inc = afterStage['order'] + 1
    if moveStage['order'] != inc:
        print(moveStage['order'], afterStage['order'], inc)
        recompute_order(space_id, project_id, afterStage['order'])
        moveStage['order'] = inc
    else:
        sub = afterStage['order']
        afterStage['order'] = moveStage['order']
        moveStage['order'] = sub
        updated_record = db_utils.upsert(space_id, domain, afterStage, request.user_id)

    moveStage['stageId'] = afterStage['stageId']
    updated_record = db_utils.upsert(space_id, domain, moveStage, request.user_id)
    return (200, {'data': updated_record})

def recompute_order(space_id, project_id, order):
    stages = db_utils.find(space_id, domain, {'$and': [{'projectId': project_id}, {'order': {'$gt': order}}]}, [('order', pymongo.ASCENDING)])
    for stage in stages:
        stage['order'] = nextval(space_id, 'stageOrder', project_id)
        db_utils.upsert(space_id, domain, stage)