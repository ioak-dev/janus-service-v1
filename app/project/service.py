import os, datetime, time
from library.db_connection_factory import get_collection
import library.db_utils as db_utils
import app.sequence.service as sequence_service

domain = 'Project'

def find(request, spaceId):
    return (200, {'data': find_all_projects(spaceId)})

def update(request, spaceId, data):
    new_record = False
    if '_id' not in data:
        new_record = True
    updated_record = db_utils.upsert(spaceId, domain, data, request.user_id)
    if new_record:
        sequence_service.create_sequence(spaceId, 'taskOrder', updated_record['_id'], 1)
        sequence_service.create_sequence(spaceId['name'], 'taskId', project['_id'], 1)
    return (200, {'data': updated_record})

def delete(request, spaceId, id):
    result = db_utils.delete(spaceId, domain, {'_id': id}, request.user_id)
    return (200, {'deleted_count': result.deleted_count})

def find_by_id(request, spaceId, id):
    data = db_utils.find(spaceId, domain, {'_id': id})
    return (200, {'data': data})

def find_all_projects(spaceId):
    return db_utils.find(spaceId, domain, {})