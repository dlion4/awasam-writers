from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class HomeView(TemplateView):
    template_name = "dashboard/editor/pages/home.html"
    
editor_home_view = HomeView.as_view()
