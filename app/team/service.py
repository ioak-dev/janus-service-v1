import os, datetime, time
from library.db_connection_factory import get_collection
import library.db_utils as db_utils

domain = 'Team'

def find(request, spaceId):
    data = db_utils.find(spaceId, domain, {})
    return (200, {'data': data})

def update(request, spaceId, data):
    updated_record = db_utils.upsert(spaceId, domain, data, request.user_id)
    return (200, {'data': updated_record})

def delete(request, spaceId, id):
    result = db_utils.delete(spaceId, domain, {'_id': id}, request.user_id)
    return (200, {'deleted_count': result.deleted_count})

def find_by_id(request, spaceId, id):
    data = db_utils.find(spaceId, domain, {'_id': id})
    return (200, {'data': data})
