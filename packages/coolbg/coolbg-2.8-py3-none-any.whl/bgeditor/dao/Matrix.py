from bgeditor.dao.Summon import Summon
import random
from PIL import Image
from bgeditor.common.image_helper import ReduceOpacity
import numpy as np
from moviepy.editor import *
class Matrix:
    def __init__(self, bg_path, rate_summon, arr_summon_tempalte, duration, arr_direction, rang_locx, rang_locy, rang_speedx=[20,200], rang_speedy=[20, 200], rang_opacity=[0,800], rang_delay=[0,15], m_w=1920, m_h=1080):
        """
        :param bg_path:
        :param rate_summon:
        :param arr_summon_tempalte:
        :param duration: time of audio
        :param arr_direction:0,1,2,3,4,5,6,7 :12h,1h,3h,4h,6h,
        :param rang_locx: [x1,x2], randge of location x asis
        :param rang_locy: [y1,y2], randge of location y asis
        :param rang_speedx:[v1,v2], speed of x asis
        :param rang_speedy:[v1,v2], speed of y asis
        :param rang_opacity:[0,1000], range of opacity
        :param rang_delay:[0,duration], time appear of star
        :param m_w:1920
        :param m_h:1080
        """
        self.rate_summon= rate_summon
        self.arr_summon_tempalte= arr_summon_tempalte
        self.duration= duration
        self.n_summon = rate_summon*duration
        self.m_w = m_w
        self.m_h = m_h
        self.arr_direction= arr_direction
        self.rang_locx=rang_locx
        self.rang_locy=rang_locy
        self.rang_speedx=rang_speedx
        self.rang_speedy=rang_speedy
        self.rang_opacity=rang_opacity
        self.rang_delay=rang_delay
        self.bg_path=bg_path

    def setup_summon_template(self):
        self.list_template = {}
        for summon_template_path in self.arr_summon_tempalte:
            template_a = Image.open(summon_template_path).convert('RGBA')
            self.list_template[summon_template_path] = template_a
    def setup(self):
        try:
            self.list_summon = []
            self.setup_summon_template()
            self.img_bg = Image.open(self.bg_path)
            for i in range(self.n_summon):
                summon = {}
                summon['template'] = random.choice(self.arr_summon_tempalte)
                summon['skill'] = self.list_template[summon['template']]
                s_w, s_h = summon['skill'].size
                summon['algorithm'] = Summon.setup(self.arr_direction, self.rang_locx, self.rang_locy, self.rang_speedx,
                                                   self.rang_speedy, self.rang_opacity, self.rang_delay, s_w, s_h, self.m_w, self.m_h)
                self.list_summon.append(summon)
            return True
        except:
            pass
        return False

    def make_frame(self,t):
        img_tmp = self.img_bg.copy()
        for summon in self.list_summon:
            x, y = summon['algorithm'].move(t)
            if x and y:
                img_rd = ReduceOpacity(summon['skill'], summon['algorithm'].opacity)
                img_tmp.paste(img_rd, (int(x), int(y)), img_rd)
        return np.asarray(img_tmp)
    def make(self):
        return VideoClip(self.make_frame, duration = self.duration)






