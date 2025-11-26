import tempfile
import os
import moviepy.editor as mp
from pytube import YouTube
from fastapi import HTTPException
from deep_translator import GoogleTranslator
from openai import OpenAI

client = OpenAI()

def download_youtube_audio(url):
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    temp_audio = tempfile.mktemp(suffix=".mp4")
    audio_stream.download(filename=temp_audio)
    return temp_audio

def transcribe_audio(file_path):
    with open(file_path, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=f
        )
    return transcript.text

def translate_text(text, target_lang):
    return GoogleTranslator(target=target_lang).translate(text)

def generate_dubbed_audio(text, emotion):
    speech = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text,
        emotion=emotion,
        format="mp3"
    )
    temp_audio = tempfile.mktemp(suffix=".mp3")
    with open(temp_audio, "wb") as f:
        f.write(speech.read())
    return temp_audio

def merge_audio_with_video(video_url, audio_file):
    yt = YouTube(video_url)
    stream = yt.streams.get_highest_resolution()
    temp_video = tempfile.mktemp(suffix=".mp4")
    stream.download(filename=temp_video)

    video = mp.VideoFileClip(temp_video)
    audio = mp.AudioFileClip(audio_file)
    final = video.set_audio(audio)

    output = tempfile.mktemp(suffix=".mp4")
    final.write_videofile(output, codec="libx264", audio_codec="aac")

    return output
