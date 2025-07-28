from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Profile, Skill, Project, Certification, Link, Education

class LinkInline(GenericTabularInline):
    model = Link
    extra = 1
    ordering = ['order']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """프로필 모델 어드민"""
    inlines = [LinkInline]
    list_display = ('name', 'title')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date')
    filter_horizontal = ('skills',)
    inlines = [LinkInline]

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'issuer', 'date_acquired', 'category')
    list_filter = ('category',)

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'institution', 'start_date', 'end_date')
