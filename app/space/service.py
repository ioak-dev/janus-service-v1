import os, datetime, time
from pymongo import MongoClient
from library.db_connection_factory import get_collection
import library.db_utils as db_utils
from gridfs import GridFS
import base64
from bson.binary import Binary
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

DATABASE_URI = os.environ.get('DATABASE_URI')

def do_create(data_in, banner):
    data = data_in.copy()
    if banner != None:
        data['banner'] = banner.read()
    spaceId = get_collection('janus','spaceId').insert_one(data)
    return (200, {'_id': str(spaceId.inserted_id)})

def do_get_banner(spaceId):
    spaceData = get_collection('janus','spaceId').find_one({'name': spaceId})
    spaceData['_id'] = str(spaceData['_id'])
    if 'banner' in spaceData:
        return (200, base64.b64encode(spaceData['banner']))
    else:
        return (404, None)

def do_get_space(spaceId):
    spaceData = get_collection('janus','spaceId').find_one({'name': spaceId})
    spaceData['_id'] = str(spaceData['_id'])
    spaceData.pop('banner', None)
    return (200, spaceData)

def do_update_space(spaceId, data):
    spaceData = get_collection('janus','spaceId').find_one({'name': spaceId})
    get_collection('janus','spaceId').update_one({
        '_id' : (spaceData['_id'])
    },{
        '$set':{
            'stage':data['data']
        }
    },upsert=True )
    return (200, None)

def get_all_spaces():
    return db_utils.find('janus', 'spaceId', {})
