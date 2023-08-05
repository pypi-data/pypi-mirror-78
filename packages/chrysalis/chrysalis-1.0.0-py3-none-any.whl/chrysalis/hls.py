import time
import av
import collections
import math
from log import logger
import os
import numpy
from ch_errors import FolderNotFound
import av.filter
from fractions import Fraction

class HLS:
    """
    HLS converts video to HLS video stream

    It drops first 3 frames to determine FPS with which HLS should stream
    """

    def __init__(self,folder, hls_time=10, hls_list_size=5):
        if not os.path.isdir(folder):
            raise FolderNotFound

        # clear folder
        fld = os.listdir(folder)
        for item in fld:
            if item.endswith(".ts") or item.endswith(".m3u8"):
                os.remove(os.path.join(folder, item))
                logger.debug("delete file from folder: {}".format(os.path.join(folder, item)))

        self.__folder = folder
        self.__hls_manifest = folder + "/playlist.m3u8"
        self.__hls_opts = {
            'hls_list_size': str(hls_list_size),
            'hls_time': str(hls_time),
            'hls_segment_type': 'mpegts',
            'hls_flags': 'delete_segments+discont_start',
            'hls_start_number_source': 'datetime',
            'strftime': '1',
            'use_localtime': '1',
            'hls_segment_filename': folder + "/%s.ts"
        }
        self.__ts_queue = []
        self.__fps = None
        self.__output = None
        self.__stream = None
        self.__graph = av.filter.Graph()
        self.__filter_chain = None

    def StreamImage(self, numpy_image=None):
        if len(self.__ts_queue) < 10 and self.__fps is None:
            ts = int(round(time.time() * 1000))
            self.__ts_queue.append(ts)
            if len(self.__ts_queue) == 1:
                sh = numpy_image.shape
                width = sh[1]
                height = sh[0]
            return

        if self.__fps is None:
            sh = numpy_image.shape
            width = sh[1]
            height = sh[0]
            # determinte fps from first 5 frames
            np_arr = numpy.array(self.__ts_queue)
            ts_diffs = abs(numpy.amin(np_arr[4:]) - numpy.amax(np_arr[4:]))
            self.__fps = math.floor(len(np_arr) / ts_diffs * 1000)
            logger.info("assessed fps from dropped frames {}".format(self.__fps))
            self.__ts_queue.clear()

            # test

            filter_chain = []
            filter_chain.append(self.__graph.add_buffer(width=width, height=height, format='bgr24'))
            # filter_chain.append(self.__graph.add('lutrgb', 'r=0:b=0'))
            factor = 30/self.__fps
            logger.info("assessed factor for resampling: {}".format(factor))
            # filter_chain.append(self.__graph.add('setpts', '{}*PTS'.format(factor)))
            # filter_chain.append(self.__graph.add('r', '30'))
            filter_chain.append(self.__graph.add('minterpolate', 'mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=20'))
            filter_chain[-2].link_to(filter_chain[-1])
            filter_chain.append(self.__graph.add("buffersink"))
            filter_chain[-2].link_to(filter_chain[-1])
            self.__filter_chain = filter_chain

            self.__output = av.open(self.__hls_manifest, "w", format='hls', options=self.__hls_opts)
            self.__stream = self.__output.add_stream("h264", rate=self.__fps)
            self.__stream.width = sh[1]
            self.__stream.height = sh[0]

        frame = av.VideoFrame.from_ndarray(numpy_image, format="bgr24")
        self.__filter_chain[0].push(frame)

        out_v_frame = self.__filter_chain[-1].pull()
        out_v_frame.pts = None
        self.__output.mux(self.__stream.encode(out_v_frame))
        # out = out_v_frame.to_ndarray(format="bgr24")

        


        