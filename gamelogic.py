from kivy.properties import NumericProperty, StringProperty,  ObjectProperty
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.app import MDApp
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
import config as cfg
from custombutton import CustomButton
from functools import partial
from kivy.factory import Factory
from random import choice
from copy import deepcopy


import database_pars.udareniya as udareniya
import database_pars.slovarniye as slovarniye
import database_pars.narechiya as narechiya
import database_pars.prepri as prepri
import database_pars.n_nn as n_nn
import database_pars.isklyucheniya as isklyucheniya
import database_pars.formi as formi

def read_file(file_path):
    ds = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            
            for line in file.readlines():
                j = line.strip()[1:-1].replace("'", "").replace('"', '').split(',')
                if len(j) >= 2:
                    ds.append([j[0].strip(), j[1].strip(), j[2].strip()])
    except Exception as e:
        print("Ошибка загрузки данных:", e)
    if ds == []:
        ds = [('...', '...', '...')]
    return ds


class WordButtons(MDGridLayout):
    __events__ = ('on_update_hud',) 
    disp = StringProperty("")
    dataset = ObjectProperty(None)


    def on_dataset(self, instance, value):
        self.restart()

    def on_update_hud(self, scr, hlth, left, res):
        pass

    def restart(self, dt=0, full=True, win=False):
        if win:
            self.words = deepcopy(self.dataset)
            self.left = len(self.words)
            self.errors = 0
            self.res = ''
            self.allow_interaction = True
        elif full:
            self.words = deepcopy(self.dataset)
            self.hlth = MDApp.get_running_app().hp_value
            self.left = len(self.words)
            self.scr = 0
            self.res = ''
            self.allow_interaction = True
            self.errors = 0 

        self.wrd = choice(self.words)
        self.disp = self.wrd[0]
        self.update_buttons(self.disp)
        self.dispatch('on_update_hud', self.scr, self.hlth, self.left, self.res)

    def update_buttons(self, value):
        self.clear_widgets()
        vowels = ['а', 'я', 'е', 'э', 'о', 'ё', 'и', 'у', 'ю', 'ы']
        self.cols = len(value)
        ind = 0 if '(' not in value else value.index('(')

        for i in range(len(value)):
            btn = CustomButton(
                text=value[i],
                font_name=cfg.BF,
            )
            if value[i].lower() not in vowels:
                btn.disabled = True
            if ind != 0 and i >= ind:
                btn.disabled = True

            btn.bind(on_release=partial(self.on_button_press, index=i+1))
            self.add_widget(btn)

    def on_button_press(self, instance, index):
        if not self.allow_interaction:
            return
        
        if str(index) == self.wrd[2]:
            self.words.remove(self.wrd)
            self.scr += 1
            self.res = f"Верно - {self.wrd[1]}"
            solved_inc = 1
            error_inc = 0
        else:
            self.hlth -= 1
            self.errors += 1
            self.res = f"Неверно - {self.wrd[1]}"
            solved_inc = 0
            error_inc = 1
            if self.wrd[0] != '...':
                with open('rnotxt/Ud.txt', "r", encoding="utf-8") as file:
                    lines = file.readlines()
                    self.w = (self.wrd[0], self.wrd[1], self.wrd[2])
                if f'{self.w}\n' not in lines:
                    with open('rnotxt/Ud.txt', "a", encoding="utf-8") as file:
                        file.write(f"{self.w}\n")
                self.update_rno_screen()


        self.left = len(self.words)

        MDApp.get_running_app().update_game_stats("Udareniya", self.scr, error_inc, solved_inc)

        if self.hlth <= 0:
            self.res = "Игра окончена, Перезапуск..."
            self.dispatch('on_update_hud', self.scr, self.hlth, self.left, self.res)
            self.allow_interaction = False
            Clock.schedule_once(self.restart, 2)
        elif not self.words:
            self.res = "Победа! Ещё Разок?"
            self.dispatch('on_update_hud', self.scr, self.hlth, self.left, self.res)
            self.allow_interaction = False
            Clock.schedule_once(lambda dt: self.restart(0, False, True), 2)
        else:
            self.restart(0, False)

    def update_rno_screen(self):
        app = MDApp.get_running_app()
        if not app.root.has_screen("Ud"):
            ud_screen = Factory.Ud(name="Ud")
            app.root.add_widget(ud_screen)
        ud_screen = app.root.get_screen('Ud')
        rno_screen = ud_screen.ids.rno_screen
        rno_screen.load_data()
        rno_screen.refresh_from_data()


