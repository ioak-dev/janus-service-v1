import os, datetime, time, pymongo
from library.db_connection_factory import get_collection
import library.db_utils as db_utils
import app.sequence.service as sequence_service

domain = 'log'

def add(space, domain_name, snapshot, new_record, audit_fields, user_id):
    list_of_updated_records = []
    for field in new_record.keys():
        if field in audit_fields and snapshot[field] != new_record[field]:
            updated_record = db_utils.upsert(space, domain, {
                'domain': domain_name,
                'field': field,
                'reference': new_record['_id'],
                'before': snapshot[field],
                'after': new_record[field]
            }, user_id)
            list_of_updated_records.append(updated_record)
    return list_of_updated_records

def find_logs(request, space, domain_name, reference):
    data = db_utils.find(space, domain, {'domain': domain_name, 'reference': reference}, [('createdAt', pymongo.DESCENDING)])
    return (200, {'data': data})
