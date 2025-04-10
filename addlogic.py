from kivy.uix.recycleview import RecycleView
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivymd.app import MDApp
from kivy.properties import NumericProperty, StringProperty


class BaseAdd(MDScreen):
    pass

class BaseAddScreen(BaseAdd):
    name_screen = ""
    def update_add_screen(self):
        app = MDApp.get_running_app()
        _add_screen = app.root.get_screen(self.name_screen)
        add_screen = _add_screen.ids.add_screen
        add_screen.load_data()
        add_screen.refresh_from_data()
        app.update_switch(app.switch_active)
    
    def clear_all(self, add_screen):
        app = MDApp.get_running_app()
        add_screen.data = []
        add_screen.save_data()
        add_screen.refresh_from_data()
        app.update_switch(False)
        app.update_switch(app.switch_active)

class Add_Element(RecycleDataViewBehavior, MDBoxLayout):
    index = NumericProperty(0)
    display_text = StringProperty("")  
    original_text = StringProperty("") 

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.original_text = data.get('text', '')  
        self.display_text = self.original_text.replace("_", " ").replace("/", "").replace('#', ' # ')   # Изменённый текст
        return super().refresh_view_attrs(rv, index, data)
    
    def remove_element(self):
        rv = self.parent.parent 
        app = MDApp.get_running_app()
        if 0 <= self.index < len(rv.data):
            rv.data.pop(self.index)
            rv.refresh_from_data()
            rv.save_data()
            app.update_switch(False)
            app.update_switch(app.switch_active)

class Add_Screen(RecycleView):
    file_path = StringProperty("")

    def on_file_path(self, instance, value):
        self.load_data()

    def load_data(self):
        self.data = []
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
                for line in lines:
                    if len(line) >= 2:
                        self.data.append({
                            'text': line.strip(),
                        })
        except Exception as e:
            print("Ошибка загрузки данных:", e)

    def save_data(self):
        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                for item in self.data:
                    file.write(item['text'] + "\n")
        except Exception as e:
            print("Ошибка сохранения данных:", e)


class Add_ud(BaseAddScreen):
    name_screen = "Add_ud"
    def enter(self):
        text_field = self.ids.text_add
        alph = "йцукенгшщзхъфывапролджэячсмитьбюёАУОИЭЫЯЮЕЁ- ()"
        with open(self.fp, "r", encoding="utf-8") as file:
            lines = file.readlines()
            if f'{text_field.text}\n' not in lines:
                flag_gen = True
                c = 0
                for i in text_field.text:
                    if i in alph:
                        if i.upper() == i and i not in "()- ": c += 1
                    else:
                        flag_gen = False 
                if c == 1 and flag_gen:
                    text_field.error = False
                    with open(self.fp, "a", encoding="utf-8") as file:  
                        file.write(f"{text_field.text}\n") 
                else:
                    text_field.error = True
            self.update_add_screen()
    
class Add_sl_sl(BaseAddScreen):
    name_screen = "Add_sl_sl"
    def enter(self):
        text_field = self.ids.text_add
        alph = "йцукенгшщзхъфывапролджэячсмитьбюё- ()"
        with open(self.fp, "r", encoding="utf-8") as file:
            lines = file.readlines()
            if f'{text_field.text}\n' not in lines:
                flag_gen = True
                for i in text_field.text:
                    if i not in alph:
                        flag_gen = False
                if flag_gen and text_field.text:
                    text_field.error = False
                    with open(self.fp, "a", encoding="utf-8") as file:  
                        file.write(f"{text_field.text}\n") 
                else:
                    text_field.error = True
            self.update_add_screen()

