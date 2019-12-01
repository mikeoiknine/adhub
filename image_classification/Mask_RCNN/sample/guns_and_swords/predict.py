import os
import sys
import base64, uuid
import random
import math
import re
import time
import numpy as np
import tensorflow as tf
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import skimage

# Root directory of the project
ROOT_DIR = os.path.abspath("../../")

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn import utils
from mrcnn import visualize
from mrcnn.visualize import display_images
import mrcnn.model as modellib
from mrcnn.model import log

from sample.guns_and_swords import gns

def get_ax(rows=1, cols=1, size=16):
    """Return a Matplotlib Axes array to be used in
    all visualizations.Provide a central point to control graph sizes.
    Adjust the size attribute to control how big to render images
    """
    _, ax = plt.subplots(rows, cols, figsize=(size*cols, size*rows))
    return ax

def load_image(image_path):
    """Load the specified image and return a [H,W,3] Numpy array.
    """
    # Load image
    image = skimage.io.imread(image_path)
    # If grayscale. Convert to RGB for consistency.
    if image.ndim != 3:
        image = skimage.color.gray2rgb(image)
    # If has an alpha channel, remove it for consistency
    if image.shape[-1] == 4:
        image = image[..., :3]
    return image

def prediction(img_64):
    # Directory of saved logs and trained models
    MODEL_DIR = os.path.join(ROOT_DIR, "logs")

    # Path to trained weights & guns dataset
    GNS_WEIGHTS_PATH = "../../logs/gns20191127T1201/mask_rcnn_gns_0060.h5" 
    GNS_DIR = "../../../procdata"

    # Model Configurations
    config = gns.gnsConfig()
    config.display()

    # Train on GPU, Infer(Predict) on CPU
    DEVICE = "/cpu:0"  # or /gpu:0
    TEST_MODE = "inference"

    # Open model in inference mode
    with tf.device(DEVICE):
        model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR,
                                config=config)

    # Load Weights
    weights_path = GNS_WEIGHTS_PATH
    model.load_weights(weights_path, by_name=True)

    # Load validation dataset
    dataset = gns.gnsDataset()
    dataset.load_gns(GNS_DIR, "val")
    dataset.prepare()

    # Remove comma and decode
    img_64 = img_64.split(',', 1)[-1]
    imgdata = base64.b64decode(img_64)

    # make local jpg file with image data
    filename = "test.jpg"
    with open(filename, 'wb') as f:
        f.write(imgdata)
    image = load_image(filename)
    bad_image_path = "../../../procdata/bad_samples/" + filename

    # Run object detection
    results = model.detect([image], verbose=1)

    # Get Results & axis for plot 
    # (AI only scores images above 90% certainty)
    ax = get_ax(1)
    r = results[0]

    # If 0 instances of any bad images found, then image is kept
    if r['scores'].shape[0] == 0:
        return True
    else:
        # Construct Pyplot
        plt = visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'], 
                                    dataset.class_names, r['scores'], ax=ax,
                                    title="Predictions")
        
        # Show Constructed plot
        #plt.show()
        
        # Or save bad image pyplot in MongoDB separate folder if needed
        plt.savefig(bad_image_path)

        return False