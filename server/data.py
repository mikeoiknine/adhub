import uuid
from bson.objectid import ObjectId
from flask import (
        Blueprint, request, jsonify, g, session
)
from .db import mongo
from . import helper

bp = Blueprint('data', __name__, url_prefix='/data')

@bp.route('/aditem', methods=['GET', 'POST', 'PUT', 'DELETE'])
def ad_item_controller():
    """
    Allows user to add new ad to the system

    Expected Fields:
    user_id: ID of the user adding this ad item
    name: Name of the ad image
    image_64: Base64 encoded string of the image
    region: Region that the ad is being uploaded from
    upload_date: Current date
    category: Type of ad being uploaded
    """
    content = request.json

    if request.method == 'POST':
        # Save image in Azure Blob for this user
        ad_id = uuid.uuid1()
        image_path = helper.decode_image(ad_id, content['image_64'])

        # Add advertisement item
        ads = mongo.db.advertisements
        ad_id = ads.insert({
                'ad_id': str(ad_id),
                'user_id': content['user_id'],
                'name': content['name'],
                'image_path': image_path,
                'image_64': content['image_64'],
                'region': content['region'],
                'upload_date': content['upload_date'],
                'category': content['category'],
                'stats': {
                    'day_view_count': 0,
                    'month_view_count': 0,
                    'year_view_count': 0,
                    'total_view_count': 0
                    }
                })

        # Add this ad to the user
        mongo.db.users.update(
            { '_id': ObjectId(content['user_id']) },
            { '$addToSet': { 'ads': str(ad_id) } },
            upsert=True
        )

    return jsonify({'msg': 'Success!'})

@bp.route('/config', methods=['POST'])
def set_user_config():
    """
    Sets the user config which describes the types of ads this user is interested in
    If the user is not interested in any particular filters, they should be omitted or left blank.

    Expected Fields:
    user_id: The ID of the user this config corresponds to
    region: Preferred Region
    category: Type of preferred ad
    """
    if request.method != 'POST':
        return None

    content = request.json

    config_file = {}
    if 'region' in content:
        config_file['region'] = content['region']

    if 'category' in content:
        config_file['category'] = content['category']

    mongo.db.users_config.update({ '_id': ObjectId(content['user_id']) }, config_file, upsert=True)
    return jsonify({'msg': 'Success!'})

@bp.route('/adstat', methods=['GET'])
def get_ad_stats():
    """
    Returns the stats of the ad corresponding to the passed id

    Expected Fields:
    ad_id: Id of the adverstisement of interest
    """
    if request.method != 'GET':
        return jsonify({'msg': 'Invalid request type'})

    content = request.json
    if content['ad_id'] is None or len(content['ad_id']) < 12:
        return jsonify({'msg': 'No such ad ID'})

    ad = mongo.db.advertisements.find_one({'_id': ObjectId(content['ad_id'])})
    if ad is None:
        return jsonify({'msg': 'No such ad ID'})

    return jsonify({'msg': 'Success!', 'stats': ad['stats']})

@bp.route('/next', methods=['POST'])
def get_next_ad():
    """
    Returns the next ad item. The ad with the lowest view count
    that meets the criteria defined by the user config is returned.
    The only guarantee is that the ad won't be the same as the previous one
    except in the case that only a single ad matches the criteria

    If the config is non-existant, all ads are considered in the choosing process

    Expected fields:
    user_id: User making the request
    last_ad_id: Id of the most previous advertisement, empty if this is the first
    """
    if request.method != 'POST':
        return jsonify({'msg': 'Invalid request type'})

    content = request.json
    user_config = mongo.db.users_config.find_one({'_id': ObjectId(content['user_id'])})
    print("User Config is:", user_config)
    print("Requested filters:", content)
    adverts = mongo.db.advertisements

    filter_by = {}
    if 'category' in user_config and user_config['category'] != "":
        filter_by['category'] = user_config['category']

    if 'region' in user_config and user_config['region'] != "":
        filter_by['region'] = user_config['region']

    print("Filters applied:", filter_by)
    ads = adverts.find(filter_by).sort([('total_view_count', -1)])

    if ads.count() == 0:
        return jsonify({'msg': 'No image matching query'})

    if ads.count() == 1:
        mongo.db.advertisements.update(
            { '_id': ObjectId(ads[0]['_id']) },
            { '$inc': { 'stats.total_view_count': 1} } ,
            upsert=True
        )
        print("returning ad:", ads['_id'])
        return jsonify({ 'msg': 'Success!', 'ad_id': str(ads[0]['_id']), 'image_64': ads[0]['image_64']})

    for ad in ads:
        if str(ad['_id']) != content['last_ad_id']:
            mongo.db.advertisements.update(
                { '_id': ObjectId(ad['_id']) },
                { '$inc': { 'stats.total_view_count': 1} } ,
                upsert=True
            )

            print("returning ad:", ad['_id'])
            return jsonify({'msg': 'Success!',
                'ad_id': str(ad['_id']),
                'image_64': ad['image_64']
                })
