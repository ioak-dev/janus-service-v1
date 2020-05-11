import os, datetime, time, pymongo
import library.db_utils as db_utils
import app.sequence.service as sequence_service

domain = 'log'

def add(space_id, domain_name, snapshot, new_record, audit_fields, user_id):
    list_of_updated_records = []
    for field in new_record.keys():
        if field in audit_fields and snapshot[field] != new_record[field]:
            updated_record = db_utils.upsert(space_id, domain, {
                'domain': domain_name,
                'field': field,
                'reference': new_record['_id'],
                'before': snapshot[field],
                'after': new_record[field]
            }, user_id)
            list_of_updated_records.append(updated_record)
    return list_of_updated_records

def find_logs(request, space_id, domain_name, reference):
    data = db_utils.find(space_id, domain, {'domain': domain_name, 'reference': reference}, [('createdAt', pymongo.DESCENDING)])
    return (200, {'data': data})
