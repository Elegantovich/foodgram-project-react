from cgitb import html
from django.shortcuts import render
from .models import Recipe
from django.core.paginator import Paginator


def index(request):
    recipes = Recipe.objects.order_by('-pub_date')
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, context)


def recipe(request):
    pass


def user(request):
    pass
