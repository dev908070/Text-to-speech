from gtts import gTTS
import pygame
import io
from datetime import datetime

def save_as_audio(input_text,file_name):
    if input_text:
        tts = gTTS(input_text)
        tts.save(str(file_name)+str(datetime.now().strftime("H%M%S"))+".mp3")

def main():
    try:
        print("Text-to-Speech Converter")
        text = input("Enter the text you want to convert to speech: ")
        save_option = input("Do you want to save the speech as an audio file? (yes/no): ")

        if save_option.lower() == 'yes':
            filename = input("Enter the filename (e.g., output.mp3): ")
            save_as_audio(text, filename)
            print(f'Saved as {filename}')
        else:
            print("Please wait we are playing the speech...\n")
            tts = gTTS(text)
            audio_file = io.BytesIO()
            tts.write_to_fp(audio_file)
            audio_file.seek(0)
            pygame.mixer.init()
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            pygame.mixer.quit()
            return "Speech Played successfully"
    except Exception as ex:
        print(str(ex))

if __name__ == "__main__":
    while True:
        main()
