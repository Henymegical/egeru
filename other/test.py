import time
import requests as r

#[{'username': 'alexlarin', 'stat_2': 0, 'stat_4': 0, 'stat_6': 0,
#  'mistakes': 0, 'id': 1, 'updated_at': '2025-04-14T17:09:48', 'stat_1': 0,
#  'stat_3': 0, 'stat_5': 0, 'stat_7': 0, 'solved': 0, 'created_at': '2025-04-14T17:09:48'},
# 
#  {'username': 'cakeeater2108', 'stat_2': 0, 'stat_4': 100, 'stat_6': 0, 'mistakes': 204,
#  'id': 2, 'updated_at': '2025-04-14T17:11:32', 'stat_1': 0, 'stat_3': 0, 'stat_5': 5,
#  'stat_7': 0, 'solved': 105, 'created_at': '2025-04-14T17:10:28'}]

# Получение всех пользователей
#data = r.get("https://test-repo-59eu.onrender.com/users/").json()

#Добавление пользрователя 
#data = r.post('https://test-repo-59eu.onrender.com/users/', json={'username': 'AlexLarin'}).json()

#Изменение прарамтеров пользователя
#data = r.put('https://test-repo-59eu.onrender.com/users/1', json={'stat_1': 0}).json() 

#Удалить всех пользователей
#data = r.get('https://test-repo-59eu.onrender.com/init')  

# Получение конкретного пользователя ...
#data = r.get("https://test-repo-59eu.onrender.com/users/1").json()
while True:
    time.sleep(10)
    try:
        data = r.get("https://test-repo-59eu.onrender.com/users/").json()
    except r.exceptions.RequestException as e:
        print(f"Error: {e}")
        data = None
    print(data)