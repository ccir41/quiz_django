from django.contrib import admin
from .models import (Category, QuizExam, Question, Option, UserResponse)

admin.site.register(Category)
admin.site.register(QuizExam)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(UserResponse)
