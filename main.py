from __future__ import unicode_literals
import gi
import youtube_dl
import sys
from kivy.config import Config
from kivy.uix.progressbar import ProgressBar
from youtube_dl import DownloadError
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '450')
Config.set('graphics', 'height', '600')
gi.require_version('Gtk', '3.0')
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager,Screen

from kivy.uix.boxlayout import BoxLayout
Window.clearcolor = (140/255.0, 175/255.0, 255/255.0, 1)

button_group = []
check = None

class MyLogger(object):

    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        pass


def my_hook(d):
    if d['status'] == 'downloading':
        print(d['filename'])
        print(d['speed'])
        print(d['downloaded_bytes'])
        print(d['eta'])
    if d['status'] == 'finished':
        print(d['status'])
        print('Done downloading, now converting ...')

ydl_opts = {'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'logger': MyLogger(),
            'progress_hooks': [my_hook], }


class ScreenManagement(ScreenManager):

    def p(self):
        pass


class FirstScreen(Screen):

    def insert(self, text):
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                a = ydl.extract_info(text, download=False)
                title = "TITLE : "
                title += a.get('title')
                title = title[:66]+'\n             '+title[66:]
                print(a)
                formats = a.get('formats', [a])
                table = [
                    [f['format_id'], f['ext'], ydl.format_resolution(f), ydl._format_note(f)]
                    for f in formats
                    if f.get('preference') is None or f['preference'] >= -1000]
                global button_group
                button_group = []
                self.manager.ids.secondd.ids.title.text=title
            for t in table:
                alone_button = Button(text=" (" + t[0] + ")  " + t[1] + "  " + t[2], height=150,
                       background_color=(27 / 255.0, 75 / 255.0, 199 / 255.0, 1)
                       , on_press=self.action)
                button_group.append(alone_button)
                self.manager.ids.secondd.ids.grid.height += 50
                self.manager.ids.secondd.ids.grid.add_widget(alone_button)
                self.manager.transition.direction = 'left'
                self.manager.current = 'second'
        except DownloadError as e:
            msg = str(e)
            error_msg = None
            if (msg.endswith('YouTube')):
                msg = "please enter the valid url."
                error_msg = "You have entered an invalid url"
            elif (msg.endswith('truncated.')):
                msg = "url looks truncated."
            else:
                msg = "unable to reach webpage or invalid url."

            self.ids.page1input.text= ""
            self.ids.page1input.text= msg
            self.manager.current = 'first'

    def action(self,args):
        global check
        if check == None:
            check = args
            check.background_color=(1,0,1,1)
        elif check != args:
            check.background_color=(27 / 255.0, 75 / 255.0, 199 / 255.0, 1)
            check=args
            check.background_color=(1,0,1,1)

        global blabla
        blabla = check.text.find(')')
        blabla = check.text[2:blabla]
        # print(blabla)  // this is used to show the code


class SecondScreen(Screen):
    def down(self):
        # print blabla    used to show code
        # youtube_dl.main(['-f',blabla,self.ids.url.text])
        # self.manager.transition.direction = 'left'
        # self.manager.current = 'third'
        ydl_opts = {
            'format': str(blabla),

            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],

            'logger': MyLogger(),
            'progress_hooks': [self.manager.ids.thirdd.my_hook],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.ids.url.text])
    def back(self):
        for b in button_group:
            self.manager.ids.secondd.ids.grid.height -= 50
            self.ids.grid.remove_widget(b)

    def move(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'third'


class ThirdScreen(Screen):
    val = ""
    @staticmethod
    def my_hook(d):
        if d['status'] == 'downloading':
            print(d['filename'])
            print(d['speed'])
            val = d['downloaded_bytes']
            print(d['eta'])
        if d['status'] == 'finished':
            print(d['status'])
            print('Done downloadisldjfsdlfjng, now converting ...')


class DownloaderApp(App):

    def build(self):
        self.load_kv('main.kv')

        return ScreenManagement()

def onee():
    pass
sys.stderr.isatty=onee


if __name__ == "__main__":

    DownloaderApp().run()

