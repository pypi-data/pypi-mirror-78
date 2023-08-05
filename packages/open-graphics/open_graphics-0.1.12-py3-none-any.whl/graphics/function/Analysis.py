import os
import shutil

import cv2
import numpy as np
import requests
from tqdm import tqdm

from .Format import get_file_md5
from ..common.logs import logs

__all__ = ["delete_file",
           "extract_frames",
           "download"]


def delete_file(src, dst="../"):
    all_md5 = {}
    dirs = os.listdir(src)
    if ".DS_Store" in dirs:
        dirs.remove(".DS_Store")
    for p in dirs:
        md5 = get_file_md5(os.path.join(src, p))
        if md5 in all_md5.values():
            shutil.move(os.path.join(src, p), os.path.join(dst, p))
            logs.info(os.path.join(src, p))
        else:
            all_md5[p] = md5


def extract_frames(path, threshold=30.0):
    """
    提取视频关键帧
    :param path: the video path
    :param threshold: the threshold of two frames`s pixel diff
    :return: [frame for (idx, frame) in key_frames.items()]
    """
    idx, key_frames, prev_frame = 0, {}, None
    try:
        video_capture = cv2.VideoCapture(path)
        success, frame = video_capture.read()
        height, width = frame.shape[:2]
        key_frames[idx] = frame[:, :, ::-1]
        idx += 1
        while success:
            curr_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LUV)
            if curr_frame is not None and prev_frame is not None:
                diff = cv2.absdiff(curr_frame, prev_frame)
                diff_sum_mean = np.sum(diff) / (width * height)
                if diff_sum_mean > threshold:
                    key_frames[idx] = frame[:, :, ::-1]
            idx += 1
            prev_frame = curr_frame
            success, frame = video_capture.read()
        video_capture.release()
    except ValueError:
        pass

    return key_frames


def download(url, path=None, overwrite=False):
    """
    下载文件
    Args:
        url: 下载的文件地址
        path: 文件保存路径，默认保存在当前文件夹
        overwrite: 如果文件存在，是否覆盖原文件
    Returns: 下载的文件路径
    """

    if path is None:
        file_name = url.split('/')[-1]
    else:
        path = os.path.expanduser(path)
        if os.path.isdir(path):
            file_name = os.path.join(path, url.split('/')[-1])
        else:
            file_name = path

    if overwrite or not os.path.exists(file_name):
        dir_name = os.path.dirname(os.path.abspath(os.path.expanduser(file_name)))
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        print('Downloading %s from %s' % (file_name, url))
        r = requests.get(url, stream=True)
        if r.status_code != 200:
            raise RuntimeError("Failed downloading url %s" % url)
        total_length = r.headers.get('content-length')
        with open(file_name, 'wb') as f:
            if total_length is None:  # no content length header
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
            else:
                total_length = int(total_length)
                for chunk in tqdm(r.iter_content(chunk_size=1024),
                                  total=int(total_length / 1024. + 0.5),
                                  unit='KB', unit_scale=False, dynamic_ncols=True):
                    f.write(chunk)
    return file_name
