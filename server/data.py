from bson.objectid import ObjectId
from flask import (
    Blueprint, request, jsonify
)

from . import helper
from .db import mongo

bp = Blueprint('data', __name__, url_prefix='/data')

@bp.route('/me', methods=['GET'])
def get_user_info():
    if request.method != 'GET':
        return jsonify({'msg': 'Invalid request type'})

    content = request.args

    if 'user_id' not in content or content['user_id'] == "":
        return jsonify({'msg': 'Invalid request - Missing user_id'})

    user = mongo.db.users.find_one( { '_id': ObjectId(content['user_id']) } )
    return jsonify(user)

@bp.route('/ads', methods=['GET'])
def get_user_ads():
    """
    Return all the ads that this user has uploaded.

    Expected:
    user_id: Id of the user
    """
    if request.method != 'GET':
        return jsonify({'msg': 'Invalid request type'})

    content = request.args
    users_ads = mongo.db.users.find_one( { '_id': ObjectId(content['user_id']) }, {'_id': 0, 'ads': 1} )

    print("User ads:", users_ads)

    data = []
    ads = mongo.db.advertisements
    if users_ads.get('ads', None) is not None:
        for ad_id in users_ads['ads']:
            ad_item = ads.find_one( {'_id': ObjectId(ad_id) })

            if ad_item is not None:
                print("Appending:", ad_item['name'])
                # Removing $oid tag
                ad_item['_id'] = str(ad_item['_id'])
                # getting from blob
                ad_item['image_64'] = helper.download_blob(str(ad_item['_id']) + '.jpg')
                data.append(ad_item)
            else:
                print("Ad with id:", ad_id, "is None")

    return jsonify({'msg': 'Success!', 'ads': data})

@bp.route('/add', methods=['POST'])
def add_item():
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
    if request.method != 'POST':
        return jsonify({'msg': 'Invalid request type'})

    content = request.json

    # Save image in Azure Blob for this user


    # Add advertisement item
    ads = mongo.db.advertisements
    ad_id = ads.insert({
            'user_id': content['user_id'],
            'name': content['name'],
            # 'image_path': image_path,
            'image_64': content['image_64'],
            'region': content['region'],
            'upload_date': content['upload_date'],
            'category': content['category'],
            'is_active': True,
            'stats': {
                'day_view_count': 0,
                'month_view_count': 0,
                'year_view_count': 0,
                'total_view_count': 0
                }
            })

    image_path = helper.decode_image(str(ad_id), content['image_64'])

    ads.update({'_id': ad_id}, {'$set': {'image_path': image_path}})

    # Add this ad to the user
    mongo.db.users.update(
        { '_id': ObjectId(content['user_id']) },
        { '$addToSet': { 'ads': str(ad_id) } },
        upsert=True
    )

    return jsonify({'msg': 'Success!', 'ad_id': str(ad_id) })

@bp.route('/delete', methods=['DELETE'])
def remove_ad_item():
    """
    Remove a specific ad

    Expected:
    user_id: ID of the user this ad belongs to
    ad_id: ID of the ad that is to be deleted
    """
    if request.method != 'DELETE':
        return jsonify({'msg': 'Invalid request type'})

    content = request.args
    users_ads = mongo.db.users.find_one({'_id': ObjectId(content['user_id'])})
    if users_ads is None:
        return jsonify({'msg': 'Invalid request - No ads for this user'})

    # Check if the ad_id belongs to this user
    if content['ad_id'] not in users_ads['ads']:
        return jsonify({'msg': 'Invalid request - No ad with this id for this user'})

    # Remove this ad from the advertisement
    mongo.db.advertisements.remove( {'_id': ObjectId(content['ad_id']) } )

    #remove from azure
    helper.delete_blob(content['ad_id'] + '.jpg')

    # Remove this ad from the users ad list
    mongo.db.users.update( {'_id': ObjectId(content['user_id']) }, {"$pull": {"ads": content['ad_id']} } )

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
        return jsonify({'msg': 'Invalid request type'})

    content = request.get_json()

    config_file = {}
    if 'user_id' in content:
        user = mongo.db.users.find_one({'_id': ObjectId(content['user_id'])})
        config_file['region'] = user['location']

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

    content = request.get_json()
    if content['ad_id'] is None or len(content['ad_id']) < 12:
        return jsonify({'msg': 'No such ad ID'})

    ad = mongo.db.advertisements.find_one({'_id': ObjectId(content['ad_id'])})
    if ad is None:
        return jsonify({'msg': 'No such ad ID'})

    return jsonify({'msg': 'Success!', 'stats': ad['stats']})

