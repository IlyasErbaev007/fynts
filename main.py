import webbrowser
import pyttsx3
import pyglet
import time
import random
import speech_recognition as sr
import pyautogui
import os

from pywebio.input import *
from pywebio.output import *
from pywebio.platform.flask import start_server



# ссылки
YouTube = 'https://www.youtube.com/'
Vk = 'https://vk.com/feed'
Browser = 'https://'
Telegram = 'https://web.telegram.org/k/'
Whatsapp = 'https://web.whatsapp.com/'

# Команды
commands = {
    'fynt': ('фунт', 'fynt'),
    'hi': ('привет', 'салам', 'здарова'),
    'poka': ('пока', 'до свидания', 'отключись', 'выключись'),
    'vk': (
        'открой вк', 'открой vk', 'открой вконтакте', 'vkontakte', 'открыть вк', 'открыть vk', 'вк открой' 'vk открой',),
    'Vk_mess': ('Кто ни будь что нибудь писал', 'зайди в сообщения', 'зайди в мессенджер', 'глянь сообщения'),
    'youtube': ('открой ютуб', 'ютуб открой', 'открой youtube', 'youtube открой'),
    'telegram': ('открой телеграм', 'телеграм открой', 'открой telegram', 'telegram открой'),
    'whatsapp': ('открой ватсап', 'ватсап открой', 'открой whatsapp', 'whatsapp открой'),
    'browser': ('открой браузер', 'браузер открой', 'запусти браузер'),
    'music': ('включи музыку', 'музыку включи', 'музыку вруби'),
    'Ex_youtube': ('закрой ютуб', 'ютуб закрой', 'закрой youtube', 'youtube закрой'),
    'lang': ('поменяй язык', 'поменяй раскладку', 'язык поменяй', 'раскладку поменяй', 'смени язык', 'смени раскладку',
             'язык смени', 'раскладку смени', 'сменить раскладку', 'сменить язык', 'язык сменить', 'раскладку сменить'),
    'screenshot': ('сделай скриншот', 'скриншот'),
}


def lister_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        put_text('Говорите...')
        r.pause_threshold = 0.5

        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        our_speech = r.recognize_google(audio, language='ru-RU')
        put_text('Вы сказали: ' + our_speech)
        return our_speech
    except sr.UnknownValueError:
        put_text('Не удалось распознать команду.')
    except sr.RequestError:
        put_text('Ошибка при обращении к сервису распознавания голоса.')


# Исполняет команду/
def do_this(message):
    message = message.lower()

    rand_music = ('mus/1.mp3', 'mus/yest.mp3', 'mus/yes_s.mp3')
    rand = random.choice(rand_music)

    # получаем путь к рабочему столу пользователя
    desktop_folder = os.path.expanduser("~/Desktop")

    play_sound = False  # флаг, указывающий, нужно ли воспроизводить звук
    for command, keywords in commands.items():
        for keyword in keywords:
            if keyword in message:
                if command == 'fynt':
                    mus = pyglet.resource.media('mus/yes_s.mp3')
                    mus.play()
                elif command == 'hi':
                    mus = pyglet.resource.media('mus/run.mp3')
                    mus.play()
                elif command == 'poka':
                    mus = pyglet.resource.media('mus/off.mp3')
                    mus.play()
                    time.sleep(3)
                    exit()
                elif command == 'vk':
                    play_sound = True
                    webbrowser.open(Vk)
                elif command == 'telegram':
                    play_sound = True
                    webbrowser.open(Telegram)
                elif command == 'whatsapp':
                    play_sound = True
                    webbrowser.open(Whatsapp)
                # elif command == 'Vk_mess':
                # webbrowser.open(Vk)
                elif command == 'youtube':
                    play_sound = True
                    webbrowser.open(YouTube)
                elif command == 'browser':
                    play_sound = True
                    webbrowser.open(Browser)
                elif command == 'music':
                    play_sound = True
                elif command == 'Ex_youtube':
                    pass
                elif command == 'lang':
                    pyautogui.hotkey('win', 'space')
                    play_sound = True
                elif command == 'screenshot':
                    # делаем скриншот и сохраняем на рабочий стол
                    myScreenshot = pyautogui.screenshot()
                    screenshot_path = os.path.join(desktop_folder, 'screenshot.png')
                    myScreenshot.save(screenshot_path)
                    webbrowser.open(screenshot_path)
                    play_sound = True

                    # устанавливаем флаг, что нужно воспроизвести звук

        if play_sound:
            mus = pyglet.resource.media(rand)
            mus.play()


def say_message(message):
    engine.say(message)
    engine.runAndWait()
    print(message)


engine = pyttsx3.init()
engine.setProperty('rate', 100)
engine.setProperty('volume', 1)


# Определяем функцию, которая будет запускать голосовой помощник
def voice_assistant():
    while True:
        command = lister_command()
        do_this(command)


# Запускаем сервер с помощью PyWebIO
start_server(voice_assistant, port=80, host='0.0.0.0')