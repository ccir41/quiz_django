from django.shortcuts import render
from django.views import View

from quiz.models import Category


class HomeView(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        return render(request, 'index.html', {'categories': categories})
