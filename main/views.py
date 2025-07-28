from django.shortcuts import render
from .models import Profile, Skill, Project, Certification, Education
from django.db.models import Q

# Create your views here.

def home(request):
    """포트폴리오 홈페이지 뷰"""
    profile = Profile.objects.first()
    skills = Skill.objects.all().order_by('name')
    
    # Projects
    ongoing_projects = Project.objects.filter(end_date__isnull=True).order_by('start_date')
    completed_projects = Project.objects.filter(end_date__isnull=False).order_by('start_date')

    # Educations
    ongoing_educations = Education.objects.filter(end_date__isnull=True).order_by('start_date')
    completed_educations = Education.objects.filter(end_date__isnull=False).order_by('start_date')
    
    # Certifications
    certificates = Certification.objects.filter(category='certificate').order_by('-date_acquired')
    awards = Certification.objects.filter(category='award').order_by('-date_acquired')

    context = {
        'profile': profile,
        'skills': skills,
        'ongoing_projects': ongoing_projects,
        'completed_projects': completed_projects,
        'ongoing_educations': ongoing_educations,
        'completed_educations': completed_educations,
        'certificates': certificates,
        'awards': awards,
    }
    return render(request, 'main/home.html', context)

def handler404(request, exception):
    return render(request, 'main/404.html', status=404)
