#!/usr/bin/env python3

from pytube import YouTube
import pandas as pd

SAVE_PATH = "/home/sai/Aish/Pivotchain/video_dwn/gas_cylinder"
df = pd.read_csv('gas_cylin.csv')
for i in df['url']:
    try:

        yt = YouTube(i)
    except:
        print("Connection Error")
    stream = yt.streams.first()
    try:
        # downloading the video
        print('Downloading')
        stream.download(SAVE_PATH)
        print('Downloaded')

    except:
        print("Some Error!")
print('Task Completed!')



