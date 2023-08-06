import pafy
import colorama,time
import json
from playsound import playsound
from youtube_api import YoutubeDataApi
from pyfiglet import Figlet
import subprocess,sys,os
import multiprocessing

glurl=""

FREE_API_KEY="AIzaSyA_qsbJMvLaklHfbLKMq4zaoVE-7UTTqcM"


'''Play function'''
def play():
    playsound(glurl)
'''Multiprocessed play function end'''


def makeStreamable(string):
    return "https://www.youtube.com/watch?v=" + string

def listToString(lst):
    return "".join(lst)

def getResults(query):
    streamableLinks=[]

    yt=YoutubeDataApi(FREE_API_KEY)
    searches=yt.search(q=query,max_results=10)

    for i in searches:
        streamableLinks.append(makeStreamable(i["video_id"]))
    return streamableLinks


def del0(lst):
    if lst[0]=="0":
        del lst[0]
    return lst


def timeToInt(tstr):
    components=tstr.split(":")
    hourSubcomponents=list(components[0])
    minSubcomponents=list(components[1])
    secComponents=list(components[2])

    hourSubcomponents=3600 * int(listToString(del0(hourSubcomponents)))
    minSubcomponents=60 * int(listToString(del0(minSubcomponents)))
    secComponents=int(listToString(del0(secComponents)))
    return hourSubcomponents+minSubcomponents+secComponents+2



def main():
    global glurl
    colorama.init()
    cs_fig=Figlet(font="jazmine")
    print(colorama.Fore.LIGHTGREEN_EX,cs_fig.renderText("Yt_Streamer"),colorama.Style.RESET_ALL)

    inp=input(colorama.Fore.CYAN+"Enter video query: "+colorama.Fore.YELLOW)
    res=getResults(inp)
    res_counter=1
    for re in res:
        video=pafy.new(re)
        bestaudio=video.getbestaudio()
        url=bestaudio.url
        glurl=url
        xz=timeToInt(video.duration)
        print(colorama.Fore.GREEN,f"Now playing[{res_counter}]: [{video.title}][{video.duration}][@{bestaudio.quality}]",colorama.Style.RESET_ALL)


        process=multiprocessing.Process(target=play)
        process.start()
        args=input("~ ")

        if args.lower()=="quit":
            process.terminate()
            print(colorama.Fore.RED+"\nStream Stopped"+colorama.Style.RESET_ALL)
            break

        if args.lower()=="next":
            process.terminate()
            continue


        res_counter+=1
    print(colorama.Fore.RED+"\nQueue finished")
    print("Exited")
'''if __name__=="__main__":
    main()'''
