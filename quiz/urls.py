from django.urls import path
from . import views

app_name = 'quiz'


urlpatterns = [
    path('quiz-categories/', views.QuizCategories.as_view(), name='quiz-categories'),
    path('quiz-exams/<slug:category_slug>/',
         views.QuizExams.as_view(), name='quiz-exams'),
    path('quiz-questions/<slug:quiz_exam_slug>/',
         views.QuizQuestions.as_view(), name='quiz-questions'),

    path('quiz-admin/', views.QuizAdmin.as_view(), name='quiz-admin'),
    path('quiz-admin/quiz-category-add/', views.QuizCategoryCreate.as_view(),
         name='quiz-category-add'),
    path('quiz-admin/quiz-category-list/', views.QuizCategoryList.as_view(),
         name='quiz-category-list'),
    path('quiz-admin/quiz-category-detail/<slug:slug>/',
         views.QuizCategoryDetail.as_view(), name='quiz-category-detail'),
    path('quiz-admin/quiz-category-update/<slug:slug>/',
         views.QuizCategoryUpdate.as_view(), name='quiz-category-update'),
    path('quiz-admin/quiz-category-delete/<slug:slug>/',
         views.QuizCategoryDelete.as_view(), name='quiz-category-delete'),
]
