import os, datetime, time
import library.db_utils as db_utils

domain = 'Task.Comment'

def find_by_taskid(request, space, task_id):
    data = db_utils.find(space, domain, {'taskId': task_id})
    return (200, {'data': data})

def update(request, space_id, data):
    updated_record = db_utils.upsert(space_id, domain, data, request.user_id)
    return (200, {'data': updated_record})
