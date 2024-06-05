from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.conf import settings
from moviepy.editor import *
from .models import Ticker
from django.template import loader
import os

def make_ticker (text, 
                 text_color = "White", 
                 fontsize = 70, 
                 bg_size_x = 100, 
                 bg_size_y = 100, 
                 bg_color = [0, 0, 0], 
                 duration = 3):

    file_name = str(settings.BASE_DIR) + "/creeping/generatedvideos/" + text + ".mp4"
                     
    txt_clip = TextClip(text, color=text_color, fontsize=fontsize)
    bg_clip = ColorClip(size=(bg_size_x, bg_size_y), color=bg_color)

    txt_move = txt_clip.set_position(lambda t: (bg_size_x - (((txt_clip.w + bg_size_x) / duration) * t), "top"))

    video = CompositeVideoClip([bg_clip, txt_move]).set_duration(duration)
    video.write_videofile(file_name, fps=24, codec="mpeg4")
    return file_name

def index(request):
        
    page = loader.get_template("index.html")

    return HttpResponse(
        page.render({}, request)
    )

def send(response, text):
    video = open(make_ticker(text), "rb")
    response = FileResponse(video)
    response["Content-Disposition"] = "attachment; filename=" + text + ".mp4"

    Ticker.objects.create(video=text)

    return response