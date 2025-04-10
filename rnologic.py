from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleview import RecycleView
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ObjectProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.factory import Factory

class RNO_Element(RecycleDataViewBehavior, MDBoxLayout):
    index = NumericProperty(0)
    text = StringProperty("")
    answer = StringProperty("")
    is_shown = BooleanProperty(False)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.text = data.get('text', '')
        self.answer = data.get('answer', '')
        self.is_shown = data.get('is_shown', False)
        self.update_view()
        return super(RNO_Element, self).refresh_view_attrs(rv, index, data)

    def toggle_answer(self):
        self.is_shown = not self.is_shown
        self.update_view()
        rv = self.parent.parent
        rv.data[self.index]['is_shown'] = self.is_shown

    def update_view(self):
        if self.is_shown:
            self.ids.lbl.text = self.answer
            self.ids.btn_act.icon = "eye-off"
        else:
            self.ids.lbl.text = self.text
            self.ids.btn_act.icon = "eye-outline"

    def remove_element(self):
        rv = self.parent.parent 
        if 0 <= self.index < len(rv.data):
            rv.data.pop(self.index)
            rv.refresh_from_data()
            rv.save_data()

class RNO_Screen(RecycleView):
    file_path = StringProperty("")

    def on_file_path(self, instance, value):
        self.load_data()

    def load_data(self):
        self.data = []
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
                for line in lines:
                    j = line.strip()[1:-1].replace("'", "").replace('"', '').split(',')
                    if len(j) >= 2:
                        self.data.append({
                            'text': j[0].strip(),
                            'answer': j[1].strip(),
                            'key': j[2].strip(),
                            'is_shown': False
                        })
        except Exception as e:
            print("Ошибка загрузки данных:", e)

    def save_data(self):
        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                for item in self.data:
                    file.write("('{}', '{}', '{}')\n".format(item['text'], item['answer'], item['key']))
        except Exception as e:
            print("Ошибка сохранения данных:", e)


class BaseRNOScreen(MDScreen):
    def update_do(self, do):
        MDApp.get_running_app().switch_screen(do)
        self.manager.get_screen(do).reread() 

    def clear_all(self, rno_screen):
        rno_screen.data = []
        rno_screen.save_data()
        rno_screen.refresh_from_data()


class Ud(BaseRNOScreen):
    pass
class Sl(BaseRNOScreen):
    pass
class Na(BaseRNOScreen):
    pass
class Pr(BaseRNOScreen):
    pass
class N_(BaseRNOScreen):
    pass
class Is(BaseRNOScreen):
    pass
class Fo(BaseRNOScreen):
    pass