class BaseUdarScreen(MDScreen):
    dataset = ObjectProperty(None)
    score_value = NumericProperty(0)
    hp_value = NumericProperty(cfg.HP)
    left_value = NumericProperty(1)
    result_text = StringProperty("")
    all_words = NumericProperty(1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rest()

    def rest(self):
        self.left_value = len(self.dataset)
        self.all_words = len(self.dataset)

    def on_kv_post(self, base_widget):
        app = MDApp.get_running_app()
        self.hp_value = app.hp_value
        app.bind(hp_value=lambda instance, value: setattr(self, 'hp_value', value))

    def update_hud(self, widget, scr, hlth, left, res):
        self.score_value = scr
        self.hp_value = hlth
        self.left_value = left
        self.result_text = res

    def restart(self, dt=0, full=True):
        self.ids.word_buttons.restart(dt, full)


class BaseGameScreen(MDScreen):
    score_value = NumericProperty(0)
    hp_value = NumericProperty(cfg.HP)
    left_value = NumericProperty(1)
    result_text = StringProperty("")
    question_text = StringProperty("")
    all_words = NumericProperty(1)

    dataset = None
    file_name = None
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.restart()

    def restart(self, dt=0, full=True, win=False):
        if win:
            self.words = deepcopy(self.dataset)
            self.left = len(self.words)
            self.errors = 0
            self.res = ''
            self.allow_interaction = True
        elif full:
            self.words = deepcopy(self.dataset)
            self.scr = 0
            self.hlth = MDApp.get_running_app().hp_value
            self.left = len(self.words)
            self.res = ''
            self.allow_interaction = True
            self.all_words = len(self.dataset)
            self.errors = 0
        self.wrd = choice(self.words)
        self.quest = self.wrd[0]
        self.update_hud(self.scr, self.hlth, self.left, self.res, self.quest)

    def update_hud(self, scr, hlth, left, res, quest):
        self.score_value = scr
        self.hp_value = hlth
        self.left_value = left
        self.result_text = res
        self.question_text = quest

    def logic(self, index):
        if not self.allow_interaction:
            return
        

        if str(index) == self.wrd[2]:
            self.words.remove(self.wrd)
            self.scr += 1
            self.res = f"Верно - {self.wrd[1]}"
            solved_inc = 1
            error_inc = 0
        else:
            self.hlth -= 1
            self.errors += 1
            self.res = f"Неверно - {self.wrd[1]}"
            solved_inc = 0
            error_inc = 1

            if self.wrd[0] != '...':
                with open(self.file_name, "r", encoding="utf-8") as file:
                    lines = file.readlines()
                    self.w = (self.wrd[0], self.wrd[1], self.wrd[2])
                    
                    if index == "True" or index == "False":
                        try:
                            if self.wrd[3] != 'False':
                                self.w = (self.wrd[3], self.wrd[1].lower(), self.wrd[2])
                        except:
                            pass
                if f'{self.w}\n' not in lines:
                    with open(self.file_name, "a", encoding="utf-8") as file:
                        file.write(f"{self.w}\n")
                self.update_rno_screen()
            

        self.left = len(self.words)

        app = MDApp.get_running_app()
        mode_name = self.__class__.__name__
        app.update_game_stats(mode_name, self.scr, error_inc, solved_inc)

        if self.hlth <= 0:
            self.res = "Игра окончена, Перезапуск..."
            self.update_hud(self.scr, self.hlth, self.left, self.res, self.quest)
            self.allow_interaction = False
            Clock.schedule_once(self.restart, 2)
        elif not self.words:
            self.res = "Победа! Ещё Разок?"
            self.update_hud(self.scr, self.hlth, self.left, self.res, self.quest)
            self.allow_interaction = False
            Clock.schedule_once(lambda dt: self.restart(0, False, True), 2)
        else:
            self.restart(0, False)

    def update_rno_screen(self):
        app = MDApp.get_running_app()
        class_name = self.file_name[7:9]
        if not app.root.has_screen(class_name):
            _screen = getattr(Factory, class_name)()
            app.root.add_widget(_screen)
        _screen = app.root.get_screen(class_name)
        rno_screen = _screen.ids.rno_screen
        rno_screen.load_data()
        rno_screen.refresh_from_data()


class BaseRNOGAMEScreen(BaseGameScreen):
    file_name = None
    dataset = read_file(file_name)
    def reread(self):
        self.dataset = read_file(self.file_name)
        self.dataset = self.dataset  
        self.restart()  



#=======================GAME SCREENS====================

class Udareniya(BaseUdarScreen):
    dataset = udareniya.words
class Slovarniye(BaseGameScreen):
    dataset = slovarniye.words
    file_name = f'rnotxt/Sl.txt'
class Narechiya(BaseGameScreen):
    dataset = narechiya.words
    file_name = f'rnotxt/Na.txt'
class Prepri(BaseGameScreen):
    dataset = prepri.words
    file_name = f'rnotxt/Pr.txt'
class N_nn(BaseGameScreen):
    dataset = n_nn.words
    file_name = f'rnotxt/N_.txt'
class Isklyucheniya(BaseGameScreen):
    dataset = isklyucheniya.words
    file_name = f'rnotxt/Is.txt'
    def on_enter(self):
        self.ids.hidden_input.focus = True
    def on_leave(self):
        self.ids.hidden_input.focus = False
class Formi(BaseGameScreen):
    dataset = formi.words
    file_name = f'rnotxt/Fo.txt'


class UdDO(BaseUdarScreen):
    file_name = "rnotxt/Ud.txt"
    dataset = read_file(file_name) 
    def reread(self):
        self.dataset = read_file(self.file_name)
        self.ids.word_buttons.dataset = self.dataset  
        self.ids.word_buttons.restart()  
        self.rest()
class SlDO(BaseRNOGAMEScreen):
    file_name = "rnotxt/Sl.txt"
class NaDO(BaseRNOGAMEScreen):
    file_name = "rnotxt/Na.txt"
class PrDO(BaseRNOGAMEScreen):
    file_name = "rnotxt/Pr.txt"
class N_DO(BaseRNOGAMEScreen):
    file_name = "rnotxt/N_.txt"
class IsDO(BaseRNOGAMEScreen):
    file_name = 'rnotxt/Is.txt'
class FoDO(BaseRNOGAMEScreen):
    file_name = 'rnotxt/Fo.txt'
