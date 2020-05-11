import os, datetime, time, base64
import library.db_utils as db_utils

domain = 'Task.Attachment'

def find_by_taskid(request, space_id, task_id):
    data = db_utils.find(space_id, domain, {'taskId': task_id})
    response = []
    for item in data:
        del item['attachment']
        response.append(item)
    return (200, {'data': response})

def download_attachment(request, space_id, attachment_id):
    data = db_utils.find(space_id, domain, {'_id': attachment_id})
    if len(data) == 1:
        return (200, base64.b64encode(data[0]['attachment']))
    else:
        return (404, {'data': 'attachment not found'})

def add(request, space_id, task_id, attachment):
    data = {}
    data['taskId'] = task_id
    data['attachment'] = attachment.read()
    data['name'] = attachment.name
    data['size'] = attachment.size
    updated_record = db_utils.upsert(space_id, domain, data, request.user_id)
    del updated_record['attachment']
    # return (200, base64.b64encode(updated_record['attachment']))
    # return (200, updated_record['attachment'])
    # return (200, {'data': updated_record})
    return (200, {'data': updated_record})

def delete(request, space_id, attachment_id):
    result = db_utils.delete(space_id, domain, {'_id': attachment_id}, request.user_id)
    return (200, {'deleted_count': result.deleted_count})
