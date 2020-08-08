from django.urls import path
from . import views

app_name = 'quiz'


urlpatterns = [
    path('quiz-categories/', views.QuizCategories.as_view(), name='quiz-categories'),
    path('quiz-exams/<slug:category_slug>/',
         views.QuizExams.as_view(), name='quiz-exams'),
    path('quiz-questions/<slug:quiz_exam_slug>/',
         views.QuizQuestions.as_view(), name='quiz-questions'),
]
