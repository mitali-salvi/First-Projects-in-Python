'''
Created on 21-Jun-2018

@author: mitalisalvi
'''

from pytube import YouTube

from os import path

#User home folder
homeFolder = path.expanduser("~")

#Save videos to a folder
pictureLocation = homeFolder + "/Movies/DownloadVideos/"

def main():
    yt = YouTube('https://www.youtube.com/watch?v=9bZkp7q19f0')
    print(yt.title)
    stream = yt.streams.first()
    stream.download(pictureLocation)
    print('DONE')
    
main()