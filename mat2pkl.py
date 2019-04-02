# -*- encoding: utf-8 -*-
'''
@File    :   mat2pkl.py
@Time    :   2019/04/02 17:05:14
@Author  :   zhiwei
'''

# here put the import lib

import scipy.io as sio
import numpy as np
import sys
import os
import os.path
import pickle
import argparse


def argsParser():
    parser = argparse.ArgumentParser(description="mat2pkl")
    parser.add_argument(
        '--mode',
        '-mode',
        type=str,
        required=True,
        default='',
        dest='mode',
        help='train/test')
    parser.add_argument(
        '--file',
        '-file',
        type=str,
        required=True,
        default='',
        dest='file',
        help='mat_file')

    args = parser.parse_args()
    return args


mode = sys.argv[1]
file = sys.argv[1]


def save_object(obj, file_name, pickle_format=2):
    file_name = os.path.abspath(file_name)
    with open(file_name, 'wb') as f:
        pickle.dump(obj, f, pickle_format)


if __name__ == "__main__":
    args = argsParser()
    mode = args.mode
    file = args.file
    print("mode:{}, file:{}".format(args.mode, args.file))
    if args.mode == 'train':
        with open('./mat/train.txt', 'r') as f:
            data = f.readlines()

        train_list = []
        for line in data:
            train_list.append(int(line.strip('\n')))

    if file.endswith('.mat'):
        boxes = []
        scores = []
        ids = []
        root = './mat/'
        old_path = file

        print("loading:", old_path)
        if args.mode == 'train':
            new_path1 = './mat/eb_voc_2007_train.pkl'
            new_path2 = './mat/eb_voc_2007_val.pkl'

            print("saving to:", new_path1)
            print("saving to:", new_path2)
        else:
            new_path1 = './mat/eb_voc_2007_test.pkl'
            print("saving to:", new_path1)

        mat_data = sio.loadmat(old_path)
        # print mat_data
        # print 'here'

        print("type before saving:", type(mat_data))

        # for key in list(mat_data.keys()):
        #     if "_" == key[0]:
        #         del mat_data[key]
        if args.mode == 'train':
            boxes_train = []
            scores_train = []
            ids_train = []

            boxes_val = []
            scores_val = []
            ids_val = []

            print(mat_data.keys())
            print(mat_data['images'].shape)
            print(mat_data['boxes'].shape)
            print(mat_data['boxScores'].shape)
            for i in range(mat_data['images'].shape[1]):
                id_in = int(mat_data['images'][0][i])
                if id_in in train_list:

                    boxes_data = mat_data['boxes'][0][i]
                    scores_data = mat_data['boxScores'][0][i].astype(
                        np.float32)

                    boxes_data_ = boxes_data.astype(np.uint16) - 1
                    boxes_data = boxes_data_[:, (1, 0, 3, 2)]
                    id_data = int(mat_data['images'][0][i])

                    boxes_train.append(boxes_data.astype(np.uint16))
                    scores_train.append(scores_data.astype(np.float32))
                    ids_train.append(id_data)
                else:
                    boxes_data = mat_data['boxes'][0][i]
                    scores_data = mat_data['boxScores'][0][i].astype(
                        np.float32)

                    boxes_data_ = boxes_data.astype(np.uint16) - 1
                    boxes_data = boxes_data_[:, (1, 0, 3, 2)]
                    id_data = int(mat_data['images'][0][i])

                    boxes_val.append(boxes_data.astype(np.uint16))
                    scores_val.append(scores_data.astype(np.float32))
                    ids_val.append(id_data)
            print("saving to:{}, len={}".format(new_path1, len(ids_train)))
            save_object(
                dict(boxes=boxes_train, scores=boxes_train, indexes=ids_train),
                new_path1)
            print("saving to:{}, len={}".format(new_path2, len(ids_val)))
            save_object(
                dict(boxes=boxes_val, scores=boxes_val, indexes=ids_val),
                new_path2)
        else:
            boxes_test = []
            scores_test = []
            ids_test = []

            print(mat_data.keys())
            print(mat_data['images'].shape)
            print(mat_data['boxes'].shape)
            print(mat_data['boxScores'].shape)
            for i in range(mat_data['images'].shape[1]):
                id_in = int(mat_data['images'][0][i])

                boxes_data = mat_data['boxes'][0][i]
                scores_data = mat_data['boxScores'][0][i].astype(np.float32)

                boxes_data_ = boxes_data.astype(np.uint16) - 1
                boxes_data = boxes_data_[:, (1, 0, 3, 2)]
                id_data = int(mat_data['images'][0][i])

                boxes_test.append(boxes_data.astype(np.uint16))
                scores_test.append(scores_data.astype(np.float32))
                ids_test.append(id_data)
            print("saving to:{}, len={}".format(new_path1, len(ids_test)))
            save_object(
                dict(boxes=boxes_test, scores=boxes_test, indexes=ids_test),
                new_path1)
