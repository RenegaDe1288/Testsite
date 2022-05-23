from django.contrib import admin
from .models import *


class CandidateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'lastname')


admin.site.register(Candidate, CandidateAdmin)


class SkillAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Skill, SkillAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Tag, TagAdmin)

