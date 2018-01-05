from __future__ import absolute_import, unicode_literals
from celery import shared_task
#from celery import Celery
import requests
import json
import threading
from duo.models import User
from .celery import app

@app.task
def add(x, y):
    return x + y

@app.task
def addu(username):
    u = User(username=username)
    u.save()
    return None

#celery -A tasks worker --loglevel=info
#celery -A Duoboard worker -l info
#celery -A Duoboard beat
def findUser(username, lis):
    for user in lis:
        if user['username'] == username:
            return user
    return None

def updateUser(username):
    user = User.objects.filter(username=username)[0]
    try:
        r = requests.get("http://www.duolingo.com/users/" + username)
        if r.status_code == 200:
            try:
                userapi = json.loads(r.text)
                user.img = "http:"+userapi["avatar"]+"/xlarge"
                user.streak = userapi["site_streak"]
                user.xp = findUser(username, userapi['language_data'][list(userapi['language_data'].keys())[0]]["points_ranking_data"])['points_data']['total']
                user.lingots = userapi["rupees"]
                user.save()
            except:
                user.delete()
        else:
            user.delete()
    except:
        user.delete()

@app.task
def updateUsers():
    threads = []
    for user in User.objects.all():
        t = threading.Thread(target=updateUser, args=(user.username,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
