from distutils.command.upload import upload
from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
import cv2
from math import ceil
from cv2 import INTER_LINEAR
from cv2 import INTER_CUBIC
from cv2 import waitKey
import json
import os
progress_percent=0
# Create your views here.
def home(request):
    return render(request,'index.html')
lastFileName=''

def upscale(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        uploaded_file=request.FILES['videodata']
        print(uploaded_file.name)
        print(uploaded_file.size)
        lastFileName=uploaded_file.name
        fs=FileSystemStorage()
        fileList=fs.listdir('')
        for file in fileList[1]:
            # print(file)
            if fs.exists(file):
                fs.delete(file)
        fs.save(uploaded_file.name,uploaded_file)
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
    sr.setModel("fsrcnn", 4) # set the model by passing the value and the upsampling ratio
    result = sr.upsample(img) # upscale the input image
    cv2.imwrite('result.png',result)
    # img=cv2.resize(img,dsize=(0,0),fx=4,fy=4,interpolation=INTER_CUBIC)
    # cv2.imwrite('resultResize.png',img)
    return result
def upsamplevideo(videoFilePath,scale):
    videoObj=cv2.VideoCapture(videoFilePath)
    videoObj.open(videoFilePath)
    fps=ceil(videoObj.get(cv2.CAP_PROP_FPS))
    height=int(videoObj.get(cv2.CAP_PROP_FRAME_HEIGHT))*scale
    width=int(videoObj.get(cv2.CAP_PROP_FRAME_WIDTH))*scale
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    frameCount=int(videoObj.get(cv2.CAP_PROP_FRAME_COUNT))
    # print(width,height,fourcc,fps)
    upsampledVideoObj= cv2.VideoWriter('output.mp4',fourcc,fps,(width,height)) 
    if scale==4:
        MODEL_PATH="FSRCNN_x4.pb"
    elif scale==3:
        MODEL_PATH="FSRCNN_x3.pb"
    else:
        MODEL_PATH="FSRCNN_x2.pb"
    f=1
    k=1
    while k<=frameCount:
        f,imgFrame=videoObj.read()
        upsampledFrame=upsampleFSRCNN(MODEL_PATH,imgFrame,scale)
        upsampledVideoObj.write(upsampledFrame)
        progress_percent=k/frameCount
        progress_percent=progress_percent
        print(k)
        k+=1
    upsampledVideoObj.release()
    videoObj.release()
    cv2.destroyAllWindows()
# upsamplevideo('test2.mp4',4)

def startprocess(request):
    scaleFactor=request.POST["scalingValue"]
    scaleFactor=int(scaleFactor)
    upsamplevideo()
    return render(request,'downloadpage.html')
    upsamplevideo('../media/'+lastFileName,scaleFactor)

def progressupdate(request):
    return JsonResponse({'progress':progress_percent},safe=False)
    
