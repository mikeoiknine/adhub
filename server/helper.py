import base64
import os

from azure.storage.blob import BlockBlobService, PublicAccess

# Create the BlockBlockService that is used to call the Blob service for the storage account
block_blob_service = BlockBlobService(account_name='adbucket', account_key='+Gxx83Ptj2iOe5kXZJ3lky3Zx45jLpIqRKQZvInIDUHZla48EsoFQ67L0RKhzGzyOhGvy8geIlDMNMngmnrgjA==')
container_name = "images"

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
    # Set permissions to public
    block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)

    # Create a file in Documents to test the upload and download.
    local_path = os.path.abspath(os.path.curdir)
    full_path_to_file = os.path.join(local_path, filename)

    # Upload the created file
    block_blob_service.create_blob_from_path(container_name, filename, full_path_to_file)

    # Remove local file
    os.remove(full_path_to_file)

def download_all_blobs():
    generator = block_blob_service.list_blobs(container_name)

    # Code below lists all the blobs in the container and downloads them one after another
    for blob in generator:
        print(blob.name)
        print("{}".format(blob.name))
        # Check if the path contains a folder structure, create the folder structure
        if "/" in "{}".format(blob.name):
            print("there is a path in this")
            # Extract the folder path and check if that folder exists locally, and if not create it
            head, tail = os.path.split("{}".format(blob.name))
            print(head)
            print(tail)
            if (os.path.isdir(os.getcwd() + "/" + head)):
                # Download the files to this directory
                print("directory and sub directories exist")
                block_blob_service.get_blob_to_path(container_name, blob.name, os.getcwd() + "/" + head + "/" + tail)
            else:
                # Create the diretcory and download the file to it
                print("Directory doesn't exist, creating it now")
                os.makedirs(os.getcwd() + "/" + head, exist_ok=True)
                print("Directory created, download initiated")
                block_blob_service.get_blob_to_path(container_name, blob.name,os.getcwd() + "/" + head + "/" + tail)
        else:
            block_blob_service.get_blob_to_path(container_name,blob.name,blob.name)

def download_blob(blob_name):
    block_blob_service.get_blob_to_path(container_name, blob_name, blob_name)

    # Convert jpg to base64 string
    with open(blob_name, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read())

    # Delete jpg 
    os.remove(blob_name)

    return 'data:image/jpeg;base64,' + b64_string.decode("utf-8")

def delete_blob(blob_name):
    block_blob_service.delete_blob(container_name, blob_name)

def delete_container(cont_name):
    block_blob_service.delete_container(cont_name)

#download_blob("096bb616-113a-11ea-8127-802bf91a7257.jpg")