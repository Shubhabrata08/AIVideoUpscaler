from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'index.html')

def upscale(request):
    return render(request,'upscale.html')

def about(request):
    return render(request,'about.html')