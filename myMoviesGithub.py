import os
import time
import sys
from pymongo import MongoClient

def videoFilesIMySystem():
    try:
        myMovies = []
        MoviesTimeline = []
        MoviesPath = []
        availext = [".mkv", ".mp4",".avi"]
        avoid = ["path of any folders inside the drive that needs to be avoided separated by comma's (E:/documents,E:/Photos)"]
        for root, dirs, files in os.walk("E:"):
            for file in files:
                if (file.endswith(tuple(availext))):
                    isflag = ((root in avoid))
                    if (isflag == False):
                        rotfilename = root + "\\" + file;
                        print(time.ctime(os.stat(rotfilename).st_atime))
                        timeLastUsed = time.ctime(os.stat(rotfilename).st_atime)
                        print("---------------------")
                        print(file)
                        print("**********************")
                        myMovies.append(file)
                        MoviesTimeline.append(timeLastUsed)
                        MoviesPath.append(rotfilename);

        insertDataMongoDb(myMovies,MoviesTimeline,MoviesPath)
    except:
        print("Something went wrong", sys.exc_info()[0])

def insertDataMongoDb(movieDetails,MovieTime, MoviePath):
    try:
        print("Came Here")
        client = MongoClient();
        db = client.mytest
        coll = db.myMoviesNew
        print("DB Connection Done")
        count = len(movieDetails)
        countime = len(MovieTime)
        print(count)
        print(countime)
        for MovieName, MovieLast, MoviePth in zip(movieDetails, MovieTime, MoviePath):
            print('{} ::: {}'.format(MovieName, MovieLast))
            coll.insert_one({"nameOfMovie": MovieName, "LastTimeUsed":MovieLast, "MoviePath": MoviePth  });
            print("Path {}".format(MoviePth))


    except:
        print("Unexpected error:", sys.exc_info()[0])















if __name__ == "__main__":
    videoFilesIMySystem()




