from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Category, QuizExam, Question, Option, UserResponse


class QuizCategories(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        return render(request, 'quiz/quiz-categories.html', {'categories': categories})


class QuizExams(View):
    def get(self, request, *args, **kwargs):
        category_slug = kwargs.get('category_slug')
        category = None
        if category_slug:
            try:
                category = Category.objects.get(slug=category_slug)
            except:
                pass
            quiz_exams = QuizExam.objects.filter(
                category__slug__icontains=category_slug)
        else:
            quiz_exams = []
        return render(request, 'quiz/quiz-exams.html', {'quiz_exams': quiz_exams, 'category': category})


class QuizQuestions(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        quiz_exam_slug = kwargs.get('quiz_exam_slug')
        if quiz_exam_slug:
            results = []
            # use generator insted
            questions = Question.objects.filter(
                quiz_exam__slug__iexact=quiz_exam_slug)
            for question in questions:
                options = Option.objects.filter(question=question)
                question_options = []
                for opt in options:
                    question_options.append({'id': opt.id, 'name': opt.name})
                results.append({'question': {'id': question.id, 'name': question.name},
                                'options': question_options})
        else:
            results = []
        return render(request, 'quiz/quiz-questions.html', {'results': results, 'quiz_exam_slug': quiz_exam_slug})

    def post(self, request, *args, **kwargs):
        data = dict(request.POST)
        # print(data)
        score = 0
        for key, value in data.items():
            if key == 'csrfmiddlewaretoken':
                continue
            try:
                for opt in value:
                    option = Option.objects.get(
                        id=int(opt), question_id=int(key))
                    if option.isAnswer:
                        is_correct = True
                    else:
                        is_correct = False
                        break
            except:
                pass
            if is_correct:
                score += 1
        return render(request, 'quiz/results.html', {'score': score})
