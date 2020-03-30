import os, datetime, time
from library.db_connection_factory import get_collection
import library.db_utils as db_utils

domain = 'sequence'

def is_present(spaceId, field, context):
    if len(db_utils.find(spaceId, domain, {'field': field, 'context':context})) == 1:
        return True
    return False

def create_sequence(spaceId, field, context, factor):
    db_utils.upsert(spaceId, domain, {
        'field': field,
        'context': context,
        'nextVal': 1,
        'factor': factor
    })

def reset_sequence(spaceId, field, context):
    sequence = db_utils.find(spaceId, domain, {'field': field, 'context': context})[0]
    sequence['nextVal'] = 1
    return db_utils.upsert(spaceId, domain, sequence)

def nextval(spaceId, field, context):
    print(spaceId, field, context)
    data = db_utils.find(spaceId, domain, {'field': field, 'context': context})[0]
    currVal = data['nextVal']
    data['nextVal'] = data['nextVal'] + data['factor']
    db_utils.upsert(spaceId, domain, data)
    return currVal
