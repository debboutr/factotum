from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.views.generic import TemplateView
# Create your views here.
# @login_required(login_url='/login')
# def index(request):
# 	return render(request, 'dashboard/index.html')

class indexView(TemplateView):
	template_name = 'dashboard/index.html'
