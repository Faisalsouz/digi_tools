from django.shortcuts import render
# from tp_scraper.models import Document
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import default_storage
from django.http import HttpResponse
import os
from tp_scraper.code.main_scraper import scraper_py,test_zip
#from email_scraper.tp_scraper.code.main_scraper import scraper_py
import csv
# Create your views here.
# def main_page(request):
#     return render(request,'page1.html',{})

def show_db(reqeust):

    context={}
    return render(reqeust,'page1.html',context)
def scraper_main(reqeust):

    if reqeust.method == 'POST' and reqeust.FILES['myfile']:

        myfile = reqeust.FILES['myfile']

        fs = FileSystemStorage()
        filename = fs.save('file_1.xlsx', myfile)
        uploaded_file_url = fs.url(filename)
        return render(reqeust, 'em_scrap.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(reqeust, 'em_scrap.html')
def output(request):
    res=scraper_py()
   # return(res)

def download_zip(request):
    res = test_zip()
    return (res)



    #return render(request,'em_scrap.html', {'output_k': out})


def how_to(reqeust):

    context={}
    return render(reqeust,'Howto.html',context)

