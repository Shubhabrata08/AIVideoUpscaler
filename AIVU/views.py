from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from AIVideoUpscaler.settings import BASE_DIR
import cv2
from math import ceil
from cv2 import INTER_LINEAR
from cv2 import INTER_CUBIC
from cv2 import waitKey
import json
import os
import mimetypes

from  django.conf import settings
# Create your views here.
def home(request):
    return render(request,'index.html')
lastFileName=''
progress_percent=0
currentScaleFactor=2

def upscale(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        uploaded_file=request.FILES['videodata']
        print(uploaded_file.name)
        print(uploaded_file.size)
        lastFileName=uploaded_file.name
        fs=FileSystemStorage()
        fileList=fs.listdir(os.path.join(BASE_DIR,'media/'))
        print(os.path.join(BASE_DIR,'media/'))
        print(fileList)
        
        for file in fileList[1]:
            # print(file)
            if fs.exists(file):
                fs.delete(file)
        fs.save(uploaded_file.name,uploaded_file)
        print(uploaded_file.name)
        # fs.delete(uploaded_file.name)
        return render(request,'about.html')
    return render(request,'upscale.html')

def about(request):
    return render(request,'about.html')


MODEL_PATH='FSRCNN_x4.pb'
def upsampleFSRCNN(modelPath,img,scale):
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    path = modelPath
    sr.readModel(path)
    sr.setModel("fsrcnn", scale) # set the model by passing the value and the upsampling ratio
    result = sr.upsample(img) # upscale the input image
    cv2.imwrite('result.png',result)
    # img=cv2.resize(img,dsize=(0,0),fx=4,fy=4,interpolation=INTER_CUBIC)
    # cv2.imwrite('resultResize.png',img)
    return result
def upsamplevideo(videoFilePath,scale):
    fs=FileSystemStorage()
    fileList=fs.listdir(os.path.join(settings.BASE_DIR,'media/'))
    for fl in fileList[1]:
        # print(file)
        if fs.exists(fl) and fl!=videoFilePath:
            fs.delete(fl)
    extraFilePath=os.path.join(settings.BASE_DIR,'media/')
    videoFilePath=extraFilePath+videoFilePath
    print(videoFilePath)
    videoObj=cv2.VideoCapture(videoFilePath)
    videoObj.open(videoFilePath)
    fps=ceil(videoObj.get(cv2.CAP_PROP_FPS))
    height=int(videoObj.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width=int(videoObj.get(cv2.CAP_PROP_FRAME_WIDTH))
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    frameCount=int(videoObj.get(cv2.CAP_PROP_FRAME_COUNT))
    MODEL_PATH=os.path.join(settings.BASE_DIR,'static\\models\\')
    print(width,height,fourcc,fps)
    print(MODEL_PATH)
    if scale==2:
        MODEL_PATH+="FSRCNN_x4.pb"
    elif scale==1:
        MODEL_PATH+="FSRCNN_x3.pb"
    else:
        MODEL_PATH+="FSRCNN_x2.pb"
    f=1
    k=1
    scale+=2
    upsampledVideoObj= cv2.VideoWriter(os.path.join(settings.BASE_DIR,'media/output.mp4'),fourcc,fps,(int(width*scale),int(height*scale))) 
    global progress_percent
    while k<=frameCount:
        f,imgFrame=videoObj.read()
        upsampledFrame=upsampleFSRCNN(MODEL_PATH,imgFrame,scale)
        # cv2.imshow("Test",upsampledFrame)
        # waitKey(1000)
        upsampledVideoObj.write(upsampledFrame)
        progress_percent=(k/frameCount)*100
        print(progress_percent)
        k+=1
    upsampledVideoObj.release()
    videoObj.release()
    cv2.destroyAllWindows()
# upsamplevideo('test2.mp4',4)

def startprocess(request):
    scaleFactor=request.POST["scalingValue"]
    scaleFactor=int(scaleFactor)
    global currentScaleFactor
    currentScaleFactor=scaleFactor
    upsamplevideo(lastFileName,scaleFactor)
    return render(request,'downloadpage.html')

def startscaling(request):
    fs=FileSystemStorage()
    fileNames=(fs.listdir(os.path.join(settings.BASE_DIR,'media/')))[1]
    print(fs.listdir(os.path.join(settings.BASE_DIR,'media/')))
    file=fileNames[0]
    print(file)
    if(file=="output.mp4"):
        return HttpResponse("Failure")
    upsamplevideo(file,currentScaleFactor)
    print(progress_percent)
    return HttpResponse("Success")

def progressupdate(request):
    data={
        'progress':progress_percent
    }
    return JsonResponse(data)
    return HttpResponse(progress_percent)
    
def download_file(request):
    file_path = os.path.join(settings.BASE_DIR,'media/')
    filename = "output.mp4"
    file_path+=filename
    fl = open(file_path, 'r',errors="ignore")
    mime_type, _ = mimetypes.guess_type(file_path)
    response = HttpResponse(fl, content_type='application/vnd.mp4')
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response