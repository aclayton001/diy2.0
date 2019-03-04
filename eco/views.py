from django.shortcuts import render, render_to_response

# Create your views here.

from django.http import HttpResponse


def index(request):
	#return HttpResponse("Hello, world. You're at the DIY Eco System")
	return render_to_response('index.html')
