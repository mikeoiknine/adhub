import os, uuid, sys, base64
from azure.storage.blob import BlockBlobService, PublicAccess

# Uploads received base64 image to Azure blob Storage
def decode_image(name, img_string):
    # Remove comma and decode
    img_string = img_string.split(',', 1)[-1]
    imgdata = base64.b64decode(img_string)

    # make local jpg file with image dats
    filename = str(name) + ".jpg"

    with open(filename, 'wb') as f:
        f.write(imgdata)

    # Upload image to storage
    upl_img_blob(filename)

def upl_img_blob(filename):
    # Create the BlockBlockService that is used to call the Blob service for the storage account
    block_blob_service = BlockBlobService(account_name='adbucket', account_key='+Gxx83Ptj2iOe5kXZJ3lky3Zx45jLpIqRKQZvInIDUHZla48EsoFQ67L0RKhzGzyOhGvy8geIlDMNMngmnrgjA==')
    container_name = "images"

    # Set permissions to public
    block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)

    # Create a file in Documents to test the upload and download.
    local_path = os.path.abspath(os.path.curdir)
    full_path_to_file = os.path.join(local_path, filename)

    # Upload the created file
    block_blob_service.create_blob_from_path(container_name, filename, full_path_to_file)

    # Remove local file
    os.remove(full_path_to_file)

