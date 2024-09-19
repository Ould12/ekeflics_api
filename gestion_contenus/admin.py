from django.contrib import admin
from .models import Genre, Film, Serie,Episode,EvenementLive, Saison

# Register your models here.
admin.site.register(Genre)
admin.site.register(Film)
admin.site.register(Saison)
admin.site.register(Serie)
admin.site.register(Episode)
admin.site.register(EvenementLive)