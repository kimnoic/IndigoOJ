from django.contrib import admin
from .models import *
from . import models

admin.site.register(OnlineOJ)
admin.site.register(Status)
admin.site.register(Problem)
admin.site.register(models.User)
admin.site.register(Contest)
admin.site.register(ContestProblem)
admin.site.register(ContestProblemStatus)
admin.site.register(ContestLog)
# Register your models here.
