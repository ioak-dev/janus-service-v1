import os, datetime, time
from library.db_connection_factory import get_collection
import library.db_utils as db_utils
import app.sequence.service as sequence_service

domain = 'Project'

def find(request, space):
    return (200, {'data': find_all_projects(space)})

def update(request, space, data):
    new_record = False
    if '_id' not in data:
        new_record = True
    updated_record = db_utils.upsert(space, domain, data, request.user_id)
    if new_record:
        sequence_service.create_sequence(space, 'taskOrder', updated_record['_id'], 1)
        sequence_service.create_sequence(space['name'], 'taskId', project['_id'], 1)
    return (200, {'data': updated_record})

def delete(request, space, id):
    result = db_utils.delete(space, domain, {'_id': id}, request.user_id)
    return (200, {'deleted_count': result.deleted_count})

def find_by_id(request, space, id):
    data = db_utils.find(space, domain, {'_id': id})
    return (200, {'data': data})

def find_all_projects(space):
    return db_utils.find(space, domain, {})