from moviepy.editor import *
from bgeditor.common.image_helper import create_virgin_layer
from bgeditor.common.utils import *
import os, json, textwrap, requests
os.environ["IMAGEMAGICK_BINARY"] = "magick"

class Lyric:

    def __init__(self, lyric_json, font_url, font_size, color, duration, stroke_color, stroke_width, bg_color, w=1920, h=1080):
        self.lyric_json = lyric_json
        self.lyric_data = json.loads(self.lyric_json)
        self.font_url = font_url
        self.font_path=None
        self.font_size = font_size
        self.duration = duration
        self.color = color
        self.w = w # width of group textbox
        self.h = h # high of group textbox
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width
        self.bg_color=bg_color
    def init(self):
        self.font_path = cache_file(self.font_url)
        if self.font_path is None:
            return False
        self.normalnize()
        return True
    def optimize_font(self):
        wrapper = textwrap.TextWrapper(width=30)
        for lyric in self.lyric_data:
            lyric['line'] = wrapper.fill(text=lyric['line'])
        data_post = {}
        data_post['w'] = self.w
        data_post['font_url'] = self.font_url
        data_post['json_lyric'] = json.dumps(self.lyric_data)
        data_post['font_size_want'] = self.font_size
        font_size_tmp = requests.post("http://db.automusic.win/music/lyric/font", json = data_post).text
        if font_size_tmp.isdigit():
            self.font_size = int(font_size_tmp)
            return True
        return False

    def normalnize(self):
        lyric_data_normal = []
        for lyric in self.lyric_data:
            try:
                if 'milliseconds' in lyric and 'line' in lyric and int(lyric['milliseconds']) >= 0 and lyric['line'] is not None:
                    lyric_data_normal.append(lyric)
            except:
                pass
        self.lyric_data=lyric_data_normal


    def make(self):
        arr_composite = []
        last_time = 0
        i = 0
        max_h = 0
        for lyric in self.lyric_data:
            txt = TextClip(lyric['line'], font=self.font_path, color=self.color, fontsize=self.font_size,
                           bg_color=self.bg_color, stroke_color=self.stroke_color, stroke_width=self.stroke_width)
            start_time = int(lyric['milliseconds']) / 1000
            if i < len(self.lyric_data) - 1:
                end_time = int(self.lyric_data[i + 1]['milliseconds']) / 1000
            else:
                end_time = start_time + 5
            w_txt, h_txt = txt.size
            end_time += 0.4 #stay 1s
            if i % 2 == 0:
                last_h = h_txt
            else:
                if max_h < last_h + h_txt:
                    max_h = last_h + h_txt
            arr_composite.append(
                txt.set_position(("center", int((i % 2) * last_h))).set_duration(end_time - start_time).set_start(
                    start_time).crossfadein(0.4).crossfadeout(0.4))
            last_time = end_time
            txt.close()
            i += 1
        if last_time < self.duration:
            txt = TextClip("...", font=self.font_path, color=self.color, fontsize=self.font_size,
                           bg_color=self.bg_color, stroke_color=self.stroke_color, stroke_width=self.stroke_width)
            arr_composite.append(
                txt.set_position("center").set_duration(self.duration - last_time).set_start(
                    last_time).crossfadein(0.4).crossfadeout(0.4))
            txt.close()
        print('create vigrin with maxh : '+str(max_h))
        arr_composite.insert(0, ImageClip(create_virgin_layer(self.w, max_h))) #auto high of textlyric
        return CompositeVideoClip(arr_composite)



