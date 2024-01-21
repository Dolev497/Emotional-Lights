import cohere
from cohere.responses.classify import Example
from cohere.custom_model_dataset import CsvDataset
import time
import numpy as np
import sklearn
import spotipy
import json
import flask
from spotipy.oauth2 import SpotifyOAuth
import sqlite3 as sql
import tqdm 
import Lyrics_To_Colour_Map as Ly
import matplotlib.pylab as pl
import os
import dotenv
dotenv.load_dotenv()
CoKey = os.environ["COHEREKEY"]
class TextData():
    def __init__(self, path):
        self.path = path
        self.values = {}
        fivehundred = {"sadness": 0, "fear": 0, "joy": 0, "anger": 0, "surprise": 0, "love": 0}
        with open(path, "r", encoding="UTF-8") as file:
            print("Beginning to prepare SQL Database")
            for line in tqdm.tqdm(file):
                Eline = line.removesuffix("\n")
                segments = Eline.split(";")
                if fivehundred[segments[1]] < 500:
                    self.values[segments[0]] = segments[1]
                    fivehundred[segments[1]] += 1
                else:
                    continue
        print(fivehundred)
        print(self.values)
        with open(path[:-5]+"2"+path[-5:], "w", encoding="UTF-8") as file:
            self.classes = list(self.values.values())
            self.samples = list(self.values.keys())
            print(self.classes)
            lines = [self.samples[x]+","+self.classes[x]+"\n" for x in range(len(self.values))]
            file.writelines(lines)
    def get_set(self):
        return self.values.items()
    
    def get_classes(self):
        return np.array(self.values.values())
    
    def get_samples(self):
        return np.array(self.values.keys())

class ColourMap():
    def __init__(self, Split_Lyrics, SectionInfo):
        self.Split_Lyrics = [' '.join(x) for x in Split_Lyrics]
        self.Cohe = cohere.Client(CoKey)
        print(SectionInfo)
        print(SectionInfo[0]["start"])
        self.durations = [SectionInfo[x]["duration"] for x in range(len(SectionInfo))]
        self.TimetoLyric = [(self.durations[x], Split_Lyrics[x]) for x in range(len(self.durations))]
        print(self.TimetoLyric)
    def Time_to_Emotion(self):
        self.LeemotionMap = []
        emotionlist = self.Cohe.classify(self.Split_Lyrics, "e7c79a7b-3bf0-4c94-82e9-2bd03501e668-ft")
        for count, sect in enumerate(emotionlist.classifications):
            self.LeemotionMap.append((self.TimetoLyric[count][0], sect.prediction))
        print(self.LeemotionMap)
    def Time_to_Colour(self):
        ColourDic = {"sadness": "#0071b6", "joy": "#f0a412", "anger": "#fa8989", "fear": "#2f2323", "love": "#F7B3CD", "surprise": "#AAFF00"}
        self.ColourMaaap = []
        for count, sect in enumerate(self.LeemotionMap):
            self.ColourMaaap.append((sect[0], ColourDic[sect[1]]))
        print(self.ColourMaaap)
    def Time_to_Map(self):
        pl.figure()
        start = 0
        for period in self.ColourMaaap:
            pl.plot([start, start+period[0]], [0, 0], color=period[1], linewidth = 15)
            start+=period[0]
        pl.legend()
        pl.xlabel("Time")
        pl.ylabel("Colours")
        pl.title("ColourMap")
        pl.show()
cursor = sql.connect("Train.db")

#Database = TextData(r"C:\Users\dolev\Desktop\Programs\APIs\Emotional_Lights\trai2n.txt")
'''

values = Database.get_set()
cursor.execute("CREATE TABLE Train(Sample string, Class string, PointID integer PRIMARY KEY)")
cursor.executemany("INSERT INTO Train(Sample, Class) VALUES(?, ?)", values)
print([x for x in cursor.execute("SELECT PointID FROM Train ORDER BY PointID DESC LIMIT 1")])
'''

#Cohe = cohere.Client("Z4qwucm7otTNnqGZkjZoKH1PrO7e1tQOXl1eXr79")
#Train_Set = CsvDataset(r"C:\Users\dolev\downloads\trai2n.csv", ",")


#ModelReturns = Cohe.create_custom_model("round_2", "CLASSIFY", Train_Set)

cursor.commit()

if __name__ == "__main__":
    ID = str(input("Song ID pls"))
    Song, Analysis = Ly.RunSplittsies(ID)
    CM = ColourMap(Song.get_split_lyrics(), Analysis.get_sections())
    CM.Time_to_Emotion()
    CM.Time_to_Colour()
    CM.Time_to_Map()
