'''
Created on 15-Apr-2017

@author: mitalisalvi
'''

#HERE IT IS ASSUMED THERE'S EXISTS A FOLDER CALLED BING WALLPAPER IN THE PICTURES FOLDER. IF NOT CREATED , CODE EXISTS IN PINGFUNCTIONALITYCHECK.PY
import json
import subprocess

#Try with python3
try:
    from urllib2 import urlopen
    from urllib import urlretrieve

#Else try python2
except:
    from urllib2 import urlopen
    from urllib import urlretrieve

from os import path

SCRIPT = """/usr/bin/osascript<<END
        tell application "Finder"
        set desktop picture to POSIX file "%s"
        end tell
        END"""

#User home folder
homeFolder = path.expanduser("~")

#Save pictures to a folder
pictureLocation = homeFolder + "/Pictures/bing-wallpaper/"


def main():
    ########Defining variables#######

    #URL in json format for latest wallpaper
    #here mkt refers to MARKET that is LANGUAGE_COUNTRY, mine is set to India
    #to get list of available market - https://msdn.microsoft.com/en-us/library/dd251064.aspx
    # dx denotes the day before the current day. idx=0 means current day, idx=1 means yesterday and so on.
    # n is an integer denoting the number of days before the day denoted by idx. It grabs data about all the n number of images.
    url = "http://www.bing.com/HPImageArchive.aspx?format=js&idx=5&n=1&mkt=en-IN"
    
    getHighRes = 1 #Manually change the resolution in the url to 1920x1200. Change to 0 if url breaks.

    #Get json response from bing.com
    response = urlopen(url)

    #Trying python 3
    try:
        output = response.readall().decode('utf-8')

    #Else trying python2
    except:
        output = response.read()
           
    #Get json output
    data = json.loads(output)

    #Form image url from json
    output_url = "http://www.bing.com/" + data["images"][0]["url"]

    #Form 1920x1200 image from above url
    output_url_highres = output_url.replace("1080", "1200")


    #If higher resolution is preferred(default)
    if getHighRes == 1:
        
        #Use try block to catch any failure in getting the high res image
        try:
            process_url(output_url_highres)

        except:
            process_url(output_url)

    else:
        process_url(output_url)


def process_url(image_url):
    if not check_url(image_url)  == 1:
        filename = pictureLocation + image_url.split('/')[-1]
        #Get the filename of the new file from the url

        #Retrieve the image from the web and save it to desired location
        req = urlretrieve(image_url, filename)

        #Save the file path + filename to the output variable
        bingImage = path.abspath(filename)
        #print(bingImage)
        set_desktop_background(bingImage)

    else:
        raise Exception('bad url')

def check_url(image_url):
    conn = urlopen(image_url)
    if not conn.getcode() == 200:
        return 1
    
def set_desktop_background(filename):
    subprocess.Popen(SCRIPT%filename, shell=True)
    
main()
