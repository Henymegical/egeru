import os
import json
import uuid
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleview import RecycleView
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivy.network.urlrequest import UrlRequest

SETTINGS_PATH = os.path.join(os.getcwd(), 'settings.json')
STORE_PATH = os.path.join(os.getcwd(), 'user_store.json')
USERS_PATH = os.path.join(os.getcwd(), 'users.json')
API_URL = "https://test-repo-59eu.onrender.com/users/"
maxlen = 13
maxtop = 99

rv_numeric_props = {
    'stat_1','stat_2','stat_3','stat_4','stat_5','stat_6','stat_7','mistakes','solved'
}


def load_local_stats():
    try:
        data = json.load(open(SETTINGS_PATH, 'r', encoding='utf-8'))
        game = data.get('game_stats', {})
    except Exception:
        game = {}
    mapping = {
        'Udareniya':'stat_1','Slovarniye':'stat_2','Narechiya':'stat_3',
        'Prepri':'stat_4','N_nn':'stat_5','Isklyucheniya':'stat_6','Formi':'stat_7',
        'total_errors':'mistakes','total_solved':'solved'
    }
    return {sv: game.get(local, 0) for local, sv in mapping.items()}

class API:
    @staticmethod
    def fetch_users(success, failure):
        UrlRequest(
            API_URL,
            on_success=lambda req, res: success(res),
            on_error=lambda req, err: failure(err),
            on_failure=lambda req, res: failure(res),
            chunk_size=8192
        )

    @staticmethod
    def update_user(user_id, data, success, failure):
        UrlRequest(
            f"{API_URL}{user_id}",
            req_body=json.dumps(data),
            method='PUT',
            req_headers={'Content-Type': 'application/json'},
            on_success=lambda req, res: success(res),
            on_error=lambda req, err: failure(err),
            on_failure=lambda req, res: failure(res)
        )

    @staticmethod
    def create_user(payload, success, failure):
        UrlRequest(
            API_URL,
            req_body=json.dumps(payload),
            method='POST',
            req_headers={'Content-Type': 'application/json'},
            on_success=lambda req, res: success(res),
            on_error=lambda req, err: failure(err),
            on_failure=lambda req, res: failure(res)
        )

class LB_Element(RecycleDataViewBehavior, BoxLayout):
    index = NumericProperty(-1)
    username = StringProperty("")
    stat_1 = NumericProperty(0)
    stat_2 = NumericProperty(0)
    stat_3 = NumericProperty(0)
    stat_4 = NumericProperty(0)
    stat_5 = NumericProperty(0)
    stat_6 = NumericProperty(0)
    stat_7 = NumericProperty(0)
    mistakes = NumericProperty(0)
    solved = NumericProperty(0)
    created_at = StringProperty("")
    updated_at = StringProperty("")

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        for prop in ('username','created_at','updated_at'):
            setattr(self, prop, data.get(prop, ""))
        for prop in rv_numeric_props:
            setattr(self, prop, data.get(prop, 0))
        return super().refresh_view_attrs(rv, index, data)

