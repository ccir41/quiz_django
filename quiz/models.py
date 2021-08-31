from django.db import models
from django.db.models.fields.related import ManyToManyField
from django.utils.text import slugify
from jsonfield import JSONField

from core.models import BaseModel
from user.models import User

# Data backup and restore
# python manage.py dumpdata quiz.Category quiz.QuizExam quiz.Question quiz.Option > db.json
# python manage.py loaddata db.json


class Category(BaseModel):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['created_at']
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class QuizExam(BaseModel):
    name = models.CharField(max_length=64)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['name', 'category']
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Question(BaseModel):
    name = models.CharField(max_length=255)
    quiz_exam = models.ForeignKey(QuizExam, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['name', 'quiz_exam']
        ordering = ['created_at']

    def __str__(self):
        return self.name

class Option(BaseModel):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='options')
    name = models.CharField(max_length=255)
    isAnswer = models.BooleanField(default=False)

    class Meta:
        unique_together = ['question', 'name', 'isAnswer']
        ordering = ['created_at']

    def __str__(self):
        return self.question.name


class UserResponse(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz_exam = models.ForeignKey(QuizExam, on_delete=models.CASCADE)
    score = models.IntegerField()
    attempted = models.PositiveBigIntegerField(default=0)
    response = JSONField()

    class Meta:
        unique_together = ['user', 'quiz_exam']
        ordering = ['created_at']

    def __str__(self):
        return self.user.email
