from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import *

class UserAdmin(BaseUserAdmin):
    list_display = (
        'login',
        'fio',
        'work',
        'date_joined',

    )
    ordering = ('id',)
    #inlines = []
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                        'login',
                        'fio',
                        'work',
                       'avatar',
                       'added_by',
                       'is_moderator',
                       'password1',
                       'password2',
                       ), }),)
    search_fields = ('id','login', 'fio', 'work',)
    list_filter = (
        'is_moderator',
                   )
    fieldsets = (
        (None, {'fields': ('login', 'password')}),
        ('Personal info',
         {'fields': (
              'fio',
                'work',
               'avatar',
               'added_by',
               'is_moderator',

         )}
         ),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups',)}),)

admin.site.register(User,UserAdmin)



