from kivy.properties import ListProperty
from kivy.uix.button import Button
from kivy.animation import Animation
from kivymd.app import MDApp

class CustomButton(Button):
    pulse_color = ListProperty([0, 0, 0, 0])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.update_font_size)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = [0, 0, 0, 0]
        self.bind(pulse_color=self._update_canvas)
        self._update_canvas()
        self.disabled_color = [0.5, 0.5, 0.5, 0.8]

        app = MDApp.get_running_app()
        if app.theme_cls.theme_style == "Dark":
            self.color = [1, 1, 1, 1]  # белый текст для темной темы
        else:
            self.color = [0, 0, 0, 1]  # черный текст для светлой темы

        # Если нужно обновлять цвет динамически при смене темы,
        # можно подписаться на изменение свойства theme_style:
        app.theme_cls.bind(theme_style=lambda instance, value: self.update_text_color())

    def update_font_size(self, *args):
        self.font_size = min(self.width*1.25, self.height*1.25)

    def update_text_color(self):
        app = MDApp.get_running_app()
        if app.theme_cls.theme_style == "Dark":
            self.color = [1, 1, 1, 1]
        else:
            self.color = [0, 0, 0, 1]

    def _update_canvas(self, *args):
        self.canvas.before.clear()
        if any(self.pulse_color):
            with self.canvas.before:
                from kivy.graphics import Color, Rectangle
                Color(rgba=self.pulse_color)
                Rectangle(pos=self.pos, size=self.size)

    def on_press(self):
        anim = Animation(pulse_color=[0.5, 0.5, 0.5, 0.5], duration=0.2)
        anim.start(self)
        return super().on_press()

    def on_release(self):
        anim = Animation(pulse_color=[0, 0, 0, 0], duration=0.2)
        anim.start(self)
        return super().on_release()

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            self.on_release()
        else:
            anim = Animation(pulse_color=[0, 0, 0, 0], duration=0.2)
            anim.start(self)
        return super().on_touch_up(touch)