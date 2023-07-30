import cv2
from math import ceil
from cv2 import INTER_LINEAR
from cv2 import INTER_CUBIC
from cv2 import waitKey
import matplotlib.pyplot as plt
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
        print(k)
        k+=1
    upsampledVideoObj.release()
    videoObj.release()
    cv2.destroyAllWindows()
# upsamplevideo('test2.mp4',4)
