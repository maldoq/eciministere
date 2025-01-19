from django.contrib import admin
from .models import People

class PeopleAdmin(admin.ModelAdmin):
    list_display = ('user', 'numberPeople', 'addressPeople', 'indicatorPeople')
    search_fields = ('user__username', 'numberPeople')

admin.site.register(People, PeopleAdmin)