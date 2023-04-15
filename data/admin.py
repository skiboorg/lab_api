from django.contrib import admin
from .models import *

class SintezInline (admin.TabularInline):
    model = Sintez
    extra = 0


class ProjectAdmin(admin.ModelAdmin):
    model = Project
    inlines = [SintezInline]



class SintezStepInline (admin.TabularInline):
    model = SintezStep
    extra = 0

class SintezImageInline (admin.TabularInline):
    model = SintezImage
    extra = 0

class SintezFileInline (admin.TabularInline):
    model = SintezFile
    extra = 0

class SintezCardInline (admin.TabularInline):
    model = SintezCard
    extra = 0


class SintezAdmin(admin.ModelAdmin):
    model = Sintez
    inlines = [SintezCardInline, SintezStepInline,SintezImageInline,SintezFileInline]
    list_filter = (
        'project',
    )

admin.site.register(Project, ProjectAdmin)
admin.site.register(Sintez, SintezAdmin)



