import imp
import bagpy
from bagpy import bagreader
import pandas as pd


stat_reader_open = bagreader('stationaryDataOpen.bag')
walk_reader_open = bagreader('MovingDataOpen.bag')
stat_reader_occ = bagreader('StationaryDataOccluded.bag')
walk_reader_occ = bagreader('MovingDataOccluded.bag')
circle_reader_stat = bagreader('CircleStationaryRTK.bag')
circle_reader_walk = bagreader('CircleRTKOccluded.bag')



##stat_data_open = stat_reader_open.message_by_topic('/gps')
#walk_data_open = walk_reader_open.message_by_topic('/gps')
#stat_data_occ = stat_reader_occ.message_by_topic('/gps')
#walk_data_occ = walk_reader_occ.message_by_topic('/gps')
circle_stat = circle_reader_stat.message_by_topic('/gps')
circle_walk = circle_reader_walk.message_by_topic('/gps')






