<<<<<<< HEAD
from models import AuthUser

def init_users():
    rob = AuthUser(a_id='1234', email='rob@live.ca', user_id='12344', password='password')
    rob.save()
=======
import uuid
from bson.objectid import ObjectId
from flask import (
        Blueprint, request, jsonify, g, session
)
from db import mongo
from .auth import login_required
import helper

bp = Blueprint('data', __name__, url_prefix='/data')

@bp.route('/aditem', methods=['GET', 'POST', 'PUT', 'DELETE'])
def ad_item_controller():
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
@login_required
def set_user_config():
    if request.method != 'POST':
        return None

    content = request.json


    # Set config on what kind of ads this user wants
    # Save it into the db (either in user table or new table)
    # Expected fields:
    # user_id
    # Region: Where should the ads be from
    # category: What kind of ads should be shown

@bp.route('/adstat', methods=['GET'])
def get_ad_stats():
    if request.method != 'GET':
        return jsonify({'msg': 'Invalid request type'})

    content = request.json
    if content['ad_id'] is None or len(content['ad_id']) < 12:
        return jsonify({'msg': 'No such ad ID'})

    ad = mongo.db.advertisements.find_one({'_id': ObjectId(content['ad_id'])})
    if ad is None:
        return jsonify({'msg': 'No such ad ID'})

    return jsonify('msg': 'Success!', ad['stats'])

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
    user_config = mongo.db.users.find_one({'_id': ObjectId(content['user_id'])})
    adverts = mongo.db.advertisements
    if user_config['category'] is not None and user_config['region'] is None:
        ads = adverts.find( { category :  user_config['category']  }, {name: 1, category: 1, stats: 1}).sort( {total_view_count: -1} )
    elif user_config['region'] is not None and user_config['category'] is None:
        ads = adverts.find( { region: user_config['region']  }, {name: 1, category: 1, stats: 1}).sort( {total_view_count: -1} )
    else
        ads = adverts.find( { }, {name: 1, category: 1, stats: 1}).sort( {total_view_count: -1} )

    if len(ads) == 0:
        return jsonify({'msg': 'No image matching query'})
    if len(ads) == 1:
        # Todo: Update total view count for this ad
        return jsonify({'msg': 'Success!',
            'ad_id': ads['_id'],
            'image_64': ads['image_64']
            })

    for ad in ads:
        if ad['_id'] != content['last_ad_id']:
            # Todo: Update total view count for this ad
            return jsonify({'msg': 'Success!',
                'ad_id': ad['_id'],
                'image_64': ad['image_64']
                })












>>>>>>> 3fd9b72... Crude attempt at returning new ads
