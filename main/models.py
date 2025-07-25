from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

# Create your models here.

class Link(models.Model):
    """범용 링크 모델"""
    url = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.url

class Profile(models.Model):
    """프로필 모델"""
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    links = GenericRelation('Link', related_query_name='profile')

    def __str__(self):
        return self.name

class Skill(models.Model):
    """기술 스택 모델"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Project(models.Model):
    """프로젝트 정보 모델"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField("시작일")
    end_date = models.DateField("종료일", null=True, blank=True)
    skills = models.ManyToManyField(Skill)
    links = GenericRelation(Link)

    def __str__(self):
        return self.title

class Certification(models.Model):
    """자격증 및 수상 내역 모델"""
    name = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200, verbose_name="발급 기관")
    date_acquired = models.DateField(verbose_name="취득일")

    class Meta:
        ordering = ['-date_acquired']

    def __str__(self):
        return self.name

class Education(models.Model):
    """교육 사항 모델"""
    course_name = models.CharField(max_length=200, verbose_name="과정/전공명")
    institution = models.CharField(max_length=200, verbose_name="교육 기관")
    start_date = models.DateField("시작일")
    end_date = models.DateField("종료일", null=True, blank=True)

    class Meta:
        ordering = ['-start_date']
        verbose_name_plural = "Education"

    def __str__(self):
        return f"{self.course_name} at {self.institution}"
