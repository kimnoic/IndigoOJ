from django.contrib import admin
from .models import *
from . import models

admin.site.register(OnlineOJ)
admin.site.register(Status)
admin.site.register(Problem)
admin.site.register(models.User)
# Register your models here.
