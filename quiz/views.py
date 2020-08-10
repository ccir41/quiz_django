from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .models import Category, QuizExam, Question, Option, UserResponse
from core.utils import StaffMemberRequiredMixin


class QuizAdmin(StaffMemberRequiredMixin, TemplateView):
    template_name = 'quiz/admin.html'


class QuizCategoryList(StaffMemberRequiredMixin, ListView):
    model = Category
    paginate_by = 4
    template_name = 'quiz/category/quiz-category-list.html'


class QuizCategoryDetail(StaffMemberRequiredMixin, DetailView):
    model = Category
    template_name = 'quiz/category/quiz-category-detail.html'
    #context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class QuizCategoryCreate(StaffMemberRequiredMixin, CreateView):
    model = Category
    fields = ['name']
    #success_url = reverse_lazy('quiz:quiz-category-list')
    template_name = 'quiz/category/quiz-category-form.html'

    def get_success_url(self):
        messages.success(self.request, 'Quiz category created!')
        return reverse('quiz:quiz-category-list')


class QuizCategoryUpdate(StaffMemberRequiredMixin, UpdateView):
    model = Category
    fields = ['name']
    #success_url = reverse_lazy('quiz:quiz-category-list')
    template_name = 'quiz/category/quiz-category-update.html'

    def get_success_url(self):
        messages.info(self.request, 'Quiz category updated!')
        return reverse('quiz:quiz-category-list')


class QuizCategoryDelete(StaffMemberRequiredMixin, DeleteView):
    model = Category
    #success_url = reverse_lazy('quiz:quiz-category-list')
    template_name = 'quiz/category/quiz-category-delete.html'

    def get_success_url(self):
        messages.error(self.request, 'Quiz category deleted!')
        return reverse('quiz:quiz-category-list')


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
        quiz_exam = QuizExam.objects.get(slug=kwargs.get('quiz_exam_slug'))
        # print(data)
        response = {}
        score = 0
        for key, value in data.items():
            if key == 'csrfmiddlewaretoken':
                continue
            response[f"{key}"] = value
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
        try:
            user_response = UserResponse.objects.get(
                user=request.user, quiz_exam=quiz_exam)
            user_response.score = score
            user_response.response = response
            user_response.save()
        except:
            user_response = UserResponse.objects.create(
                user=request.user, quiz_exam=quiz_exam, score=score, response=response)

        results = []
        for key, value in response.items():
            question = Question.objects.get(id=int(key))
            options = Option.objects.filter(question=question)
            results.append(
                {'question': question, 'options': options, 'user_answer': value})

        return render(request, 'quiz/results.html', {'score': score, 'results': results})
