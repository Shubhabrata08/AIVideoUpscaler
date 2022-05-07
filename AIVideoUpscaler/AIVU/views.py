from distutils.command.upload import upload
from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse

# Create your views here.
def home(request):
    return render(request,'index.html')

def upscale(request):
    if request=='POST':
        return render(request,'about.html')
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        uploaded_file=request.FILES['videodata']
        print(uploaded_file.name)
        print(uploaded_file.size)
        fs=FileSystemStorage()
        fs.save(uploaded_file.name,uploaded_file)
        # fs.delete(uploaded_file.name)
        return render(request,'about.html')
    return render(request,'upscale.html')

def about(request):
    return render(request,'about.html')

# def startProcess(request):
#     scaleFactor=request.POST["scalingValue"]
    
    