from django.shortcuts import render
from .models import User
from .models import Username
from .forms import Submit
import requests
import json
import threading
from django.shortcuts import redirect

def findUser(username, lis):
    for user in lis:
        if user['username'] == username:
            return user
    return None
def updateUser(username):
    user = User.objects.get(username=username)
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

def updateUsers():
    threads = []
    for user in User.objects.all():
        t = threading.Thread(target=updateUser, args=(user.username,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

def rd(request):
    return redirect('xp')

def xp(request):
    #updateUsers()
    #from duo.tasks import updateUsers
    #updateUsers()
    users = User.objects.values('username', 'img', 'profile', 'xp').order_by('-xp')
    return render(request, "duo/index.html", {'users': users, 'xp': True})

def streak(request):
    users = User.objects.values('username', 'img', 'profile', 'streak').order_by('-streak')
    return render(request, "duo/index.html", {'users': users, 'streak': True})

def lingots(request):
    users = User.objects.values('username', 'img', 'profile', 'lingots').order_by('-lingots')
    return render(request, "duo/index.html", {'users': users, 'lingots': True})

def about(request):
    return render(request, 'duo/index.html', {'about': True})

def submit(request):
    newform = Submit()
    message = 'Submit successful.'
    if request.method == 'POST':
        form = Submit(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).count() == 0:
                if Username.objects.filter(username=username).count() == 0:
                    Username(username=username).save()
                try:
                    r = requests.get("http://www.duolingo.com/users/" + username)
                    userapi = json.loads(r.text)
                    user = User(username=username, profile="https://duolingo.com/" + username,
                        img="http:"+userapi["avatar"]+"/xlarge",
                        streak=userapi["site_streak"],
                        xp=findUser(username, userapi['language_data'][list(userapi['language_data'].keys())[0]]["points_ranking_data"])['points_data']['total'],
                        lingots=userapi["rupees"])
                    user.save()
                except:
                    message = 'User does not exist.'
            else:
                message = 'User already entered.'
        return render(request, 'duo/index.html', {'submit': True, 'form': newform, 'message': message})
    return render(request, 'duo/index.html', {'submit': True, 'form': newform})
