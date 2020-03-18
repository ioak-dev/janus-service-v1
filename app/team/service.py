import os, datetime, time
from library.db_connection_factory import get_collection
import library.db_utils as db_utils

domain = 'Team'

def find(request, space):
    data = db_utils.find(space, domain, {})
    return (200, {'data': data})

def update(request, space, data):
    updated_record = db_utils.upsert(space, domain, data, request.user_id)
    return (200, {'data': updated_record})

def delete(request, space, id):
    result = db_utils.delete(space, domain, {'_id': id}, request.user_id)
    return (200, {'deleted_count': result.deleted_count})

def find_by_id(request, space, id):
    data = db_utils.find(space, domain, {'_id': id})
    return (200, {'data': data})
