from gtts import gTTS
text = input ("Enter the text you want to convert to speech: ")
tts = gTTS(text=text, lang='en')
filename = input("Enter the name of the output file (without extension): ")
tts.save (filename + ".mp3")
print("Text-to-speech conversion completed. The audio has been saved as '" + filename + ".mp3'.")