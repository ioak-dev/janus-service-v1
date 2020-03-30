import os, datetime, time
from library.db_connection_factory import get_collection
import library.db_utils as db_utils

domain = 'Task.Comment'

def find_by_taskid(request, space, task_id):
    data = db_utils.find(space, domain, {'taskId': task_id})
    return (200, {'data': data})

def update(request, space, data):
    print(space)
    print(domain)
    print(data)
    print(request.user_id)
    updated_record = db_utils.upsert(space, domain, data, request.user_id)
    return (200, {'data': updated_record})
