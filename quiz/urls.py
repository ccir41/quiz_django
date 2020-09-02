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

    path('quiz-admin/quiz-exam-list/',
         views.QuizExamList.as_view(), name='quiz-exam-list'),
    path('quiz-admin/quiz-exam-add/', views.QuizExamCreate.as_view(),
         name='quiz-exam-add'),
    path('quiz-admin/quiz-exam-detail/<slug:slug>/',
         views.QuizExamDetail.as_view(), name='quiz-exam-detail'),
    path('quiz-admin/quiz-exam-update/<slug:slug>/',
         views.QuizExamUpdate.as_view(), name='quiz-exam-update'),
    path('quiz-admin/quiz-exam-delete/<slug:slug>/',
         views.QuizExamDelete.as_view(), name='quiz-exam-delete'),

    path('quiz-admin/quiz-question-add/<slug:quiz_exam_slug>/',
         views.QuizQuestionCreate.as_view(), name='quiz-question-add'),
    path('quiz-admin/quiz-question-list/<slug:quiz_exam_slug>/',
         views.QuizQuestionList.as_view(), name='quiz-question-list'),
    path('quiz-admin/quiz-question-detail/<slug:quiz_exam_slug>/<int:pk>/',
         views.QuizQuestionDetail.as_view(), name='quiz-question-detail'),
    path('quiz-admin/quiz-question-update/<slug:quiz_exam_slug>/<int:pk>/',
         views.QuizQuestionUpdate.as_view(), name='quiz-question-update'),
    path('quiz-admin/quiz-question-delete/<slug:quiz_exam_slug>/<int:pk>/',
         views.QuizQuestionDelete.as_view(), name='quiz-question-delete'),
]
