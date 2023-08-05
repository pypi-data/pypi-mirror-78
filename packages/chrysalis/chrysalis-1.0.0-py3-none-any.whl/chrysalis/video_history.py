import av
from chunker import Chunker
import logging as logger
import os
from fractions import Fraction

class VideoHistory:

    def __init__(self, redis_conn, video_stream_name, audio_stream_name):
        self.__redis_conn = redis_conn
        self.__video_stream_name = video_stream_name
        self.__audio_stream_name = audio_stream_name
        self.__video_codec = av.Codec('h264', 'r').create()
        self.__audio_codec = av.Codec('aac', 'r').create()
        self.__last_query = None
        self.__last_query_timestamp = 0
        self.__default_folder = "/tmp/chrys_video_archive"
        if not os.path.exists(self.__default_folder):
            os.makedirs(self.__default_folder)

    def RecordVideo(self, fromtimestamp, totimestamp):
        filename = str(fromtimestamp) + "_" + str(totimestamp) + ".mp4"
        container = av.open(self.__default_folder + "/" + filename, 'w', format="mp4")
        stream = container.add_stream("h264", rate=20)
        stream.time_base = Fraction(500,1)

        packet_count = 0

        self.__last_query = fromtimestamp

        while True: 
            buffer = self.__redis_conn.xread({self.__video_stream_name:self.__last_query}, block=1000)
            if len(buffer) > 0:
                arr = buffer[0]
                inner_buffer = arr[1]
                logger.debug("returned packets: {} in {} s".format(len(inner_buffer), (fromtimestamp - totimestamp)))
                last = inner_buffer[-1]
                self.__last_query = last[0]
                self.__last_query_timestamp = int(self.__last_query.decode('utf-8').split("-")[0])

                segment_length = self.__last_query_timestamp - fromtimestamp
                print("LENGTH: {} ms".format(segment_length))

                video_packets = Chunker(self.__video_codec).packets(inner_buffer)
                video_keys = video_packets.keys()
                lst = sorted(video_keys)

                prev_pts = 0                    
                for ts in lst:
                    packet = video_packets[ts]
                    packet_count += 1
                    # if packet.is_keyframe:
                    #     print(ts, packet_count, packet, packet.is_keyframe)
                    since_start = abs(fromtimestamp - ts)
                    print(since_start)

                    # if packet.pts is None:
                    #     packet.pts = prev_pts
                    #     packet.dts = prev_pts
                    # else:
                    #     packet.dts = prev_pts
                    # # packet.pts = int(ts / 10)
                    
                    # print(packet.dts,packet.pts)
                    packet.stream = stream
                    container.mux(packet)
                    # prev_pts = packet.dts
                    prev_pts += 40


                if self.__last_query_timestamp >= totimestamp:
                    logger.debug("finished recording a video from buffer at {}".format(self.__last_query_timestamp))
                    break

            else:
                # TODO: throw error
                if self.__last_query_timestamp == 0:
                    pass
                break
        

        container.close()