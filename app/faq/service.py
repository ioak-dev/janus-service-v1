import os, datetime, time
from library.db_connection_factory import get_collection
import library.db_utils as db_utils

domain = 'Faq'

def find(request, spaceId):
    faq_list = db_utils.find(spaceId, domain, {})
    category_list = []
    for item in faq_list:
        if item.get('category') not in category_list:
            category_list.append(item['category'])
    return (200, {'faq': faq_list ,'category': category_list})

def update(request, spaceId, data):
    updated_record = db_utils.upsert(spaceId, domain, data, request.user_id)
    return (200, {'data': updated_record})

def delete(request, spaceId, id):
    result = db_utils.delete(spaceId, domain, {'_id': id}, request.user_id)
    return (200, {'deleted_count': result.deleted_count})

def find_faq_by_category(request, spaceId, category):
    data = db_utils.find(spaceId, domain, {'category': category})
    return (200, {'data': data})
