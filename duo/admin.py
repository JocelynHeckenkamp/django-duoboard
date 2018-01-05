from django.contrib import admin

from .models import User, Username
from .forms import Submit
admin.site.register(Username)
admin.site.register(User)
