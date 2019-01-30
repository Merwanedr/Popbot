import cv2
import numpy as np
import os
import sys
from samples import coco
from mrcnn import utils
from mrcnn import model as modellib
import string
from random import *
from imageservice import myImage, mySubject


# Change the config infermation
class InferenceConfig(coco.CocoConfig):
    GPU_COUNT = 1
    
    # Number of images to train with on each GPU. A 12GB GPU can typically
    # handle 2 images of 1024x1024px.
    # Adjust based on your GPU memory and image sizes. Use the highest
    # number that your GPU can handle for best performance.
    IMAGES_PER_GPU = 1
    
config = InferenceConfig()




image = cv2.imread(os.path.join('uploads', myImage()))
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ROOT_DIR = os.getcwd()
MODEL_DIR = os.path.join(ROOT_DIR, "logs")
COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
if not os.path.exists(COCO_MODEL_PATH):
    utils.download_trained_weights(COCO_MODEL_PATH)

# COCO dataset object names
model = modellib.MaskRCNN(
    mode="inference", model_dir=MODEL_DIR, config=config
)
model.load_weights(COCO_MODEL_PATH, by_name=True)
class_names = [
    'BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
    'bus', 'train', 'truck', 'boat', 'traffic light',
    'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
    'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
    'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
    'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard',
    'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
    'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
    'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
    'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
    'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
    'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
    'teddy bear', 'hair drier', 'toothbrush'
]



class Model:
    # Input the original image name
    def apply_mask(self, image, mask):
        image[:, :, 0] = np.where(
            mask == 0,
            gray_image[:, :],
            image[:, :, 0]
        )
        image[:, :, 1] = np.where(
            mask == 0,
            gray_image[:, :],
            image[:, :, 1]
        )
        image[:, :, 2] = np.where(
            mask == 0,
            gray_image[:, :],
            image[:, :, 2]
        )
        return image

    def display_instances(self, image, boxes, masks, ids, names, scores):
        # max_area will save the largest object for all the detection results
        max_area = 0
        
        # n_instances saves the amount of all objects
        n_instances = boxes.shape[0]

        if not n_instances:
            print('NO INSTANCES TO DISPLAY')
        else:
            assert boxes.shape[0] == masks.shape[-1] == ids.shape[0]

        for i in range(n_instances):
            if not np.any(boxes[i]):
                continue

            # compute the square of each object
            y1, x1, y2, x2 = boxes[i]
            square = (y2 - y1) * (x2 - x1)

            # use label to select person object from all the 80 classes in COCO dataset
            label = names[ids[i]]
            if label == mySubject():
                # save the largest object in the image as main character
                # other people will be regarded as background
                if square > max_area:
                    max_area = square
                    mask = masks[:, :, i]
                else:
                    continue
            else:
                continue

            # apply mask for the image
        # by mistake you put apply_mask inside for loop or you can write continue in if also
        image = self.apply_mask(image, mask)
            
        return image

    def performImage(self):
        results = model.detect([image], verbose=0)
        r = results[0]
        frame = self.display_instances(
            image, r['rois'], r['masks'], r['class_ids'], class_names, r['scores']
        )
        min_char = 6
        max_char = 6
        allchar = string.ascii_letters + string.digits
        generated = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
        cv2.imwrite(os.path.join('uploads', generated+'_image.jpg') , image)









