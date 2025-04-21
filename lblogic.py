import os
import json
import uuid
import threading
import asyncio
import aiohttp
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


SETTINGS_PATH = os.path.join(os.getcwd(), 'settings.json')
STORE_PATH = os.path.join(os.getcwd(), 'user_store.json')
USERS_PATH = os.path.join(os.getcwd(), 'users.json')
API_URL = "https://test-repo-59eu.onrender.com/users/"
maxlen = 13
maxtop = 99


event_loop = asyncio.new_event_loop()
def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()
threading.Thread(target=start_loop, args=(event_loop,), daemon=True).start()


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

class AsyncAPI:
    _session = None

    @classmethod
    async def get_session(cls):
        if cls._session is None:
            cls._session = aiohttp.ClientSession()
        return cls._session

    @classmethod
    async def close_session(cls):
        if cls._session:
            await cls._session.close()
            cls._session = None

    @classmethod
    async def fetch_users(cls):
        session = await cls.get_session()
        async with session.get(API_URL) as resp:
            resp.raise_for_status()
            return await resp.json()

    @classmethod
    async def update_user(cls, user_id, data):
        session = await cls.get_session()
        async with session.put(f"{API_URL}{user_id}", json=data) as resp:
            resp.raise_for_status()
            return await resp.json()

    @classmethod
    async def create_user(cls, payload):
        session = await cls.get_session()
        async with session.post(API_URL, json=payload) as resp:
            resp.raise_for_status()
            return await resp.json()


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
        Clock.schedule_once(lambda dt: asyncio.run_coroutine_threadsafe(self.load_and_render(), event_loop), 0)
        self._users_cache = []

    async def load_and_render(self):
        try:
            users = await AsyncAPI.fetch_users()
            with open(USERS_PATH,'w',encoding='utf-8') as f:
                json.dump(users, f, ensure_ascii=False, indent=4)
        except Exception:
            users = json.load(open(USERS_PATH,'r',encoding='utf-8')) if os.path.exists(USERS_PATH) else []
        self._users_cache = users
        Clock.schedule_once(lambda dt: self._update_view(), 0)

    def _update_view(self):
        sorted_users = sorted(self._users_cache, key=lambda u: u.get('solved',0), reverse=True)
        self._sorted_users = sorted_users  
	        
        display_users = [
	        u for idx, u in enumerate(sorted_users)
	        if idx < maxtop
	    ]

        self.data = [
	        {**{k: u.get(k, 0) for k in rv_numeric_props},
	            'username':      u.get('username', ''),
	            'created_at':    u.get('created_at', ''),
	            'updated_at':    u.get('updated_at', '')}
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
        Clock.schedule_once(lambda dt: self.update_screen(), 1.0)

    def on_pre_enter(self):
        if not self._asked:
            self._asked = True
            Clock.schedule_once(lambda dt: asyncio.run_coroutine_threadsafe(self.check_user(), event_loop), 0)
        self.upd_sc_fix()

    async def check_user(self):
        store = JsonStore(STORE_PATH)
        try:
            users = await AsyncAPI.fetch_users()
        except:
            users = JsonStore(USERS_PATH)
        user_exists = store.exists('user') and any((u['id']==store.get('user')['id'] and u['username']==store.get('user')['username'])  for u in users)
        if not user_exists:
            if store.exists('user'):
                os.remove(STORE_PATH)
            Clock.schedule_once(lambda dt: self.show_nickname_dialog(), 0)
        else:
            await self.update_user_and_board()

    async def update_user_and_board(self):
        store = JsonStore(STORE_PATH)
        if store.exists('user') and any(self.stats.values()):
            await AsyncAPI.update_user(store.get('user')['id'], self.stats)
        Clock.schedule_once(lambda dt: self.ids.lb_screen._update_view(), 0)

    def show_nickname_dialog(self):
        self.nickname_field = MDTextField(hint_text="Введите ваш никнейм", max_text_length=maxlen)
        self.dialog = MDDialog(
            title="Регистрация пользователя", type="custom", content_cls=self.nickname_field,
            buttons=[
                MDFlatButton(text="ОТМЕНА", on_release=lambda *a:self.dialog.dismiss()),
                MDFlatButton(text="OK", on_release=lambda *a: asyncio.run_coroutine_threadsafe(self.create_user(), event_loop))
            ]
        )
        self.dialog.open()

    async def create_user(self):
        self.nickname_field.error = False
        self.nickname_field.helper_text = ""
        self.nickname_field.helper_text_mode = "on_error"

        username = self.nickname_field.text.strip()

        if not username:
            self.nickname_field.error = True
            self.nickname_field.helper_text = "Укажите никнейм"
            return

        if len(username) > maxlen:
            self.nickname_field.error = True
            self.nickname_field.helper_text = f"Не более {maxlen} символов"
            return

        allowed = set("1234567890йцукенгшщзхъфывапролджэячсмитьбюёabcdefghijklmnopqrstuvwxyz- ()")
        if any(c.lower() not in allowed for c in username):
            self.nickname_field.error = True
            self.nickname_field.helper_text = "Недопустимые символы"
            return

        payload = {'username': username, **self.stats}

        try:
            users = await AsyncAPI.fetch_users()
            existing_ids = {u['id'] for u in users}
            new_id = str(uuid.uuid4())
            while new_id in existing_ids:
                new_id = str(uuid.uuid4())
            payload['id'] = new_id

            user = await AsyncAPI.create_user(payload)

        except Exception as e:
            self.nickname_field.error = True
            self.nickname_field.helper_text = f"Сетевая ошибка"
            return

        store = JsonStore(STORE_PATH)
        store.put('user',
                  id=user['id'],
                  username=user['username'],
                  **self.stats)


        await AsyncAPI.update_user(user['id'], self.stats)
        await self.update_user_and_board()

        Clock.schedule_once(lambda dt: self.dialog.dismiss(), 0)
        self.upd_sc_fix()


    def update_screen(self):
        self.stats = load_local_stats()

        store = JsonStore(STORE_PATH)
        if store.exists('user') and any(self.stats.values()):
            asyncio.run_coroutine_threadsafe(self.update_user_and_board(), event_loop)
        if not store.exists('user'):
            self._asked = False

        user_data = self.get_user_data()
        if user_data:
            self.ids.user_row.refresh_view_attrs(None, 0, user_data)

        Clock.schedule_once(lambda dt: asyncio.run_coroutine_threadsafe(self.ids.lb_screen.load_and_render(), event_loop), 0)

    def get_user_data(self):
        store = JsonStore(STORE_PATH)
        if store.exists('user'):
            user_id = store.get('user')['id']
            sorted_users = sorted(self.ids.lb_screen._users_cache, key=lambda u: u.get('solved', 0), reverse=True)
            for idx, u in enumerate(sorted_users):
                if u['id'] == user_id:
                    user_data = dict(u)
                    user_data['index'] = idx
                    return user_data
        return None


def on_app_stop():
    asyncio.run_coroutine_threadsafe(AsyncAPI.close_session(), event_loop)
