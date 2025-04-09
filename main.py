import database_pars.udareniya as udareniya
import database_pars.slovarniye as slovarniye
import database_pars.narechiya as narechiya
import database_pars.prepri as prepri
import database_pars.n_nn as n_nn
import database_pars.isklyucheniya as isklyucheniya
import database_pars.formi as formi
import config as cfg


from kivy.clock import Clock
from kivy.properties import NumericProperty, BooleanProperty
from kivy.storage.jsonstore import JsonStore
from kivy.core.window import Window
#Window.size = (cfg.W, cfg.H)

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen



#=========================MENU SCREENS======================
class Mainmenu(MDScreen):
    pass
class Playmenu(MDScreen):
    pass
class Optionsmenu(MDScreen):
    pass



class Myapp(MDApp):
    hp_value = NumericProperty(cfg.HP)
    switch_active = BooleanProperty(False) 
    best_udareniya = NumericProperty(0)
    best_slovarniye = NumericProperty(0)
    best_narechiya = NumericProperty(0)
    best_prepri = NumericProperty(0)
    best_n_nn = NumericProperty(0)
    best_isklyucheniya = NumericProperty(0)
    best_formi = NumericProperty(0)
    total_errors = NumericProperty(0)
    total_solved = NumericProperty(0)
    _update_hp_clock = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.store = JsonStore('settings.json')
        if self.store.exists('user_settings'):
            settings = self.store.get('user_settings')
            self.hp_value = settings.get('hp', cfg.HP)
            self.theme_cls.theme_style = settings.get('theme', "Dark")
            self._initial_switch = settings.get('switch', False)
        else:
            self.hp_value = cfg.HP
            self.theme_cls.theme_style = "Dark"
            self._initial_switch = False


        if self.store.exists('game_stats'):
            stats = self.store.get('game_stats')
            self.best_udareniya    = stats.get('Udareniya', 0)
            self.best_slovarniye    = stats.get('Slovarniye', 0)
            self.best_narechiya     = stats.get('Narechiya', 0)
            self.best_prepri        = stats.get('Prepri', 0)
            self.best_n_nn          = stats.get('N_nn', 0)
            self.best_isklyucheniya = stats.get('Isklyucheniya', 0)
            self.best_formi         = stats.get('Formi', 0)
            self.total_errors       = stats.get('total_errors', 0)
            self.total_solved       = stats.get('total_solved', 0)
        else:
            self.store.put('game_stats',
                           Udareniya=0,
                           Slovarniye=0,
                           Narechiya=0,
                           Prepri=0,
                           N_nn=0,
                           Isklyucheniya=0,
                           Formi=0,
                           total_errors=0,
                           total_solved=0)
            
    def on_start(self):
        self.switch_active = self._initial_switch

    def update_settings(self):

        self.store.put('user_settings', hp=self.hp_value,
                       theme=self.theme_cls.theme_style,
                       switch=self.switch_active)

    def update_switch(self, value):
        if value:
    
            for obj, new_words in (
                (udareniya, udareniya.ud_pars('addtxt/Add_ud.txt')),
                (slovarniye, slovarniye.sl_pars('addtxt/Add_sl_sl.txt')),
                (narechiya, narechiya.na_pars('addtxt/Add_nar.txt')),
                (prepri, prepri.pr_pars('addtxt/Add_pre_pri.txt')),
                (n_nn, n_nn.n__pars('addtxt/Add_n_nn.txt')),
                (isklyucheniya, isklyucheniya.is_pars('addtxt/Add_iskl.txt')),
                (formi, formi.fo_pars('addtxt/Add_form.txt'))
            ):
                new_words_to_add = [word for word in new_words if word not in obj.words]
                obj.words.extend(new_words_to_add)
        else:
            for obj in (udareniya, slovarniye, narechiya, prepri, n_nn, isklyucheniya, formi):
                obj.words.clear()
                obj.words.extend(obj.copywords)

        self.update_settings()
        for screen in self.root.screens:
            if hasattr(screen, 'restart'):
                screen.restart(0, True)

    def on_switch_active(self, instance, value):
        if not self.root:
            Clock.schedule_once(lambda dt: self.update_switch(value), 0)
        else:
            self.update_switch(value)

    def schedule_update_hp_all(self, new_hp):
        if self._update_hp_clock is not None:
            self._update_hp_clock.cancel()
        self._update_hp_clock = Clock.schedule_once(lambda dt: self.update_hp_all(new_hp), 0.5)

    def update_hp_all(self, new_hp):
        cfg.HP = int(new_hp)
        self.hp_value = int(new_hp)
        self.update_settings()
        for screen in self.root.screens:
            if hasattr(screen, 'restart'):
                screen.restart(0, True)

    def change_theme(self):
        if self.theme_cls.theme_style == "Light":
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"
        self.update_settings()

    def restart_game(self):
        current_screen = self.root.current_screen
        if hasattr(current_screen, 'restart'):
            current_screen.restart(0, True)

    def on_keyboard(self, window, key, scancode, codepoint, modifier):
        if key == 27:
            if self.root.current in ["Playmenu",
                                      "Optionsmenu",
                                      "Add_ud",
                                      "Add_sl_sl",
                                        "Add_nar",
                                        "Add_pre_pri",
                                        "Add_n_nn",
                                        "Add_iskl",
                                        "Add_form",
                                      ]:
                self.root.current = "Mainmenu"
            elif self.root.current in ["Udareniya",
                                        "Slovarniye",
                                        "Narechiya",
                                        "Prepri", 
                                        "N_nn", 
                                        "Isklyucheniya", 
                                        'Formi',
                                        "Ud", 
                                        "Sl", 
                                        "Na", 
                                        "Pr", 
                                        "N_", 
                                        "Is",
                                        "Fo",
                                        ]:
                self.root.current = "Playmenu"
            elif self.root.current in "UdDO":
                self.root.current = 'Ud'
            elif self.root.current in "SlDO":
                self.root.current = 'Sl'
            elif self.root.current in "NaDO":
                self.root.current = 'Na'
            elif self.root.current in "PrDO":
                self.root.current = 'Pr'
            elif self.root.current in "N_DO":
                self.root.current = 'N_'
            elif self.root.current in "IsDO":
                self.root.current = 'Is'
            elif self.root.current in "FoDO":
                self.root.current = 'Fo'
            else:
                self.stop()
            return True
        return False

    def update_game_stats(self, mode: str, current_score: float, error_inc: int, solved_inc: float):
        current_best = getattr(self, f'best_{mode.lower()}', 0)
        if current_score > current_best:
            setattr(self, f'best_{mode.lower()}', int(current_score))
        self.total_errors += error_inc
        self.total_solved += int(solved_inc)
        self.store.put('game_stats',
                       Udareniya=self.best_udareniya,
                       Slovarniye=self.best_slovarniye,
                       Narechiya=self.best_narechiya,
                       Prepri=self.best_prepri,
                       N_nn=self.best_n_nn,
                       Isklyucheniya=self.best_isklyucheniya,
                       Formi=self.best_formi,
                       total_errors=self.total_errors,
                       total_solved=self.total_solved)

    def build(self):
        self.theme_cls.theme_style = self.theme_cls.theme_style
        self.theme_cls.primary_palette = "BlueGray"
        Clock.schedule_once(lambda dt: Window.bind(on_keyboard=self.on_keyboard))
        return super().build()


if __name__ == '__main__':
    Myapp().run()   