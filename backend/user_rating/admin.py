from django.contrib import admin
from .models import MyUser, UserAnswer, UserQuestion


admin.site.register(MyUser)
admin.site.register(UserAnswer)
admin.site.register(UserQuestion)
