from kivy.app import App
from kivy.uix.label import Label
from kivy.core.text import Label as CoreLabel
from kivy.properties import NumericProperty, BooleanProperty
from kivy.clock import Clock
from kivymd.uix.label import MDLabel
import config as cfg
from kivy.metrics import dp


class AutoFontLabel(MDLabel):
    max_font_size = NumericProperty(dp(50))  
    min_font_size = NumericProperty(dp(5))   
    padding_x = NumericProperty(dp(10))      
    center_text = BooleanProperty(True)  

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = cfg.BF
        self.bind(
            text=self.update_font_size,
            size=self.update_font_size,
            font_name=self.update_font_size
        )
        Clock.schedule_once(self.update_font_size)  # Первоначальный расчёт

    def update_font_size(self, *args):
        if not self.text or not self.width:
            return

        target_width = self.width - 2 * self.padding_x
        low = self.min_font_size
        high = self.max_font_size
        best_size = low

        for _ in range(8):  
            mid = (low + high) / 2
            core_label = CoreLabel(
                text=self.text,
                font_size=mid,
                font_name=self.font_name
            )
            core_label.refresh()
            text_width = core_label.texture.width

            if text_width <= target_width:
                best_size = mid
                low = mid
            else:
                high = mid

        self.font_size = best_size
        self.halign = 'center'
        if self.center_text:
            self.text_size = (self.width, None)
            self.valign = 'middle'
        else:
            self.text_size = (self.width, self.height)
            self.valign = 'top'
            self.font_name = cfg.SF
            self.theme_text_color = "Secondary"