from django.shortcuts import render
from .models import Profile, Skill, Project, Certification, Education

# Create your views here.

def home(request):
    """포트폴리오 홈페이지 뷰"""
    profile = Profile.objects.first()
    skills = Skill.objects.all()
    projects = Project.objects.all()
    certifications = Certification.objects.all()
    education_history = Education.objects.all()

    context = {
        'profile': profile,
        'skills': skills,
        'projects': projects,
        'certifications': certifications,
        'education_history': education_history
    }
    return render(request, 'main/home.html', context)