class LB_Screen(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(lambda dt: self.load_and_render(), 0)
        self._users_cache = []

    def load_and_render(self):
        def success(users):
            with open(USERS_PATH,'w',encoding='utf-8') as f:
                json.dump(users, f, ensure_ascii=False, indent=4)
            self._users_cache = users
            self._update_view()

        def failure(err):
            if os.path.exists(USERS_PATH):
                self._users_cache = json.load(open(USERS_PATH,'r',encoding='utf-8'))
            self._update_view()

        API.fetch_users(success, failure)

    def _update_view(self):
        sorted_users = sorted(self._users_cache, key=lambda u: u.get('solved',0), reverse=True)
        display_users = sorted_users[:maxtop]
        self.data = [
            {**{k: u.get(k, 0) for k in rv_numeric_props},
                'username':   u.get('username', ''),
                'created_at': u.get('created_at', ''),
                'updated_at': u.get('updated_at', '')}
            for u in display_users
        ]
        super().refresh_from_data()

    def save_data_locally(self):
        with open(USERS_PATH,'w',encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

class Leaderboard(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None
        self._asked = False
        self.stats = load_local_stats()

    def upd_sc_fix(self):
        self.update_screen()
        Clock.schedule_once(lambda dt: self.update_screen(), 1.5)

    def on_pre_enter(self):
        if not self._asked:
            self._asked = True
            Clock.schedule_once(lambda dt: self.check_user(), 0)
        self.upd_sc_fix()

    def check_user(self):
        store = JsonStore(STORE_PATH)
        def on_fetch(users):
            user_exists = store.exists('user') and any(
                u['id']==store.get('user')['id'] and u['username']==store.get('user')['username']
                for u in users
            )
            if not user_exists:
                if store.exists('user'):
                    os.remove(STORE_PATH)
                self.show_nickname_dialog()
            else:
                self.update_user_and_board()

        def on_fail(err):
            self.show_nickname_dialog()

        API.fetch_users(on_fetch, on_fail)

    def update_user_and_board(self):
        store = JsonStore(STORE_PATH)
        if store.exists('user') and any(self.stats.values()):
            def on_upd(_):
                self.ids.lb_screen._update_view()
            def on_err(_): pass
            API.update_user(store.get('user')['id'], self.stats, on_upd, on_err)

    def show_nickname_dialog(self):
        self.nickname_field = MDTextField(hint_text="Введите ваш никнейм", max_text_length=maxlen)
        self.dialog = MDDialog(
            title="Регистрация пользователя", type="custom", content_cls=self.nickname_field,
            buttons=[
                MDFlatButton(text="ОТМЕНА", on_release=lambda *a: self.dialog.dismiss()),
                MDFlatButton(text="OK", on_release=lambda *a: self.create_user())
            ]
        )
        self.dialog.open()

    def create_user(self):
        if JsonStore(STORE_PATH).exists('user'):
            self.nickname_field.error = True
            self.nickname_field.helper_text = "Сетевая ошибка"
            self.nickname_field.helper_text_mode = "on_error"
            return
        self.nickname_field.error = False
        username = self.nickname_field.text.strip()
        if not username or len(username)>maxlen or any(
            c.lower() not in set("1234567890йцукенгшщзхъфывапролджэячсмитьбюёabcdefghijklmnopqrstuvwxyz- ()")
            for c in username
        ):
            self.nickname_field.error = True
            self.nickname_field.helper_text = "Недопустимый никнейм"
            self.nickname_field.helper_text_mode = "on_error"
            return
        payload = {'username': username, **self.stats}
        def on_fetch(users):
            existing_ids = {u['id'] for u in users}
            new_id = str(uuid.uuid4())
            while new_id in existing_ids:
                new_id = str(uuid.uuid4())
            payload['id'] = new_id
            API.create_user(payload, on_create, on_err)
        def on_err(err):
            self.nickname_field.error = True
            self.nickname_field.helper_text = "Сетевая ошибка"
            self.nickname_field.helper_text_mode = "on_error"
        def on_create(user):
            if 'id' not in user:
                self.nickname_field.error = True
                self.nickname_field.helper_text = "Никнейм уже занят"
                self.nickname_field.helper_text_mode = "on_error"
                return
            JsonStore(STORE_PATH).put('user', id=user['id'], username=user['username'], **self.stats)
            self.update_user_and_board()
            self.dialog.dismiss()
            self.upd_sc_fix()
        API.fetch_users(on_fetch, on_err)

    def update_screen(self):
        self.stats = load_local_stats()
        store = JsonStore(STORE_PATH)
        if not store.exists('user'):
            self._asked = False
        else:
            self.update_user_and_board()
            user_data = self.get_user_data()
            if user_data:
                self.ids.user_row.refresh_view_attrs(None, 0, user_data)
        Clock.schedule_once(lambda dt: self.ids.lb_screen.load_and_render(), 0)

    def get_user_data(self):
        store = JsonStore(STORE_PATH)
        if store.exists('user'):
            uid = store.get('user')['id']
            sorted_users = sorted(self.ids.lb_screen._users_cache, key=lambda u: u.get('solved', 0), reverse=True)
            for idx, u in enumerate(sorted_users):
                if u['id'] == uid:
                    user_data = dict(u)
                    user_data['index'] = idx
                    return user_data
        return None