@bp.route('/next', methods=['GET'])
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
    if request.method != 'GET':
        return jsonify({'msg': 'Invalid request type'})

    content = request.args
    user_config = mongo.db.users_config.find_one({'_id': ObjectId(content['user_id'])})
    advertisements = mongo.db.advertisements

    print("User Config is:", user_config)
    print("Requested filters:", content)

    filter_by = {}
    if user_config is not None:
        print("applying filters...")
        if 'category' in user_config and user_config['category'] != "":
            filter_by['category'] = { '$in' : user_config['category'] }

        if 'region' in user_config and user_config['region'] != "":
            filter_by['region'] = { '$elemMatch' : {'$eq' : user_config['region']} }

        filter_by['is_active'] = True

    print("Filters applied:", filter_by)
    ads = advertisements.find(filter_by).sort([('total_view_count', -1)])

    if ads.count() == 0:
        print('0 ads found')
        return jsonify({'msg': 'No image matching query'}), 510

    print("loopidity doopity")
    for ad in ads:
        print("Analysizing:", str(ad['_id']), "......")
        if 'last_ad_id' in content and str(ad['_id']) == content['last_ad_id']:
            continue
        print(ad['name'], 'has different ID!')
        # update the users ad display count
        mongo.db.users.update(
                { '_id': ObjectId(content['user_id']) },
                { '$inc': { 'stats.total_ads_displayed': 1} },
                upsert=True)

        # Update the ad view count
        mongo.db.advertisements.update(
            { '_id': ObjectId(ad['_id']) },
            { '$inc': { 'stats.total_view_count': 1, 'stats.year_view_count': 1, 'stats.month_view_count': 1, 'stats.day_view_count': 1} } ,
            upsert=True
        )

        #get image from blob bucket
        ad['image_64'] = helper.download_blob(str(ad['_id']) + '.jpg')

        print("returning ad:", ad['_id'])
        return jsonify({'msg': 'Success!',
            'ad_id': str(ad['_id']),
            'image_64': ad['image_64']
            })
    return jsonify({'msg': 'No image matching query'}), 510



@bp.route('/setactive', methods=['POST', 'PUT'])
def set_active_status():
    """
    Sets the active status for a given ad. Ads that are not active will not be considered
    when deciding which ad to return to users.

    Expected Fields:
    user_id: ID of the user that owns the ad having its status changed
    ad_id: ID of the advertisement being modified
    is_active: Boolean denoting whether the ad should be considered active
    """
    if request.method != 'POST' and request.method != 'PUT':
        return jsonify({'msg': 'Invalid request type'})

    content = request.get_json()
    users_ads = mongo.db.users.find_one( { '_id': ObjectId(content['user_id']) }, {'_id': 0, 'ads': 1} )
    if users_ads is None:
        return jsonify({'msg': 'Invalid request - No ads for this user'})

    # Check if the ad_id belongs to this user
    if content['ad_id'] not in users_ads['ads']:
        return jsonify({'msg': 'Invalid request - No ad with this id for this user'})

    # Update the status of this ad
    mongo.db.advertisements.update_one(
            { '_id': ObjectId(content['ad_id']) },
            { "$set": {'is_active': content['is_active'] } },
            upsert=False
        )

    return jsonify({'msg': 'Success!'})


@bp.route('/myrevenue', methods=['GET'])
def get_revenue():
    """
    Returns the total revenue the user has earned thus far

    The revenue is calculated: (total ads displayed) * 0.01$

    Expected Field:
    user_id: ID of the user requesting the data
    """
    if request.method != 'GET':
        return jsonify({'msg': 'Invalid request type'})

    content = request.args

    if 'user_id' not in content or content['user_id'] == "":
        return jsonify({'msg': 'Invalid request - Missing user_id'})

    total_views = mongo.db.users.find_one( {'_id': ObjectId(content['user_id']) },
            { '_id': 0, 'stats.total_ads_displayed': 1 })

    return jsonify({'msg': 'Success!', 'revenue': ( 0.01 * total_views['stats']['total_ads_displayed'])})


@bp.route('/myexpense', methods=['GET'])
def get_expense():
    """
    Returns the total expense the user will be charged for his ads
    being displayed

    The expense is calculated: (total views on ads uploaded) * 0.02$

    Expected Field:
    user_id: ID of the user requesting the data
    """
    if request.method != 'GET':
        return jsonify({'msg': 'Invalid request type'})

    content = request.args

    if 'user_id' not in content or content['user_id'] == "":
        return jsonify({'msg': 'Invalid request - Missing user_id'})

    advertisements = mongo.db.advertisements

    # Get all ads for this user
    users_ads = mongo.db.users.find_one( { '_id': ObjectId(content['user_id']) }, {'_id': 0, 'ads': 1} )

    if 'ads' not in users_ads:
        return jsonify({'msg': 'No ads'}), 510

    total_views = 0
    for ad in users_ads['ads']:
        views = advertisements.find_one({ '_id': ObjectId(ad) }, {'_id': 0, 'stats': 1} )
        if views is None:
            continue
        print("Views:", views)
        total_views += views['stats']['total_view_count']

    return jsonify({'msg': 'Success!', 'expense': ( 0.02 * total_views)})

