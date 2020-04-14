from django.shortcuts import render

import requests
from bs4 import BeautifulSoup

# Create your views here.
def index(request):
    return render(request,'index.html')

def form(request):
    country = request.POST['country']
    url = 'https://www.worldometers.info/coronavirus/'
    html = requests.post(url)
    purehtml = html.content

    # Souping
    soup = BeautifulSoup(purehtml,'html.parser')
    th = soup.find_all('table' , id='main_table_countries_today')

    #getting all headings
    para_list = []
    for trr in th[0].find_all('tr'):
        for i in trr.find_all('th'):
            para_list.append(i.text)

    # fetching particular country's data
    data_list = []
    bool = False
    for trr in th[0].find_all('tr'):
        for i in trr.find_all('td'):
            if i.text == country or bool:
                bool = True
                data_list.append(i.text)
            else:
                break
        bool = False


    #making dictionaries
    data = dict(zip(para_list,data_list))

    return render(request,'other.html',{'country':data['Country,Other'],'cases':data['TotalCases'],'deaths':data['TotalDeaths'],'perm':data['Tot\xa0Cases/1M pop'],'recovered':data['TotalRecovered']})

def local(request):


    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')


    geo_request_url = 'https://get.geojs.io/v1/ip/geo/' + ip + '.json'
    geo_request = requests.get(geo_request_url)
    geo_data = geo_request.json()
    local_country = geo_data['country']
    local_state = geo_data['region']


    confirmcase = 'No data Found'
    deaths = 'No data Found'
    recover = 'No data Found'
    new = 'No data Found'

    if local_country=='India':
        url = 'https://api.covid19india.org/data.json'
        html = requests.get(url).json()
        state = html['statewise']
        count = 0
        for i in state:
            count += 1
            if i['state'] == local_state:
                break

        confirmcase = html['statewise'][count - 1]['confirmed']
        deaths = html['statewise'][count - 1]['deaths']
        recover = html['statewise'][count - 1]['recovered']
        new = html['statewise'][count - 1]['deltaconfirmed']


    # url declared and fetching from url
    url = 'https://www.worldometers.info/coronavirus/'
    html = requests.post(url)
    purehtml = html.content

    # Souping
    soup = BeautifulSoup(purehtml,'html.parser')
    th = soup.find_all('table' , id='main_table_countries_today')

    #getting all headings
    para_list = []
    for trr in th[0].find_all('tr'):
        for i in trr.find_all('th'):
            para_list.append(i.text)

    # fetching particular country's data
    data_list = []
    bool = False
    for trr in th[0].find_all('tr'):
        for i in trr.find_all('td'):
            if i.text == local_country or bool:
                bool = True
                data_list.append(i.text)
            else:
                break
        bool = False


    #making dictionaries
    data = dict(zip(para_list,data_list))

    return render(request,'Indian.html',{'state':local_state,'cases':confirmcase,'deaths':deaths,'recover':recover,'recovered':data['TotalRecovered'],
                'inc':new,'country':local_country,'ccases':data['TotalCases'],'cdeaths':data['TotalDeaths'],'newc':data['NewCases']})
