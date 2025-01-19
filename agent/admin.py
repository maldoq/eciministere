from django.contrib import admin
from .models import Service, Agent

admin.site.register(Service)
admin.site.register(Agent)