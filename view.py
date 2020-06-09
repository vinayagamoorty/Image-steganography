from django.shortcuts import render
from django.http import HttpResponse
from . import models
import pandas as pd
from  django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.files.storage import FileSystemStorage,Storage
import pyAesCrypt
import os
def index(request):
   return render(request,'page.html')

# Create your views here.
def upload(request):
    if 'upload' in request.POST :
        key = request.POST['key']
        file = request.FILES['file']

        fs = FileSystemStorage("secure_file/media/")
        fs1 = FileSystemStorage("secure_file/enc/")

        f_data = fs.save(file.name,file)
        location = os.getcwd()
        bufferSize = 1024 * 1024 *1024
        pyAesCrypt.encryptFile(location + "\\" + fs.base_location + file.name,
                               location + "\\" + fs1.base_location + file.name + ".aes", key, bufferSize)
        print(fs1.base_location)
k = models.FileData.objects.create(file_title =file.name + ".aes",key = key)
        k.save()


    return render(request,'upload.html')
def file_view(request):

    fs = FileSystemStorage("secure_file\\media\\")
    fs1 = FileSystemStorage("secure_file\\enc\\")
    fs2 = FileSystemStorage("secure_file\\dec\\")
    location  = os.getcwd()
    print(os.listdir(location+"/"+fs.base_location))

    # encryption/decryption buffer size - 64K
    bufferSize = 1024 * 1024*1024
    if request.method=="POST":
        id = request.POST["download"]
        password =request.POST["key"]
        j = models.FileData.objects.get(id=id)
        print("enc happend")
        file1 = fs1.open(j.file_title)
        print(location+"\\"+fs2.base_location+j.file_title+".aes")

 # decrypt
        try:
             pyAesCrypt.decryptFile(fs1.base_location + j.file_title,fs2.base_location + j.file_title[:-3], password, bufferSize)
             file1 = fs2.open(j.file_title)
             response = HttpResponse(file1, content_type='application')
             return response
        except Exception as e:
            return HttpResponse(e)

     
    #return 
    j = models.FileData.objects.all()
    return render(request,"fileview.html",{"files":j})

def output(request): #not used


    j = models.FileData.objects.all()
    l = []
    for jk in j:
        l.append(jk)
    # mm = open(settings.MEDIA_ROOT)
    print(len(l))
    fs = FileSystemStorage()
    mm = fs.open(l[len(l)-1].file_title)
    print(mm)
    df = pd.read_csv(mm)
    i = df.plot().get_figure()
    i.savefig('media//a.png')
    fs = FileSystemStorage()

    return HttpResponse(fs.open('a.png').file,content_type='image/png')




