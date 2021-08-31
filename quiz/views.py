from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from django.db.models import F, Count

from .models import Category, QuizExam, Question, Option, UserResponse
from core.utils import StaffMemberRequiredMixin


class QuizAdmin(StaffMemberRequiredMixin, TemplateView):
    template_name = 'quiz/admin.html'


class QuizCategoryList(StaffMemberRequiredMixin, ListView):
    model = Category
    paginate_by = 4
    context_object_name = 'quiz_categories'
    template_name = 'quiz/category/quiz-category-list.html'


class QuizCategoryDetail(StaffMemberRequiredMixin, DetailView):
    model = Category
    template_name = 'quiz/category/quiz-category-detail.html'
    context_object_name = 'quiz_category'

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
    context_object_name = 'quiz_category'
    #success_url = reverse_lazy('quiz:quiz-category-list')
    template_name = 'quiz/category/quiz-category-delete.html'

    def get_success_url(self):
        messages.error(self.request, 'Quiz category deleted!')
        return reverse('quiz:quiz-category-list')


class QuizExamList(StaffMemberRequiredMixin, ListView):
    model = QuizExam
    paginate_by = 4
    context_object_name = 'quiz_exams'
    template_name = 'quiz/exam/quiz-exam-list.html'

    def get_queryset(self):
        qs = super().get_queryset().select_related('category')
        return qs


class QuizExamDetail(StaffMemberRequiredMixin, DetailView):
    model = QuizExam
    template_name = 'quiz/exam/quiz-exam-detail.html'
    context_object_name = 'quiz_exam'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def get_queryset(self):
        qs = super().get_queryset().select_related('category')
        return qs


class QuizExamCreate(StaffMemberRequiredMixin, CreateView):
    model = QuizExam
    fields = ['name', 'category']
    template_name = 'quiz/exam/quiz-exam-form.html'

    def get_success_url(self):
        messages.success(self.request, 'Quiz exam created!')
        return reverse('quiz:quiz-exam-list')


class QuizExamUpdate(StaffMemberRequiredMixin, UpdateView):
    model = QuizExam
    fields = ['name', 'category']
    template_name = 'quiz/exam/quiz-exam-update.html'

    def get_success_url(self):
        messages.info(self.request, 'Quiz exam updated!')
        return reverse('quiz:quiz-exam-list')


class QuizExamDelete(StaffMemberRequiredMixin, DeleteView):
    model = QuizExam
    context_object_name = 'quiz_exam'
    template_name = 'quiz/exam/quiz-exam-delete.html'

    def get_success_url(self):
        messages.error(self.request, 'Quiz exam deleted!')
        return reverse('quiz:quiz-exam-list')


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
            questions = Question.objects.filter(quiz_exam__slug__iexact=quiz_exam_slug).prefetch_related('options')
        else:
            questions = []
        return render(request, 'quiz/quiz-questions.html', {'questions': questions, 'quiz_exam_slug': quiz_exam_slug})

    def post(self, request, *args, **kwargs):
        data = dict(request.POST)
        quiz_exam = QuizExam.objects.get(slug=kwargs.get('quiz_exam_slug'))
        score = 0
        del data['csrfmiddlewaretoken']
        questions = Question.objects.filter(id__in=data.keys()).prefetch_related('options')
        for question, answer in zip(questions, data.values()):
            answer_count = len(answer)
            answer_count_check = 0
            for option in question.options.all():
                if str(option.id) in answer and option.isAnswer:
                    answer_count_check += 1
            if answer_count == answer_count_check:
                score += 1
        user_response, created = UserResponse.objects.get_or_create(
            user=request.user,
            quiz_exam=quiz_exam,
            defaults={
                'score': score,
                'response': data,
                'attempted': 1
            }
        )
        if not created:
            user_response.score = score
            user_response.response = data
            user_response.attempted += 1
            user_response.save()
        return render(
            request,
            'quiz/response.html',
            {
                'message': 'Your quiz has been submitted. Click the following link to view your result!',
                'quiz_exam': quiz_exam.id
            }
        )


