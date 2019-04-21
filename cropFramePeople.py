# -*- coding: utf-8 -*-
'''
@Author: Chen Zhiwei
@Description: file content
@Date: 2019-04-20 16:53:54
@LastEditTime: 2019-04-21 20:42:41
'''
import os
import sys
import re
import cv2
PATH_RESULT = 'xxx'
PATH_VIDEO = "xxx"
PATH_CROP_IMG = "xx"


def cropXY(img, point1, point2):
    min_x = min(int(point1[0]), int(point2[0]))
    min_y = min(int(point1[1]), int(point2[1]))
    width = abs(int(point1[0]) - int(point2[0]))
    height = abs(int(point1[1]) - int(point2[1]))
    cut_img = img[min_y:min_y + height, min_x:min_x + width]
    return cut_img


if __name__ == "__main__":
    print("=====================")
    print("video_num:{}".format(len(os.listdir(PATH_VIDEO))))
    print("txt_num:{}".format(len(os.listdir(PATH_RESULT))))
    print("=====================")
    # temp_video = os.path.join(PATH_VIDEO, "ch04_20190324074316.mp4")
    # temp_txt = os.path.join(PATH_RESULT, "ch04_20190324074316.txt")

    _id = 0
    for lists in os.listdir(PATH_RESULT):
        _id += 1
        name = lists.split('.')[0]
        temp_video = os.path.join(PATH_VIDEO, name + ".mp4")
        temp_txt = os.path.join(PATH_RESULT, name + ".txt")

        pathCropImgDetail = os.path.join(PATH_CROP_IMG, name)
        if os.path.isdir(pathCropImgDetail):
            print("[{}/{}]Video:{} COMPELETE! Skip ...".format(
                _id, len(os.listdir(PATH_RESULT)), temp_video))
            continue
        else:
            os.makedirs(pathCropImgDetail)

        lines = open(temp_txt).readlines()
        if len(lines) == 1:
            print("[{}/{}]Video:{} NO People! Skip ...".format(
                _id, len(os.listdir(PATH_RESULT)), temp_video))
            continue
        print("[{}/{}] {}<-->{}".format(_id, len(os.listdir(PATH_RESULT)),
                                        temp_txt, temp_video))
        cropFrameId = []
        point1 = []
        point2 = []
        for _index, line in enumerate(lines):
            if _index == 0:
                continue
            s = re.findall(r'[(|\[](.*?)[)|\]]', line)
            cropFrameId.append(s[0])
            point1.append(s[1].split(','))
            point2.append(s[2].split(','))
        # print(_index, len(cropFrameId), len(point1), len(point2))
        # exit(0)
        _framesId = 0
        _cropFrameId = 0
        cap = cv2.VideoCapture(temp_video)
        while cap.isOpened():
            ret, frame_img = cap.read()
            if ret and (_cropFrameId != _index):
                sys.stdout.write(
                    "\r Scanning Frames[{}<->{}], Crop Frames[{}/{}]".format(
                        _framesId, int(cropFrameId[_cropFrameId]),
                        _cropFrameId + 1, _index))
                sys.stdout.flush()
                if _framesId == int(cropFrameId[_cropFrameId]):
                    sameId = 0
                    cut_img = cropXY(frame_img, point1[_cropFrameId],
                                     point2[_cropFrameId])
                    cv2.imwrite(
                        os.path.join(pathCropImgDetail,
                                     str(_framesId) + ".jpg"), cut_img)
                    _cropFrameId += 1
                elif int(cropFrameId[_cropFrameId]) == _framesId - 1:
                    cut_img = cropXY(frame_img, point1[_cropFrameId],
                                     point2[_cropFrameId])
                    cv2.imwrite(
                        os.path.join(
                            pathCropImgDetail,
                            str(_framesId) + "_" + str(sameId) + ".jpg"),
                        cut_img)
                    sameId += 1
                    _cropFrameId += 1
                    _framesId -= 1
                _framesId += 1
            else:
                break
        print()
