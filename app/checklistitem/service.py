import os, datetime, time
import library.db_utils as db_utils

domain = 'Task.checklistitem'

def find(request, space_id):
    data = db_utils.find(space_id, domain, {})
    return (200, {'data': data})

def update(request, space_id, data):
    updated_record = db_utils.upsert(space_id, domain, data, request.user_id)
    return (200, {'data': updated_record})

def delete(request, space_id, id):
    result = db_utils.delete(space_id, domain, {'_id': id}, request.user_id)
    return (200, {'deleted_count': result.deleted_count})

def find_by_taskid(request, space, id):
    data = db_utils.find(space, domain, {'taskId': id})
    return (200, {'data': data})