class Add_nar(BaseAddScreen):
    name_screen = "Add_nar"
    def enter(self):
        text_field = self.ids.text_add
        alph = "йцукенгшщзхъфывапролджэячсмитьбюё/_ -()"
        with open(self.fp, "r", encoding="utf-8") as file:
            lines = file.readlines()
            if f'{text_field.text}\n' not in lines:
                flag_letter = True
                for i in text_field.text:
                    if i not in alph\
                        or (text_field.text.count('/')==0 \
                        and text_field.text.count('_')==0)\
                        or (text_field.text.count('/')>=1 \
                        and text_field.text.count('_')>=1)\
                        or text_field.text.strip()[0] in "/_"\
                        or text_field.text.strip()[-1] in "/_":
                        flag_letter = False
                if flag_letter:
                    text_field.error = False
                    with open(self.fp, "a", encoding="utf-8") as file:  
                        file.write(f"{text_field.text }\n") 
                else:
                    text_field.error = True
            self.update_add_screen()

class Add_iskl(BaseAddScreen):
    name_screen = "Add_iskl"
    def enter(self):
        text_field = self.ids.text_add
        alph = "йцукенгшщзхъфывапролджэячсмитьбюёЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮЁ- ()"
        with open(self.fp, "r", encoding="utf-8") as file:
            lines = file.readlines()
            if f'{text_field.text}\n' not in lines:
                flag_gen = True
                c = 0
                for i in text_field.text:
                    if i in alph:
                        if i.upper() == i and i not in "()- ": c += 1
                    else:
                        flag_gen = False
                if c == 1 and flag_gen:
                    text_field.error = False
                    with open(self.fp, "a", encoding="utf-8") as file:  
                        file.write(f"{text_field.text}\n") 
                else:
                    text_field.error = True
            self.update_add_screen()

class Add_pre_pri(BaseAddScreen):
    name_screen = "Add_pre_pri"
    def enter(self):
        text_field = self.ids.text_add
        alph = "йцукенгшщзхъфывапролджэячсмитьбюё- ()"
        with open(self.fp, "r", encoding="utf-8") as file:
            lines = file.readlines()
            if f'{text_field.text}\n' not in lines:
                flag_gen = True
                for i in text_field.text:
                    if i not in alph: flag_gen = False
                if flag_gen and (text_field.text.count("пре")\
                    or text_field.text.count("при")):
                    text_field.error = False
                    with open(self.fp, "a", encoding="utf-8") as file:  
                        file.write(f"{text_field.text}\n") 
                else:
                    text_field.error = True
            self.update_add_screen()

class Add_n_nn(BaseAddScreen):
    name_screen = "Add_n_nn"
    def enter(self):                                 
        text_field = self.ids.text_add
        alph = "йцукенгшщзхъфывапролджэячсмитьбюёН- ()"
        with open(self.fp, "r", encoding="utf-8") as file:
            lines = file.readlines()
            flag_gen = True
            if f'{text_field.text}\n' not in lines:
                for i in text_field.text:
                    if i not in alph: flag_gen = False
                if flag_gen and (text_field.text.count("Н") == 1 or text_field.text.count("НН") == 1) and self.ids.text_add.text.count("Н") != 3:
                    text_field.error = False
                    with open(self.fp, "a", encoding="utf-8") as file:  
                        file.write(f"{text_field.text}\n") 
                else:
                    text_field.error = True
            self.update_add_screen()

class Add_form(BaseAddScreen):
    name_screen = "Add_form"
    def enter(self):
        text_field = self.ids.text_add
        alph = "йцукенгшщзхъфывапролджэячсмитьбюё#- ()"
        with open(self.fp, "r", encoding="utf-8") as file:
            lines = file.readlines()
            if f'{text_field.text}\n' not in lines:
                flag_gen = True
                for i in text_field.text:
                    if i not in alph\
                    or text_field.text.count("#") != 1\
                    or text_field.text.strip()[0] == "#"\
                    or text_field.text.strip()[-1] == "#":
                        flag_gen = False
                if flag_gen and text_field.text:
                    text_field.error = False
                    with open(self.fp, "a", encoding="utf-8") as file:  
                        file.write(f"{text_field.text}\n") 
                else:
                    text_field.error = True
            self.update_add_screen()
