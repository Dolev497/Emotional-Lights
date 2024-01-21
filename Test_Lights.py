import Genius_Lyrical_Grabber as LG
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import openai
import numpy
from copy import deepcopy
from numpy import dot
from numpy.linalg import norm
import minitest as mini
import dotenv

dotenv.load_dotenv()

openai.api_key = os.environ['GPTKEY']
TrackID = "4RJdwSqHapVcW5DaRtTkv0"



def splitty(lyrics:str):
        verses = lyrics.split("\n\n")
        sentences = []
        for count, verse in enumerate(verses):
            sentences.append(verse.split("\n"))
            sentences[count] = [x for x in sentences[count] if "[" not in x]
        print(sentences)
        return sentences
def cosine_similarity(a, b):
    cos_sim = dot(a, b)/(norm(a)*norm(b))
    return cos_sim
def chatgptcall(sentence):
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=f"{sentence}",
        encoding_format="float"
    )
    return response["data"][0]["embedding"]

def Sentence_To_Embsections2(sentences, sections):
        emb_sentences = []
        Dynamic_Dic = {}
        count = 0
        for verses in sentences:
            verse = []
            for sentence in verses:
                verse.append(chatgptcall(sentence))

            emb_sentences.append(verse)
        print(emb_sentences[0][0][0])
        print(emb_sentences[1][0][0])
        
        additionalcuts = numpy.absolute(len(emb_sentences)-sections)
        if additionalcuts != 0:
            Ranks = {}
            for count, verse in enumerate(emb_sentences):
                if len(verse)>1:
                    Ranks[count] = [cosine_similarity(emb_sentences[count][x], emb_sentences[count][x+1]) for x in range(len(verse)-1)]
                else:
                    Ranks[count] = [100]
            print("TEMPS PRINTING")
            pasts = []
            for cut in range(additionalcuts):
                
                max_list= [min(x) for x in Ranks.values()]
                current_max = min(max_list)
                verseno = max_list.index(current_max)
                bias = len([x for x in pasts if x <= verseno])                     
                pasts.append(verseno)
                temp = emb_sentences[verseno+bias][Ranks[verseno].index(current_max):]
                if temp == []:
                    raise ValueError
                else:
                     print("temping", current_max)
                emb_sentences[verseno+bias] = emb_sentences[verseno][:Ranks[verseno].index(current_max)]
                emb_sentences.insert(verseno+bias, temp)
                Ranks[verseno].pop(Ranks[verseno].index(current_max))
        '''
        return emb_sentences

def Emb_sections_To_Text(sentences, emb_sentences):
    all_sentence = []
    for x in sentences:
        all_sentence.extend(x)
    print(all_sentence)
    Cut_Song = deepcopy(emb_sentences)
    totalcount = 0
    for count, section in enumerate(emb_sentences):
        for count2, sentence_emb in enumerate(section):
            Cut_Song[count][count2] = all_sentence[totalcount]
            totalcount+=1
    print(Cut_Song)

def Lyric_Splitter(name, sections):
    lyrics = LG.GrabLyric(name)
    return Emb_sections_To_Text(splitty(lyrics), Sentence_To_Embsections2(splitty(lyrics), sections))
    
    HI = Sentence_To_Embsections2(splitty(lyrics))
    
    print(len(HI))
    for a in HI:
        if a == []:
            print(True)
Lyric_Splitter("Sparks Fly (Taylor's Version)", 8)
