import os, datetime, time
import library.db_utils as db_utils
import app.sequence.service as sequence_service

domain = 'Project'

def find(request, space_id):
    return (200, {'data': find_all_projects(space_id)})

def update(request, space_id, data):
    new_record = False
    if '_id' not in data:
        new_record = True
    updated_record = db_utils.upsert(space_id, domain, data, request.user_id)
    if new_record:
        sequence_service.create_sequence(space_id, 'taskOrder', updated_record['_id'], 1)
        sequence_service.create_sequence(space_id, 'taskId', updated_record['_id'], 1)
    return (200, {'data': updated_record})

def delete(request, space_id, id):
    result = db_utils.delete(space_id, domain, {'_id': id}, request.user_id)
    return (200, {'deleted_count': result.deleted_count})

def find_by_id(request, space_id, id):
    data = db_utils.find(space_id, domain, {'_id': id})
    return (200, {'data': data})

def find_all_projects(space_id):
    return db_utils.find(space_id, domain, {})