class QuizQuestionList(ListView):
    model = Question
    paginate_by = 5
    context_object_name = 'questions'
    template_name = 'quiz/question/quiz-question-list.html'

    def get_queryset(self):
        qs = super().get_queryset().select_related('quiz_exam')
        return qs.filter(quiz_exam__slug=self.kwargs.get('quiz_exam_slug'))

    def get_context_data(self):
        data = super().get_context_data()
        data['quiz_exam_slug'] = self.kwargs.get('quiz_exam_slug')
        return data


class QuizQuestionDetail(View):
    template_name = 'quiz/question/quiz-question-detail.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'question': Question.objects.get(
            id=kwargs.get('pk')), 'quiz_exam_slug': kwargs.get('quiz_exam_slug')})


class QuizQuestionCreate(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'quiz/question/quiz-question-form.html', {})

    def post(self, request, *args, **kwargs):
        quiz_exam = QuizExam.objects.get(slug=kwargs.get('quiz_exam_slug'))
        data = dict(request.POST)
        # print(data)
        if data.get('question') == ['']:
            messages.error(request, 'Question field should not be empty!')
        elif data.get('option1') is None or data.get('option1') == ['']:
            messages.error(
                request, 'Please provide question with at least two options!')
        elif data.get('option2') is None or data.get('option2') == ['']:
            messages.error(
                request, 'Please provide question with at least two options!')
        else:
            for key, value in data.items():
                if key == 'csrfmiddlewaretoken':
                    continue
                if key == 'question':
                    question, created = Question.objects.get_or_create(
                        **{'name': value[0], 'quiz_exam': quiz_exam})
                    if created:
                        continue
                    else:
                        messages.error(
                            request, 'Duplicate question, question already in database!')
                        return render(request, 'quiz/question/quiz-question-form.html', {})
                try:
                    value_length = len(value)
                    if value_length > 1:
                        option, created = Option.objects.get_or_create(
                            **{'question': question, 'name': value[1]}, **{'isAnswer': True})
                    else:
                        option, created = Option.objects.get_or_create(
                            **{'question': question, 'name': value[0]}, **{'isAnswer': False})
                except:
                    pass
            messages.success(request, 'Question added successfully')
        return render(request, 'quiz/question/quiz-question-form.html', {})


class QuizQuestionUpdate(View):
    template_name = 'quiz/question/quiz-question-update.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'question': Question.objects.get(id=kwargs.get('pk'))})

    def post(self, request, *args, **kwargs):
        data = dict(request.POST)
        # print(data)
        for key, value in data.items():
            if key == 'csrfmiddlewaretoken':
                continue
            if key == 'question':
                question = Question.objects.filter(
                    id=kwargs.get('pk')).update(name=value[0])
                continue

            option_id = int(key.split('option')[1])

            try:
                option = Option.objects.get(id=option_id)
            except:
                option = None

            if option:
                if len(value) > 1:
                    option.name = value[1]
                    option.isAnswer = True
                    option.save()
                else:
                    option.name = value[0]
                    option.isAnswer = False
                    option.save()
        messages.success(request, 'Quiz question updated successfully!')
        return HttpResponseRedirect(reverse('quiz:quiz-question-list', kwargs={'quiz_exam_slug': kwargs.get('quiz_exam_slug')}))


class QuizQuestionDelete(DeleteView):
    model = Question
    context_object_name = 'question'
    template_name = 'quiz/question/quiz-question-delete.html'

    def post(self, request, *args, **kwargs):
        self.quiz_exam_slug = kwargs.get('quiz_exam_slug')
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        messages.error(self.request, 'Quiz question deleted!')
        return reverse('quiz:quiz-question-list', kwargs={'quiz_exam_slug': self.quiz_exam_slug})
