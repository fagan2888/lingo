import os
import io
import re
import sox
import Tkinter, Tkconstants, tkFileDialog
from playsound import playsound
from google.cloud import speech
from gtts import gTTS
from apiclient.discovery import build

speech_file = 'temp2.flac'

sourceLanguages = {
    "English" : "en-US",
    "Spanish" : "es-MX",
    "Portuguese" : "pt-BR",
    "Chinese" : "cmn-Hans-CN",
    "Japanese" : "ja-JP",
    "Korean" : "ko-KR",
    "French" : "fr-FR",
    "German" : "de-DE",
    "Turkish" : "tr-TR"
    }

targetLanguages = {
    "English" : "en",
    "Spanish" : "es",
    "Portuguese" : "pt",
    "Chinese" : "zh-CN",
    "Japanese" : "ja",
    "Korean" : "ko",
    "French" : "fr",
    "German" : "de",
    "Turkish" : "tr"
    }

targetGTTSLanguages = {
    "English" : "en-us",
    "Spanish" : "es-us",
    "Portuguese" : "pt-br",
    "Chinese" : "zh-cn",
    "Japanese" : "ja",
    "Korean" : "ko",
    "French" : "fr",
    "German" : "de",
    "Turkish" : "tr"
    }

def translate_speech():
    #record sound from microphone to FLAC file
	os.popen('rec temp.flac silence 1 0.1 3% 1 3.0 3%')

    #convert single channel FLAC
	tfm = sox.Transformer()
	tfm.convert(samplerate=44100, n_channels=1, bitdepth=16)
	tfm.build('temp.flac', 'temp2.flac')

    #get audio transcript
	speech_client = speech.Client()
	with io.open(speech_file, 'rb') as audio_file:
		content = audio_file.read()
		audio_sample = speech_client.sample(
			content=content,
			source_uri=None,
			encoding='FLAC',
			sample_rate=44100
			)
	alternatives = speech_client.speech_api.sync_recognize(
	    audio_sample,
	    language_code=sourceLanguages[sourcelangs.get()],
	    max_alternatives=3
	    )

	print alternatives[0].transcript
	print alternatives[0].confidence

    #translate transcript
	service = build('translate', 'v2', developerKey='')
	collection = service.translations()
	request = collection.list(q=alternatives[0].transcript, target=targetLanguages[targetlangs.get()])
	request.uri = re.sub('www.googleapis','translation.googleapis',request.uri) + '&model=nmt'
	response = request.execute()

	print response['translations'][0]['translatedText']

    #convert translated transcript to speech
	tts = gTTS(text=response['translations'][0]['translatedText'], lang=targetGTTSLanguages[targetlangs.get()])
	tts.save('temp.mp3')
	playsound('temp.mp3')

root = Tkinter.Tk()
root.geometry("{}x{}".format(300, 125))

sourcelangs = Tkinter.StringVar(root)
targetlangs = Tkinter.StringVar(root)

display_opt = {"fill": Tkconstants.BOTH, "padx": 5, "pady": 5}

Tkinter.OptionMenu(root, sourcelangs, *sorted(sourceLanguages.keys())).pack(**display_opt)

Tkinter.OptionMenu(root, targetlangs, *sorted(targetLanguages.keys())).pack(**display_opt)

Tkinter.Button(root, text="Translate", command = translate_speech).pack(**display_opt)

root.mainloop()
