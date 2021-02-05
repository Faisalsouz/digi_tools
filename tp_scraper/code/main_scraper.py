from bs4 import BeautifulSoup
import requests
from pprint import pprint
import json
import csv
import pandas as pd
import os
from django.core.files.storage import default_storage
from django.core.files import File
from django.http import HttpResponse
from zipfile import ZipFile


def scraper_py():

#Importing all urls form the excel file contains Bundesland territories:

    #dirname = Path(os.path.dirname(__file__))
    #fx = os.path.join(dirname,'/media/file_1.xlsx')
    excel=pd.read_excel(default_storage.open('file_1.xlsx'),engine='openpyxl')
    url=excel.Title_URL.to_list()
    for i in url:
        city=i.split('-')[2].replace('.html','')
        geo=i.split('-')[1]
        base_url='https://www.tripadvisor.com'
        print(f'Looking if {city} is already parsed')
        file_name=f'./output/{city}.csv'
        print(os.getcwd())
        if f'{city}.csv' in os.listdir('./output'):
            print(f'file {city} has already been processed')
        else:
            print('new city has been found')
            url=f'https://www.tripadvisor.com/Restaurants-{geo}-oa1-{city}.html#EATERY_LIST_CONTENTS'

            print(url)
            page=BeautifulSoup(requests.get(url).text,'html.parser')
            #page=page.find_all('span',class_='_1D_QUaKi')
            #print(page)
            url_list=[]
            page_number=[link.get('data-page-number') for link in (page.find_all('a',class_='pageNum taLnk',href=True))][-1]
            # for link in page.find_all('a',class_='pageNum taLnk',href=True):#finding all classed that contains page number class
            #     page_number = link.get('data-page-number')#getting total pages for current list
            print(f'expected {page_number} pages on url:\n{url}')

            if page_number!=None:
                page_number=int(page_number)
                for pg in range(0,int(page_number),1):
                    pg=(pg*30+1)
            #
                    url=f'https://www.tripadvisor.com/Restaurants-{geo}-oa{str(pg)}-{city}.html#EATERY_LIST_CONTENTS'
                    print(f'adding{pg} for current \n{url} to urls list')
                    url_list.append(url)
            else:
                print('There is only one page found')
                url=f'https://www.tripadvisor.com/Restaurants-{geo}-oa1-{city}.html#EATERY_LIST_CONTENTS'
                url_list.append(url)
            #email_list=[]
            print(url_list)
            for j in url_list:#getting urls list first nd iterration then

                bs_parser = BeautifulSoup(requests.get(j).text, 'html.parser')

                res_link=bs_parser.find_all('a',class_='_15_ydu6b')#findig all restu links  having class _15_...

                #names.append([nm.text for  nm in res_link])#getting names of the links
                #print(names)

                # res_lnk.append([l.get('href') for l in res_link])

                for ln in res_link:
                    url_email=base_url+ln.get('href')#connecting link with base url to parse the restaurent data out of it.
                    soup_email=BeautifulSoup(requests.get(url_email).text,'html.parser')
                    email = soup_email.find_all('div', class_='_36TL14Jn _3jdfbxG0')
                    for i in email:

                        em = i.find_all('a', href=True)#email is hidden in complte division tag so finding all 'a' with href must
                        em = [a['href'] for a in em]#extracting link from a section

                        em=[i.replace('mailto:', '').replace('?subject=?', '') for i in em]#cleaning the href based email.
                        #email_list.append(em)
                        print(f'email{em}from url {url_email} is being printed')#writing it into csv file

                        with open(file_name, 'a', newline='',encoding='utf-8') as myfile:
                            f=File(myfile)
                            wr = csv.writer(f, quoting=csv.QUOTE_ALL)
                            #wr.writerow(names)
                            wr.writerow(em)
                            print(f'{em} has been wirtten to file')
            for f in os.listdir('./media'):
                os.remove(os.path.join('./media', f))

            files = os.listdir('./output')
            path = [f for f in files if f.endswith('csv')]
            with ZipFile('./output/out.zip', 'w', ) as z:
                for i in path:
                    print(i)
                    z.write(f'./output/{i}')
                    print('files has been zipped')
                out_file = open('./output/out.zip', 'rb')
                response = HttpResponse(out_file,content_type='application/force-download')  # application/zip application/force-download
                response['Content-Disposition'] = 'attachment; filename=out.zip'
                return response

def test_zip():
    files = os.listdir('./output')
    path = [f for f in files if f.endswith('csv')]
    with ZipFile('./output/out.zip', 'w',) as z:
        for i in path:
            print(i)
            z.write(f'./output/{i}')
            print('files has been zipped')
        out_file=open('./output/out.zip', 'rb')
        response = HttpResponse(out_file, content_type='application/force-download')#application/zip application/force-download
        response['Content-Disposition'] = 'attachment; filename=out.zip'
        return response


