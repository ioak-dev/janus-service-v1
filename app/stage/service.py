import os, datetime, time, pymongo
import library.db_utils as db_utils
from app.sequence.service import nextval, reset_sequence

domain = 'Stage'

def find(request, space_id):
    data = db_utils.find(space_id, domain, {}, [('order', pymongo.DESCENDING)])
    return (200, {'data': data})

def update(request, space_id, data):
    if '_id' not in data:
        data['order'] = nextval(space_id, 'stageOrder', data['projectId'])
    updated_record = db_utils.upsert(space_id, domain, data, request.user_id)
    return (200, {'data': updated_record})

def delete(request, space_id, project_id, id):
    result = db_utils.delete(space_id, domain, {'_id': id}, request.user_id)
    return (200, {'deleted_count': result.deleted_count})

def find_by_id(request, space_id, project_id, id):
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