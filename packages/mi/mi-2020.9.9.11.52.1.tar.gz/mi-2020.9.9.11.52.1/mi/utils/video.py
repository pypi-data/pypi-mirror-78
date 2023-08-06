#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : video
# @Time         : 2020/8/31 4:26 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from moviepy.editor import *


def video2audio(paths, verbose=False, subclip=None, ffmpeg_params=["-f", "mp3"]):
    """
        clip = VideoFileClip('蛋清和蛋黄是这么分离的.720p').subclip(3, 7)

    :param paths: (video_path, audio_path)
    :param subclip:
    :param ffmpeg_params:
    :return:
    """
    video_path, audio_path = paths

    with VideoFileClip(video_path) as clip:
        duration = int(clip.duration)
        if subclip:
            s, e = subclip[0], duration if subclip is None or duration < subclip[1] else subclip[1]
            clip = clip.subclip(s, e)

        clip.audio.write_audiofile(
            audio_path, fps=None, nbytes=2, buffersize=2000,
            codec=None, bitrate=None, ffmpeg_params=ffmpeg_params,
            write_logfile=False, verbose=verbose, logger='bar' if verbose else None
        )
