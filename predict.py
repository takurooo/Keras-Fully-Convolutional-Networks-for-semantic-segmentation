#-------------------------------------------
# import
#-------------------------------------------
import os
import argparse
import importlib
import json
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from dataloader import DataLoader, Dataset
import list_util
from transforms import label_to_img
#-------------------------------------------
# defines
#-------------------------------------------
CUR_PATH = os.path.join(os.path.dirname(__file__))
JSON_PATH = os.path.join(CUR_PATH, 'args.json')

N_CLASS = 21
INPUT_SIZE = 224
#-------------------------------------------
# private functions
#-------------------------------------------

'''
VOC2012 Classes
'''
# "background": 0,
# "aeroplane": 1,
# "bicycle": 2,
# "bird": 3,
# "boad": 4,
# "bottle": 5,
# "bus": 6,
# "car": 7,
# "cat": 8,
# "chair": 9,
# "cow": 10,
# "dining table": 11,
# "dog": 12,
# "horse": 13,
# "motor_bike": 14,
# "person": 15,
# "potted_plant": 16,
# "sheep": 17,
# "sofa": 18,
# "train": 19,
# "tv": 20


def get_args():
    with open(JSON_PATH, "r") as f:
        j = json.load(f)
    return j['predict']


def latest_weight(log_dir):
    weight_paths = list_util.list_from_dir(log_dir, '.hdf5')
    if len(weight_paths) == 0:
        return ""
    else:
        return weight_paths[-1]


def main(args):
    model_name = args["model"]
    img_dir = args["img_dir"]
    log_dir = args["log_dir"]
    img_idx = 1

    '''
    Create DataLoader
    '''
    dataset = Dataset(classes=21, input_size=(224, 224),
                      img_dir=img_dir, label_dir=None,
                      trans=False)

    input_img, _ = dataset[img_idx]

    print("img_len   : {}".format(len(dataset)))

    '''
    Create Model
    '''
    model = importlib.import_module("models." + model_name)
    model = model.build(classes=N_CLASS,
                        input_shape=(INPUT_SIZE, INPUT_SIZE, 3))
    # mode.summary()

    '''
    Load Weights
    '''
    weight_path = latest_weight(log_dir)
    if os.path.exists(weight_path):
        print('load weight : ', weight_path)
        model.load_weights(weight_path)

    '''
    Predict
    '''
    pred = model.predict(input_img)

    '''
    Convert
    '''
    pred_img = label_to_img(pred[0])

    input_img_ = input_img[0] * 255
    input_img_ = np.uint8(input_img_)

    '''
    Show Predict to Image
    '''
    plt.figure(figsize=(15, 15))
    img_list = [input_img_, pred_img]
    titel_list = ["input img", "predicted img"]
    plot_num = 1
    for title, img in zip(titel_list, img_list):
        plt.subplot(1, 2, plot_num)
        plt.title(title)
        plt.axis("off")
        plt.imshow(img)
        plot_num += 1

    # plt.show()
    plt.savefig("predict_{}.png".format(img_idx))


if __name__ == '__main__':
    main(get_args())
