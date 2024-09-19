from django.contrib import admin

# Register your models here.
from .models import Content,ViewingStatistics,ContentPerformance,UserEngagement

# Register your models here.
admin.site.register(Content)
admin.site.register(ViewingStatistics)
admin.site.register(ContentPerformance)
admin.site.register(UserEngagement)