## ==> GUI FILE
from main import *

from gtts import gTTS
from googletrans import Translator
import os
import pafy
from youtube_search import YoutubeSearch
import vlc
import sys
import wikipedia
import wolframalpha

class Functions(MainWindow):
    def GetAnswer(query):
        '''Return answer from wikipedia or wolframalpha'''
        if query:
            try:
                # WOLFRAMALPHA
                app_id = 'WTRAQ5-VR7PE9EHYH'
                client = wolframalpha.Client(app_id)

                res = client.query(query)

                answer = ''
                for pod in res.pods:
                    if pod.title in ["Solution", "Solutions", "Real solution", "Real solutions", "Complex solutions", "Result"] :
                        answer += pod.title
                        answer += ':\n'
                        for sub in pod.subpods:
                            answer += sub.plaintext
                            answer += '\n'
                # answer = next(res.results).text

            except:
                # WIKIPEDIA
                answer = wikipedia.summary(query, sentences=3)
            return answer
        return None
    
    def GetSound(query):
        '''Return mp3 url'''
        if query:
            try:
                # WOLFRAMALPHA
                app_id = 'WTRAQ5-VR7PE9EHYH'
                client = wolframalpha.Client(app_id)

                res = client.query(query)
                answer = ''
                for pod in res.pods:
                    if pod.title in ["Solution", "Solutions", "Real solution", "Real solutions", "Complex solutions", "Result"] :
                        answer += pod.title
                        answer += ':\n'
                        for sub in pod.subpods:
                            answer += sub.plaintext
                            answer += '\n'

            except:
                # WIKIPEDIA
                answer = wikipedia.summary(query, sentences=3)
            if os.path.exists('gtts_obj.mp3'):
                os.remove('gtts_obj.mp3')
            gtts_obj = gTTS(answer, lang='en')
            gtts_obj.save('gtts_obj.mp3')
            url = QtCore.QUrl.fromLocalFile('gtts_obj.mp3')
            return url
        return None

    def GetYouTubeLink(query):
        '''Return the best Youtube link by keywords'''
        if query:
            search_term = ""
            for word in str(query).split():
                search_term += word + " "
            results = YoutubeSearch(search_term, max_results=10).to_dict()
            url_code = results[0]['id']
            url = "https://www.youtube.com/watch?v=" + url_code  
            return url
        return None  

    def VLCPlay(url):
        '''Stream video online using VLC'''
        global media
        video = pafy.new(url)
        best = video.getbest()
        media = vlc.MediaPlayer(best.url)
        media.video_set_spu(2) 
        media.play()

    def PauseVideo():
        media.pause()

    def StopVideo():
        media.stop()

    def MediaCheck():
        try:
            if media:
                return True
        except:
            return False

    def Translate(query, src, dest):
        '''Return translated text'''
        translator = Translator()
        
        if (src == "auto detect"):
            translations = translator.translate(query.split('\n'), dest=dest)
        else:
            translations = translator.translate(query.split('\n'), src=src, dest=dest)

        origin = ''
        answer = ''
        for translation in translations:
            origin += translation.origin + '\n'
            answer += translation.text + '\n'
        return answer