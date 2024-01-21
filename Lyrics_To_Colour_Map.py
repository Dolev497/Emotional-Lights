import Genius_Lyrical_Grabber as LG
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import openai
import numpy
from copy import deepcopy
from numpy import dot
from numpy.linalg import norm
import minitest as mini
import os
import dotenv

dotenv.load_dotenv()

openai.api_key = os.environ['GPTKEY']
TrackID = "4RJdwSqHapVcW5DaRtTkv0"
class SongAnalysis():
    def __init__(self, TrackID):
        CLIENT_ID = os.environ["SPOTKEY"]
        CLIENT_SECRET = os.environ["SPOTSECRET"]


        auth_manager = SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET)
        sp = spotipy.Spotify(auth_manager=auth_manager)

        response = sp.audio_analysis(TrackID)
        self.sections = response["sections"]
        response = sp.track(TrackID)
        self.name = response["name"]
        self.number_of_sections = len(self.sections)

    def get_sections(self):
        return self.sections
    def get_number_of_sections(self):
        return self.number_of_sections
    def get_name(self):
        return self.name

class The_Song_Splitter():
    def __init__(self, lyrics:str, numsect):
        self.sections = numsect
        verses = lyrics.split("\n\n")
        self.sentences = []
        for count, verse in enumerate(verses):
            self.sentences.append(verse.split("\n"))
            self.sentences[count] = [x for x in self.sentences[count] if "[" not in x]
    def cosine_similarity(self, a, b):
        cos_sim = dot(a, b)/(norm(a)*norm(b))
        return cos_sim
    def chatgptcall(self, sentence):
        response = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=f"{sentence}",
            encoding_format="float"
        )
        return response["data"][0]["embedding"]

    def Sentence_To_Embsections(self):
        self.emb_sentences = []
        Dynamic_Dic = {}
        count = 0
        for verses in self.sentences:
            verse = []
            for sentence in verses:
                verse.append(self.chatgptcall(sentence))

            self.emb_sentences.append(verse)
        
        additionalcuts = numpy.absolute(len(self.emb_sentences)-self.sections)
        if additionalcuts != 0:
            Ranks = []
            for count, verse in enumerate(self.emb_sentences):
                Ranks.append([self.cosine_similarity(self.emb_sentences[count][x], self.emb_sentences[count][x+1]) for x in range(len(verse)-1)])
            print(Ranks)
            self.emb_sentences = mini.initiate_splittys(Ranks, self.emb_sentences, additionalcuts)

            '''print("TEMPS PRINTING")
            pasts = []
            for cut in range(additionalcuts):
                
                max_list= [min(x) for x in Ranks.values()]
                current_max = min(max_list)
                verseno = max_list.index(current_max)
                bias = len([x for x in pasts if x <= verseno])                     
                pasts.append(verseno)
                temp = self.emb_sentences[verseno+bias][Ranks[verseno].index(current_max)+1:]
                self.emb_sentences[verseno+bias] = self.emb_sentences[verseno][:Ranks[verseno].index(current_max)+1]
                self.emb_sentences.insert(verseno+bias, temp)
                Ranks[verseno].pop(Ranks[verseno].index(current_max))
                print(self.emb_sentences)
        '''
    def Emb_sections_To_Text(self):
        all_sentence = []
        for x in self.sentences:
            all_sentence.extend(x)
        print(all_sentence)
        self.Cut_Song = deepcopy(self.emb_sentences)
        totalcount = 0
        for count, section in enumerate(self.emb_sentences):
            for count2, sentence_emb in enumerate(section):
                self.Cut_Song[count][count2] = all_sentence[totalcount]
                totalcount+=1
        print(self.Cut_Song)
    def get_split_lyrics(self):
        return self.Cut_Song

def RunSplittsies(ID:str):
    Test = SongAnalysis(ID)
    print(Test.get_number_of_sections())
    Song = The_Song_Splitter(LG.GrabLyric(Test.get_name()), Test.get_number_of_sections())
    print(len(Song.sentences))
    Song.Sentence_To_Embsections()
    Song.Emb_sections_To_Text()
    return Song, Test

#print(x)
 #   hi.Emb_sections_To_Text()
  #  print(hi.Cut_Song)
#print(chatgptcall(Test.get_number_of_sections(), lyrics.replace("e", "3")))